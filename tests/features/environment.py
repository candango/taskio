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

from behave import fixture, use_fixture
from cartola.config import load_yaml_file
from taskio import process
import logging
import os
import sys
from tests import PROJECT_ROOT, FIXTURES_ROOT
from unittest.case import TestCase

logger = logging.getLogger(__name__)

TAKS_IO_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, "taskio"))

if FIXTURES_ROOT not in sys.path:
    logger.debug("Appending FIXTURES_ROOT to PYTHONPATH.")
    sys.path.append(FIXTURES_ROOT)


@fixture
def basic_program(context, timeout=1, **kwargs):
    basic_program_address = os.path.join(FIXTURES_ROOT, "basic_program")
    config_file = os.path.join(basic_program_address, "basic", "basic.yml")
    if basic_program_address not in sys.path:
        logger.debug("Appending basic program to PYTHONPATH.")
        sys.path.append(basic_program_address)
    conf = load_yaml_file(config_file)
    loader = process.TaskioLoader(conf, **kwargs)
    loader.load()
    context.basic_program = loader
    yield context.basic_program


@fixture
def tester(context, timeout=1, **kwargs):
    context.tester = TestCase()
    yield context.tester


def before_all(context):
    use_fixture(basic_program, context)
    use_fixture(tester, context)


def after_all(context):
    pass
