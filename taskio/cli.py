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

from .model import TaskioProgram
from cartola import sysexits
import logging
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

    program = TaskioProgram(conf=conf, root=root)
    program.load()
    category = program.what_category()
    if category is not None:
        command = program.what_to_run(category)
        if command is not None:
            program.run(command)

    program.show_command_line_usage()
    sys.exit()
