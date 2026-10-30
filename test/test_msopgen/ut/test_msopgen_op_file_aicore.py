# -------------------------------------------------------------------------
# This file is part of the MindStudio project.
# Copyright (c) 2026 Huawei Technologies Co.,Ltd.
#
# MindStudio is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
# -------------------------------------------------------------------------

import unittest
from collections import OrderedDict
from collections import namedtuple
import json
from types import SimpleNamespace
import pytest
from unittest import mock
from msopgen.interface import utils
from msopgen.interface.op_file_aicore import OpFileAiCore
from msopgen.interface.op_info_ir_json import JsonIROpInfo


class TestOpFileAiCoreMethods(unittest.TestCase):

    def test_generate_input_output_info_cfg(self):
        op_file = OpFileAiCore

        parsed_info = OrderedDict([('x', {
            'ir_type_list': ['DT_FLOAT', ' DT_INT32'],
            'param_type': 'required', 'format_list': ['NCHW']})])
        str_template = "input{index}.name={name}\ninput{index}.dtype={dtype}\ninput{index}.paramType={paramType}\ninput{index}.format={format}"
        self._mapping_info_cfg_type = mock.Mock(return_value="int8")
        ret = op_file._generate_input_output_info_cfg(self, parsed_info, str_template)
        print(ret)
        golden_ret = "input0.name=x\ninput0.dtype=int8,int8\ninput0.paramType=required\ninput0.format=NCHW,NCHW"
        self.assertEqual(golden_ret, ret)
        OpInfo = namedtuple('OpInfo', ['parsed_input_info'])
        value = {
            "param_type" : "optional",
            "ir_type_list" : ["DT_FLOAT"],
            "format_list" : ["ND"]
        }
        dict_value = {"a" : value}
        op_info_tmp = OpInfo(parsed_input_info = dict_value)
        self.op_info = op_info_tmp
        ret = op_file._generate_cpp_params(self, False)

@pytest.mark.parametrize("attr_type, default_value, expected", [
    ("list_int", [1, -2, 0], "ListInt({1, -2, 0})"),
    ("list_float", [0.5, -1.0], "ListFloat({0.5, -1.0})"),
    ("list_bool", [True, False], "ListBool({true, false})"),
    ("list_list_int", [[1, 2], [], [-3]], "ListListInt({{1, 2}, {}, {-3}})"),
    ("list_int", [-(1 << 63), (1 << 63) - 1], "ListInt({(-9223372036854775807 - 1), 9223372036854775807})"),
    ("list_list_int", [[-(1 << 63)]], "ListListInt({{(-9223372036854775807 - 1)}})"),
    ("list_int", [], "ListInt({})"),
    ("list_float", [], "ListFloat({})"),
    ("list_bool", [], "ListBool({})"),
    ("list_list_int", [], "ListListInt({})"),
    ("int", 0, "Int(0)"),
    ("float", 0.5, "Float(0.5)"),
    ("bool", False, "Bool(false)"),
    ("string", "ND", 'String("ND")'),
])
def test_cpp_attribute_default_from_json(tmp_path, attr_type, default_value, expected):
    """Valid JSON defaults must produce the corresponding C++ registration call."""
    input_file = tmp_path / "op.json"
    input_file.write_text(json.dumps([{
        "op": "AddCustom",
        "attr": [{"name": "value", "type": attr_type, "param_type": "optional", "default_value": default_value}],
    }]), encoding="utf-8")
    args = SimpleNamespace(input_path=str(input_file), gen_flag=True, output_path=str(tmp_path),
                           op_type="", framework="pytorch")
    info = JsonIROpInfo(args)
    info.parse()
    op_file = OpFileAiCore.__new__(OpFileAiCore)
    op_file.op_info = info

    assert op_file._generate_cpp_attrs() == '        this->Attr("value").AttrType(OPTIONAL).{};\n'.format(expected)


def test_cpp_required_list_attribute_omits_default():
    op_file = OpFileAiCore.__new__(OpFileAiCore)
    op_file.op_info = SimpleNamespace(parsed_attr_info=[["value", "ListInt", None, "required"]])
    assert op_file._generate_cpp_attrs() == '        this->Attr("value").ListInt();\n'


def test_update_kernel_cmake_uses_configured_compute_units(tmp_path):
    op_file = OpFileAiCore.__new__(OpFileAiCore)
    op_file.output_path = str(tmp_path)
    op_file.compute_unit = ["ai_core-ascend910b4", "ai_core-ascend310p3"]
    op_file.op_info = SimpleNamespace(op_type="AddCustom", fix_op_type="add_custom")
    with mock.patch("os.path.exists", return_value=True), \
            mock.patch.object(utils, "read_file", return_value="{op_name}:{compute_unit}:{kernel_name}"), \
            mock.patch.object(utils, "write_files") as write:
        op_file._update_ascendc_op_kernel_cmake()
    assert write.call_args[0][1] == "AddCustom:ascend910b;ascend310p:add_custom"


@pytest.mark.parametrize("content, missing", [
    ("ASCEND_COMPUTE_UNIT ASCEND_FRAMEWORK_TYPE", None),
    ("ASCEND_COMPUTE_UNIT", "ASCEND_FRAMEWORK_TYPE"),
    ("ASCEND_FRAMEWORK_TYPE", "ASCEND_COMPUTE_UNIT"),
])
def test_check_cmake_env_reports_only_missing_variables(content, missing):
    op_file = OpFileAiCore.__new__(OpFileAiCore)
    with mock.patch.object(utils, "print_warn_log") as warn:
        op_file._check_config_cmake_env(content, {}, "cpp")
    if missing is None:
        warn.assert_not_called()
    else:
        warn.assert_called_once_with("File config.cmake lack of {}. Please check your config env.".format(missing))


if __name__ == '__main__':
    unittest.main()
