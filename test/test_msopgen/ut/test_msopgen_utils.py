import unittest
import pytest
from unittest import mock
from msopgen.interface import utils
from msopgen.interface.const_manager import ConstManager


class TestUtilsMethods(unittest.TestCase):
    def test_print_error_log(self):
        utils.print_error_log("test error log")

    def test_read_json_file(self):
        with pytest.raises(utils.MsOpGenException) as error:
            utils.read_json_file('home/json_read')
        self.assertEqual(error.value.args[0], ConstManager.MS_OP_GEN_OPEN_FILE_ERROR)

    def test_load_json_expection(self):
        with pytest.raises(utils.MsOpGenException) as error:
            utils.json_load('home/json_read', '')
        self.assertEqual(error.value.args[0], ConstManager.MS_OP_GEN_READ_FILE_ERROR)

    def test_check_name_valid(self):
        utils.check_name_valid("")
        utils.check_name_valid('***')

    def test_make_dirs(self):
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('os.path.isdir', return_value=False):
                with mock.patch('os.makedirs', side_effect=OSError):
                    utils.make_dirs('/home/test1')
        self.assertEqual(error.value.args[0], ConstManager.MS_OP_GEN_MAKE_DIRS_ERROR)

    def test_read_file(self):
        with pytest.raises(utils.MsOpGenException) as error:
            utils.read_file("/home/test_read_file")
        self.assertEqual(error.value.args[0], ConstManager.MS_OP_GEN_READ_FILE_ERROR)

    def test_write_json_file(self):
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('os.fdopen', side_effect=IOError):
                utils.write_json_file('/home/test1', "ok")
        self.assertEqual(error.value.args[0], ConstManager.MS_OP_GEN_WRITE_FILE_ERROR)

    def test_check_path_valid1(self):
        with pytest.raises(utils.MsOpGenException) as error:
            utils.check_path_valid('', True)
        self.assertEqual(error.value.args[0], ConstManager.MS_OP_GEN_INVALID_PATH_ERROR)

    def test_check_path_valid2(self):
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('os.path.exists', return_value=False):
                utils.check_path_valid('/home/result.txt', False)
        self.assertEqual(error.value.args[0], ConstManager.MS_OP_GEN_INVALID_PATH_ERROR)

    def test_check_path_valid3(self):
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('os.path.exists', return_value=True):
                with mock.patch('os.access', return_value=False):
                    utils.check_path_valid('/home/result', False)
        self.assertEqual(error.value.args[0], ConstManager.MS_OP_GEN_INVALID_PATH_ERROR)

    def test_check_path_valid4(self):
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('os.path.exists', return_value=False):
                with mock.patch('os.makedirs', side_effect=OSError):
                    utils.check_path_valid('/home/result', True)
        self.assertEqual(error.value.args[0], ConstManager.MS_OP_GEN_INVALID_PATH_ERROR)

    def test_check_path_valid5(self):
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('os.path.exists', return_value=True):
                with mock.patch('os.access', return_value=[True, False]):
                    utils.check_path_valid('/home/result', True)
        self.assertEqual(error.value.args[0], ConstManager.MS_OP_GEN_INVALID_PATH_ERROR)

    def test_check_path_valid6(self):
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('os.path.exists', return_value=True):
                with mock.patch('os.access', return_value=True):
                    with mock.patch('os.path.isdir', return_value=False):
                        utils.check_path_valid('/home/result', True)
        self.assertEqual(error.value.args[0], ConstManager.MS_OP_GEN_INVALID_PATH_ERROR)

    def test_check_path_valid7(self):
        with pytest.raises(utils.MsOpGenException) as error:
            with mock.patch('os.path.exists', return_value=True):
                with mock.patch('os.access', return_value=True):
                    with mock.patch('os.path.isfile', return_value=False):
                        utils.check_path_valid('/home/result', False)
        self.assertEqual(error.value.args[0], ConstManager.MS_OP_GEN_INVALID_PATH_ERROR)

    def test_fix_name_lower_with_under(self):
        before_convert_list = ["Abc", "AbcDef", "ABCDef", "Abc2DEf", "Abc2DEF", "ABC2dEF"]
        after_convert_list = ['abc', 'abc_def', 'abc_def', 'abc2_d_ef', 'abc2_def', 'abc2d_ef']
        result = []
        for i in before_convert_list:
            result.append(utils.fix_name_lower_with_under(i))
        self.assertEqual(result, after_convert_list)

    def test_check_path_pattern_valid1(self):
        with mock.patch('os.path.realpath', return_value='c\\home'):
            with mock.patch('platform.system', return_value='Windows'):
                result = utils.check_path_pattern_valid('/home/result')
        self.assertTrue(result is not None)

    def test_check_path_pattern_valid2(self):
        with mock.patch('os.path.realpath', return_value='/home/result'):
            with mock.patch('platform.system', return_value='Linux'):
                result = utils.check_path_pattern_valid('/home/result')
        self.assertTrue(result is not None)

    def test_check_path_length_valid1(self):
        with mock.patch('os.path.realpath', return_value='c\\home'):
            with mock.patch('platform.system', return_value='Windows'):
                result = utils.check_path_length_valid('/home/result')
        self.assertTrue(result is True)

    def test_check_path_length_valid2(self):
        with mock.patch('os.path.realpath', return_value='/home/result'):
            with mock.patch('platform.system', return_value='Linux'):
                result = utils.check_path_length_valid('/home/result')
        self.assertTrue(result is True)

    def test_check_path_is_valid_softlink_should_warn_not_block(self):
        """软链接路径应输出警告但不阻断执行"""
        with mock.patch('msopgen.interface.utils.islink', return_value=True):
            with mock.patch('msopgen.interface.utils.check_path_pattern_valid', return_value=True):
                with mock.patch('msopgen.interface.utils.check_path_length_valid', return_value=True):
                    with mock.patch('msopgen.interface.utils.print_warn_log') as mock_warn:
                        # 不应抛出异常
                        utils.check_path_is_valid('/home/softlink')
                        mock_warn.assert_called_once()

    # ========== cross-module-003 fix: check_cpp_identifier_valid ==========

    def test_check_cpp_identifier_valid_empty(self):
        """空字符串应返回错误"""
        self.assertEqual(utils.check_cpp_identifier_valid(""), ConstManager.MS_OP_GEN_INVALID_PARAM_ERROR)

    def test_check_cpp_identifier_valid_none(self):
        """None 应返回错误"""
        self.assertEqual(utils.check_cpp_identifier_valid(None), ConstManager.MS_OP_GEN_INVALID_PARAM_ERROR)

    def test_check_cpp_identifier_valid_too_long(self):
        """超过1000字符应返回错误"""
        long_name = "a" * 1001
        self.assertEqual(utils.check_cpp_identifier_valid(long_name), ConstManager.MS_OP_GEN_INVALID_PARAM_ERROR)

    def test_check_cpp_identifier_valid_starts_with_number(self):
        """数字开头应返回错误"""
        self.assertEqual(utils.check_cpp_identifier_valid("1invalid"), ConstManager.MS_OP_GEN_INVALID_PARAM_ERROR)

    def test_check_cpp_identifier_valid_special_chars(self):
        """含特殊字符（注入用）应返回错误"""
        malicious_names = [
            "x; system(\"id\")",
            "name)",
            "x, TensorType({DT_FLOAT}))",
            "test\nmalicious",
            "x\r\n",
            "good_bad;",
            "name\"",
            "test'",
            "attr{",
            "attr}",
            "test(",
            "test)",
            "x`ls`",
        ]
        for name in malicious_names:
            self.assertEqual(
                utils.check_cpp_identifier_valid(name),
                ConstManager.MS_OP_GEN_INVALID_PARAM_ERROR,
                f"Should reject: {name}",
            )

    def test_check_cpp_identifier_valid_normal(self):
        """正常 C++ 标识符应通过"""
        valid_names = [
            "x",
            "input_tensor",
            "output0",
            "weight_matrix",
            "_private",
            "TensorName",
            "a" * 1000,  # 边界：刚好1000
            "y1",
            "input_desc",
        ]
        for name in valid_names:
            self.assertEqual(
                utils.check_cpp_identifier_valid(name), ConstManager.MS_OP_GEN_NONE_ERROR, f"Should accept: {name}"
            )

    # ========== cross-module-003 fix: check_cpp_value_valid ==========

    def test_check_cpp_value_valid_none(self):
        """None 应通过（无默认值）"""
        self.assertEqual(utils.check_cpp_value_valid(None), ConstManager.MS_OP_GEN_NONE_ERROR)

    def test_check_cpp_value_valid_too_long(self):
        """超过1024字符应返回错误"""
        long_val = "a" * 1025
        self.assertEqual(utils.check_cpp_value_valid(long_val), ConstManager.MS_OP_GEN_INVALID_PARAM_ERROR)

    def test_check_cpp_value_valid_dangerous_chars(self):
        """含代码注入字符应返回错误"""
        dangerous_values = [
            "1; system(\"id\")",
            "true;",
            "1)",
            "1(",
            "true\n",
            "1\r",
            "1\t",
            "true`",
            "1\"",
            "1'",
        ]
        for val in dangerous_values:
            self.assertEqual(
                utils.check_cpp_value_valid(val),
                ConstManager.MS_OP_GEN_INVALID_PARAM_ERROR,
                f"Should reject: {repr(val)}",
            )

    def test_check_cpp_value_valid_normal(self):
        """正常默认值应通过"""
        valid_values = [
            "true",
            "false",
            "1",
            "1.5",
            "0.001",
            "-1",
            "{1, 2, 3}",
            "ListInt",
            "",
        ]
        for val in valid_values:
            self.assertEqual(
                utils.check_cpp_value_valid(val), ConstManager.MS_OP_GEN_NONE_ERROR, f"Should accept: {repr(val)}"
            )


if __name__ == '__main__':
    unittest.main()
