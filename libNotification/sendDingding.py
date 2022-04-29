import requests
import urllib.parse



def send_ding_talk_notify_markdown(content_title, content_text, access_token, at_mobiles=[], secret=None, headers=None):
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    hook_url = "https://oapi.dingtalk.com/robot/send?access_token={}".format(access_token)
    if secret:
        timestamp, sign = generate_timestamp_and_sign(secret)
        hook_url = "https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}".format(access_token,
                                                                                                      timestamp, sign)
    data = {
        "msgtype": "markdown",
    }
    if at_mobiles and "@all" in at_mobiles:
        data['markdown'] = {
            "title": "{} @all".format(content_title),
            "text": "{} @all".format(content_text)
        }
        data['at'] = {
            "atMobiles": at_mobiles,
            "isAtAll": True
        }
    elif at_mobiles and "@all" not in at_mobiles:
        if len(at_mobiles) > 1:
            at_mobiles_str = "@".join(at_mobiles)
            at_mobiles_str = "@{}".format(at_mobiles_str)
        else:
            at_mobiles_str = "@{}".format(at_mobiles[0])
        data['markdown'] = {
            "title": "{} {}".format(content_title, at_mobiles_str),
            "text": "{} {}".format(content_text, at_mobiles_str)
        }
        data['at'] = {
            "atMobiles": at_mobiles,
            "isAtAll": False
        }
    notify_res = requests.post(url=hook_url, json=data, headers=headers)
    return notify_res


def generate_timestamp_and_sign(secret):
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign



import base64
import hashlib
import hmac
import time
import urllib.parse

from typing import Any
from dingtalkchatbot.chatbot import DingtalkChatbot, FeedLink

from libNetwork.libNetwork import get_host_ip
from libAllure.allureResultParser import AllureResultParser

webhook_base = None
secret = None


class DingTalkSendMsg(object):

    def __init__(self, webhook_base, secret):
        if webhook_base is None or secret is None:
            raise ValueError
        self.webhook_base = webhook_base
        self.secret = secret

        self.timeStamp = str(round(time.time() * 1000))
        self.sign = self.get_sign()

        # 获取 webhook地址
        self.webhook = f"{self.webhook_base}&timestamp={self.timeStamp}&sign={self.sign}"
        self.xiaoDing = DingtalkChatbot(self.webhook)
        self.Process = AllureResultParser()

    def get_sign(self) -> str:
        """
        根据时间戳 + "sign" 生成密钥
        :return:
        """
        string_to_sign = f'{self.timeStamp}\n{self.secret}'.encode('utf-8')
        hmac_code = hmac.new(self.secret.encode('utf-8'), string_to_sign, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign

    def send_text(self, msg: str, mobiles=None) -> None:
        """
        发送文本信息
        :param msg: 文本内容
        :param mobiles: 艾特用户电话
        :return:
        """
        if not mobiles:
            self.xiaoDing.send_text(msg=msg, is_at_all=True)
        else:
            if isinstance(mobiles, list):
                self.xiaoDing.send_text(msg=msg, at_mobiles=mobiles)
            else:
                raise TypeError("mobiles类型错误 不是list类型.")

    def send_link(self, title: str, text: str, message_url: str, pic_url: str) -> None:
        """
        发送link通知
        :return:
        """
        try:
            self.xiaoDing.send_link(title=title, text=text, message_url=message_url, pic_url=pic_url)
        except Exception:
            raise

    def send_markdown(self, title: str, msg: str, mobiles=None, is_at_all=False) -> None:
        """

        :param is_at_all:
        :param mobiles:
        :param title:
        :param msg:
        markdown 格式
        """

        if mobiles is None:
            self.xiaoDing.send_markdown(title=title, text=msg, is_at_all=is_at_all)
        else:
            if isinstance(mobiles, list):
                self.xiaoDing.send_markdown(title=title, text=msg, at_mobiles=mobiles)
            else:
                raise TypeError("mobiles类型错误 不是list类型.")

    @staticmethod
    def feed_link(title: str, message_url: str, pic_url: str) -> Any:

        return FeedLink(title=title, message_url=message_url, pic_url=pic_url)

    def send_feed_link(self, *arg) -> None:
        try:
            self.xiaoDing.send_feed_card(list(arg))
        except Exception:
            raise

    def send_ding_notification(self, project_name, tester_name):
        # 发送钉钉通知
        text = f"""#### {project_name}自动化通知  
                    >Python脚本任务: {project_name}
                    >环境: TEST
                    >执行人: {tester_name}
                    >执行结果: {self.Process.pass_rate()}% 
                    >总用例数: {self.Process.count_total()}
                    >成功用例数: {self.Process.pass_rate()}
                    >失败用例数: {self.Process.count_failed()} 
                    >跳过用例数: {self.Process.count_skipped()}
                    ![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)
                    > ###### 测试报告 [详情](http://{get_host_ip()}:9999/index.html)
                    """
        self.send_markdown(title="【接口自动化通知】", msg=text, mobiles=[18867507063])


if __name__ == "__main__":

    pass
