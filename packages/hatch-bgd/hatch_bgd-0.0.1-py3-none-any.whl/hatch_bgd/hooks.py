# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
from hatchling.plugin import hookimpl

from hatch_bgd.version_source import VCSVersionSource


@hookimpl
def hatch_register_version_source():
    return VCSVersionSource
