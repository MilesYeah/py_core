"""
Apache-2.0 License
References Code: https://github.com/httprunner/httprunner
"""

import re
import ast
from libSubstitute import selfFuncs
import types
from typing import Any, Text, Callable, Dict

from libErrorExceptions.libExceptions import FunctionCallError, VariableNotFound

VariablesMapping = Dict[Text, Any]
FunctionsMapping = Dict[Text, Callable]

dolloar_regex_compile = re.compile(r"\$\$")
# function_regex_compile = re.compile(r"\$\{(\w+)\(([\$\w\.\-/\s=,]*)\)\}")
function_regex_compile = re.compile(r"\$\{(\w+)\(([\$\%\w\.\-/\s=,]*)\)\}")  # 参数增加匹配%符号
variable_regex_compile = re.compile(r"\$\{(\w+)\}|\$(\w+)")

register_parser_functions = {}  # type: FunctionsMapping


def load_module_functions(module) -> Dict[Text, Callable]:
    """ load python module functions.
    module 一般为一个python文件，将文件中定义的function作为列表返回

    Args:
        module: python module

    Returns:
        dict: functions mapping for specified python module

            {
                "func1_name": func1,
                "func2_name": func2
            }

    """
    module_functions = {}

    for name, item in vars(module).items():
        if isinstance(item, types.FunctionType):
            module_functions[name] = item

    return module_functions


def load_builtin_functions() -> Dict[Text, Callable]:
    """ load builtin module functions
    """
    return load_module_functions(selfFuncs)


def get_mapping_function(function_name: Text, functions_mapping: FunctionsMapping) -> Callable:
    """ get function from functions_mapping,
        if not found, then try to check if builtin function.

    Args:
        function_name (str): function name
        functions_mapping (dict): functions mapping

    Returns:
        mapping function object.

    Raises:
        exceptions.FunctionNotFound: function is neither defined in debugtalk.py nor builtin.

    """
    if function_name in functions_mapping:
        return functions_mapping[function_name]

    # modify start: 注释掉当前项目不用的条件
    # elif function_name in ["parameterize", "P"]:
    #     return loader.load_csv_file
    #
    # elif function_name in ["environ", "ENV"]:
    #     return utils.get_os_environ
    #
    # elif function_name in ["multipart_encoder", "multipart_content_type"]:
    #     # extension for upload test
    #     from httprunner.ext import uploader
    #
    #     return getattr(uploader, function_name)
    # modify end

    try:
        # check if HttpRunner builtin functions
        built_in_functions = load_builtin_functions()
        return built_in_functions[function_name]
    except KeyError:
        pass

    try:
        # check if Python builtin functions
        return getattr(selfFuncs, function_name)
    except AttributeError:
        pass
    # modify start: 替换成当前项目中定义的异常
    raise ModuleNotFoundError(f"{function_name} is not found.")
    # modify end


def parse_string_value(str_value: Text) -> Any:
    """ parse string to number if possible
    e.g. "123" => 123
         "12.2" => 12.3
         "abc" => "abc"
         "$var" => "$var"
    """
    try:
        return ast.literal_eval(str_value)
    except ValueError:
        return str_value
    except SyntaxError:
        # e.g. $var, ${func}
        return str_value


def parse_function_params(params: Text) -> Dict:
    """ parse function params to args and kwargs.

    Args:
        params (str): function param in string

    Returns:
        dict: function meta dict

            {
                "args": [],
                "kwargs": {}
            }

    Examples:
        >>> parse_function_params("")
        {'args': [], 'kwargs': {}}

        >>> parse_function_params("5")
        {'args': [5], 'kwargs': {}}

        >>> parse_function_params("1, 2")
        {'args': [1, 2], 'kwargs': {}}

        >>> parse_function_params("a=1, b=2")
        {'args': [], 'kwargs': {'a': 1, 'b': 2}}

        >>> parse_function_params("1, 2, a=3, b=4")
        {'args': [1, 2], 'kwargs': {'a': 3, 'b': 4}}

    """
    function_meta = {"args": [], "kwargs": {}}

    params_str = params.strip()
    if params_str == "":
        return function_meta

    args_list = params_str.split(",")
    for arg in args_list:
        arg = arg.strip()
        if "=" in arg:
            key, value = arg.split("=")
            function_meta["kwargs"][key.strip()] = parse_string_value(value.strip())
        else:
            function_meta["args"].append(parse_string_value(arg))

    return function_meta


