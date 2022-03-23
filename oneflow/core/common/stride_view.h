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
#ifndef ONEFLOW_CORE_REGISTER_STRIDE_VIEW_H_
#define ONEFLOW_CORE_REGISTER_STRIDE_VIEW_H_

#include "oneflow/core/common/util.h"
#include "oneflow/core/common/shape_vec.h"

namespace oneflow {

class StrideProto;
class Stride;

template<typename DimT>
class StrideViewBase {
 public:
  using DimType = DimT;
  StrideViewBase(DimType* ptr, int64_t num_axes) : ptr_(ptr), num_axes_(num_axes) {}
  StrideViewBase(const StrideViewBase& rhs) = default;
  ~StrideViewBase() = default;

  int64_t NumAxes() const { return num_axes_; }
  int64_t At(int64_t index) const;
  int64_t Count(int64_t begin_axis) const;
  int64_t Count(int64_t begin_axis, int64_t end_axis) const;
  int64_t ElemCnt() const;
  const DimType* ptr() const { return ptr_; }

  bool operator==(const StrideViewBase& rhs) const;
  std::string ToString() const;
  void ToStrideVector(StrideVector* dim_vec) const;
  void ToStride(Stride* stride) const;

  void set_ptr(DimType* ptr) { ptr_ = ptr; }

 protected:
  DimType* dim_ptr() const { return ptr_; }

 private:
  DimType* ptr_;
  int64_t num_axes_;
};

class StrideView final : public StrideViewBase<const int64_t> {
 public:
  StrideView() : StrideViewBase<const int64_t>(nullptr, 0) {}
  StrideView(const int64_t* ptr, int64_t num_axes) : StrideViewBase<const int64_t>(ptr, num_axes) {}
  StrideView(const StrideProto& stride_proto);
  StrideView(const Stride& stride);
  StrideView(const StrideView& rhs) = default;
  ~StrideView() = default;
};

std::ostream& operator<<(std::ostream& out, const StrideView& stride);

class MutStrideView final : public StrideViewBase<int64_t> {
 public:
  MutStrideView() : StrideViewBase<int64_t>(nullptr, 0) {}
  MutStrideView(int64_t* ptr, int64_t num_axes) : StrideViewBase<int64_t>(ptr, num_axes) {}
  MutStrideView(const MutStrideView& rhs) = default;
  ~MutStrideView() = default;

  int64_t* mut_ptr() const { return dim_ptr(); }
  void Set(int64_t axis, int64_t val);

  void set_stride(const Stride& val);
  void set_stride(const StrideView& stride);
};

template<typename DimT>
bool StrideViewBase<DimT>::operator==(const StrideViewBase<DimT>& rhs) const {
  if (this->NumAxes() != rhs.NumAxes()) { return false; }
  FOR_RANGE(int, i, 0, this->NumAxes()) {
    if (At(i) != rhs.At(i)) { return false; }
  }
  return true;
}

}  // namespace oneflow

#endif  // ONEFLOW_CORE_REGISTER_STRIDE_VIEW_H_