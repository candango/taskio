#!/usr/bin/env python
#
# Copyright 2019-2022 Flavio Gonçalves Garcia
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




class FirstLevelTask():

    def run(self, namespace):
        print("buuuu")


class GenerateUuidTask():

    def add_arguments(self, parser):
        """

        :param  parser:
        :return:
        """
        parser.add_argument("-a", "--addresses", required=True)

    def get_error_message(self, error):
        return "Error executing 'do something'.\n%s" % error.help

    def is_my_error(self, error):
        if "argument -a/--addresses" in error.help:
            return True
        return False

    """ Generates an uuid4 string
    """
    def run(self, namespace=None):
        from uuid import uuid4
        print(uuid4())
