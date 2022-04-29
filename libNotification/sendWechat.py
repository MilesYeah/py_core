import requests


def send_wxwork_notify_markdown(content, api_key, headers=None):
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    hook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={api_key}"
    data = {"msgtype": "markdown",
            "markdown": {
                "content": f"{content}"
            }}
    notify_res = requests.post(url=hook_url, json=data, headers=headers)
    return notify_res


def send_wxwork_notify_text(content, mentioned_mobile_list, api_key, headers=None):
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    if not mentioned_mobile_list or not isinstance(mentioned_mobile_list, list):
        raise TypeError("mentioned_mobile_list should be a list!")

    hook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={api_key}"
    data = {"msgtype": "text",
            "text": {
                "content": f"{content}",
                "mentioned_mobile_list": mentioned_mobile_list
            }}
    notify_res = requests.post(url=hook_url, json=data, headers=headers)
    return notify_res


if __name__ == "__main__":

    pass
