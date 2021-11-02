from abc import ABC, abstractmethod
from functools import lru_cache


class ObjDB(ABC):
    def __init__(self, name, obj, db):
        self._name = name
        self._obj = obj
        self._db = db

    @lru_cache(maxsize=None)
    def _reverse(self, accessor):
        if accessor == "index":
            return {k: k for k in self.index}

        values = getattr(self, accessor)
        return {values[k]: k for k in self.index}

    @abstractmethod
    def __getattr__(self, attr):
        # the basic principle is that value[index] exists and is consistent
        pass

    @abstractmethod
    def has_attr(self, attr):
        pass

    def __len__(self):
        return len(self.index)

    def __iter__(self):
        self._n = 0
        self._max = len(self)
        return self

    def __next__(self):
        if self._n < self._max:
            result = self._db._pointer(self._name, self.index[self._n])
            self._n += 1
            return result
        else:
            raise StopIteration
