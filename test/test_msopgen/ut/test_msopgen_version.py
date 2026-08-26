import sys
import unittest
from io import StringIO
from unittest import mock

from msopgen.interface import version_info
from msopgen.interface.arg_parser import ArgParser


class TestArgParserVersionFlag(unittest.TestCase):
    """Test -V/--version detection in ArgParser."""

    def _run_parser(self, argv):
        stdout = StringIO()
        stderr = StringIO()
        with mock.patch.object(sys, 'argv', argv), mock.patch('sys.stdout', stdout), mock.patch('sys.stderr', stderr):
            try:
                ArgParser()
            except SystemExit as ex:
                return ex.code, stdout.getvalue(), stderr.getvalue()
        return None, stdout.getvalue(), stderr.getvalue()

    def test_version_short_flag_exits_zero(self):
        code, stdout, stderr = self._run_parser(['msopgen', '-V'])
        self.assertEqual(code, 0)

    def test_version_long_flag_exits_zero(self):
        code, stdout, stderr = self._run_parser(['msopgen', '--version'])
        self.assertEqual(code, 0)

    def test_version_short_flag_prints_version_to_stdout(self):
        code, stdout, stderr = self._run_parser(['msopgen', '-V'])
        self.assertIn('msopgen', stdout)
        self.assertIn('Copyright (c) 2026 Huawei Technologies Co., Ltd.', stdout)
        self.assertIn('License: Mulan PSL v2.', stdout)
        self.assertIn('Build Info:', stdout)
        self.assertIn('Repo:', stdout)

    def test_version_long_flag_prints_version_to_stdout(self):
        code, stdout, stderr = self._run_parser(['msopgen', '--version'])
        self.assertIn('msopgen', stdout)
        self.assertIn('Build Info:', stdout)

    def test_version_flag_prints_logo_to_stderr(self):
        code, stdout, stderr = self._run_parser(['msopgen', '-V'])
        self.assertIn('MindStudio', stderr)


class TestVersionInfo(unittest.TestCase):
    """Test version_info helper functions."""

    def test_format_version_info_structure(self):
        text = version_info.format_version_info()
        self.assertIn('msopgen', text)
        self.assertIn('Copyright (c) 2026 Huawei Technologies Co., Ltd.', text)
        self.assertIn('License: Mulan PSL v2.', text)
        self.assertIn('Build Info:', text)
        self.assertIn('Date:', text)
        self.assertIn('Repo:', text)
        self.assertIn('https://gitcode.com/Ascend/msopgen', text)

    def test_format_version_info_omits_dependencies_when_no_revision(self):
        with mock.patch.object(version_info, 'ASC_TOOLS_REVISION', ''):
            text = version_info.format_version_info()
        self.assertNotIn('Dependencies:', text)

    def test_format_version_info_omits_dependencies_when_unknown(self):
        with mock.patch.object(version_info, 'ASC_TOOLS_REVISION', 'unknown'):
            text = version_info.format_version_info()
        self.assertNotIn('Dependencies:', text)

    def test_format_version_info_includes_dependencies_when_valid(self):
        with mock.patch.object(version_info, 'ASC_TOOLS_REVISION', 'abc123'):
            text = version_info.format_version_info()
        self.assertIn('Dependencies:', text)
        self.assertIn('asc-tools: abc123', text)

    def test_get_wheel_version_returns_installed_version(self):
        with mock.patch('importlib.metadata.version', return_value='91.2.3'):
            self.assertEqual(version_info._get_wheel_version(), '91.2.3')

    def test_get_wheel_version_falls_back_to_default(self):
        def raise_pnf(name):
            from importlib.metadata import PackageNotFoundError

            raise PackageNotFoundError(name)

        with mock.patch('importlib.metadata.version', side_effect=raise_pnf):
            self.assertEqual(version_info._get_wheel_version(), '26.2.0')

    def test_is_valid_revision_rejects_empty(self):
        self.assertFalse(version_info._is_valid_revision(''))
        self.assertFalse(version_info._is_valid_revision('   '))

    def test_is_valid_revision_rejects_unknown(self):
        self.assertFalse(version_info._is_valid_revision('unknown'))
        self.assertFalse(version_info._is_valid_revision('UNKNOWN'))
        self.assertFalse(version_info._is_valid_revision('<unknown>'))

    def test_is_valid_revision_accepts_real_value(self):
        self.assertTrue(version_info._is_valid_revision('abc123'))
        self.assertTrue(version_info._is_valid_revision('  abc123  '))


if __name__ == '__main__':
    unittest.main()
