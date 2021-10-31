from enum import Enum
import pandas as pd
from functools import lru_cache
import networkx as nx


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


# In[4]:


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


# In[5]:


class DataFrameDB(ObjDB):
    def __getattr__(self, attr):
        if attr == "index":
            return list(range(len(self._obj)))
        
        elif attr == "value":
            return self._obj.loc
        
        elif attr in self._obj.columns:
            return self._obj[attr]
        
        else:
            raise AttributeError("ListDB has no attribute", attr)
            
    def has_attr(self, attr):
        return attr in (["index", "value"] + self._obj.columns)


# In[6]:


def _obj_db(name, obj, db):
    if isinstance(obj, list):
        return ListDB(name, obj, db)

    elif isinstance(obj, dict):
        return DictDB(name, obj, db)

    elif isinstance(obj, pd.DataFrame):
        return DataFrameDB(name, obj, db)
    
    else:
        raise TypeError("Type not understood", type(obj))


# In[7]:


class DBPointer:
    def __init__(self, backend, path, index):
        self.db = backend
        self.path = path
        self.index = index


# In[8]:


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
            xtrans = self._inner_obj[xpath[0]]._reverse(xpath[1])
            ytrans = self._inner_obj[ypath[0]]._reverse(ypath[1])
            return ytrans[xtrans[index]]
        return transition_function
        
    def get_transition(self, obj_source, obj_target):
        """Generate a partial func graph to go to the given value"""
        # TODO make a full graph search
        link_graph = [(l[0][0], l[1][0], {"k" : l}) for l in self._links]
        graph = nx.MultiGraph(link_graph)
        min_path = nx.shortest_path(graph, obj_source, obj_target)
        pairs = [(min_path[x], min_path[x + 1]) for x in range(len(min_path) - 1)]
        links = [list(graph[a][b].values())[0]["k"] for a, b in pairs]
        return [self.generate_transition_function(xpath, ypath) for xpath, ypath in links]


# In[9]:


class _DBViewState(Enum):
    Raw = 0
    Rel = 1
    # Obj = 2
    RelObj = 3
    RelObjAttr = 4
    Pointer = 5


# In[10]:


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


# In[11]:


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
        # we must do with current path and attr
        return _strategy_from_state(self._state)(self._backendDB, attr, self._path)
    
    def link(self, *args):
        self._backendDB.link(*args)


# In[12]:


class _PointerDBState(Enum):
    Raw = 0
    Rel = 1
    # Obj = 2
    RelObj = 3
    RelObjAttr = 4
    Pointer = 5


# In[13]:


class PointerItem:
    def __init__(self, obj, index):
        self.obj = obj
        self.index = index

    def __getattr__(self, attr):
        return getattr(self.obj, attr)[self.index]
            
    def has_attr(self, attr):
        return self.obj.has_attr(attr)


# In[14]:


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
        
        return PointerItem(self._backendDB.get_object(attr), index)  # TODO here


# In[15]:


a = [2, 4, 6, 8]
b = {"a": 0, "b": 1, "c": 2, "d": 3}


# In[16]:


db = DB(a=a, b=b)


# In[17]:


db.link(db.rel.a.index, db.rel.b.value)


# In[19]:


for x in db.a:
    print(x.a.value, x.b.index)


# In[ ]:




