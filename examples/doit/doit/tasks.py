from taskio.model import TaskioTask


class GenerateUuidTask(TaskioTask):

    def add_arguments(self, parser):
        """

        :param  parser:
        :return:
        """
        parser.add_argument("-a", "--addresses", required=True)

    def get_error_message(self, parser, error):
        return "This is the error message"

    """ Generates an uuid4 string
    """
    def run(self, namespace):
        from uuid import uuid4
        print(uuid4())
