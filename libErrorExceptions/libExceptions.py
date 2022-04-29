# coding=utf-8


class TestBaseException(Exception): pass


class ParseException(TestBaseException): pass


class VariableNotFound(ParseException): pass


class FunctionNotFound(ParseException): pass


class FunctionCallError(ParseException): pass


class DispatcherException(TestBaseException): pass


class ManualStopException(DispatcherException): pass


class ScriptExecException(DispatcherException):
    def __init__(self, line_no, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.line_no = line_no
        self.value = value


class PostScriptExecException(ScriptExecException): pass


class PreScriptExecException(ScriptExecException): pass

