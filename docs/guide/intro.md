# Introduction

Taskio is a Python library for command-line argument processing based on
argparse designed to support multi-level commands organized in categories.

After the framework finds the command to be executed based on the arguments
passed to the program, all tasks assigned to the program will be executed or an
error message will be displayed to the user.

A configuration dictionary is used to define some program's basic properties
and where Taskio must search for commands to be loaded in it's structure.
Preferentially Candango projects will store this structure and use
`cartola.config.load_yaml_file` function to provide a configuration to
`taskio.cli.run`. This step isn't mandatory and a developer can retrieve this
information from any source such as a database or another type of configuration
file.  

During it's execution arguments are resolved and the remaining arguments are
assigned to it's children as they are being resolved. Each item from this
execution will have it's on argument parser with arguments based it's level in
the hierarchy.

For instance, when we execute the command `myprogram cat1 command1 subcommand1
-p parameter`:

1. taskio will try to find the category cat1 or the command cat1 with no
category
1. in the case we find cat1 then we try to find command1 in it's children
1. command1 exists and subcommand1 is also found as it's children
1. the subcommand1's parser will validate if `-p parameter` is valid to this
command
1. a task inside the parameter added the parameter to subcommand1's parser
before, when taskio was building the program structure, therefore the parameter
is valid
1. all subcommand1's tasks are executed using the it's argument parser

On this execution if takio don't find a category or a command an error is
displayed to the user with the program usage.

Arguments are added to the command by it's tasks.

Help messages and error messages are defined inside commands and tasks.

If a parse error is found inside a command, a customized error message is
displayed to the user. 

A command without(or empty) category is designed to the default category and
can be run directly as:

- `myprogram command1`
- `myprogram command2 subcommand`

This structure was inherited from Firenado's management tool in order to create
a command-line framework to help implement programs across the Candango Open
Source Group projects and anyone that could be interest to use it for personal
or commercial use.

Taskio is licensed under Apache 2 license.
