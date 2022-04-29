import requests
import allure

from handlerLogger import logger
from libConfParser.parserJSON import str2json


class Transmission:
    PARAMS: str = "params"
    DATA: str = "data"
    JSON: str = "json"


class HttpRequest(object):

    def __init__(self):
        self._session = None
        self.resp = None

    @property
    def session(self):
        if self._session is None:
            self._session = requests.Session()
            return self._session

    @classmethod
    def handler_files(cls, file_obj: str) -> object:
        """file对象处理方法
        :param file_obj: 上传文件使用，格式：接口中文件参数的名称:"文件路径地址"/["文件地址1", "文件地址2"]
        实例- 单个文件: &file&D:
        """
        if file_obj:
            for k, v in str2json(file_obj).items():
                # 多文件上传
                if isinstance(v, list):
                    files = []
                    for path in v:
                        files.append((k, (open(path, 'rb'))))
                else:
                    # 单文件上传
                    files = {k: open(v, 'rb')}
            return files

    @allure.step("发起请求")
    def request(self, method: str, url: str, parametric_key: Transmission, data=None, jdata=None, headers=None, file=None,
                *args, **kwargs):
        """
        请求的基础类
        :param method: 请求方式
        :param url: 请求的url
        :param parametric_key: 入参关键字，
            params(查询参数类型，明文传输，一般在url?参数名=参数值)
            json
            data(一般用于form表单类型参数)
        :param data: 请求的参数
        :param headers: 请求头
        :param file: 上传文件使用，格式：接口中文件参数的名称:"文件路径地址"/["文件地址1", "文件地址2"]
        """
        try:
            if parametric_key == 'params':
                self.resp = self.session.request(method=method, url=url, params=data, headers=headers)
            elif parametric_key == 'data':
                self.resp = self.session.request(method=method, url=url, data=data, files=file, headers=headers)
            elif parametric_key == 'json':
                self.resp = self.session.request(method=method, url=url, data=data, json=jdata, files=file,
                                                 headers=headers)
            else:
                raise ValueError('可选关键字为params, json, data')

            with allure.step("请求日志"):
                logger.info("请求信息:")
                logger.info(f"request_url:{self.resp.request.url}")
                logger.info(f"request_headers:{self.resp.request.headers}")
                logger.info(f"request_body:{self.resp.request.body}")
                logger.info(f"request_cookies:{self.resp.cookies}")
                logger.info("响应信息:")
                logger.info(f"response_headers:{self.resp.headers}")
                logger.info(f"response_body:{self.resp.text}")
        except Exception:
            logger.error(Exception)
            raise Exception("请求异常请检查")

    # 获取请求的cookies
    @property
    def cookies(self):
        return self.resp.cookies

    # 获取接口返回的json对象
    @property
    def resp_as_json(self):
        return self.resp.json()

    # 获取接口的返回的code
    @property
    def resp_code(self):
        return self.resp.status_code

    # 获取接口的全部响应时间
    @property
    def resp_elapsed_time(self):
        return self.resp.elapsed.total_seconds()

    # @classmethod
    # def handle_data(cls, variable: str) -> dict:
    #     """请求数据处理
    #     :param variable: 请求数据，传入的是可转换字典/json的字符串,其中可以包含变量表达式
    #     return 处理之后的json/dict类型的字典数据
    #     """
    #     if variable == '':
    #         return
    #     data = rep_expr(variable, cls.response_dict)
    #     variable = convert_json(data)
    #     return variable

    # @classmethod
    # def handle_sql(cls, sql: str, db: object):
    #     """处理sql，并将结果写到响应字典中"""
    #     if sql not in ['no', '']:
    #         sql = rep_expr(sql, DataProcess.response_dict)
    #     else:
    #         sql = None
    #     allure_step('运行sql', sql)
    #     logger.info(sql)
    #     if sql is not None:
    #         # 查后置sql
    #         result = db.fetch_one(sql)
    #         allure_step('sql执行结果', {"sql_result": result})
    #         logger.info(f'结果：{result}')
    #         if result is not None:
    #             # 将查询结果添加到响应字典里面，作用在，接口响应的内容某个字段 直接和数据库某个字段比对，在预期结果中
    #             # 使用同样的语法提取即可
    #             DataProcess.response_dict.update(result)


if __name__ == '__main__':
    url = "https://v0.yiketianqi.com/api"
    paras ={"version": "v61",
            "appid": "45164426",
            "appsecret": "fWnVlW1c",
            "city": "广水"
            }
    a = HttpRequest()
    a.request(method="get", url=url, parametric_key="params", data=paras)

    print()
