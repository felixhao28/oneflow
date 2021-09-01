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
#include "oneflow/core/common/device_type.pb.h"
#include "oneflow/user/kernels/view_copy_kernel.h"

namespace oneflow {

namespace {

__device__ void compute_index(int64_t offset, int ndim, const int64_t stride[], int64_t index[]) {
  int64_t v = offset;

#pragma unroll
  for (int i = 0; i < ndim; ++i) {
    int64_t idx = v / stride[i];
    index[i] = idx;
    v -= idx * stride[i];
  }
}

__device__ int64_t compute_offset(const int64_t index[], int ndim, const int64_t stride[]) {
  int64_t v = 0;

#pragma unroll
  for (int i = 0; i < ndim; ++i) { v += index[i] * stride[i]; }

  return v;
}

__global__ void copy_view(cudaStream_t cuda_stream, int64_t count, size_t dsize,
                          const int64_t in_stride[], const int64_t out_stride[],
                          const char* in_dptr, char* out_dptr, int64_t ndim,
                          int64_t contiguous_block_size) {
  int64_t in_index[SHAPE_MAX_AXIS_SIZE];

  CUDA_1D_KERNEL_LOOP_T(int64_t, i, count) {
    const int64_t out_offset = i * contiguous_block_size;

    compute_index(out_offset, ndim, out_stride, in_index);
    const int64_t in_offset = compute_offset(in_index, ndim, in_stride);

    char *out_dptr_offset = out_dptr + out_offset * dsize;
    const char *in_dptr_offset = in_dptr + in_offset * dsize;

#pragma unroll
    for (int j = 0; j < contiguous_block_size * dsize; ++j) { out_dptr_offset[j] = in_dptr_offset[j]; }
  }
}

}  // namespace

template<>
void ViewCopyUtil<kGPU>::operator()() {
  if (contiguous_dim == -1) {
    OF_CUDA_CHECK(cudaMemcpyAsync(out_dptr, in_dptr, contiguous_block_size * dsize,
                                  cudaMemcpyDeviceToDevice, ctx->cuda_stream()));
  } else {
    int64_t count = count_blocks();
    init_out_stride();

    int ndim = contiguous_dim + 1;
    int stride_size = ndim * sizeof(int64_t);

    int64_t *cuda_in_stride, *cuda_out_stride;
    OF_CUDA_CHECK(cudaMalloc(&cuda_in_stride, stride_size));
    OF_CUDA_CHECK(cudaMalloc(&cuda_out_stride, stride_size));

    OF_CUDA_CHECK(
        cudaMemcpy(cuda_in_stride, in_stride.data(), stride_size, cudaMemcpyHostToDevice));
    OF_CUDA_CHECK(
        cudaMemcpy(cuda_out_stride, out_stride.data(), stride_size, cudaMemcpyHostToDevice));

    copy_view<<<BlocksNum4ThreadsNum(count), kCudaThreadsNumPerBlock, 0, ctx->cuda_stream()>>>(
        ctx->cuda_stream(), count, dsize, cuda_in_stride, cuda_out_stride, in_dptr, out_dptr, ndim,
        contiguous_block_size);

    OF_CUDA_CHECK(cudaDeviceSynchronize());

    OF_CUDA_CHECK(cudaFree(cuda_in_stride));
    OF_CUDA_CHECK(cudaFree(cuda_out_stride));
  }
}

}  // namespace oneflow
