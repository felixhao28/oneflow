#ifndef ONEFLOW_CORE_OPERATOR_ALL_REDUCE_FACADE_OP_H_
#define ONEFLOW_CORE_OPERATOR_ALL_REDUCE_FACADE_OP_H_

#include "oneflow/core/operator/operator.h"

namespace oneflow {

class AllReduceFacadeOp final : public Operator {
 public:
  OF_DISALLOW_COPY_AND_MOVE(AllReduceFacadeOp);
  AllReduceFacadeOp() = default;
  ~AllReduceFacadeOp() override = default;

  void InitFromOpConf() override;
  const PbMessage& GetCustomizedConf() const override;

  void InferBlobDescs(std::function<BlobDesc*(const std::string&)> GetBlobDesc4BnInOp,
                      const ParallelContext* parallel_ctx) const override;

 private:
  void InferHasBatchDim(std::function<bool*(const std::string&)> HasBatchDim4BnInOp) const override;

  void InferSbpSignature(SbpSignature* sbp_signature, const SbpSignature& sbp_sig_conf,
                         const std::function<int32_t(const SbpSignature&)>& CalcOrderValue4SbpSig,
                         std::function<const SbpInferHint&(const std::string&)> SbpInferHint4Ibn,
                         const ParallelDesc& parallel_desc) const override;
  LogicalNode* NewProperLogicalNode() const override;
};

}  // namespace oneflow

#endif  // ONEFLOW_CORE_OPERATOR_ALL_REDUCE_FACADE_OP_H_
