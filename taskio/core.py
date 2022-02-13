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

from . import process
import click
from click.core import Command, Group
import os
from typing import Any, List, Optional


class TaskioCommand(click.MultiCommand):

    def __init__(
            self, name=None, invoke_without_command: bool = False,
            no_args_is_help=None, subcommand_metavar=None,
            chain: bool = False, result_callback=None, **attrs,
    ) -> None:
        self.conf = {}
        if "taskio_conf" in attrs:
            self.conf = attrs.pop("taskio_conf")
        self.loader = process.TaskioLoader(self.conf, self)
        self.loader.load()
        if self.loader.full_name:
            name = self.loader.full_name
        super().__init__(name, invoke_without_command, no_args_is_help,
                         subcommand_metavar, chain, result_callback, **attrs)
        # print("Name: %s" % name)
        # print("Invoke without command: %s" % invoke_without_command)
        # print("No args is help: %s" % no_args_is_help)
        # print("Subcommand metavar: %s" % subcommand_metavar)
        # print("Chain: %s" % chain)
        # print("Result callback: %s" % result_callback)
        # print("kwargs: %s" % attrs)

    def list_commands(self, ctx: Any) -> List[str]:
        # for name, val in foo.__dict__.iteritems():
        #     if callable(val):  # check if callable (normally functions)
        #         val()
        rv = []
        groups = []
        for source in self.loader.sources:
            for key, item in source.__dict__.items():
                if isinstance(item, Command):
                    if isinstance(item, Group):
                        groups.append(item)
                    rv.append(item.name)
        for group in groups:
            for key, item in group.commands.items():
                if item.name in rv:
                    rv.remove(item.name)
                    print(item.name)
        rv.sort()
        return rv

    def get_command(self, ctx: Any, cmd_name: str) -> Optional[click.Command]:
        for source in self.loader.sources:
            for name, val in source.__dict__.items():
                if isinstance(val, Command) and val.name == cmd_name:
                    return val
        return


class TaskioContext(object):

    def __init__(self, **kwargs):
        self.current = os.getcwd()
        print("buuuu")
        print(kwargs)


def get_context():
    return click.make_pass_decorator(TaskioContext, ensure=True)
