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

from .argparse_ext import TaskioArgumentError, TaskioArgumentParser
from .config import resolve_name, resolve_version
import argparse
from cartola import sysexits
from cartola.config import get_from_string
import logging
import os
import sys

logger = logging.getLogger(__name__)


class TaskioCategory(object):

    def __init__(self, program, name):
        self._program = program
        self._name = None
        self._commands = []
        self.name = name

    @property
    def program(self):
        return self._program

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def commands(self):
        return self._commands

    def add(self, command):
        self.commands.append(command)
        command.parent = self
        command.level = self.level + 1

    @property
    def level(self):
        if self.name == self.program._TASKIO_NO_CATEGORY_:
            return 0
        return 1

    def has_category(self, name):
        return self.program.has_category(name)

    @property
    def help(self):
        padding = "  " * self.level
        help_message = ""
        if self.level > 0:
            help_message = "{}{}\n".format(padding, self.name)
        if len(self.commands) > 0:
            help_message = (
                "{help_message}{padding}\n{padding}Commands:"
                "\n\n".format(help_message=help_message, padding=padding)
            )
            for command in self.commands:
                help_message = (
                    "{help_message}{padding}{command_help}\n".format(
                        help_message=help_message,
                        padding=padding,
                        command_help=command.help
                    ))
            help_message = "{help_message}\n".format(help_message=help_message)
        if self.level == 0:
            help_message = "{}{}Categories:\n".format(help_message, padding)
        return help_message

    def get_existing_command(self, command):
        """ Check if the given command was registered. In another words if it
        exists.
        """
        for category_command in self.commands:
            if category_command.match(self.namespace.command):
                return category_command
        return None


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
        self._name = None
        self._parent = None
        self._program = None
        self._category_name = None
        self._command_help = None
        self._level = 0

        self.name = name
        self.description = description

        # from kwargs
        self.category_name = kwargs.get("category_name", "")
        self.sub_commands = kwargs.get("sub_commands", [])
        self.command_help = kwargs.get("command_help", None)
        self.parent = kwargs.get("parent", None)

        tasks = kwargs.get("tasks", None)
        self.tasks = []
        if tasks is not None:
            if isinstance(tasks, list):
                for task in tasks:
                    self.tasks.append(task(self))
            else:
                self.tasks.append(tasks(self))


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def category_name(self):
        return self.program.resolve_category_name(self._category_name)

    @category_name.setter
    def category_name(self, category_name):
        self._category_name = category_name

    @property
    def commands(self):
        commands = self._name.split("(")
        if len(commands) > 1:
            commands[1] = "%s%s" % (commands[0], commands[1][:-1])
        return commands

    @property
    def command_help(self):
        return self._command_help

    @command_help.setter
    def command_help(self, command_help):
        self._command_help = command_help

    @property
    def help(self):
        return "{}".format(self.name)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def program(self):
        return self._program

    @program.setter
    def program(self, program):
        self._program = program

    def load(self, program):
        self._program = program
        if not self.program.has_category(self.category_name):
            self.program.add_category(self.category_name)
        self.program.get_category(self.category_name).add(self)

    def match(self, command):
        return command in self.commands


