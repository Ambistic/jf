from jf.db.db import BackendDB
from jf.db.view.state import _DBViewState


class DB:
    """
    DB is a view on the BackendDB
    """
    def __init__(self, _backendDB=None, _path=[], _state=_DBViewState.Raw, **kwargs):
        if _backendDB is None:
            self._backendDB = BackendDB(**kwargs)
        else:
            self._backendDB = _backendDB
        self._path = _path
        self._state = _state

    def __getattr__(self, attr):
        from jf.db.view.strategy import _strategy_from_state
        # we must do with current path and attr
        return _strategy_from_state(self._state)(self._backendDB, attr, self._path)

    def link(self, *args):
        self._backendDB.link(*args)