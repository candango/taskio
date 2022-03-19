# Copyright 2019-2022 Flavio Gonçalves Garcia
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
import click
from cartola.config import load_yaml_file
import logging
import os
import taskio
from taskio import core
import sys

logger = logging.getLogger(__name__)

conf = {
    'commands': []
}

DOIT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOIT_CONFIG_FILE = os.path.join(DOIT_ROOT, "doit", "doit.yml")


pass_context = click.make_pass_decorator(core.TaskioContext, ensure=True)


@taskio.root(taskio_conf=load_yaml_file(DOIT_CONFIG_FILE))
@pass_context
def doit_cli(ctx):
    pass


if DOIT_ROOT not in sys.path:
    logger.debug("Appending DOIT_ROOT to PYTHONPATH.")
    sys.path.append(DOIT_ROOT)
