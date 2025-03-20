# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
import os
import subprocess

from hatchling.version.source.plugin.interface import VersionSourceInterface


class VCSVersionSource(VersionSourceInterface):
    PLUGIN_NAME = 'bgd'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__config_base_version = None
        self.__config_type = None

    @property
    def config_build_type(self):
        if self.__config_type is None:
            build_type = self.config.get("build-type", "dev")
            if not isinstance(build_type, str):
                raise TypeError("option `type` must be a string with options ['dev', 'release'].")

            self.__config_build_type = build_type

        return self.__config_build_type

    @property
    def config_base_version(self):
        if self.__config_base_version is None:
            base_version = self.config.get("base-version", "0.0.1")
            if not isinstance(base_version, str):
                raise TypeError("option `base-version` must be a string")

            self.__config_base_version = base_version

        return self.__config_base_version

    def get_git_info(self):
        git_root = (
            subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=self.root, stderr=subprocess.STDOUT)
            .decode()
            .strip()
        )

        commit_id = subprocess.check_output(["git", "log", "-1", "--pretty=format:%H"], cwd=git_root).decode().strip()[:7]

        commit_date = (
            subprocess.check_output(["git", "log", "-1", "--pretty=format:%cd", "--date=iso"], cwd=git_root)
            .decode()
            .strip()
            .split()[0]
            .replace("-", "")
        )

        return commit_id, commit_date
    
    def get_version_data(self):
        if self.config_build_type == "dev":
            commit_id, commit_date = self.get_git_info()
            version = f"{self.config_base_version}+g{commit_id}.d{commit_date}"
        else:
            version = self.config_base_version
        return {'version': version}
