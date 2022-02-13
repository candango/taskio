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

import argparse
from gettext import gettext as _


class TaskioException(Exception):
    """ Base exception to be thrown by any part of the code and be displayed by
    the current runner.
    """

    def __init__(self, *args, **kwargs):
        super(TaskioException, self).__init__(*args, **kwargs)
        self._help = kwargs.get("help", None)
        self._source = kwargs.get("source", None)
        self._reason = kwargs.get("reason", None)
        self._show_usage = False

    @property
    def help(self):
        return self._help

    @help.setter
    def help(self, help):
        self._help = help

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source

    @property
    def reason(self):
        return self._reason

    @reason.setter
    def reason(self, reason):
        self._reason = reason

    @property
    def show_usage(self):
        return self._show_usage

    @show_usage.setter
    def show_usage(self, show_usage):
        self._show_usage = show_usage


class TaskioArgumentError(TaskioException):
    """ An error thrown while parsing arguments with TaskioArgumentParser.
    """
    pass


class TaskioArgumentParser(argparse.ArgumentParser):
    """ Argument parser that trows an exception leaving stderr untouched.
    """

    def error(self, message):
        args = {'message': message}
        message = _("%(message)s") % args
        raise TaskioArgumentError(message)