def get_mapping_variable(variable_name: Text,
                         variables_mapping: VariablesMapping
                         ) -> Any:
    """ get variable from variables_mapping.

    Args:
        variable_name (str): variable name
        variables_mapping (dict): variables mapping

    Returns:
        mapping variable value.

    Raises:
        exceptions.VariableNotFound: variable is not found.

    """
    try:
        return variables_mapping[variable_name]
    except KeyError:
        # modify start: 替换成当前项目中定义的异常
        raise ValueError(f"{variable_name} not found in {variables_mapping}")
        # modify end


def parse_string(raw_string: Text,
                 variables_mapping: VariablesMapping,
                 functions_mapping: FunctionsMapping) -> Any:
    """ parse string content with variables and functions mapping.

    Args:
        raw_string: raw string content to be parsed.
        variables_mapping: variables mapping.
        functions_mapping: functions mapping.

    Returns:
        str: parsed string content.

    Examples:
        >>> raw_string = "abc${add_one($num)}def"
        >>> variables_mapping = {"num": 3}
        >>> functions_mapping = {"add_one": lambda x: x + 1}
        >>> parse_string(raw_string, variables_mapping, functions_mapping)
            "abc4def"

    """
    try:
        match_start_position = raw_string.index("$", 0)
        parsed_string = raw_string[0:match_start_position]
    except ValueError:
        parsed_string = raw_string
        return parsed_string

    while match_start_position < len(raw_string):

        # Notice: notation priority
        # $$ > ${func($a, $b)} > $var

        # search $$
        dollar_match = dolloar_regex_compile.match(raw_string, match_start_position)
        if dollar_match:
            match_start_position = dollar_match.end()
            parsed_string += "$"
            continue

        # search function like ${func($a, $b)}
        func_match = function_regex_compile.match(raw_string, match_start_position)
        if func_match:
            func_name = func_match.group(1)
            func = get_mapping_function(func_name, functions_mapping)

            func_params_str = func_match.group(2)
            function_meta = parse_function_params(func_params_str)
            args = function_meta["args"]
            kwargs = function_meta["kwargs"]
            parsed_args = parse_data(args, variables_mapping, functions_mapping)
            parsed_kwargs = parse_data(kwargs, variables_mapping, functions_mapping)

            try:
                func_eval_value = func(*parsed_args, **parsed_kwargs)
            except Exception as ex:
                # modify start: 替换成当前项目中定义的异常
                raise FunctionCallError(
                    f"call function error:\n"
                    f"func_name: {func_name}\n"
                    f"args: {parsed_args}\n"
                    f"kwargs: {parsed_kwargs}\n"
                    f"{type(ex).__name__}: {ex}"
                )
                # modify end

            func_raw_str = "${" + func_name + f"({func_params_str})" + "}"
            if func_raw_str == raw_string:
                # raw_string is a function, e.g. "${add_one(3)}", return its eval value directly
                return func_eval_value

            # raw_string contains one or many functions, e.g. "abc${add_one(3)}def"
            parsed_string += str(func_eval_value)
            match_start_position = func_match.end()
            continue

        # search variable like ${var} or $var
        var_match = variable_regex_compile.match(raw_string, match_start_position)
        if var_match:
            var_name = var_match.group(1) or var_match.group(2)
            # modify start: 如果未匹配到变量则按照raw文本返回
            # var_value = get_mapping_variable(var_name, variables_mapping)
            try:
                var_value = get_mapping_variable(var_name, variables_mapping)
            except VariableNotFound:
                var_value = var_match.group(0)  # 比如匹配到了${num}, 当num变量未找到时，依然返回${num}
            # modify end
            if f"${var_name}" == raw_string or "${" + var_name + "}" == raw_string:
                # raw_string is a variable, $var or ${var}, return its value directly
                return var_value

            # raw_string contains one or many variables, e.g. "abc${var}def"
            parsed_string += str(var_value)
            match_start_position = var_match.end()
            continue

        curr_position = match_start_position
        try:
            # find next $ location
            match_start_position = raw_string.index("$", curr_position + 1)
            remain_string = raw_string[curr_position:match_start_position]
        except ValueError:
            remain_string = raw_string[curr_position:]
            # break while loop
            match_start_position = len(raw_string)

        parsed_string += remain_string

    return parsed_string


