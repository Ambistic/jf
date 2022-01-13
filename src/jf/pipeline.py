class Pipeline:
    def __init__(self, ls_func):
        self.ls_func = ls_func

    def __call__(self, *args, **kwargs):
        for func in self.ls_func:
            pass
