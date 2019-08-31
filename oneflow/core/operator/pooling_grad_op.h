#ifndef ONEFLOW_CORE_OPERATOR_POOLING_GRAD_OP_H_
#define ONEFLOW_CORE_OPERATOR_POOLING_GRAD_OP_H_

#include "oneflow/core/operator/operator.h"
#include "oneflow/core/operator/operator_util.h"

namespace oneflow {

class PoolingGradOp : public Operator {
 public:
  OF_DISALLOW_COPY_AND_MOVE(PoolingGradOp);
  PoolingGradOp() = default;
  virtual ~PoolingGradOp() = default;

  void InitFromOpConf() override;

  Maybe<void> InferBlobDescs(std::function<BlobDesc*(const std::string&)> GetBlobDesc4BnInOp,
                             const ParallelContext* parallel_ctx) const override;

 private:
  const PbMessage& GetCustomizedConf() const override;
  void CheckPoolSizeAndStrides() const;
  Maybe<void> InferHasBatchDim(
      std::function<bool*(const std::string&)> HasBatchDim4BnInOp) const override {
    return NaiveInferHasBatchDim(HasBatchDim4BnInOp);
  }
  void GetSbpSignatures(
      const std::function<const BlobDesc&(const std::string&)>& LogicalBlobDesc4Ibn,
      SbpSignatureList* sbp_sig_list) const override;
};

}  // namespace oneflow

#endif  // ONEFLOW_CORE_OPERATOR_POOLING_GRAD_OP_H_
