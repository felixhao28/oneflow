#ifndef ONEFLOW_CORE_OPERATOR_SCALAR_ADD_OP_H_
#define ONEFLOW_CORE_OPERATOR_SCALAR_ADD_OP_H_

#include "oneflow/core/operator/operator.h"

namespace oneflow {

class ScalarAddOp final : public Operator {
 public:
  OF_DISALLOW_COPY_AND_MOVE(ScalarAddOp);
  ScalarAddOp() = default;
  ~ScalarAddOp() = default;

  void InitFromOpConf() override;
  void InferBlobDescs(std::function<BlobDesc*(const std::string&)> GetBlobDesc4BnInOp,
                      const ParallelContext* parallel_ctx) const override;
  const PbMessage& GetCustomizedConf() const override { return op_conf().scalar_add_conf(); }
  bool NeedInBlobWhenBackward() const override { return false; }
  bool NeedOutBlobWhenBackward() const override { return false; }

 private:
  void InferHasBatchDim(
      std::function<bool*(const std::string&)> HasBatchDim4BnInOp) const override {
    NaiveInferHasBatchDim(HasBatchDim4BnInOp);
  }

  void GetSbpSignatures(
      const std::function<const BlobDesc&(const std::string&)>& LogicalBlobDesc4Ibn,
      SbpSignatureList* sbp_sig_list) const override;
};

}  // namespace oneflow

#endif  // ONEFLOW_CORE_OPERATOR_SCALAR_ADD_OP_H_
