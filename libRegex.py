import re

from base0core import exec_str2cmd
from libConfParser.parserJSON import json_extractor
from handlerLogger import logger


pattern_var = r"\${(.*?)}"
pattern_eval = r"\$Eval\((.*?)\)"
pattern_str = r'\$RandStr\(([0-9]*?)\)'
pattern_int = r'\$RandInt\(([0-9]*,[0-9]*?)\)'
pattern_choice = r"\$RandChoice\((.*?)\)"
pattern_float = r'\$RandFloat\(([0-9]*,[0-9]*,[0-9]*)\)'
pattern_phone = r'\$GenPhone\(\)'
pattern_guid = r'\$GenGuid\(\)'
pattern_wxid = r'\$GenWxid\(\)'
pattern_noid = r'\$GenNoid\((.*?)\)'
pattern_date = r'\$GenDate\((.*?)\)'
pattern_datetime = r'\$GenDatetime\((.*?)\)'
pattern_name = r'\$GenName\((.*?)\)'
pattern_unreal_phone = r'\$GenUnrealPhone\((.*?)\)'
pattern_company = r'\$GenCompany\((.*?)\)'
partern_email = r'\$GenEmail\((.*?)\)'
partern_bank_card = r'\$GenBankCard\((.*?)\)'


def replace_pattern(pattern, value):
    """替换正则表达式

    :param pattern: 匹配字符
    :param value: 匹配值
    :return:
    """
    patterns = pattern.split('(.*?)')
    return ''.join([patterns[0], value, patterns[-1]])


def replace_relevance(param, relevance=None):
    """替换变量关联值
    :param param: 参数对象
    :param relevance: 关联对象
    :return:
    """
    global pattern
    result = re.findall(pattern_var, str(param))
    if (not result) or (not relevance):
        pass
    else:
        for each in result:
            try:
                # 关联参数多值替换
                relevance_index = 0
                if isinstance(relevance[each], list):
                    try:
                        param = re.sub(pattern, relevance[each][relevance_index], param, count=1)
                        relevance_index += 1
                    except IndexError:
                        relevance_index = 0
                        param = re.sub(pattern, relevance[each][relevance_index], param, count=1)
                        relevance_index += 1
                value = relevance[each]
                pattern = re.compile(r'\${' + each + '}')
                try:
                    param = re.sub(pattern, str(value), param)
                    if not isinstance(value, str) and not isinstance(value, int):
                        param = eval(param)
                except TypeError as e:
                    param = param
                    raise e
            except KeyError:
                raise KeyError('替换变量{0}失败，未发现变量对应关联值！\n关联列表：{1}'.format(param, relevance))
                # pass
    return param


def sub_from_eval(param):
    """从param中找到eval表达式，然后计算每个eval表达式的值，并替换到param中

    :param param: 参数对象
    :return:
    """
    result = re.findall(pattern_eval, str(param))
    if result:
        for expression in result:
            try:
                if 'import' in expression:
                    raise Exception('存在非法标识import')
                else:
                    value = str(eval(expression))
                    param = re.sub(pattern_eval, value, param)
            except KeyError as e:
                raise Exception('获取值[ % ]失败！\n%'.format(param, e))
            except SyntaxError:
                pass
    return param


def rep_expr(content: str, data: dict, expr: str = '&(.*?)&') -> str:
    """从请求参数的字符串中，使用正则的方法找出合适的字符串内容并进行替换
    :param content: 原始的字符串内容
    :param data: 在该项目中一般为响应字典，从字典取值出来
    :param expr: 查找用的正则表达式
    return content： 替换表达式后的字符串
    """
    for ctt in re.findall(expr, content):
        content = content.replace(f'&{ctt}&', str(json_extractor(data, ctt)))

    # 增加自定义函数得的调用，函数写在tools/hooks.py中
    for func in re.findall('@(.*?)@', content):
        try:
            content = content.replace(f'@{func}@', exec_str2cmd(func))
        except Exception as e:
            logger.error(e)
            continue
    return content


if __name__ == '__main__':

    print()
