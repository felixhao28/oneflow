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
#ifndef ONEFLOW_CORE_DEVICE_CUDA_STREAM_HANDLE_DEVICE_CONTEXT_H_
#define ONEFLOW_CORE_DEVICE_CUDA_STREAM_HANDLE_DEVICE_CONTEXT_H_

#include "oneflow/core/kernel/kernel_context.h"
#include "oneflow/core/device/device_context.h"
#include "oneflow/core/device/cuda_stream_handle.h"
#include "oneflow/core/device/hip_stream_handle.hip.h"
#include "oneflow/core/common/callback.msg.h"
#include "oneflow/core/vm/cuda_allocator.h"
#include "oneflow/core/vm/thread_safe_allocator.h"

namespace oneflow {
namespace vm {

#ifdef WITH_CUDA

class CudaStreamHandleDeviceCtx : public DeviceCtx {
 public:
  OF_DISALLOW_COPY_AND_MOVE(CudaStreamHandleDeviceCtx);
  CudaStreamHandleDeviceCtx() = delete;
  ~CudaStreamHandleDeviceCtx() override = default;

  CudaStreamHandleDeviceCtx(CallbackMsgListPtr callback_msg_list, int64_t device_id)
      : cuda_handler_(new CudaStreamHandle(nullptr)),
        callback_msg_list_(callback_msg_list),
        cuda_allocator_(
            new ThreadSafeAllocator(std::unique_ptr<Allocator>(new CudaAllocator(device_id)))) {}

  const cudaStream_t& cuda_stream() const override { return *(cuda_handler_->cuda_stream()); }
  const cublasHandle_t& cublas_pmh_handle() const override {
    return *(cuda_handler_->cublas_pmh_handle());
  }
  const cublasHandle_t& cublas_tensor_op_math_handle() const override {
    return *(cuda_handler_->cublas_tensor_op_math_handle());
  }
  const cublasHandle_t& cublas_pmd_handle() const override {
    return *(cuda_handler_->cublas_pmd_handle());
  }
  const cudnnHandle_t& cudnn_handle() const override { return *(cuda_handler_->cudnn_handle()); }

  void SyncDevice() override { OF_CUDA_CHECK(cudaStreamSynchronize(cuda_stream())); }

  void AddCallBack(std::function<void()> callback) const override {
    callback_msg_list_->EmplaceBack(ObjectMsgPtr<CallbackMsg>::New(callback));
  }

  vm::Allocator* mut_allocator() override { return cuda_allocator_.get(); }

 protected:
  std::unique_ptr<CudaStreamHandle> cuda_handler_;
  CallbackMsgListPtr callback_msg_list_;
  std::unique_ptr<Allocator> cuda_allocator_;
};

#endif  // WITH_CUDA

#ifdef WITH_HIP

class CudaStreamHandleDeviceCtx : public DeviceCtx {
 public:
  OF_DISALLOW_COPY_AND_MOVE(CudaStreamHandleDeviceCtx);
  CudaStreamHandleDeviceCtx() = delete;
  ~CudaStreamHandleDeviceCtx() override = default;

  CudaStreamHandleDeviceCtx(CallbackMsgListPtr callback_msg_list, int64_t device_id)
      : cuda_handler_(new HipStreamHandle(nullptr)),
        callback_msg_list_(callback_msg_list),
        cuda_allocator_(
            new ThreadSafeAllocator(std::unique_ptr<Allocator>(new CudaAllocator(device_id)))) {}

  const hipStream_t& hip_stream() const override { return *(cuda_handler_->hip_stream()); }
  const hipblasHandle_t& hipblas_pmh_handle() const override {
    return *(cuda_handler_->hipblas_pmh_handle());
  }
  const hipblasHandle_t& hipblas_tensor_op_math_handle() const override {
    return *(cuda_handler_->hipblas_tensor_op_math_handle());
  }
  const hipblasHandle_t& hipblas_pmd_handle() const override {
    return *(cuda_handler_->hipblas_pmd_handle());
  }
  const miopenHandle_t& miopen_handle() const override { return *(cuda_handler_->miopen_handle()); }

  void SyncDevice() override { OF_HIP_CHECK(hipStreamSynchronize(hip_stream())); }

  void AddCallBack(std::function<void()> callback) const override {
    callback_msg_list_->EmplaceBack(ObjectMsgPtr<CallbackMsg>::New(callback));
  }

  vm::Allocator* mut_allocator() override { return cuda_allocator_.get(); }

 protected:
  std::unique_ptr<HipStreamHandle> cuda_handler_;
  CallbackMsgListPtr callback_msg_list_;
  std::unique_ptr<Allocator> cuda_allocator_;
};

#endif  // WITH_CUDA

}  // namespace vm
}  // namespace oneflow

#endif  // ONEFLOW_CORE_DEVICE_CUDA_STREAM_HANDLE_DEVICE_CONTEXT_H_
