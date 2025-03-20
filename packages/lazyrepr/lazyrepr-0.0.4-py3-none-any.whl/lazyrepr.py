""" Utilities for concise object representation """

import itertools

from inspect import Signature


class MissingValue:
    def __repr__(self):
        return "?"


MISSING = MissingValue()


def format_call(name, *args, **kwargs):
    """naive representation of a function call"""

    params = tuple(repr(v) for v in args) + tuple("%s=%r" % kv for kv in kwargs.items())
    params = ", ".join(params)

    return f"{name}({params})"


def split_arguments(func, data):
    """split arguments into positional and keyword arguments"""

    signature = Signature.from_callable(func)
    parameters = signature.parameters.values()

    args, kwargs = [], {}

    for p in parameters:
        v = data.get(p.name, MISSING)
        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD):
            args.append(v)
        elif v != p.default:
            kwargs[p.name] = v
    
    return args, kwargs


def format_partial(func, data, *, name: str = None):
    """format a partial function call"""
    if name is None:
        name = func.__name__

    args, kwargs = split_arguments(func, data)

    return format_call(name, *args, **kwargs)



def lazy_repr(obj):
    """minimal __repr__ based on __init__ signature"""
    cname = obj.__class__.__qualname__

    return format_partial(obj.__init__, data=obj.__dict__, name=cname)


class ReprMixin:
    """Mixin with __repr__ and _repr_pretty_ implementations"""

    __repr__ = lazy_repr

    def _repr_pretty_(self, p, cycle):
        """IPython pretty printer handler"""

        if cycle:
            p.text("...")
            return

        cname = self.__class__.__name__
        args, kwargs = split_arguments(self.__init__, self.__dict__)

        counter = itertools.count(0)

        prefix, suffix = cname + "(", ")"
        with p.group(len(prefix), prefix, suffix):
            for v in args:
                if next(counter):
                    p.text(",")
                    p.breakable()
                p.pretty(v)
            for k, v in kwargs.items():
                if next(counter):
                    p.text(",")
                    p.breakable()
                prefix = k + "="
                with p.group(len(prefix), prefix):
                    p.pretty(v)
