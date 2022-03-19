# Configuration

Here is described the configuration dictionary used to build the program
structure before it's execution.

Here is an example:

```:python
from taskio import cli

conf = {
    taskio: {
        name: "myprogram",
        version: "0.1",
        commands: [
            "myprogram.commands._list"
        ]
    }
}

if __name__ == "__main__":
    cli.run(conf)
```

A configuration dictionary must have a root index. By default this index is
'taskio' but it can be changed. In this case it is necessary to inform the
custom root to execute the program:

```:python
from taskio import cli

conf = {
    custom_root: {
        name: "myprogram",
        version: "0.1",
        commands: [
            "myprogram.commands._list"
        ]
    }
}

if __name__ == "__main__":
    cli.run(conf, root="custom_root")
```

The name and version are used to create the program header and they are not
mandatory. If name isn't provided taskio will use the first item from sys.argv.
If version isn't provided no version reference will be displayed.

We must provide the list of commands to be loaded to the program. In the list
must have a reference for a list of commands in a module.

On the previous examples we have `myprogram.commands._list` inside the commands
list. Here is an implementation:

```:python
from . import tasks
from taskio.model import TaskioCommand

_list = [
    TaskioCommand(
        "command1",
        "Do command 1 tasks",
        help="I do command 1 tasks",
        category_name="category1",
        tasks=[tasks.Command1Task1, tasks.Command1Task2]
    ),
    TaskioCommand(
        "command2",
        "Do command 2 tasks",
        help="I do the command 2 task",
        category_name="category1",
        tasks=[tasks.Command2Task]
    )
]

```

On this program we can execute:

```:shell script
> myprogram category1 command1
> myprogram category1 command2
```
