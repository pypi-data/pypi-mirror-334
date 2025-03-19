from contextlib import contextmanager


class GradMode:
    _enable = True

    @classmethod
    def is_enabled(cls):
        return cls._enable

    @classmethod
    def set_enable(cls, mode: bool):
        cls._enable = mode


@contextmanager
def no_grad():
    GradMode.set_enable(False)
    try:
        yield
    finally:
        GradMode.set_enable(True)


no_grad.__module__ = "anygrad.autograd"
