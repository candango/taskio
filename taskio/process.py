# Copyright 2019-2024 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations


from .config import resolve_reference
from cartola import sysexits
import importlib
import logging
import sys
import typing

if typing.TYPE_CHECKING:
    from core import TaskioRootGroup

logger = logging.getLogger(__name__)


class TaskioLoader(object):

    _conf: dict
    _description: str
    _name: str
    _root: str
    _program: TaskioRootGroup
    _sources: list
    _version: str

    def __init__(self, conf, program: TaskioRootGroup = None, **kwargs):
        self._conf = conf
        self._root = kwargs.get("root", "taskio")
        self._program = program
        self._sources = []
        if not self._conf:
            print("Taskio FATAL ERROR:\n Please provide a configuration to "
                  "the command.")
            sys.exit(sysexits.EX_FATAL_ERROR)
        if not self._root or self._root not in self._conf:
            print("Taskio FATAL ERROR:\n  Please add a root to the command "
                  "configuration")
            sys.exit(sysexits.EX_FATAL_ERROR)

    def load(self):
        if "program" in self.conf:
            if "name" in self.conf['program']:
                self.conf['program']['name'] = resolve_reference(
                    self.conf['program']['name']
                )
            if "desc" in self.conf['program']:
                self.conf['program']['description'] = resolve_reference(
                    self.conf['program']['desc']
                )
            if "description" in self.conf['program']:
                self.conf['program']['description'] = resolve_reference(
                    self.conf['program']['description']
                )
            if "version" in self.conf['program']:
                self.conf['program']['version'] = resolve_reference(
                    self.conf['program']['version']
                )

        if "sources" in self.conf:
            for source in self.conf['sources']:
                self._sources.append(importlib.import_module(source))

    @property
    def program(self) -> TaskioRootGroup:
        return self._program

    @property
    def name(self) -> str:
        if "program" in self.conf and "name" in self.conf['program']:
            return self.conf['program']['name']
        return None

    @property
    def description(self) -> str:
        if "program" in self.conf and "description" in self.conf['program']:
            return self.conf['program']['description']
        return None

    @property
    def version(self) -> str:
        if "program" in self.conf and "version" in self.conf['program']:
            return self.conf['program']['version']
        return None

    @property
    def full_name(self):
        if self.description:
            if self.version:
                return "%s %s" % (self.description, self.version)
            return self.description
        if self.name:
            name = self.name
            if self.version:
                return "%s %s" % (name, self.version)
            return name
        return None

    @property
    def conf(self):
        return self._conf[self._root]

    @property
    def sources(self):
        return self._sources
