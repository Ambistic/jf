class PointerItem:
    def __init__(self, obj, index):
        self.obj = obj
        self.index = index

    def __getattr__(self, attr):
        return getattr(self.obj, attr)[self.index]

    def has_attr(self, attr):
        return self.obj.has_attr(attr)