def parse_data(raw_data: Any,
               variables_mapping: VariablesMapping = None,
               functions_mapping: FunctionsMapping = None,
               ) -> Any:
    """ parse raw data with evaluated variables mapping.
        Notice: variables_mapping should not contain any variable or function.
    """
    if isinstance(raw_data, str):
        # content in string format may contains variables and functions
        variables_mapping = variables_mapping or {}
        functions_mapping = functions_mapping or {}
        # only strip whitespaces and tabs, \n\r is left because they maybe used in changeset
        raw_data = raw_data.strip(" \t")
        return parse_string(raw_data, variables_mapping, functions_mapping)

    elif isinstance(raw_data, (list, set, tuple)):
        return [
            parse_data(item, variables_mapping, functions_mapping) for item in raw_data
        ]

    elif isinstance(raw_data, dict):
        parsed_data = {}
        for key, value in raw_data.items():
            parsed_key = parse_data(key, variables_mapping, functions_mapping)
            parsed_value = parse_data(value, variables_mapping, functions_mapping)
            parsed_data[parsed_key] = parsed_value

        return parsed_data

    else:
        # other types, e.g. None, int, float, bool
        return raw_data


if __name__ == '__main__':
    a = load_builtin_functions()
    b = get_mapping_function()
    print(parse_data('aaa${num}bbb', {'num': 3}, {}))
    print(parse_data('aaa${num} ${hhh} bbb', {'num': 3, 'hhh': 'gan'}, {}))
    print(parse_data('aaa${num}$hhh bbb', {'num': 3, 'hhh': 'gan'}, {}))
    print(parse_data('aaa${add_one($num)}bbb', {'num': 3, 'hhh': 'gan'}, {"add_one": lambda x: x + 1}))
    # def is_true():
    #     return True
    # print(parse_data('aaa${is_true()}bbb', {'num': 3, 'hhh': 'gan'}, {"is_true": is_true}))
    # print(parse_data('aaa${add($num, $hhh)}bbb', {'num': 3, 'hhh': 4}, {"add": lambda x, y: x + y}))
    # print(parse_data('aaa${get_current_date()}bbb', {}, {}))
    # muilt_line_str = """aaa
    #     ${get_current_date()}
    #     ${get_timestamp()}
    #     bbb
    # """
    # print(parse_data(muilt_line_str, {}, {}))
    # print(parse_data(muilt_line_str))
    # print(parse_data('aaa${num}bbb$hello', {'hello': ' this is hello '}, {}))
    # def current_time(format=None):
    #     print('format: ', format)
    #     try:
    #         from datetime import datetime
    #         if format is None:
    #             format = '%Y%m%d_%H%M%S'
    #         return datetime.now().strftime(format)
    #     except Exception as e:
    #         return None
    # print(parse_data("${currentTime()}", {}, {"currentTime": current_time}))
    # print(parse_data("${currentTime(%H%M)}", {}, {"currentTime": current_time}))
    # print(parse_data("${currentTime(format=%H%M)}", {}, {"currentTime": current_time}))
    pass
