#!/usr/bin/env python
#
# Copyright 2015-2023 Flavio Garcia
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
import sys

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    print("error: Upgrade to a pip version newer than 10. Run \"pip install "
          "--upgrade pip\".")
    sys.exit(1)

with open("README.md", "r") as fh:
    long_description = fh.read()


# Solution from http://bit.ly/29Yl8VN
def resolve_requires(requirements_file):
    try:
        requirements = parse_requirements("./%s" % requirements_file,
                                          session=False)
        return [str(ir.req) for ir in requirements]
    except AttributeError:
        # for pip >= 20.1.x
        # Need to run again as the first run was ruined by the exception
        requirements = parse_requirements("./%s" % requirements_file,
                                          session=False)
        # pr stands for parsed_requirement
        return [str(pr.requirement) for pr in requirements]


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
    python_requires=">= 3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries"
    ],
    packages=["taskio"],
)
