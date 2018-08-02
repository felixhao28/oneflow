#ifndef ONEFLOW_CORE_REGISTER_BLOB_DESC_H_
#define ONEFLOW_CORE_REGISTER_BLOB_DESC_H_

#include "oneflow/core/common/data_type.h"
#include "oneflow/core/common/shape.h"
#include "oneflow/core/register/field_desc.h"
#include "oneflow/core/register/blob_desc.pb.h"
#include "oneflow/core/job/job_desc.h"

namespace oneflow {

class BlobDesc {
 public:
  // OF_DISALLOW_COPY_AND_MOVE(BlobDesc);
  ~BlobDesc() = default;

  BlobDesc();
  BlobDesc(const Shape&, DataType, bool has_data_id, bool has_col_num, int32_t max_col_num);
  BlobDesc(const Shape& shape) : body_field_(shape) {}
  BlobDesc(const BlobDescProto& proto);
  BlobDesc(int64_t header_byte_size, const Shape&, DataType, int32_t max_col_num);

  const Shape& shape() const { return body_field_.shape(); }
  Shape& mut_shape() { return body_field_.mut_shape(); }

  DataType data_type() const { return body_field_.data_type(); }
  void set_data_type(DataType val) { body_field_.set_data_type(val); }

  bool header_is_opaque() const { return header_is_opaque_; };

  bool has_data_id_field() const { return has_data_id_; }
  void set_has_data_id_field(bool val);

  bool has_col_num_field() const { return has_col_num_; }
  void set_has_col_num_field(bool val);

  int32_t max_col_num() const { return max_col_num_; }
  void set_max_col_num(int32_t val) { max_col_num_ = val; }

  bool operator==(const BlobDesc& rhs) const;
  void ToProto(BlobDescProto* proto) const;

 private:
  void HeaderToProto(BlobDescProto* proto) const;
  void DataIdFieldToProto(FieldHeaderDesc* proto) const;
  void ColNumFieldToProto(FieldHeaderDesc* proto) const;

  bool header_is_opaque_;
  FieldDesc opaque_header_;

  bool has_data_id_;
  bool has_col_num_;
  int64_t max_col_num_;

  FieldDesc body_field_;
};

std::unique_ptr<BlobDesc> ComputePackedBlobDesc(std::function<const BlobDesc*()> NextBlobDesc);

}  // namespace oneflow

#endif  // ONEFLOW_CORE_REGISTER_BLOB_DESC_H_
