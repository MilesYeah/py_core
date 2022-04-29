import os
import allure
import pytest

from comm.unit.initializePremise import init_premise
from comm.unit.apiSend import send_request
from comm.unit.checkResult import check_result

from libConfParser.parserYAML import ParserYAML

case_yaml = os.path.realpath(__file__).replace('testcase', 'page').replace('.py', '.yaml')
case_path = os.path.dirname(case_yaml)
case_dict = ParserYAML(case_yaml)


@allure.feature(case_dict["test_info"]["title"])
class TestTemplate:

    @allure.title("{case_data[title]}")
    @pytest.mark.parametrize("case_data", case_dict["test_case"])
    @allure.story("test_template")
    def test_template(self, case_data):
        allure.dynamic.description(case_data['describe'])
        # 初始化请求：执行前置接口+替换关联变量
        test_info, case_data = init_premise(case_dict["test_info"], case_data, case_path)
        # 发送当前接口
        code, data = send_request(test_info, case_data)
        # 校验接口返回
        check_result(case_data, code, data)

