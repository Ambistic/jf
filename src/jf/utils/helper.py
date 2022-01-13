def nonestr(string: [None, str]) -> str:
    if string is None:
        return ""
    return string


def zipswap(ls):
    return list(zip(*ls))
