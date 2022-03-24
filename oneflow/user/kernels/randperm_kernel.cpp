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
#include "oneflow/user/kernels/op_kernel_wrapper.h"
#include "oneflow/core/common/data_type.h"
#include "oneflow/core/ep/include/stream.h"
#include "oneflow/core/framework/random_generator.h"
#include "oneflow/user/kernels/arange_kernel_util.h"
#include "oneflow/user/kernels/distributions/common.h"
#include "oneflow/core/job/nd_sbp_util.h"
#include "oneflow/core/common/container_util.h"
#include "oneflow/core/register/tensor_slice_view.h"

namespace oneflow {

class CpuRandPermKernel final : public user_op::OpKernel {
 public:
  CpuRandPermKernel() = default;
  ~CpuRandPermKernel() = default;
  std::shared_ptr<user_op::OpKernelState> CreateOpKernelState(
      user_op::KernelInitContext* ctx) const override {
    const auto& generator = CHECK_JUST(one::MakeGenerator(kCPU));
    generator->set_current_seed(ctx->Attr<int64_t>("seed"));

    int64_t parallel_num = ctx->parallel_ctx().parallel_num();
    const NdSbp& nd_sbp = ctx->NdSbp4ArgNameAndIndex("out", 0);
    if (parallel_num > 1) {
      const Shape& hierarchy = *ctx->parallel_desc().hierarchy();
      int64_t parallel_id = ctx->parallel_ctx().parallel_id();
      int32_t n = ctx->Attr<int32_t>("n");
      const Shape& logical_shape = Shape({n});
      view = GetTensorSliceView4ParallelId(hierarchy, nd_sbp, logical_shape, parallel_id);
    }
    return std::make_shared<DistributionKernelState>(generator);
  }

 private:
  void Compute(user_op::KernelComputeContext* ctx, user_op::OpKernelState* state,
               const user_op::OpKernelCache*) const override {
    user_op::Tensor* out = ctx->Tensor4ArgNameAndIndex("out", 0);
    int32_t* output = out->mut_dptr<int32_t>();
    const int32_t n = ctx->Attr<int32_t>("n");
    user_op::Tensor* tmp_buffer = ctx->Tensor4ArgNameAndIndex("tmp_buffer", 0);
    int32_t* temp = tmp_buffer->mut_dptr<int32_t>();
    if (n == 0) { return; }
    auto* distribution_state = dynamic_cast<DistributionKernelState*>(state);
    CHECK_NOTNULL(distribution_state);
    const auto& generator = distribution_state->generator();
    const auto& cpu_generator = CHECK_JUST(generator->Get<one::CPUGeneratorImpl>());
    CHECK_NOTNULL(generator);
    user_op::ArangeFunctor<DeviceType::kCPU, int32_t>()(ctx->stream(), 0, 1, n, temp);
    std::shuffle(temp, temp + n, cpu_generator->engine());
    auto len = view.At(0).end()-view.At(0).begin();
    memcpy(output, temp+view.At(0).begin(), sizeof(int32_t)*len);
  }
  bool AlwaysComputeWhenAllOutputsEmpty() const override { return false; }

 private:
  mutable TensorSliceView view;
};

REGISTER_USER_KERNEL("randperm")
    .SetCreateFn<CpuRandPermKernel>()
    .SetIsMatchedHob((user_op::HobDeviceType() == DeviceType::kCPU))
    .SetInferTmpSizeFn([](user_op::InferContext* ctx) {
      const int32_t n = ctx->Attr<int32_t>("n");
      return n * sizeof(int32_t);
    });
}  // namespace oneflow
