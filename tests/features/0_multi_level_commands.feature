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

Feature: Program category
  # A taskio program is organized in categories. This organization is used to
  # help the creation of hierarchical commands. If no category is informed
  # taskio will assume the command is located at the default category.
  #
  # A program command can be located/called by:
  #
  # * No category:
  # > program command_name <args>
  #
  # * With category:
  # > program category_name command_name <args>
  #
  # * Multiple categories:
  # > program category_name sub_category_name command_name <args>
  # > program category_name sub_category_name sub_sub_category_name command_name <args>

  Scenario: Call command with no category

    Given basic program is loaded
    When nocategory is called from basic program
    Then program will resolve command
