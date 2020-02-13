#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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

from .argparse_ext import TaskioArgumentError, TaskioArgumentParser
import argparse
from cartola import sysexits
import logging
import os
import sys

categories = {}
logger = logging.getLogger(__name__)


def run(conf, **kwargs):
    root = kwargs.get("root", "taskio")
    if conf is None:
        print("Taskio FATAL ERROR:\n Please provide a configuration to the "
              "command.")
        sys.exit(sysexits.EX_FATAL_ERROR)

    if root is None or root not in conf:
        print("Taskio FATAL ERROR:\n  Please add a root to the command "
              "configuration")
        sys.exit(sysexits.EX_FATAL_ERROR)

    if "commands" in conf[root]:
        for command_conf in conf[root]['commands']:
            try:
                logger.debug(
                    "Loading commands from module {}.".format(command_conf)
                )
                exec("import {}".format(command_conf))
            except ModuleNotFoundError as mnfe:
                print("Taskio FATAL ERROR:\n  Module \"{}\" not found.\n  "
                      "Please add it to the PYTHONPATH.".format(command_conf))
                sys.exit(sysexits.EX_FATAL_ERROR)
        command_index = 1
        for arg in sys.argv[1:]:
            command_index += 1
            if arg[0] != "-":
                break
        arguments = sys.argv[1:command_index]
        if len(sys.argv[1:command_index]) == 0:
            # As command is positional let's add a default if none.
            arguments.append("help")
        parser = TaskioArgumentParser(
            prog=os.path.split(sys.argv[0])[1],
            add_help=False)
        parser.add_argument("-h", "--help", default=argparse.SUPPRESS)
        parser.add_argument("command", help="Command to executed")
        namespace = parser.parse_args(arguments)
        print(namespace)
    else:
        print("Taskio FATAL ERROR:\n  Please add commands to the command "
              "configuration root.")
        sys.exit(sysexits.EX_FATAL_ERROR)


class TaskioCommand(object):
    """ Taskio commands are classified by categories for better organization.
    Developers can create new categories of commands and distribute them with
    their application and/or components. A command with sub commands will
    became a sub category and list all sub commands by default."""

    def __init__(self, name, description, **kwargs):
        """ To register a management command it is necessary inform the
        category you the command belongs, it's name and description and a
        meaningful help to be displayed.

        :param name: Command's name
        :param description: Command's description
        :param command_help: Meaningful help to be displayed
        :param category: Command's category
        :param sub_commands: Sub commands aggregated into the command
        :param tasks: Tasks to be executed when command is called
        """
        self.name = name
        self.commands = self.name.split("(")
        if len(self.commands) > 1:
            self.commands[1] = "%s%s" % (self.commands[0],
                                         self.commands[1][:-1])
        self.description = description

        # from kwargs
        self.category = kwargs.get("category", "")
        if self.category is not None:
            if self.category not in sys.modules[__name__].categories:
                sys.modules[__name__].categories[self.category] = []
            sys.modules[__name__].categories[self.category].append(self)

        self.sub_commands = kwargs.get("sub_commands", [])
        self.command_help = kwargs.get("command_help", None)
        self.parent = kwargs.get("parent", [])
        tasks = kwargs.get("tasks", None)
        self.tasks = []
        if tasks is not None:
            if isinstance(tasks, list):
                for task in tasks:
                    self.tasks.append(task(self))
            else:
                self.tasks.append(tasks(self))
