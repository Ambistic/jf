import pandas as pd
from jf.db import DB


def test_db():
    pos = [(2, 3), (4, 5), (6, 8), (9, 9)]
    df = pd.DataFrame({"type": ["blue", "red", "yellow", "blue"], "cell_id": [24, 21, 12, 13]})
    corr = {24: 2, 21: 1, 12: 0, 13: 3}
    db = DB(pos=pos, corr=corr, history=df)

    db.link(db.rel.history.cell_id, db.rel.corr.index)
    db.link(db.rel.corr.value, db.rel.pos.index)

    res = [(el.pos.value, el.history.type) for el in db.pos]

    assert res == [((2, 3), 'yellow'), ((4, 5), 'red'), ((6, 8), 'blue'), ((9, 9), 'blue')]
