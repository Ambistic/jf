from jf.db.view.pointeritem import PointerItem


class PointerDB:
    def __init__(self, _backendDB, _name, _index):
        self._backendDB = _backendDB
        self._name = _name
        self._index = _index

    def __getattr__(self, attr):
        # we must generate the transition functions there
        transitions = self._backendDB.get_transition(self._name, attr)
        index = self._index
        for transition in transitions:
            index = transition(index)

        return PointerItem(self._backendDB.get_object(attr), index)