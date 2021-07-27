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
#ifndef ONEFLOW_CORE_THREAD_THREAD_CONTEXT_H_
#define ONEFLOW_CORE_THREAD_THREAD_CONTEXT_H_

#include "oneflow/core/device/cuda_stream_handle.h"
#include "oneflow/core/device/hip_stream_handle.hip.h"

namespace oneflow {

struct ThreadCtx {
#ifdef WITH_CUDA
  std::unique_ptr<CudaStreamHandle> g_cuda_stream;
  Channel<CudaCBEvent>* cb_event_chan;
#endif

#ifdef WITH_HIP
  std::unique_ptr<HipStreamHandle> g_hip_stream;
  Channel<HipCBEvent>* cb_event_chan;
#endif
};

}  // namespace oneflow

#endif  // ONEFLOW_CORE_THREAD_THREAD_CONTEXT_H_
