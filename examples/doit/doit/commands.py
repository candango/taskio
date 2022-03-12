from . import tasks
from taskio.model import TaskioCommand
import taskio
from taskio import core
import click


def task_function(cmd, namespace):
    print("The value set by the lambda before was %s." %
          cmd.context['a_value'])


pass_context = click.make_pass_decorator(core.TaskioContext, ensure=True)


@click.command(short_help="Initializes a repo.")
@click.argument("path", required=False, type=click.Path(resolve_path=True))
@pass_context
def init(ctx, path):
    """Initializes a repository."""
    print(ctx)


@click.command(short_help="Do another thing")
@pass_context
def another(ctx):
    print("another")


@taskio.group(name="g1", short_help="A group level 1")
def groupl1():
    print("Group level 1 stuff")


@groupl1.group(name="g2", cls=core.TaskioGroup, short_help="A group level 2")
def groupl2():
    print("Group level 2 stuff")


@groupl2.group(name="g3", short_help="A group level 3")
def groupl3():
    print("Group level 3 stuff")


@groupl3.command(short_help="Do something inside from cli1")
def child1():
    print("Test cli1 command")
