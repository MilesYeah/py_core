import os

ProjectName = "CoreOfMiles"

CORE_ABSPATH = os.path.abspath(__file__)
CORE_DIR = os.path.dirname(__file__)
CORE_DRIVE = os.path.splitdrive(__file__)[0]

CORE_PARENT_PATH = os.path.split(CORE_DIR)[0]

PROJECT_ROOT = CORE_PARENT_PATH


def exec_str2cmd(func: str) -> str:
    """执行函数(exec可以执行Python代码)
    :params func 字符的形式调用函数
    : return 返回的将是个str类型的结果
    """
    # 得到一个局部的变量字典，来修正exec函数中的变量，在其他函数内部使用不到的问题
    loc = locals()
    exec(f"result = {func}")
    return str(loc['result'])


print()
