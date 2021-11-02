from jf.db.view.dbview import DB
from jf.db.view.state import _DBViewState


def _raw_strategy(backend, attr, path):
    if attr == "rel":
        return DB(_backendDB=backend, _path=[], _state=_DBViewState.Rel)

    elif backend.has_attr(attr):
        return backend.get_object(attr)

    else:
        raise AttributeError(f"No {attr} found")


def _rel_strategy(backend, attr, path):
    if backend.has_attr(attr):
        return DB(_backendDB=backend, _path=[attr], _state=_DBViewState.RelObj)

    else:
        raise AttributeError(f"No {attr} found")


def _rel_obj_strategy(backend, attr, path):
    if backend.get_object(path[0]).has_attr(attr):
        return DB(_backendDB=backend, _path=path + [attr], _state=_DBViewState.RelObjAttr)

    else:
        raise AttributeError(f"No {attr} found")


def _strategy_from_state(state):
    if state == _DBViewState.Raw:
        return _raw_strategy

    elif state == _DBViewState.Rel:
        return _rel_strategy

    elif state == _DBViewState.RelObj:
        return _rel_obj_strategy

    elif state == _DBViewState.RelObjAttr:
        raise RuntimeError("No strategy found for sub accessing RelObjAttr")