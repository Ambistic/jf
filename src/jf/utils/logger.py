import sys


class Logger:
    def __init__(self, filename):
        self.file = open(filename, 'w')

    def write(self, message):
        self.file.write(message)

    def flush(self):
        self.file.flush()
