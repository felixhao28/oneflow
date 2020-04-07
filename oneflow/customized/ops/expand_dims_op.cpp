#include "oneflow/core/framework/framework.h"

namespace oneflow {

namespace {

int32_t TransformNegativeAxisToPositive(int32_t axis, const int32_t num_axes) {
  axis = axis < 0 ? axis + num_axes + 1 : axis;
  CHECK_GE(axis, 0);
  CHECK_LE(axis, num_axes);
  return axis;
}

}  // namespace

REGISTER_USER_OP("expand_dims")
    .Input("in")
    .Output("out")
    .Attr("axis", UserOpAttrType::kAtInt32)
    .SetTensorDescInferFn([](user_op::InferContext* ctx) -> Maybe<void> {
      const Shape* in_shape = ctx->Shape4ArgNameAndIndex("in", 0);
      Shape* out_shape = ctx->Shape4ArgNameAndIndex("out", 0);
      const int32_t axis =
          TransformNegativeAxisToPositive(ctx->GetAttr<int32_t>("axis"), in_shape->NumAxes());

      auto dim_vec = in_shape->dim_vec();
      dim_vec.insert(dim_vec.begin() + axis, 1);
      *out_shape = Shape(dim_vec);
      *ctx->Dtype4ArgNameAndIndex("out", 0) = *ctx->Dtype4ArgNameAndIndex("in", 0);
      return Maybe<void>::Ok();
    })
    .SetBatchAxisInferFn([](user_op::BatchAxisContext* ctx) -> Maybe<void> {
      const auto& in_desc = ctx->LogicalTensorDesc4InputArgNameAndIndex("in", 0);
      const auto* in_batch_axis = ctx->BatchAxis4ArgNameAndIndex("in", 0);
      auto* out_batch_axis = ctx->BatchAxis4ArgNameAndIndex("out", 0);
      const int32_t axis =
          TransformNegativeAxisToPositive(ctx->GetAttr<int32_t>("axis"), in_desc.shape().NumAxes());

      if (in_batch_axis->has_value()) {
        out_batch_axis->set_value(axis <= static_cast<int32_t>(in_batch_axis->value())
                                      ? in_batch_axis->value() + 1
                                      : in_batch_axis->value());
      } else {
        out_batch_axis->clear_value();
      }
      return Maybe<void>::Ok();
    })
    .SetGetSbpFn([](user_op::SbpContext* ctx) -> Maybe<void> {
      const auto& in_desc = ctx->LogicalTensorDesc4InputArgNameAndIndex("in", 0);
      const int32_t axis =
          TransformNegativeAxisToPositive(ctx->GetAttr<int32_t>("axis"), in_desc.shape().NumAxes());

      auto dim_vec = in_desc.shape().dim_vec();
      FOR_RANGE(int32_t, in_axis, 0, dim_vec.size()) {
        SbpSignatureBuilder()
            .Split("in", in_axis)
            .Split("out", in_axis < axis ? in_axis : in_axis + 1)
            .Build(ctx->sbp_sig_list()->mutable_sbp_signature()->Add());
      }

      SbpSignatureBuilder().PartialSum("in", 0).PartialSum("out", 0).Build(
          ctx->sbp_sig_list()->mutable_sbp_signature()->Add());

      return Maybe<void>::Ok();
    });

REGISTER_USER_OP_GRAD("expand_dims")
    .SetGenBackwardOpConfFn([](const user_op::UserOpWrapper& op, user_op::AddOpFn AddOp) {
      if (op.NeedGenGradTensor4OpInput("in", 0)) {
        user_op::UserOpConfWrapperBuilder builder(op.op_name() + "_grad");
        user_op::UserOpConfWrapper grad_op =
            builder.Op("reshape_like")
                .Input("in", op.GetGradTensorWithOpOutput("out", 0))
                .Input("like", op.input("in", 0))
                .Output("out")
                .Build();
        op.BindGradTensorWithOpInput(grad_op.output("out", 0), "in", 0);
        AddOp(grad_op);
      }
    });

}  // namespace oneflow
