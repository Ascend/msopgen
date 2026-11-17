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

import sys

import pytest

from msopgen import msopgen
from msopgen.interface import utils
from msopgen.interface.const_manager import ConstManager


@pytest.mark.parametrize("compute_unit", [
    "ai_core-ascendxxx",
    "ai_core-AscendXXX",
    "ai_core-ascend910B4,ai_core-ascendxxx",
])
def test_gen_rejects_soc_placeholder(tmp_path, monkeypatch, capsys, compute_unit):
    input_path = tmp_path / "op.json"
    input_path.write_text('[{"op": "AddCustom"}]', encoding="utf-8")
    output_path = tmp_path / "out"
    # pytest's temporary directory may contain non-ASCII characters.
    monkeypatch.setattr(utils, "check_path_is_valid", lambda _: None)
    monkeypatch.setattr(sys, "argv", [
        "msopgen", "gen", "-i", str(input_path), "-c", compute_unit,
        "-f", "pytorch", "-lan", "cpp", "-out", str(output_path),
    ])

    with pytest.raises(SystemExit) as error:
        msopgen.main()

    assert error.value.code == ConstManager.MS_OP_GEN_CONFIG_INVALID_COMPUTE_UNIT_ERROR
    assert "placeholder" in capsys.readouterr().out
    assert not output_path.exists()
