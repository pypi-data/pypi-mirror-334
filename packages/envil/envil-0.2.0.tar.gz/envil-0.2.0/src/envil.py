import os


__version__ = "0.2.0"


RAISE_EXCEPTION = object()

FALSY_STRINGS = {"0", "false", "f", "no", "n"}


class EnvironmentVariableNotSet(Exception):
    def __init__(self, varname):
        self.varname = varname

    def __str__(self):
        return f"{self.__class__.__name__}({self.varname!r})"


def get_int(varname, default=RAISE_EXCEPTION):
    if varname in os.environ:
        return int(os.environ[varname])
    if default is RAISE_EXCEPTION:
        raise EnvironmentVariableNotSet(varname)
    return default


def get_float(varname, default=RAISE_EXCEPTION):
    if varname in os.environ:
        return float(os.environ[varname])
    if default is RAISE_EXCEPTION:
        raise EnvironmentVariableNotSet(varname)
    return default


def get_bool(varname, default=RAISE_EXCEPTION, falsy_strings=None):
    if falsy_strings is None:
        falsy_strings = FALSY_STRINGS
    if varname in os.environ:
        return os.environ[varname].lower() not in falsy_strings
    if default is RAISE_EXCEPTION:
        raise EnvironmentVariableNotSet(varname)
    return default


def get_str(varname, default=RAISE_EXCEPTION):
    if varname in os.environ:
        return os.environ[varname]
    if default is RAISE_EXCEPTION:
        raise EnvironmentVariableNotSet(varname)
    return default
