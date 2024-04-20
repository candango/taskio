from taskio.model import TaskioTask


class FirstLevelTask(TaskioTask):

    def run(self, namespace):
        print("buuuu")


class GenerateUuidTask(TaskioTask):

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

    def run(self, namespace):
        """ Generates an uuid4 string
        """
        from uuid import uuid4
        print(uuid4())
