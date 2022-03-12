from .core import TaskioCommand, TaskioMultiCommand, TaskioGroup
from click.decorators import _make_command
import types
import typing as t

F = t.TypeVar("F", bound=t.Callable[..., t.Any])
FC = t.TypeVar("FC", bound=t.Union[t.Callable[..., t.Any], TaskioCommand])


def group(name: t.Optional[str] = None,
          **attrs: t.Any) -> t.Callable[[F], TaskioGroup]:
    """Creates a new :class:`Group` with a function as callback.  This
    works otherwise the same as :func:`command` just that the `cls`
    parameter is set to :class:`Group`.
    """
    attrs.setdefault("cls", TaskioGroup)
    return t.cast(TaskioGroup, command(name, **attrs))


def command(
    name: t.Optional[str] = None,
    cls: t.Optional[t.Type[TaskioCommand]] = None,
    **attrs: t.Any,
) -> t.Callable[[F], TaskioCommand]:
    r"""Creates a new :class:`Command` and uses the decorated function as
    callback.  This will also automatically attach all decorated
    :func:`option`\s and :func:`argument`\s as parameters to the command.

    The name of the command defaults to the name of the function with
    underscores replaced by dashes.  If you want to change that, you can
    pass the intended name as the first argument.

    All keyword arguments are forwarded to the underlying command class.

    Once decorated the function turns into a :class:`Command` instance
    that can be invoked as a command line utility or be attached to a
    command :class:`Group`.

    :param name: the name of the command.  This defaults to the function
                 name with underscores replaced by dashes.
    :param cls: the command class to instantiate.  This defaults to
                :class:`Command`.
    """
    if cls is None:
        cls = TaskioCommand

    def decorator(f: t.Callable[..., t.Any]) -> TaskioCommand:
        cmd = _make_command(f, name, attrs, cls)  # type: ignore
        cmd.__doc__ = f.__doc__
        return cmd

    return decorator


def root(
    name: t.Optional[str] = None,
    **attrs: t.Any,
) -> t.Callable[[F], TaskioCommand]:
    r"""Creates a new :class:`Command` and uses the decorated function as
    callback.  This will also automatically attach all decorated
    :func:`option`\s and :func:`argument`\s as parameters to the command.

    The name of the command defaults to the name of the function with
    underscores replaced by dashes.  If you want to change that, you can
    pass the intended name as the first argument.

    All keyword arguments are forwarded to the underlying command class.

    Once decorated the function turns into a :class:`Command` instance
    that can be invoked as a command line utility or be attached to a
    command :class:`Group`.

    :param name: the name of the command.  This defaults to the function
                 name with underscores replaced by dashes.
    :param cls: the command class to instantiate.  This defaults to
                :class:`Command`.
    """
    cls = TaskioMultiCommand

    def decorator(f: t.Callable[..., t.Any]) -> TaskioMultiCommand:
        cmd = _make_command(f, name, attrs, cls)  # type: ignore
        cmd.__doc__ = f.__doc__
        return cmd

    return decorator