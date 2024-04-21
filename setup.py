#!/usr/bin/env python
#
# Copyright 2015-2024 Flavio Garcia
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

import taskio
from setuptools import setup
from codecs import open
import os

with open("README.md", "r") as fh:
    long_description = fh.read()


def resolve_requires(requirements_file):
    requires = []
    if os.path.isfile(f"./{requirements_file}"):
        file_dir = os.path.dirname(f"./{requirements_file}")
        with open(f"./{requirements_file}") as f:
            for raw_line in f.readlines():
                line = raw_line.strip().replace("\n", "")
                if len(line) > 0:
                    if line.startswith("-r "):
                        partial_file = os.path.join(file_dir, line.replace(
                            "-r ", ""))
                        partial_requires = resolve_requires(partial_file)
                        requires = requires + partial_requires
                        continue
                    requires.append(line)
    return requires


setup(
    name="taskio",
    version=taskio.get_version(),
    license=taskio.__licence__,
    description=taskio.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/candango/taskio",
    author=taskio.get_author(),
    author_email=taskio.get_author_email(),
    maintainer=taskio.get_author(),
    maintainer_email=taskio.get_author_email(),
    install_requires=resolve_requires("requirements/basic.txt"),
    python_requires=">= 3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries"
    ],
    packages=["taskio"],
)
