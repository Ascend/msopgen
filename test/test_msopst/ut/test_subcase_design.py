import unittest
import pytest
import sys

from unittest import mock
from msopst.st.interface import utils
from msopst.st.interface.const_manager import ConstManager
from msopst.st.interface.subcase_design import SubCaseDesign
from msopst.st.interface.subcase_design_fuzz import SubCaseDesignFuzz
from msopst.st.interface.st_report import OpSTReport

report = OpSTReport()
case_design = SubCaseDesign("test.json", {"name": "add"}, [], report)


class TestUtilsMethods(unittest.TestCase):
    def test_check_key_exist_error(self):
        with pytest.raises(utils.OpTestGenException) as error:
            case_design._check_key_exist({"name": "add"}, "type", "INPUT")
        self.assertEqual(error.value.args[0], ConstManager.OP_TEST_GEN_INVALID_DATA_ERROR)

    def test_check_shape_valid_error1(self):
        with pytest.raises(utils.OpTestGenException) as error:
            case_design._check_shape_valid(["a", 1, 2])
        self.assertEqual(error.value.args[0], ConstManager.OP_TEST_GEN_INVALID_DATA_ERROR)

    def test_check_shape_valid_error2(self):
        with pytest.raises(utils.OpTestGenException) as error:
            case_design._check_shape_valid([-3, 1, 2])
        self.assertEqual(error.value.args[0], ConstManager.OP_TEST_GEN_INVALID_DATA_ERROR)

    def test_check_range_value_valid_error1(self):
        with pytest.raises(utils.OpTestGenException) as error:
            case_design._check_range_value_valid([-3, 1, 2])
        self.assertEqual(error.value.args[0], ConstManager.OP_TEST_GEN_INVALID_DATA_ERROR)

    def test_check_range_value_valid_error2(self):
        with pytest.raises(utils.OpTestGenException) as error:
            case_design._check_range_value_valid(["-3", 1])
        self.assertEqual(error.value.args[0], ConstManager.OP_TEST_GEN_INVALID_DATA_ERROR)

    def test_check_range_value_valid_error3(self):
        with pytest.raises(utils.OpTestGenException) as error:
            case_design._check_range_value_valid([6, 1])
        self.assertEqual(error.value.args[0], ConstManager.OP_TEST_GEN_INVALID_DATA_ERROR)

    def test_check_bin_valid_error(self):
        with pytest.raises(utils.OpTestGenException) as error:
            case_design._check_bin_valid("error.py", "/home")
        self.assertEqual(error.value.args[0], ConstManager.OP_TEST_GEN_INVALID_PATH_ERROR)

    def test_check_name_type_valid_error1(self):
        with pytest.raises(utils.OpTestGenException) as error:
            case_design._check_range_value_valid({"a": 1}, "a")
        self.assertEqual(error.value.args[0], ConstManager.OP_TEST_GEN_INVALID_DATA_ERROR)

    def test_check_name_type_valid_error2(self):
        with pytest.raises(utils.OpTestGenException) as error:
            case_design._check_range_value_valid({"a": ""}, "a")
        self.assertEqual(error.value.args[0], ConstManager.OP_TEST_GEN_INVALID_DATA_ERROR)

    def test_check_name_type_valid_error3(self):
        with pytest.raises(utils.OpTestGenException) as error:
            case_design._check_range_value_valid({"type": "error"}, "type")
        self.assertEqual(error.value.args[0], ConstManager.OP_TEST_GEN_INVALID_DATA_ERROR)

    def test_get_fuzz_func_no_syspath_pollution(self):
        original_path = sys.path.copy()
        mock_module = mock.MagicMock()
        setattr(mock_module, "my_fuzz_func", lambda: {"key": "value"})
        mock_spec = mock.MagicMock()
        mock_spec.loader.exec_module = mock.MagicMock()
        with mock.patch('importlib.util.spec_from_file_location', return_value=mock_spec):
            with mock.patch('importlib.util.module_from_spec', return_value=mock_module):
                result = SubCaseDesignFuzz._get_fuzz_func("test_module", "my_fuzz_func", "/tmp/test_module.py")
                self.assertTrue(callable(result))
                self.assertEqual(sys.path, original_path)
