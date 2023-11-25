# Copyright 2019-2023 Flavio Garcia
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


@when("{command} is called from {program} program")
def step_is_called_from_program(context, command, program):
    program_attribute = "%s_program" % program
    current_program: TaskioLoader = getattr(context, program_attribute)
    current_program.program.args = [command]
    current_category = current_program.program.what_category()
    context.what_to_run = current_program.program.what_to_run(
        current_category)


@then("program will resolve command")
def set_program_will_resolve_command(context):
    context.tester.assertTrue(isinstance(context.what_to_run, TaskioCommand))
