import pandas as pd

from jf.db.objdb.dataframedb import DataFrameDB
from jf.db.objdb.dictdb import DictDB
from jf.db.objdb.listdb import ListDB


def _obj_db(name, obj, db):
    if isinstance(obj, list):
        return ListDB(name, obj, db)

    elif isinstance(obj, dict):
        return DictDB(name, obj, db)

    elif isinstance(obj, pd.DataFrame):
        return DataFrameDB(name, obj, db)

    else:
        raise TypeError("Type not understood", type(obj))