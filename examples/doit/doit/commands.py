import click
import taskio


def task_function(cmd, namespace):
    print("The value set by the lambda before was %s." %
          cmd.context['a_value'])


pass_context = taskio.make_pass_decorator(taskio.CliContext, ensure=True)


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
