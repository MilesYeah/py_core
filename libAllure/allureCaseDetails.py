#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import os.path

from base0core import CORE_PARENT_PATH


class AllureCaseDetails():
    """allure 报告数据清洗，提取业务需要得数据"""

    @property
    def get_testcases(cls) -> list:
        """ 获取所有 allure 报告中执行用例的情况"""
        # 将所有数据都收集到files中
        files = []
        for i in os.path.join(CORE_PARENT_PATH, "report", 'html/data/test-cases'):
            with open(i, 'r', encoding='utf-8') as fp:
                date = json.load(fp)
                files.append(date)
        return files

    def get_failed_case(self) -> list:
        """ 获取到所有失败的用例标题和用例代码路径"""
        error_case = []
        for i in self.get_testcases:
            if i['status'] == 'failed' or i['status'] == 'broken':
                error_case.append((i['name'], i['fullName']))
        return error_case

    def get_failed_cases_detail(self) -> str:
        """ 返回所有失败的测试用例相关内容 """
        date = self.get_failed_case()
        # 判断有失败用例，则返回内容
        if len(date) >= 1:
            values = "失败用例:\n"
            values += "        **********************************\n"
            for i in date:
                values += "        " + i[0] + ":" + i[1] + "\n"
            return values
        else:
            # 如果没有失败用例，则返回False
            return ""


if __name__ == "__main__":
    o = AllureCaseDetails()

    pass
