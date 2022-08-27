import datetime
from colorama import Fore as Color


class Logger:
    def __init__(self, name: str = 'app'):
        self.name = name

    def info(self, msg: str):
        print('{}[{}] {}INFO    | {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.name,
                                           Color.WHITE, msg) + Color.RESET)

    def warn(self, msg: str):
        print('{}[{}] {}WARN    | {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.name,
                                           Color.YELLOW, msg) + Color.RESET)

    def error(self, msg: str):
        print('{}[{}] {}ERROR   | {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.name,
                                           Color.RED, msg) + Color.RESET)

    def success(self, msg: str):
        print('{}[{}] {}SUCCESS | {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.name,
                                           Color.GREEN, msg) + Color.RESET)