class TaskioProgram(object):

    def __init__(self, **kwargs):
        self._whole_conf = kwargs.get("conf", {})
        self._args = None
        self._command_index = None
        self._name = None
        self._namespace = None
        self._parser = None
        self._version = None
        self._root = kwargs.get("root", "taskio")
        self._categories = dict()
        self._TASKIO_NO_CATEGORY_ = "__taskio_no_category__"
        self.add_category(self._TASKIO_NO_CATEGORY_)

    @property
    def categories(self):
        return self._categories

    @property
    def conf(self):
        return self._whole_conf[self._root]

    @property
    def name(self):
        return self._name

    @property
    def namespace(self):
        return self._namespace

    @property
    def parser(self):
        return self._parser

    def has_category(self, name):
        if name in self.categories:
            return True
        return False

    def add_category(self, name):
        if self.has_category(name):
            logger.debug("Category %s already exists. Ignoring program's add"
                         "new category call." % name)
        else:
            logger.debug("Adding new category %s." % name)
            self.categories[name] = TaskioCategory(self, name)

    def get_category(self, name):
        return self.categories[name]

    def resolve_category_name(self, name):
        if name is None or name.strip() == "":
            return self._TASKIO_NO_CATEGORY_
        return name.strip()

    def what_category(self):
        # First check if command is in _TASKIO_NO_CATEGORY_
        for category_command in self.get_category(
                self._TASKIO_NO_CATEGORY_).commands:
            if category_command.match(self._namespace.command):
                return self.get_category(self._TASKIO_NO_CATEGORY_)

        # If not found in commands set to next argument index
        self._command_index += 1

        for name, category in self.categories.items():
            if name == self._namespace.command:
                self._command_index += 1
                return category

        return None

    def get_existing_command(self):
        """ Check if the given command was registered. In another words if it
        exists.
        """
        print(self.namespace)

        for name, category in self.categories.items():
            for category_command in category.commands:
                if category_command.match(self.namespace.command):
                    return category_command
        return None

    def load(self):
        if "commands" in self.conf:
            for command_conf in self.conf['commands']:
                try:
                    logger.debug(
                        "Loading commands from module {}.".format(command_conf)
                    )
                    command_reference = get_from_string(command_conf)
                    if isinstance(command_reference, list):
                        for command in get_from_string(command_conf):
                            command.load(self)
                except ModuleNotFoundError as mnfe:
                    print("Taskio FATAL ERROR:\n  Module \"{}\" not found.\n  "
                          "Please add it to the PYTHONPATH.".format(
                        command_conf))
                    sys.exit(sysexits.EX_FATAL_ERROR)
            self._name = os.path.split(sys.argv[0])[1]
            if "program" in self.conf:
                if "name" in self.conf['program']:
                    self._name = resolve_name(self.conf['program']['name'])
                if "version" in self.conf['program']:
                    self._version = resolve_version(
                        self.conf['program']['version']
                    )
            self._command_index = 0
            self._name = os.path.split(sys.argv[0])[1]
            self._args = sys.argv[1:]
            if len(self._args) == 0:
                # As command is positional let's add a default if none.
                self._args.append("help")
            self._parser = TaskioArgumentParser(
                prog=self.name,
                add_help=False)
            self.parser.add_argument("-h", "--help", default=argparse.SUPPRESS)
            self.parser.add_argument("command", help="Command to executed")
            print(self._command_index)
            self._namespace = self.parser.parse_args(self.current_args())

    def run(self, command):
        command.run(sys.argv[self.command_index:])

    def current_args(self):
        return self._args[self._command_index:1]

    def what_to_run(self, category):
        print(self._command_index)
        try:
            return category.get_existing_command(self.current_args()[0])
        except IndexError:
            return None

    def show_command_line_usage(self, usage=False):
        """ Show the command line help
        """
        print(self.get_command_header(usage))
        for name, category in self.categories.items():
            print(category.help)

    def get_command_header(self, usage=False):
        """ Return the command line header

        :param parser:
        :param usage_message:
        :param usage:
        :return: The command header
        """
        header_message = self.name
        if self._version is not None:
            header_message = "%s %s" % (header_message,self._version)
        if usage:
            test = """{% if usage %}
    Usage: {{ parser.prog }} [-h] {%raw usage_message %}
    {% end %}"""

        # loader = template.Loader(os.path.join(
        #     firenado.conf.ROOT, 'management', 'templates', 'help'))
        # return loader.load("header.txt").generate(
        #     parser=parser, usage_message=usage_message, usage=usage,
        #     firenado_version=".".join(map(str, firenado.__version__))).decode(
        #     sys.stdout.encoding)
        return header_message
