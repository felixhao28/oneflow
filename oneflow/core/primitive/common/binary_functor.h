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
#ifndef ONEFLOW_CORE_PRIMITIVE_COMMON_BINARY_FUNCTOR_H_
#define ONEFLOW_CORE_PRIMITIVE_COMMON_BINARY_FUNCTOR_H_

#include "oneflow/core/primitive/include/unary_op.h"
#include "oneflow/core/common/data_type.h"
namespace oneflow {

namespace primitive {

template<DeviceType device, BinaryOp binary_op, typename Src, typename Dst>
struct BinaryFunctor;

template<DeviceType device, typename Src, typename Dst>
struct BinaryFunctor<device, BinaryOp::kAdd, Src, Dst> {
  OF_DEVICE_FUNC Dst operator()(Src src0, Src src1) const { return static_cast<Dst>(src0 + src1); }
};

template<DeviceType device, typename Src, typename Dst>
struct BinaryFunctor<device, BinaryOp::kSub, Src, Dst> {
  OF_DEVICE_FUNC Dst operator()(Src src0, Src src1) const { return static_cast<Dst>(src0 - src1); }
};

template<DeviceType device, typename Src, typename Dst>
struct BinaryFunctor<device, BinaryOp::kMul, Src, Dst> {
  OF_DEVICE_FUNC Dst operator()(Src src0, Src src1) const { return static_cast<Dst>(src0 * src1); }
};

template<DeviceType device, typename Src, typename Dst>
struct BinaryFunctor<device, BinaryOp::kDiv, Src, Dst> {
  OF_DEVICE_FUNC Dst operator()(Src src0, Src src1) const { return static_cast<Dst>(src0 / src1); }
};

template<DeviceType device, typename Src, typename Dst>
struct BinaryFunctor<device, BinaryOp::kMax, Src, Dst> {
  OF_DEVICE_FUNC Dst operator()(Src src0, Src src1) const {
    if (src0 >= src1) {
      return src0;
    } else {
      return src1;
    }
  }
};

template<DeviceType device, typename Src, typename Dst>
struct BinaryFunctor<device, BinaryOp::kMin, Src, Dst> {
  OF_DEVICE_FUNC Dst operator()(Src src0, Src src1) const {
    if (src0 <= src1) {
      return src0;
    } else {
      return src1;
    }
  }
};

template<DeviceType device, typename Src, typename Dst>
struct BinaryFunctor<device, BinaryOp::kEqual, Src, Dst> {
  OF_DEVICE_FUNC Dst operator()(Src src0, Src src1) const { return src0 == src1; }
};

template<DeviceType device, typename Src, typename Dst>
struct BinaryFunctor<device, BinaryOp::kNotEqual, Src, Dst> {
  OF_DEVICE_FUNC Dst operator()(Src src0, Src src1) const { return src0 != src1; }
};

template<DeviceType device, typename Src, typename Dst>
struct BinaryFunctor<device, BinaryOp::kLessThan, Src, Dst> {
  OF_DEVICE_FUNC Dst operator()(Src src0, Src src1) const { return src0 < src1; }
};

template<DeviceType device, typename Src, typename Dst>
struct BinaryFunctor<device, BinaryOp::kLessEqual, Src, Dst> {
  OF_DEVICE_FUNC Dst operator()(Src src0, Src src1) const { return src0 <= src1; }
};

template<DeviceType device, typename Src, typename Dst>
struct BinaryFunctor<device, BinaryOp::kGreaterThan, Src, Dst> {
  OF_DEVICE_FUNC Dst operator()(Src src0, Src src1) const { return src0 > src1; }
};

template<DeviceType device, typename Src, typename Dst>
struct BinaryFunctor<device, BinaryOp::kGreaterEqual, Src, Dst> {
  OF_DEVICE_FUNC Dst operator()(Src src0, Src src1) const { return src0 >= src1; }
};

template<DeviceType device, typename Src, typename Dst>
struct BinaryFunctor<device, BinaryOp::kLogicalAnd, Src, Dst> {
  OF_DEVICE_FUNC Dst operator()(Src src0, Src src1) const { return src0 && src1; }
};

template<DeviceType device, typename Src, typename Dst>
struct BinaryFunctor<device, BinaryOp::kLogicalOr, Src, Dst> {
  OF_DEVICE_FUNC Dst operator()(Src src0, Src src1) const { return src0 || src1; }
};

template<DeviceType device, typename Src, typename Dst>
struct BinaryFunctor<device, BinaryOp::kLogicalXor, Src, Dst> {
  OF_DEVICE_FUNC Dst operator()(Src src0, Src src1) const { return (!src0) != (!src1); }
};

}  // namespace primitive

}  // namespace oneflow

#endif  // ONEFLOW_CORE_PRIMITIVE_COMMON_BINARY_FUNCTOR_H_