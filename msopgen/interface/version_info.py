#!/usr/bin/env python
# coding=utf-8
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
"""Build and format msopgen version information."""

import sys


_DISTRIBUTION_NAME = "mindstudio-opgen"
_DEFAULT_WHEEL_VERSION = "26.2.0"
_DEFAULT_BUILD_VALUE = "unknown"
_REPOSITORY_URL = "https://gitcode.com/Ascend/msopgen"

try:
    from msopgen._build_info import ASC_TOOLS_REVISION, BUILD_DATE, COMMIT_REVISION
except ImportError:
    ASC_TOOLS_REVISION = ""
    BUILD_DATE = _DEFAULT_BUILD_VALUE
    COMMIT_REVISION = _DEFAULT_BUILD_VALUE


def _get_wheel_version() -> str:
    """Return the installed wheel version, or the source-tree default."""
    if sys.version_info >= (3, 8):
        from importlib.metadata import PackageNotFoundError, version

        try:
            return version(_DISTRIBUTION_NAME)
        except PackageNotFoundError:
            return _DEFAULT_WHEEL_VERSION

    from pkg_resources import DistributionNotFound, get_distribution

    try:
        return get_distribution(_DISTRIBUTION_NAME).version
    except DistributionNotFound:
        return _DEFAULT_WHEEL_VERSION


def _is_valid_revision(revision: str) -> bool:
    value = revision.strip()
    return bool(value) and value.lower() not in ("unknown", "<unknown>")


def format_version_info() -> str:
    """Return complete, human-readable product and build information."""
    lines = [
        "msopgen {} ({})".format(_get_wheel_version(), COMMIT_REVISION),
        "Copyright (c) 2026 Huawei Technologies Co., Ltd.",
        "License: Mulan PSL v2.",
        "",
        "Build Info:",
        "  Date: {}".format(BUILD_DATE),
        "  Repo: {}".format(_REPOSITORY_URL),
    ]
    if _is_valid_revision(ASC_TOOLS_REVISION):
        lines.extend(("", "Dependencies:", "  asc-tools: {}".format(ASC_TOOLS_REVISION.strip())))
    return "\n".join(lines) + "\n"
