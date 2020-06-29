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

from .argparse_ext import TaskioArgumentError
from .config import resolve_name, resolve_version
from .model import TaskioCommand, TaskioProgram
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
        self._program = None
        if self._conf is None:
            print(
                "Taskio FATAL ERROR:\n Please provide a configuration to the "
                "command.")
            sys.exit(sysexits.EX_FATAL_ERROR)

        if self._root is None or self._root not in self._conf:
            print("Taskio FATAL ERROR:\n  Please add a root to the command "
                  "configuration")
            sys.exit(sysexits.EX_FATAL_ERROR)

    def load(self):
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
    def conf(self):
        return self._conf[self._root]


class TaskioRunner(object):

    def __init__(self, loader):
        self._loader = loader

    def run(self):
        category = self._loader.program.what_category()
        if category is not None:
            command = self._loader.program.what_to_run(category)
            if command is not None:
                try:
                    command.run(self._loader.program.current_args())
                except TaskioArgumentError as error:
                    if error.source is not None:
                        if isinstance(error.source, TaskioCommand):
                            error_message = error.source.get_error_message(
                                error)
                            print(error_message)
                            sys.exit(error.source.exit_code)
                    # Get all taskio
                    print("***********")
                    print(error.help)
                    print("***********")
                    if error.show_usage:
                        print(error.source.usage)
                        print(error.source.help)
                    sys.exit(sysexits.EX_MISUSE)
        self._loader.program.show_command_line_usage()
        sys.exit()
