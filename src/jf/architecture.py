from pathlib import Path
import os


ROOT_JF = None


def init():
    global ROOT_JF
    wd = Path(os.getcwd())
    while True:
        if (wd / "root.jf").exists():
            ROOT_JF = wd
            return
        elif len(wd.parents) > 0:
            wd = wd.parent


def assert_init():
    global ROOT_JF
    if ROOT_JF is None:
        raise ValueError("jf root is not initialized")


def root():
    global ROOT_JF
    assert_init()
    return ROOT_JF


def code_root():
    global ROOT_JF
    assert_init()
    return ROOT_JF / "code"


def data_root():
    global ROOT_JF
    assert_init()
    return ROOT_JF / "data"


def output_root():
    global ROOT_JF
    assert_init()
    return ROOT_JF / "output"
