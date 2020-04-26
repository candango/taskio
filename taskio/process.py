#!/usr/bin/env python
#
# Copyright 2019-2020 Flavio Garcia
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

from . import argparse_ext
from .config import resolve_name, resolve_version
from .model import TaskioProgram
from cartola import sysexits
from cartola.config import get_from_string
import logging
import os
import sys

logger = logging.getLogger(__name__)


class TaskioLoader(object):

    def __init__(self, conf, **kwargs):
        self._conf = conf
        self._root = kwargs.get("root", "taskio")
        if self._conf is None:
            print(
                "Taskio FATAL ERROR:\n Please provide a configuration to the "
                "command.")
            sys.exit(sysexits.EX_FATAL_ERROR)

        if self._root is None or self._root not in self._conf:
            print("Taskio FATAL ERROR:\n  Please add a root to the command "
                  "configuration")
            sys.exit(sysexits.EX_FATAL_ERROR)

    def load_program(self):
        program = TaskioProgram(conf=self._conf, root=self._root)
        if "commands" in self.conf:
            for command_conf in self.conf['commands']:
                try:
                    logger.debug(
                        "Loading commands from module {}.".format(command_conf)
                    )
                    command_reference = get_from_string(command_conf)
                    if isinstance(command_reference, list):
                        for command in get_from_string(command_conf):
                            command.load(program)
                except ModuleNotFoundError as mnfe:
                    print("Taskio FATAL ERROR:\n  Module \"{}\" not found.\n  "
                          "Please add it to the PYTHONPATH.".format(
                        command_conf))
                    sys.exit(sysexits.EX_FATAL_ERROR)
            program.name = os.path.split(sys.argv[0])[1]
            if "program" in self.conf:
                if "name" in self.conf['program']:
                    program.name = resolve_name(self.conf['program']['name'])
                if "version" in self.conf['program']:
                    program.version = resolve_version(
                        self.conf['program']['version']
                    )
            program.args = sys.argv[1:]
        return program

    @property
    def conf(self):
        return self._conf[self._root]


class TaskioRunner(object):

    def run(loader):
        pass

