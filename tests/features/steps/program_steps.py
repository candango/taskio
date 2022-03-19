# -*- coding: UTF-8 -*-
#
# Copyright 2019-2021 Flávio Gonçalves Garcia
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

from behave import given, when, then
from taskio.process import TaskioLoader
from behave.api.async_step import async_run_until_complete
from tests import PROJECT_ROOT
import sys


@given("{program} program is loaded")
def step_program_is_loaded(context, program):
    program_attribute = "%s_program" % program
    context.current_program = getattr(context, program_attribute)
    context.tester.assertTrue(
        isinstance(context.current_program, TaskioLoader))
