from collections import OrderedDict

import numpy as np
import oneflow as flow
from test_util import GenArgList, type_name_to_flow_type, type_name_to_np_type


def TestListDataTypeAndListShapeAndListStringAttr(
    input, out_shapes, out_types, string_list
):
    assert isinstance(out_shapes, list)
    assert isinstance(out_types, list)
    return (
        flow.user_op_builder("TestListDataTypeAndListShapeAndListStringAttr")
        .Op("TestListDataTypeAndListShapeAndListStringAttr")
        .Input("in", [input])
        .Output("out", 3)
        .Attr("out_shapes", out_shapes, "AttrTypeListShape")
        .Attr("out_types", out_types, "AttrTypeListDataType")
        .Attr("string_list", string_list, "AttrTypeListString")
        .Build()
        .InferAndTryRun()
        .RemoteBlobList()
    )


def RunTest(out_shapes, out_types):
    flow.clear_default_session()
    func_config = flow.FunctionConfig()
    func_config.default_data_type(flow.float)

    @flow.global_function(func_config)
    def TestListDataTypeAndListShapeAndListStringAttrJob(
        input=flow.FixedTensorDef((10, 10), dtype=flow.float)
    ):
        return TestListDataTypeAndListShapeAndListStringAttr(
            input,
            out_shapes,
            [type_name_to_flow_type[data_type] for data_type in out_types],
            ["string1", "string2", "string3"],
        )

    input = np.random.random_sample((10, 10)).astype(np.float32)
    outputs = [
        x.numpy() for x in TestListDataTypeAndListShapeAndListStringAttrJob(input).get()
    ]
    for i in range(len(outputs)):
        assert outputs[i].shape == out_shapes[i]
        assert outputs[i].dtype == type_name_to_np_type[out_types[i]]


def gen_arg_list():
    arg_dict = OrderedDict()
    arg_dict["out_shapes"] = [[(4, 4), (6, 6), (8, 8)]]
    # TODO: fix bugs in ForeignOutputKernel with "float16" and "char" dtype, do not test these two dtypes here
    arg_dict["out_types"] = [["float32", "double", "int8"], ["int32", "int64", "uint8"]]

    return GenArgList(arg_dict)


def test_data_type_attr(test_case):
    for arg in gen_arg_list():
        RunTest(*arg)