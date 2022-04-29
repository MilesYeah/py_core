#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

from base0core import CORE_PARENT_PATH
from libConfParser.parserJSON import ParserJSON


class AllureResultParser(object):
    def __init__(self):
        self.j_fpn = os.path.join(CORE_PARENT_PATH, "report/html/widgets/summary.json")
        self.allure_data = ParserJSON(self.j_fpn)

    @property
    def statistic(self):
        return self.allure_data.get_group("statistic", dict())

    @property
    def exec_time(self):
        return self.allure_data.get_group("time", dict())

    @property
    def count_pass(self) -> int:
        """用例成功数"""
        return self.statistic.get('passed', None)

    @property
    def count_failed(self) -> int:
        """用例失败数"""
        return self.statistic.get('failed', None)

    @property
    def count_broken(self) -> int:
        """用例异常数"""
        return self.statistic.get('broken', None)

    @property
    def count_skipped(self) -> int:
        """用例跳过数"""
        return self.statistic.get('skipped', None)

    @property
    def count_total(self) -> int:
        """用例总数"""
        return self.statistic.get('total', None)

    @property
    def pass_rate(self) -> float:
        """用例成功率"""
        # 四舍五入，保留2位小数
        try:
            pass_rate = round((self.count_pass + self.count_skipped) / self.count_total * 100, 2)
            return pass_rate
        except ZeroDivisionError:
            return 0.00


if __name__ == "__main__":
    o = AllureResultParser()

    print()
