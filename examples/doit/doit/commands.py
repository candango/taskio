from taskio.model import TaskioCommand

list = [
    TaskioCommand(
        "help1",
        "Help Commands",
        help="Show commands help.",
        category_name=""
    ),
    TaskioCommand(
        "something",
        "Do something",
        help="A do something help",
        category_name="do"
    ),
    TaskioCommand(
        "something-(else)",
        "Do something else",
        help="A do something else help",
        category_name="do"
    )
]
