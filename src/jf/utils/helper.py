from collections import defaultdict


def nonestr(string: [None, str]) -> str:
    if string is None:
        return ""
    return string


def zipswap(ls):
    return list(zip(*ls))


_index_provider = defaultdict(int)


def provide_id(value=-1):
    _index_provider[value] += 1
    return _index_provider[value]
