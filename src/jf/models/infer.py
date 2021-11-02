from sympy.solvers import solve
from sympy import Symbol, symbols, Eq
from sympy.core.expr import Expr as _Expr
from sympy.core.symbol import Symbol as _Symbol

def answer(ls_eq, values):
    new_ls_eq = []
    for eq in ls_eq:
        for k, v in values.items():
            eq = eq.replace(k, v)
        new_ls_eq.append(eq)
    return solve(new_ls_eq)

class Vars(object):
    def __init__(self):
        self._equations = dict()

    def __getattr__(self, attr):
        s = Symbol(attr)
        self.__setattr__(attr, s)
        return s

    def __setattr__(self, attr, val):
        if attr.startswith("_"):
            object.__setattr__(self, attr, val)
        if isinstance(val, _Symbol):
            object.__setattr__(self, attr, val)
        elif isinstance(val, _Expr):
            s = Symbol(attr)
            self._equations[s] = Eq(val, s)
            object.__setattr__(self, attr, s)
        else:
            object.__setattr__(self, attr, val)

    def solve(self, params):
        pr_params = {p if isinstance(p, _Symbol) else Symbol(p): v for p, v in params.items()}
        return answer(list(self._equations.values()), pr_params)
