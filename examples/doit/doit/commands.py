from taskio.command import TaskioCommand

TaskioCommand(
    "help",
    "Help Commands",
    help="Show commands help.",
    category=""
)

TaskioCommand(
    "something",
    "Do something",
    help="A do something help",
    category="do"
)

TaskioCommand(
    "something-else",
    "Do something else",
    help="A do something else help",
    category="do"
)
