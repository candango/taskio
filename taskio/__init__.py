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

__author__ = "Flavio Garcia <piraz@candango.org>"
__description__ = "A Python library for command-line argument processing."
__version__ = (0, 0, 6)
__licence__ = "Apache License V2.0"


def get_version():
    return ".".join(map(str, __version__))


def get_author():
    return __author__.split(" <")[0]


def get_author_email():
    return __author__.split(" <")[1][:-1]


try:
    from .core import TaskioCliContext as CliContext
    from .core import TaskioContext as Context
    from .core import TaskioRootGroup as RootGroup
    from .decorators import command as command
    from .decorators import group as group
    from .decorators import root as root
# Will try to load modules not found during a clean installation.
# Ignoring this error here.
except ModuleNotFoundError:
    pass
