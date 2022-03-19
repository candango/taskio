#!/usr/bin/env python
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
import logging


context_settings = {}
logger = logging.getLogger(__name__)


def run(conf, **kwargs):
    print(conf)
    exit()
    loader = process.TaskioLoader(conf, **kwargs)
    loader.load()
    runner = process.TaskioRunner(loader)
    runner.run()
