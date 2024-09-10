"""
This file is intended to provide tools to easily record
experiments that are made with a modulation of parameters
"""
import json
from datetime import datetime
import random
import pandas as pd
import pickle
from pathlib import Path
import os
import sys


def df_filter(df, **kwargs):
    """
    Select rows where conditions are respected.
    Conditions are represented by `key == value` in the dataframe
    If a key does not exist, it returns an empty dataframe
    """
    filt = True

    try:
        for k, v in kwargs.items():
            filt &= (df[k] == v)
        res = df[filt]

    except KeyError:
        res = pd.DataFrame()

    return res


class Experiment:
    _EXP_FILE_NAME = ".experiment"
    _DATE_KEY = "date_of_experiment"

    def __init__(self, name, location="output", silent=False, copy_stdout=False,
                 redirect=True):
        """
        location can be local or centralized (ie to /var/nas/log)
        An experiment is a directory
        """
        # create only if exist
        self.name = name
        self.copy_stdout = copy_stdout
        self.key = str(random.randint(0, 1000000))
        self.location = Path(location)
        self._redirect = redirect

        self.path = self.location / name
        self.results_path = self.path / "results"
        self.export_path = self.path / "export"
        self.log_path = self.path / "log"
        self.progress_path = self.path / "progress"

        self.path.mkdir(parents=True, exist_ok=True)
        self.results_path.mkdir(parents=True, exist_ok=True)
        self.export_path.mkdir(parents=True, exist_ok=True)
        self.log_path.mkdir(parents=True, exist_ok=True)
        self.progress_path.mkdir(parents=True, exist_ok=True)

        if not silent:
            print("Exporting at {}".format(self.path))

    def _result_name(self, result_name):
        return self.results_path / result_name

    def read_result(self, result_name):
        with open(self._result_name(result_name), "r") as fp:
            return json.load(fp)

    def save_result(self, results, result_name=None):
        """
        Add the date to the dictionary
        """
        if result_name is None:
            result_name = datetime.now().isoformat()

        results = dict(results)
        results[self._DATE_KEY] = datetime.now().isoformat()
        print(f"saving {results}")
        with open(self._result_name(result_name), "w") as fp:
            json.dump(results, fp, indent=4, sort_keys=True)

        return result_name

    def list_results(self):
        """
        List all results by date, to get more information, please
        refer to `.dataframe()` method of Experiment
        """
        ls = list()
        for x in os.listdir(self.results_path):
            ls.append(Path(x))

        return ls

    def exists_result(self, **kwargs):
        df = self.dataframe()
        res_df = df_filter(df, **kwargs)
        return not res_df.empty

    def dataframe(self):
        df = pd.DataFrame()
        series = []
        for x in self.list_results():
            try:
                res = self.read_result(x)
                series.append(pd.Series(res, name=x))
            except Exception as e:
                print(f"Found exception {e}")
        return pd.concat(series)

    def export(self, obj, name):
        with open(self.export_path / name, "wb") as fd:
            pickle.dump(obj, fd)

    def load(self, name):
        with open(self.export_path / name, "rb") as fd:
            return pickle.load(fd)

    def print(self, message, slot="out"):
        with open(self.log_path / slot, "a") as fd:
            print(message, file=fd)

        if self.copy_stdout:
            print(f"[{slot}] {message}")

    def list(self):
        return os.listdir(self.export_path)

    def touch(self, name):
        (self.export_path / name).touch()

    def flag(self, name):
        self.touch(name)

    def exists(self, name):
        return (self.export_path / name).exists()

    def progress(self, x: int, name="default"):
        with open(self.progress_path / name, "a+") as fd:
            fd.seek(0)
            old = fd.read()
            value = 0 if old == "" else int(old)
            fd.seek(0)
            fd.write(str(value + x))

    def advancement(self, name="default"):
        with open(self.progress_path / name, "r") as fd:
            old = fd.read()
            value = 0 if old == "" else int(old)
        return value

    def redirect(self):
        print("Redirecting outputs to stdout.txt and stderr.txt")
        sys.stdout = open(self.log_path / "stdout.txt", "w")
        sys.stderr = open(self.log_path / "stderr.txt", "w")

    def show(self, name):
        with open(self.log_path / name, "r") as fd:
            print(fd.read())

    def __enter__(self):
        obj = dict(name=self.name, status="start", pid=os.getpid())
        run_msg = json.dumps(obj)
        with open(self.location / "running.log", "a") as f:
            print(run_msg, file=f)  # newline each time

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        status = "end" if exc_type is None else "crash"
        obj = dict(name=self.name, status=status, pid=os.getpid())
        run_msg = json.dumps(obj)
        with open(self.location / "running.log", "a") as f:
            print(run_msg, file=f)  # newline each time
