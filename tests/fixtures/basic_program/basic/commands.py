from . import tasks
from taskio.model import TaskioCommand

_list = [
    TaskioCommand(
        "nocategory",
        "Command without category",
        help="This is a command that will be called directly without"
             "categories.",
    ),
    TaskioCommand(
        "something",
        "Do something",
        help="A do something help",
        category_name="do",
        tasks=[tasks.GenerateUuidTask]
    ),
    TaskioCommand(
        "another(thing)",
        "Do something else",
        help="A do something else help",
        category_name="do"
    ),
    TaskioCommand(
        "first(-level)",
        "Task with sub-tasks",
        help="A do something else help",
        sub_commands=[
            TaskioCommand(
                    "Child",
                    "A child task",
                    help="A child from first-level command",
                    tasks=[tasks.FirstLevelTask]
                )
        ],
        category_name="do"
    )
]
