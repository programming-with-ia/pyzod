import sys

class Getter:
    def __init__(self, attr: str):
        self.attr = attr

    def __call__(self):
        return self

    def get(self, typ):
        return getattr(typ, self.attr)



class use:
    default = Getter("_default")
    error = Getter("_error")
