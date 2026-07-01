import unittest
import pytest
import sys
from unittest import mock
from msopst.st.interface import utils
from msopst.st.interface.const_manager import ConstManager
from msopst.st.interface.case_generator import CaseGenerator


class OpstArgs:
    def __init__(self, input_file, output_path):
        self.input_file = input_file
        self.output_path = output_path
        self.model_path = ""
        self.quiet = False


class TestUtilsMethods(unittest.TestCase):
    def test_msopst_check_argument_valid_error(self):
        with pytest.raises(utils.OpTestGenException) as error:
            args = OpstArgs("/home/test.txt", "/home")
            case = CaseGenerator(args)
            case.check_argument_valid()
        self.assertEqual(error.value.args[0], ConstManager.OP_TEST_GEN_INVALID_PATH_ERROR)

    def test_msopst_parse_bool_value(self):
        args = OpstArgs("/home/test.txt", "/home")
        case = CaseGenerator(args)
        result = case._parse_bool_value("false")
        self.assertEqual(result, False)

    def test_msopst_parse_list_list_int_value_error(self):
        # with pytest.raises(ValueError) as error:
        args = OpstArgs("/home/test.txt", "/home")
        case = CaseGenerator(args)
        self.assertRaises(ValueError, case._parse_list_list_int_value, "false")
        self.assertRaises(ValueError, case._parse_list_list_int_value, "[[[false]]]")

    def test_msopst_parse_py_to_json_error1(self):
        with pytest.raises(utils.OpTestGenException) as error:
            with mock.patch('importlib.util.spec_from_file_location', side_effect=NameError):
                args = OpstArgs("/home/test.py", "/home")
                case = CaseGenerator(args)
                case._parse_py_to_json()
        self.assertEqual(error.value.args[0], ConstManager.OP_TEST_GEN_INVALID_DATA_ERROR)

    def test_msopst_parse_py_to_json_error2(self):
        with pytest.raises(utils.OpTestGenException) as error:
            with mock.patch('importlib.util.spec_from_file_location', side_effect=ValueError):
                args = OpstArgs("/home/test.py", "/home")
                case = CaseGenerator(args)
                case._parse_py_to_json()
        self.assertEqual(error.value.args[0], ConstManager.OP_TEST_GEN_INVALID_DATA_ERROR)

    def test_get_ms_ops_info_no_syspath_pollution(self):
        original_path = sys.path.copy()
        mock_module = mock.MagicMock()
        mock_module.test_attr = "test_value"
        mock_spec = mock.MagicMock()
        mock_spec.loader.exec_module = mock.MagicMock()
        with mock.patch('importlib.util.spec_from_file_location', return_value=mock_spec):
            with mock.patch('importlib.util.module_from_spec', return_value=mock_module):
                result = CaseGenerator._get_ms_ops_info("test_module", "test_attr", module_file="/tmp/test_module.py")
                self.assertEqual(result, "test_value")
                self.assertEqual(sys.path, original_path)

    def test_get_ms_ops_info_without_module_file_fallback(self):
        mock_module = mock.MagicMock()
        mock_module.test_attr = "test_value"
        with mock.patch('importlib.import_module', return_value=mock_module):
            result = CaseGenerator._get_ms_ops_info("test_module", "test_attr")
            self.assertEqual(result, "test_value")

    def test_msopst_check_op_info_list_valid_error1(self):
        with pytest.raises(utils.OpTestGenException) as error:
            args = OpstArgs("/home/test.py", "/home")
            case = CaseGenerator(args)
            case._check_op_info_list_valid("", "", "")
        self.assertEqual(error.value.args[0], ConstManager.OP_TEST_GEN_CONFIG_INVALID_OPINFO_FILE_ERROR)

    def test_msopst_check_op_info_list_valid_error2(self):
        with pytest.raises(utils.OpTestGenException) as error:
            args = OpstArgs("/home/test.py", "/home")
            case = CaseGenerator(args)
            case._check_op_info_list_valid(["", "a"], "", "")
        self.assertEqual(error.value.args[0], ConstManager.OP_TEST_GEN_CONFIG_INVALID_OPINFO_FILE_ERROR)

    def test_msopst_check_op_info_list_valid_error3(self):
        args = OpstArgs("/home/test.py", "/home")
        case = CaseGenerator(args)
        case._check_op_info_list_valid(["a"], ["b"], "")

    def test_msopst_make_attr_error(self):
        with pytest.raises(utils.OpTestGenException) as error:
            args = OpstArgs("/home/test.py", "/home")
            case = CaseGenerator(args)
            case._make_attr("attr_require", "")
        self.assertEqual(error.value.args[0], ConstManager.OP_TEST_GEN_CONFIG_INVALID_OPINFO_FILE_ERROR)

    def test_msopst_check_desc_valid_error(self):
        with pytest.raises(utils.OpTestGenException) as error:
            args = OpstArgs("/home/test.py", "/home")
            case = CaseGenerator(args)
            case._check_desc_valid({"key_test": ""}, "key_test")
        self.assertEqual(error.value.args[0], ConstManager.OP_TEST_GEN_CONFIG_INVALID_OPINFO_FILE_ERROR)
