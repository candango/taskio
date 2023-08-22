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

import click
import taskio


def task_function(cmd, namespace):
    print("The value set by the lambda before was %s." %
          cmd.context['a_value'])


pass_context = click.make_pass_decorator(taskio.CliContext, ensure=True)


@taskio.command(short_help="Generates an uuid4 string")
@click.argument("path", required=False, type=click.Path(resolve_path=True))
@pass_context
def uuid(ctx):
    """Initializes a repository."""
    print(ctx)


@click.command(short_help="Do another thing")
@pass_context
def another(ctx):
    print(ctx)
    print("another")


@taskio.group(name="g1", short_help="A group level 1")
@pass_context
def group1(ctx):
    pass


@group1.group(name="g2", short_help="A group level 2")
def group2():
    print("Group level 2 stuff")


@group2.group(name="g3", short_help="A group level 3")
def group3():
    print("Group level 3 stuff")


@group3.command(short_help="Do something inside from cli1")
def child1():
    print("Test cli1 command")
