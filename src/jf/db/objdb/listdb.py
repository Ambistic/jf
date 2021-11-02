from jf.db.objdb.objdb import ObjDB


class ListDB(ObjDB):
    def __getattr__(self, attr):
        if attr == "index":
            return list(range(len(self._obj)))

        elif attr == "value":
            return self._obj

        else:
            raise AttributeError("ListDB has no attribute", attr)

    def has_attr(self, attr):
        return attr in ["index", "value"]