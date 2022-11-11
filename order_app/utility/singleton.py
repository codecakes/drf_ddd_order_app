class Singleton:
    """A singleton decorator hack for classes."""

    def __init__(self, aclass: type):
        self._aclass = aclass
        self._instance = None
        __doc__ = self._aclass.__doc__
        __module__ = self._aclass.__module__

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self._aclass(*args, **kwargs)
        return self._instance