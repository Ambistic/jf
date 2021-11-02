from jf.db.objdb.objdb import ObjDB


class DictDB(ObjDB):
    def __getattr__(self, attr):
        if attr in ["index", "key", "keys"]:
            return list(self._obj.keys())

        elif attr == "value":
            return self._obj

        else:
            raise AttributeError("ListDB has no attribute", attr)

    def has_attr(self, attr):
        return attr in ["index", "key", "keys", "value"]