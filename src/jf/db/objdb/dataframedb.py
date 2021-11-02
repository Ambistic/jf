from jf.db.objdb.objdb import ObjDB


class DataFrameDB(ObjDB):
    def __getattr__(self, attr):
        if attr == "index":
            return list(range(len(self._obj)))

        elif attr == "value":
            return self._obj.loc  # shall we cast in list ?

        elif attr in list(self._obj.columns):
            return self._obj[attr]

        else:
            raise AttributeError("ListDB has no attribute", attr)

    def has_attr(self, attr):
        return attr in (["index", "value"] + list(self._obj.columns))