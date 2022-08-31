import unicodedata


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    if len(s) < 2:
        return False

    try:
        d = 0
        if s.startswith('－'):
            s = s[1:]
        for c in s:
            if c == '－':  # 全角减号
                return False

            if c == '．':  # 全角点号
                if d > 0:
                    return False
                else:
                    d = 1
                    continue
            unicodedata.numeric(c)
        return True
    except (TypeError, ValueError):
        pass

    return False


if __name__ == "__main__":
    # 测试字符串和数字
    print(f'"foo": {is_number("foo")}')
    print(f'"1": {is_number("1")}')
    print(f'"1.3": {is_number("1.3")}')
    print(f'"-1.37": {is_number("-1.37")}')
    print(f'"1e3": {is_number("1e3")}')
    print(f'"2.345.6": {is_number("2.345.6")}')
    print(f'"-5.2-8": {is_number("-5.2-8")}')
    print(f'"52-8": {is_number("52-8")}')
    print(f'"-.5": {is_number("-.5")}')
    print(f'"-5.": {is_number("-5.")}')
    print(f'".5": {is_number(".5")}')

    # 测试Unicode
    # 阿拉伯语 5
    print(f'"٥": {is_number("٥")}')
    # 泰语 2
    print(f'"๒": {is_number("๒")}')
    # 中文数字
    print(f'"四": {is_number("四")}')
    print(f'"四卅": {is_number("四卅")}')
    # 全角数字
    print(f'"１２３": {is_number("１２３")}')
    print(f'"-１２３": {is_number("-１２３")}')
    print(f'"－１２３": {is_number("－１２３")}')
    print(f'"１２－３": {is_number("１２－３")}')
    print(f'"１２３－": {is_number("１２３－")}')
    print(f'"１.２３": {is_number("１.２３")}')
    print(f'"１．２３": {is_number("１．２３")}')
    print(f'"．２３": {is_number("．２３")}')
    print(f'"－．２３": {is_number("－．２３")}')
    print(f'"１．23": {is_number("１．23")}')
    print(f'"１．２．３": {is_number("１．２．３")}')
    # 版权号
    print(f'"©": {is_number("©")}')


