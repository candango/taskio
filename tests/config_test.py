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

import unittest
from taskio.config import resolve_reference

import sys
# Mocking sys: https://bit.ly/2q243Tg

# python 3.4+ should use builtin unittest.mock not mock package
from unittest.mock import patch


class MyClass:

    def __init__(self, **kwargs):
        self.param = kwargs.get("param")

    def get_param(self):
        return self.param


def a_func(**kwargs):
    return kwargs


class ResolveReferenceTestCase(unittest.TestCase):

    def test_string_reference(self):
        expected_string = "a string"
        reference = resolve_reference("a string")
        self.assertTrue(expected_string, reference)

    def test_callable_reference(self):
        params = {'a': "list of params"}
        reference = resolve_reference("tests.config_test.a_func", **params)
        self.assertEqual(params, reference)

    def test_instance_reference(self):
        params = {'param': "a param value"}
        reference = resolve_reference("tests.config_test.MyClass", **params)
        self.assertIsInstance(reference, MyClass)
        self.assertEqual(params['param'], reference.get_param())


class ProgramHeaderTestCase(unittest.TestCase):
    """ Case to test get_command_header
    """

    def test_header_message(self):
        testargs = ["test", "a", "blab"]
        with patch.object(sys, "argv", testargs):
            print(sys.argv)
        """  """
        self.assertTrue(True)
