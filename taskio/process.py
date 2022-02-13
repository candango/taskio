# -*- coding: UTF-8 -*-
#
# Copyright 2019-2022 Flávio Gonçalves Garcia
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

from .argparse_ext import TaskioArgumentError
from .config import resolve_name, resolve_version
from .model import TaskioCommand, TaskioProgram
from cartola import sysexits
from cartola.config import get_from_string
import importlib
import logging
import os
import sys


logger = logging.getLogger(__name__)


class TaskioContext(object):

    def __init__(self, conf, **kwargs):
        self._conf = conf


class TaskioLoader(object):

    def __init__(self, conf, program=None, **kwargs):
        self._conf = conf
        self._root = kwargs.get("root", "taskio")
        self._program = program
        self._version = None
        self._name = None
        self._sources = []
        if not self._conf:
            print(
                "Taskio FATAL ERROR:\n Please provide a configuration to the "
                "command.")
            sys.exit(sysexits.EX_FATAL_ERROR)
        if not self._root or self._root not in self._conf:
            print("Taskio FATAL ERROR:\n  Please add a root to the command "
                  "configuration")
            sys.exit(sysexits.EX_FATAL_ERROR)

    def load(self):
        if "program" in self.conf:
            if "name" in self.conf['program']:
                self.conf['program']['name'] = resolve_name(
                    self.conf['program']['name']
                )
            if "version" in self.conf['program']:
                self.conf['program']['version'] = resolve_version(
                    self.conf['program']['version']
                )

        if "sources" in self.conf:
            for source in self.conf['sources']:
                self._sources.append(importlib.import_module(source))

        if self._program is None:
            self._program = TaskioProgram(conf=self._conf, root=self._root)
            if "commands" in self.conf:
                for command_conf in self.conf['commands']:
                    try:
                        logger.debug(
                            "Loading commands from module {}.".format(
                                command_conf
                            )
                        )
                        command_reference = get_from_string(command_conf)
                        if isinstance(command_reference, list):
                            for command in get_from_string(command_conf):
                                command.load(self._program)
                        else:
                            command_reference.load(self._program)
                    except ModuleNotFoundError as mnfe:
                        print("Taskio FATAL ERROR:\n  Module \"{}\" not "
                              "found.\n  Please add it to the "
                              "PYTHONPATH.".format(command_conf))
                        sys.exit(sysexits.EX_FATAL_ERROR)
                self._program.name = os.path.split(sys.argv[0])[1]
                if "program" in self.conf:
                    if "name" in self.conf['program']:
                        self._program.name = resolve_name(
                            self.conf['program']['name']
                        )
                    if "version" in self.conf['program']:
                        self._program.version = resolve_version(
                            self.conf['program']['version']
                        )
                self._program.args = sys.argv[1:]
        else:
            logger.debug("The program was already loaded")

    @property
    def program(self):
        return self._program

    @property
    def name(self):
        if "program" in self.conf and "name" in self.conf['program']:
            return self.conf['program']['name']
        return None

    @property
    def version(self):
        if "program" in self.conf and "version" in self.conf['program']:
            return self.conf['program']['version']
        return None

    @property
    def full_name(self):
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
