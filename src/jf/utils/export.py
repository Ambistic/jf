import pickle
from jf.autocompute.jf import P
import datetime
import random
import os


class Exporter:
    def __init__(self, path=None, name=None, silent=False, copy_stdout=False):
        self.name = name
        self.copy_stdout = copy_stdout
        self.key = str(random.randint(0, 1000000))
        now = datetime.datetime.now()
        if path is None:
            if name is None:
                folder = (now.time().isoformat() + "_" + self.key)
                self.path = P("output") / now.date().isoformat() / folder
            else:
                self.path = P("output") / name
        else:
            self.path = P(path)

        self.path.mkdir(parents=True, exist_ok=True)
        if not silent:
            print("Exporting at {}".format(self.path))

    def __call__(self, *args, **kwargs):
        self.export(*args, **kwargs)

    def export(self, obj, name):
        with open(self.path / name, "wb") as fd:
            pickle.dump(obj, fd)

    def load(self, name):
        with open(self.path / name, "rb") as fd:
            return pickle.load(fd)

    def print(self, message, slot="out"):
        with open(self.path / slot, "a") as fd:
            print(message, file=fd)
            
        if self.copy_stdout:
            print(f"[{slot}] {message}")

    def list(self):
        return os.listdir(self.path)
