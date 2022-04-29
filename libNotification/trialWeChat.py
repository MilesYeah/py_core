import json
import requests


corp_id = "wwda6cbd8c3530b690"
corp_sec = "KvmdPln4ovK793JKrUamIfoor1Sm6HwvUK1ZmAbDRj4"
agent_id = 1000002


class WeChatNotification(object):
    def __init__(self, corp_id, corp_sec, agent_id):
        self.corp_id = corp_id
        self.corp_sec = corp_sec
        self.agent_id = agent_id

    @property
    def access_token(self):
        resp = requests.get(f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corp_id}&corpsecret={self.corp_sec}")
        j = resp.json()
        access_token = j.get("access_token")
        return access_token

    def send_text(self, msg, users):
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}"
        useridstr = "|".join(users)
        json_dict = {
            "touser": useridstr,
            "msgtype": "text",
            "agentid": self.agent_id,
            "text": {
                "content": msg
            },
            "safe": 0,
            "enable_id_trans": 1,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        resp = requests.post(url, data=json.dumps(json_dict))

        return resp


if __name__ == "__main__":
    o = WeChatNotification(corp_id, corp_sec, agent_id)
    resp = o.send_text("nihaoa", ["mile", "YeXiang"])
    pass
