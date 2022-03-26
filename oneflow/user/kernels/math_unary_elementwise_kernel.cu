/*
Copyright 2020 The OneFlow Authors. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
#include "oneflow/core/framework/framework.h"
#include "oneflow/user/kernels/math_unary_elementwise_func.h"
#include "oneflow/core/kernel/cuda_graph_support.h"
#include "oneflow/core/ep/cuda/cuda_stream.h"
#include "oneflow/core/device/cuda_util.h"
#include "oneflow/core/common/stride.h"
#include "oneflow/core/cuda/elementwise.cuh"

namespace oneflow {

namespace {

template<template<typename> class UnaryFunctor, typename T>
__global__ void MathUnaryElementwiseForwardGpu(const int n, const T* x, T* y) {
  CUDA_1D_KERNEL_LOOP(i, n) { y[i] = UnaryFunctor<T>::Forward(x[i]); }
}

template<template<typename> class UnaryFunctor, typename T>
__global__ void MathUnaryElementwiseWithStrideForwardGpu(const int n, const StrideParam in_stride,
                                                         const StrideParam out_stride, const T* x,
                                                         T* y) {
  CUDA_1D_KERNEL_LOOP(i, n) {
    const int32_t idx = oneflow::cuda::elementwise::offset_to_index(i, in_stride, out_stride);
    y[i] = UnaryFunctor<T>::Forward(x[idx]);
  }
}

template<template<typename> class UnaryFunctor, typename T>
__global__ void MathUnaryElementwiseBackwardGpu(const int n, const T* x, const T* dy, T* dx) {
  CUDA_1D_KERNEL_LOOP(i, n) { dx[i] = UnaryFunctor<T>::Backward(x[i], dy[i]); }
}

template<template<typename> class UnaryFunctor, typename T>
__global__ void MathUnaryElementwiseWithDyStrideDYBackwardGpu(const int n, const T* x, const T* dy,
                                                              T* dx, const StrideParam dy_stride,
                                                              const StrideParam dx_stride) {
  CUDA_1D_KERNEL_LOOP(i, n) {
    const int32_t dy_idx = oneflow::cuda::elementwise::offset_to_index(i, dy_stride, dx_stride);
    dx[i] = UnaryFunctor<T>::Backward(x[i], dy[dy_idx]);
  }
}

template<template<typename> class UnaryFunctor, typename T>
__global__ void MathUnaryElementwiseWithXStrideBackwardGpu(const int n, const T* x, const T* dy,
                                                           T* dx, const StrideParam x_stride,
                                                           const StrideParam dx_stride) {
  CUDA_1D_KERNEL_LOOP(i, n) {
    const int32_t x_idx = oneflow::cuda::elementwise::offset_to_index(i, x_stride, dx_stride);
    dx[i] = UnaryFunctor<T>::Backward(x[x_idx], dy[i]);
  }
}

template<template<typename> class UnaryFunctor, typename T>
__global__ void MathUnaryElementwiseWithStrideBackwardGpu(const int n, const T* x, const T* dy,
                                                          T* dx, const StrideParam x_stride,
                                                          const StrideParam dy_stride,
                                                          const StrideParam dx_stride) {
  CUDA_1D_KERNEL_LOOP(i, n) {
    const int32_t x_idx = oneflow::cuda::elementwise::offset_to_index(i, x_stride, dx_stride);
    const int32_t dy_idx = oneflow::cuda::elementwise::offset_to_index(i, dy_stride, dx_stride);
    dx[i] = UnaryFunctor<T>::Backward(x[x_idx], dy[dy_idx]);
  }
}

}  // namespace

template<template<typename> class UnaryFunctor, typename T>
class MathUnaryElementwiseGpuKernel final : public user_op::OpKernel,
                                            public user_op::CudaGraphSupport {
 public:
  MathUnaryElementwiseGpuKernel() = default;
  ~MathUnaryElementwiseGpuKernel() = default;

 private:
  using user_op::OpKernel::Compute;
  void Compute(user_op::KernelComputeContext* ctx) const override {
    const user_op::Tensor* tensor_x = ctx->Tensor4ArgNameAndIndex("x", 0);
    user_op::Tensor* tensor_y = ctx->Tensor4ArgNameAndIndex("y", 0);
    const T* x = tensor_x->dptr<T>();
    T* y = tensor_y->mut_dptr<T>();
    int64_t n = tensor_x->shape().elem_cnt();
    CHECK_LE(n, GetMaxVal<int32_t>() / 2);
    if (n == 0) { return; }
    // compute is_contiguous and construct input/output stride params
    const int32_t ndim = tensor_x->shape().NumAxes();
    const StrideVector& in_stride_vec = tensor_x->stride().StrideVec();
    const StrideVector& out_stride_vec = tensor_y->stride().StrideVec();
    DimVector in_shape_vec;
    tensor_x->shape().ToDimVector(&in_shape_vec);
    bool is_contiguous = oneflow::one::IsContiguous(in_shape_vec, in_stride_vec);
    StrideParam in_stride(in_stride_vec.data(), ndim), out_stride(out_stride_vec.data(), ndim);
    if (is_contiguous) {
      MathUnaryElementwiseForwardGpu<UnaryFunctor, T>
          <<<BlocksNum4ThreadsNum(n), kCudaThreadsNumPerBlock, 0,
             ctx->stream()->As<ep::CudaStream>()->cuda_stream()>>>(n, x, y);
    } else {
      MathUnaryElementwiseWithStrideForwardGpu<UnaryFunctor, T>
          <<<BlocksNum4ThreadsNum(n), kCudaThreadsNumPerBlock, 0,
             ctx->stream()->As<ep::CudaStream>()->cuda_stream()>>>(n, in_stride, out_stride, x, y);
    }
  }
  bool AlwaysComputeWhenAllOutputsEmpty() const override { return false; }
};

template<template<typename> class UnaryFunctor, typename T>
class MathUnaryElementwiseGradGpuKernel final : public user_op::OpKernel,
                                                public user_op::CudaGraphSupport {
 public:
  MathUnaryElementwiseGradGpuKernel() = default;
  ~MathUnaryElementwiseGradGpuKernel() = default;

 private:
  using user_op::OpKernel::Compute;
  void Compute(user_op::KernelComputeContext* ctx) const override {
    const user_op::Tensor* tensor_x = ctx->Tensor4ArgNameAndIndex("x", 0);
    const user_op::Tensor* tensor_dy = ctx->Tensor4ArgNameAndIndex("dy", 0);
    user_op::Tensor* tensor_dx = ctx->Tensor4ArgNameAndIndex("dx", 0);

    const T* x = tensor_x->dptr<T>();
    const T* dy = tensor_dy->dptr<T>();
    T* dx = tensor_dx->mut_dptr<T>();
    int64_t n = tensor_x->shape().elem_cnt();
    CHECK_LE(n, GetMaxVal<int32_t>() / 2);
    if (n == 0) { return; }
    const int32_t ndim = tensor_x->shape().NumAxes();
    const StrideVector& x_stride_vec = tensor_x->stride().StrideVec();
    const StrideVector& dy_stride_vec = tensor_dy->stride().StrideVec();
    const StrideVector& dx_stride_vec = tensor_dx->stride().StrideVec();
    StrideParam x_stride(x_stride_vec.data(), ndim), dy_stride(dy_stride_vec.data(), ndim),
        dx_stride(dx_stride_vec.data(), ndim);
    DimVector x_shape_vec, dy_shape_vec, dx_shape_vec;
    tensor_x->shape().ToDimVector(&x_shape_vec);
    tensor_dy->shape().ToDimVector(&dy_shape_vec);
    tensor_dx->shape().ToDimVector(&dx_shape_vec);
    bool x_contiguous = oneflow::one::IsContiguous(x_shape_vec, x_stride_vec);
    bool dy_contiguous = oneflow::one::IsContiguous(dy_shape_vec, dy_stride_vec);
    if (x_contiguous && dy_contiguous) {
      MathUnaryElementwiseBackwardGpu<UnaryFunctor, T>
          <<<BlocksNum4ThreadsNum(n), kCudaThreadsNumPerBlock, 0,
             ctx->stream()->As<ep::CudaStream>()->cuda_stream()>>>(n, x, dy, dx);
    } else if (x_contiguous) {
      MathUnaryElementwiseWithDyStrideDYBackwardGpu<UnaryFunctor, T>
          <<<BlocksNum4ThreadsNum(n), kCudaThreadsNumPerBlock, 0,
             ctx->stream()->As<ep::CudaStream>()->cuda_stream()>>>(n, x, dy, dx, dy_stride,
                                                                   dx_stride);
    } else if (x_contiguous) {
      MathUnaryElementwiseWithXStrideBackwardGpu<UnaryFunctor, T>
          <<<BlocksNum4ThreadsNum(n), kCudaThreadsNumPerBlock, 0,
             ctx->stream()->As<ep::CudaStream>()->cuda_stream()>>>(n, x, dy, dx, x_stride,
                                                                   dx_stride);
    } else {
      MathUnaryElementwiseWithStrideBackwardGpu<UnaryFunctor, T>
          <<<BlocksNum4ThreadsNum(n), kCudaThreadsNumPerBlock, 0,
             ctx->stream()->As<ep::CudaStream>()->cuda_stream()>>>(n, x, dy, dx, x_stride,
                                                                   dy_stride, dx_stride);
    }
  }
  bool AlwaysComputeWhenAllOutputsEmpty() const override { return false; }
};

#define REGISTER_MATH_UNARY_ELEMENTWISE_CUDA_KERNEL_AND_GRAD(math_type_pair, data_type_pair)       \
  REGISTER_USER_KERNEL(OF_PP_PAIR_FIRST(math_type_pair))                                           \
      .SetCreateFn<                                                                                \
          MathUnaryElementwiseGpuKernel<OF_PP_CAT(OF_PP_PAIR_SECOND(math_type_pair), Functor),     \
                                        OF_PP_PAIR_FIRST(data_type_pair)>>()                       \
      .SetIsMatchedHob((user_op::HobDeviceType() == DeviceType::kCUDA)                             \
                       && (user_op::HobDataType("x", 0) == OF_PP_PAIR_SECOND(data_type_pair))      \
                       && (user_op::HobDataType("y", 0) == OF_PP_PAIR_SECOND(data_type_pair)));    \
                                                                                                   \
  REGISTER_USER_KERNEL((std::string("") + OF_PP_PAIR_FIRST(math_type_pair) + "_grad"))             \
      .SetCreateFn<                                                                                \
          MathUnaryElementwiseGradGpuKernel<OF_PP_CAT(OF_PP_PAIR_SECOND(math_type_pair), Functor), \
                                            OF_PP_PAIR_FIRST(data_type_pair)>>()                   \
      .SetIsMatchedHob((user_op::HobDeviceType() == DeviceType::kCUDA)                             \
                       && (user_op::HobDataType("x", 0) == OF_PP_PAIR_SECOND(data_type_pair)));

OF_PP_SEQ_PRODUCT_FOR_EACH_TUPLE(REGISTER_MATH_UNARY_ELEMENTWISE_CUDA_KERNEL_AND_GRAD,
                                 MATH_UNARY_ELEMENTWISE_FUNC_SEQ, FLOATING_DATA_TYPE_SEQ)

// For some special dtype kernel register.
OF_PP_SEQ_PRODUCT_FOR_EACH_TUPLE(REGISTER_MATH_UNARY_ELEMENTWISE_CUDA_KERNEL_AND_GRAD,
                                 OF_PP_MAKE_TUPLE_SEQ("abs", Abs), UNSIGNED_INT_DATA_TYPE_SEQ)
OF_PP_SEQ_PRODUCT_FOR_EACH_TUPLE(REGISTER_MATH_UNARY_ELEMENTWISE_CUDA_KERNEL_AND_GRAD,
                                 OF_PP_MAKE_TUPLE_SEQ("abs", Abs), INT_DATA_TYPE_SEQ)

template<template<typename> class UnaryFunctor>
class MathUnaryElementwiseGpuHalfKernel final : public user_op::OpKernel,
                                                public user_op::CudaGraphSupport {
 public:
  MathUnaryElementwiseGpuHalfKernel() = default;
  ~MathUnaryElementwiseGpuHalfKernel() = default;

 private:
  using user_op::OpKernel::Compute;
  void Compute(user_op::KernelComputeContext* ctx) const override {
    const user_op::Tensor* tensor_x = ctx->Tensor4ArgNameAndIndex("x", 0);
    user_op::Tensor* tensor_y = ctx->Tensor4ArgNameAndIndex("y", 0);
    const half* x = reinterpret_cast<const half*>(tensor_x->dptr<float16>());
    half* y = reinterpret_cast<half*>(tensor_y->mut_dptr<float16>());
    int64_t n = tensor_x->shape().elem_cnt();
    CHECK_LE(n, GetMaxVal<int32_t>() / 2);
    if (n == 0) { return; }
    MathUnaryElementwiseForwardGpu<UnaryFunctor, half>
        <<<BlocksNum4ThreadsNum(n), kCudaThreadsNumPerBlock, 0,
           ctx->stream()->As<ep::CudaStream>()->cuda_stream()>>>(n, x, y);
  }
  bool AlwaysComputeWhenAllOutputsEmpty() const override { return false; }
};

template<template<typename> class UnaryFunctor>
class MathUnaryElementwiseGradGpuHalfKernel final : public user_op::OpKernel,
                                                    public user_op::CudaGraphSupport {
 public:
  MathUnaryElementwiseGradGpuHalfKernel() = default;
  ~MathUnaryElementwiseGradGpuHalfKernel() = default;

 private:
  using user_op::OpKernel::Compute;
  void Compute(user_op::KernelComputeContext* ctx) const override {
    const user_op::Tensor* tensor_x = ctx->Tensor4ArgNameAndIndex("x", 0);
    const user_op::Tensor* tensor_dy = ctx->Tensor4ArgNameAndIndex("dy", 0);
    user_op::Tensor* tensor_dx = ctx->Tensor4ArgNameAndIndex("dx", 0);

    const half* x = reinterpret_cast<const half*>(tensor_x->dptr<float16>());
    const half* dy = reinterpret_cast<const half*>(tensor_dy->dptr<float16>());
    half* dx = reinterpret_cast<half*>(tensor_dx->mut_dptr<float16>());
    int64_t n = tensor_x->shape().elem_cnt();
    CHECK_LE(n, GetMaxVal<int32_t>() / 2);
    if (n == 0) { return; }
    MathUnaryElementwiseBackwardGpu<UnaryFunctor, half>
        <<<BlocksNum4ThreadsNum(n), kCudaThreadsNumPerBlock, 0,
           ctx->stream()->As<ep::CudaStream>()->cuda_stream()>>>(n, x, dy, dx);
  }
  bool AlwaysComputeWhenAllOutputsEmpty() const override { return false; }
};

#define REGISTER_MATH_UNARY_ELEMENTWISE_GUDA_HALF_KERNEL_AND_GRAD(math_type_str, math_func_prefix) \
  REGISTER_USER_KERNEL(math_type_str)                                                              \
      .SetCreateFn<MathUnaryElementwiseGpuHalfKernel<OF_PP_CAT(math_func_prefix, Functor)>>()      \
      .SetIsMatchedHob((user_op::HobDeviceType() == DeviceType::kCUDA)                             \
                       && (user_op::HobDataType("x", 0) == DataType::kFloat16)                     \
                       && (user_op::HobDataType("y", 0) == DataType::kFloat16));                   \
                                                                                                   \
  REGISTER_USER_KERNEL((std::string("") + math_type_str + "_grad"))                                \
      .SetCreateFn<MathUnaryElementwiseGradGpuHalfKernel<OF_PP_CAT(math_func_prefix, Functor)>>()  \
      .SetIsMatchedHob((user_op::HobDeviceType() == DeviceType::kCUDA)                             \
                       && (user_op::HobDataType("x", 0) == DataType::kFloat16));

OF_PP_FOR_EACH_TUPLE(REGISTER_MATH_UNARY_ELEMENTWISE_GUDA_HALF_KERNEL_AND_GRAD,
                     MATH_UNARY_ELEMENTWISE_FUNC_SEQ)

}  // namespace oneflow
