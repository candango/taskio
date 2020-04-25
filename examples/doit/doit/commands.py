from . import tasks
from taskio.model import TaskioCommand

_list = [
    TaskioCommand(
        "help1",
        "Help Commands",
        help="Show commands help.",
    ),
    TaskioCommand(
        "something",
        "Do something",
        help="A do something help",
        category_name="do",
        tasks=[tasks.GenerateUuidTask]
    ),
    TaskioCommand(
        "something-(else)",
        "Do something else",
        help="A do something else help",
        category_name="do"
    )
]
