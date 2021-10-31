from inspect import signature, _empty
from pathlib import Path
import numpy as np
import re

class _JFObject:
    pass

_ls_funcs = []

class ComputeNode:
    def __init__(self, name, builders=[]):
        self.name = name
        self.builders = builders

class ComputeEdge:
    def __init__(self, name, func, needs=[], provides=[]):
        self.name = name
        self.func = func
        self.needs = needs
        self.provides = provides
        
    def get_nodes(self):
        return self.needs + self.provides
        
class ComputeGraph:
    def __init__(self):
        self.nodes = dict()
        self.edges = dict()
        
    def add_node(self, node):
        if not node in self.nodes:
            self.nodes[node] = ComputeNode(node)
        
    def add_edge(self, edge):
        # check nodes exists
        for node in edge.get_nodes():
            self.add_node(node)
        
        # add builders
        for out in edge.provides:
            self.nodes[out].builders.append(edge)
        
    def can_compute(self, name, knowing=dict()):
        if name in knowing:
            return True
        for builder in self.nodes[name].builders:
            ok = True
            for need in builder.needs:
                if not self.can_compute(need, knowing):
                    ok = False
                    break
            if ok:
                return True
        return False
    
    def _compute(self, name, knowing=dict()):
        if name in knowing:
            return knowing[name]
        
        for builder in self.nodes[name].builders:
            ok = True
            for need in builder.needs:
                if not self.can_compute(need, knowing):
                    ok = False
                    break
                    
            if not ok:
                continue
                
            new_params = {need: self.compute(need, knowing)}
            knowing.update(new_params)
            # keep order
            args = T([knowing[need] for need in builder.needs])
            return builder.func(*args)
            
    def compute(self, name, knowing=dict()):
        if not self.can_compute(name, knowing):
            raise ValueError(f"Could not find a way of computing {name}")
        return self._compute(name, knowing)
    
_COMPUTE_GRAPH = ComputeGraph()
    
def _register(func):
    # what if get multiple outputs ? 
    name = func.__name__
    
    pat = "build_((?:(?!_from).)*)(?:(?:_from)|$)"
    target = re.findall(pat, name)[0]
    params = _get_func_params(func)
    edge = ComputeEdge(name, func, params, [target])
    _COMPUTE_GRAPH.add_edge(edge)

# decorator
def register_func(func):
    if func.__name__.startswith("build_"):
        _register(func)
    return func

def _get_func_params(func):
    s = signature(func)
    return [p.name for p in s.parameters.values() if p.default == _empty]

class O(_JFObject):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
            
    def _get_properties_as_dict(self):
        return {
            k: v for k, v in self.__dict__.items()
            if not k.startswith("_")
        }
    
    def __getattr__(self, attr):
        try:
            value = _COMPUTE_GRAPH.compute(attr, self._get_properties_as_dict())
        except:
            raise AttributeError(f"{attr} does not exists and is not computable")
        else:
            setattr(self, attr, value)
            return value

class L(list, _JFObject):
    pass

class P(Path, _JFObject):
    pass

class S(set, _JFObject):
    pass

def A(*args):
    if len(args) > 1:
        return np.array(args)
    return np.array(*args)

class T(tuple, _JFObject):
    pass

def zipswap(ls):
    return list(zip(*ls))