import re
from pathlib import Path as P
import json
from configparser import ConfigParser
from jf.utils.helper import nonestr


_FILENAME_MODELS = ".string-model.conf"


def _parse_substring(substring):
    pat = '([\w\d]+)(?:{([\w\d]+)})?'
    return re.findall(pat, substring)[0]


def strip_param(param):
    c = "'"
    if param.startswith(c) and param.startswith(c):
        return param.strip(c)
    return param


def cover_param(param):
    if " " in param:
        return f"'{param}'"
    return param


def read_model(name, dirname="."):
    conf = ConfigParser()
    conf.read(P(dirname) / _FILENAME_MODELS)
    kwargs = dict(conf[name])
    if "default" in kwargs:
        kwargs["default"] = json.loads(kwargs["default"])

    for k in ["sep", "escape", "forbidden", "replace"]:
        kwargs[k] = strip_param(kwargs[k])
    return StringModel(**kwargs)


class StringModel:
    def __init__(self, model, default=dict(), global_default="", sep="_.", escape="$", forbidden="", replace="%"):
        """
        The escape parameter shall never be used in the values
        This class is not made for proper handling of escape mechanism
        """
        assert len(escape) == 1
        self.model = model
        self.default = default
        self.global_default = global_default
        self.sep = sep
        self.escape = escape
        self.forbidden = forbidden
        self.replace = replace

    def save(self, name, dirname="."):
        conf = ConfigParser()
        conf.read(P(dirname) / _FILENAME_MODELS)
        kwargs = dict(
            model=self.model,
            default=json.dumps(self.default),
            global_default=self.global_default,
            sep=cover_param(self.sep),
            escape=cover_param(self.escape),
            forbidden=cover_param(self.forbidden),
            replace=cover_param(self.replace),
        )

        conf[name] = {k: v.replace("%", "%%") for k, v in kwargs.items()}
        # for k, v in kwargs.items():
        #     conf[name][k] = v

        with open(P(dirname) / _FILENAME_MODELS, "w") as fp:
            conf.write(fp)

    def _split(self, string):
        pat = f"(?:^|([^{self.escape}]))[{self.sep}]"
        res = re.split(pat, string)
        size = int((len(res) + 1) / 2)
        res += ['']
        return [res[i * 2] + nonestr(res[i * 2 + 1]) for i in range(size)]

    def _get_model_slots(self):
        substrings = self._split(self.model)
        return [_parse_substring(substring) for substring in substrings]

    def _process_dict_strings(self, my_dict):
        for char in self.forbidden:
            for k, v in my_dict.items():
                my_dict[k] = str(v).replace(char, self.replace)
        return my_dict

    def fill(self, **params):
        params = self._process_dict_strings(params)
        values = {slotname: self.global_default for _, slotname in self._get_model_slots()}
        values.update(self.default)
        values.update(params)
        return self.model.format(**values)

    def _extract_slot(self, string, prefix):
        pat = f"(?:^|[{self.sep}])({prefix}[^{self.sep}]*)(?:$|[{self.sep}])"
        return re.findall(pat, string)[0]

    def extract(self, string):
        slots = self._get_model_slots()
        substrings = self._split(string)
        assert len(slots) == len(substrings), f"Are you sure {string} matches the model"
        dict_res = dict()
        for (prefix, slotname), substring in zip(slots, substrings):
            if slotname == "":
                continue
            if re.match(f"{prefix}.*", substring):
                dict_res[slotname] = re.findall(f"{prefix}(.*)", substring)[0]

        return dict_res

    def extract_old(self, string):
        slots = filter(lambda x: x[1] != "", self._get_model_slots())
        substrings = self._split(string)
        dict_res = dict()
        for prefix, slotname in slots:
            for substring in substrings:
                if re.match(f"{prefix}.*", substring):
                    dict_res[slotname] = re.findall(f"{prefix}(.*)", substring)[0]
                    break

        return dict_res

    def match(self, string):
        slots = self._get_model_slots()
        substrings = self._split(string)
        if len(slots) != len(substrings):
            return False

        for (prefix, _), substring in zip(slots, substrings):
            if not re.match(f"{prefix}.*", substring):
                return False

        return True
    
    def match_param(self, string, params):
        """Do not check for the normal match"""
        slots = self._get_model_slots()
        substrings = self._split(string)
        for (prefix, slotname), substring in zip(slots, substrings):
            if slotname == "":
                continue
            if slotname in params:
                string_value = re.findall(f"{prefix}(.*)", substring)[0]
                if string_value != str(params[slotname]):
                    return False

        return True
    
    def pick_last(self, strings, slot, params=None):
        last_number = -1
        last = None
        slots = self._get_model_slots()
        
        for string in strings:
            if not self.match(string):
                continue

            if params is not None and not self.match_param(string, params):
                continue

            value = float(self.extract(string)[slot])
            if value > last_number:
                last, last_number = string, value

        return last
