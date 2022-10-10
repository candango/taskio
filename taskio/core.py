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
from click.core import Command, Context, Group, HelpFormatter
from typing import Any, Callable, Dict, List, Optional, Sequence, Union


class TaskioContext(Context):

    def __init__(
            self,
            command: Command,
            parent: Optional[Context] = None,
            info_name: Optional[str] = None,
            obj: Optional[Any] = None,
            auto_envvar_prefix: Optional[str] = None,
            default_map: Optional[Dict[str, Any]] = None,
            terminal_width: Optional[int] = None,
            max_content_width: Optional[int] = None,
            resilient_parsing: bool = False,
            allow_extra_args: Optional[bool] = None,
            allow_interspersed_args: Optional[bool] = None,
            ignore_unknown_options: Optional[bool] = None,
            help_option_names: Optional[List[str]] = None,
            token_normalize_func: Optional[Callable[[str], str]] = None,
            color: Optional[bool] = None,
            show_default: Optional[bool] = None,
    ) -> None:
        super().__init__(command, parent, info_name, obj, auto_envvar_prefix,
                         default_map, terminal_width, max_content_width,
                         resilient_parsing, allow_extra_args,
                         allow_interspersed_args, ignore_unknown_options,
                         help_option_names, token_normalize_func, color,
                         show_default)
        self.loader = None


class TaskioMultiCommand(click.MultiCommand):

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
        if "taskio_conf" in attrs:
            if self.loader.full_name:
                name = self.loader.full_name
        super().__init__(name, invoke_without_command, no_args_is_help,
                         subcommand_metavar, chain, result_callback, **attrs)
        self.context_class = TaskioContext

    def __new__(cls, *args, **kwargs):
        """ Set TaskioMultiCommand as a singleton following:
        https://bit.ly/3rGdBjh
        :param args:
        :param kwargs:
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(
                TaskioMultiCommand, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def get_instance():
        """Return the TaskioMultiCommand previously created instance.
        If called after a regular initialization, will generate an error due
        to lack of parameters.
        """
        return TaskioMultiCommand.__new__(TaskioMultiCommand)

    def make_context(
        self,
        info_name: Optional[str],
        args: List[str],
        parent: Optional[Context] = None,
        **extra: Any,
    ) -> Context:
        """This function when given an info name and arguments will kick
        off the parsing and create a new :class:`Context`.  It does not
        invoke the actual command callback though.

        To quickly customize the context class used without overriding
        this method, set the :attr:`context_class` attribute.

        :param info_name: the info name for this invocation.  Generally this
                          is the most descriptive name for the script or
                          command.  For the toplevel script it's usually
                          the name of the script, for commands below it it's
                          the name of the command.
        :param args: the arguments to parse as list of strings.
        :param parent: the parent context if available.
        :param extra: extra keyword arguments forwarded to the context
                      constructor.

        .. versionchanged:: 8.0
            Added the :attr:`context_class` attribute.
        """
        ctx = super().make_context(info_name, args, parent, **extra)
        ctx.loader = self.loader
        return ctx

    def list_commands(self, ctx: Any) -> List[str]:
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
        rv.sort()
        return rv

    def get_command(self, ctx: Any, cmd_name: str) -> Optional[click.Command]:
        for source in self.loader.sources:
            for name, val in source.__dict__.items():
                if isinstance(val, Command) and val.name == cmd_name:
                    return val
        return

    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        pieces = self.collect_usage_pieces(ctx)
        formatter.write(self.loader.full_name)
        formatter.write("\n")
        formatter.write_usage(self.loader.name, " ".join(pieces))


class TaskioGroup(Group):

    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        TaskioMultiCommand.get_instance().format_usage(ctx, formatter)

    def resolve_params(self, ctx):
        params = ""
        current_context = ctx
        while current_context:
            if current_context.parent is not None:
                params = " ".join([current_context.info_name, params])
            current_context = current_context.parent
        return params

    def group(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], "Group"]:
        """A shortcut decorator for declaring and attaching a group to
        the group. This takes the same arguments as :func:`group` and
        immediately registers the created group with this group by
        calling :meth:`add_command`.

        To customize the group class used, set the :attr:`group_class`
        attribute.

        .. versionchanged:: 8.0
            Added the :attr:`group_class` attribute.
        """
        from .decorators import group

        if self.group_class is not None and "cls" not in kwargs:
            if self.group_class is type:
                kwargs["cls"] = type(self)
            else:
                kwargs["cls"] = self.group_class

        def decorator(f: Callable[..., Any]) -> "TaskioGroup":
            cmd = group(*args, **kwargs)(f)
            self.add_command(cmd)
            return cmd

        return decorator


class TaskioCommand(Command):

    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        TaskioMultiCommand.get_instance().format_usage(ctx, formatter)


class TaskioCliContext(object):

    def __init__(self, **kwargs):
        self.context = click.get_current_context()


def get_context():
    return click.make_pass_decorator(TaskioCliContext, ensure=True)
