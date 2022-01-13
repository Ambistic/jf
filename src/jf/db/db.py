import networkx as nx

from jf.db.objdb.getobj import _obj_db
from jf.db.view.pointerdb import PointerDB
from jf.db.view.state import _DBViewState


class BackendDB:
    def __init__(self, **kwargs):
        self._inner_obj = {
            k: _obj_db(k, v, self)
            for k, v in kwargs.items()
        }
        self._links = []
            
    def _pointer(self, name, index):
        return PointerDB(self, name, index)
    
    def has_attr(self, attr):
        return attr in self._inner_obj
    
    def get_object(self, attr):
        return self._inner_obj[attr]
            
    def __getattr__(self, attr):
        if attr == "rel":
            return self._relation
        
    def __assert_link(self, x, y):
        assert x._backendDB is self
        assert y._backendDB is self
        assert x._state == _DBViewState.RelObjAttr
        assert y._state == _DBViewState.RelObjAttr
            
    def link(self, x, y):
        self.__assert_link(x, y)
        self._links.append((x._path, y._path))
        
    def generate_transition_function(self, xpath, ypath):
        # input must be index for first
        # output must be output for second
        def transition_function(index):
            xtrans = self._inner_obj[xpath[0]]._toward(xpath[1])
            ytrans = self._inner_obj[ypath[0]]._reverse(ypath[1])
            try:
                x_index = xtrans[index]
            except:
                print(xtrans, index, xpath, ypath)
                raise

            try:
                y_index = ytrans[x_index]
            except:
                print(ytrans, x_index, index, xpath, ypath)
                raise

            return y_index
        return transition_function
        
    def get_transition(self, obj_source, obj_target):
        """Generate a partial func graph to go to the given value"""
        link_graph = [(l[0][0], l[1][0], {"k": l}) for l in self._links]
        graph = nx.MultiGraph(link_graph)
        min_path = nx.shortest_path(graph, obj_source, obj_target)
        pairs = [(min_path[x], min_path[x + 1]) for x in range(len(min_path) - 1)]
        links = [list(graph[a][b].values())[0]["k"] for a, b in pairs]
        reordered_links = [((a[0], a[1]) if a[0][0] == n[0] else (a[1], a[0]))
                           for a, n in zip(links, pairs)]

        return [self.generate_transition_function(xpath, ypath) for xpath, ypath in reordered_links]




