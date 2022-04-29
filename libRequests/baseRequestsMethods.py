import json
import logging
import os
import random

import requests
import allure
import simplejson as simplejson

from handlerLogger import logger


def post(headers, address, mime_type, timeout=120, data=None, files=None, cookies=None):
    """
    post请求
    :param headers: 请求头
    :param address: 请求地址
    :param mime_type: 请求参数格式（form_data,raw）
    :param timeout: 超时时间
    :param data: 请求参数
    :param files: 文件路径
    :param cookies:
    :return:
    """
    # 判断请求参数类型
    if 'form-data' in mime_type:
        response = None
        if files:
            if isinstance(files, str):
                param_key = files.split(' ')[0]
                filename = files.split(' ')[1]
                value = UPLOAD_DIR+filename
                path_l = {"{}".format(param_key): (os.path.basename(value), open(value, 'rb'))}
                enc = MultipartEncoder(
                    fields=path_l,
                    boundary='--------------' + str(random.randint(1e28, 1e29 - 1))
                )
                headers['Content-Type'] = enc.content_type
                response = requests.post(url=address,
                                         data=enc,
                                         params=data,
                                         headers=headers,
                                         timeout=timeout,
                                         cookies=cookies)
            elif isinstance(files, list):
                datas = []
                for item in files:
                    param, filename = item.split(' ')
                    types_ = mimetypes.guess_type(filename)[0]
                    d = (param, (filename, open(UPLOAD_DIR+filename, 'rb'), types_))
                    datas.append(d)
                response = requests.post(url=address, headers=headers, data=data, files=datas,
                                         cookies=cookies, timeout=120)
            else:
                logging.debug("不支持该文件传入格式！")
        else:
            datas = None
            response = requests.post(url=address, headers=headers, data=data, files=datas,
                                     cookies=cookies, timeout=120)
    elif 'data' in mime_type or 'x-www-form-urlencoded' in mime_type:
        response = requests.post(url=address,
                                 data=data,
                                 headers=headers,
                                 timeout=timeout,
                                 files=files,
                                 cookies=cookies)
    else:
        response = requests.post(url=address,
                                 json=data,
                                 headers=headers,
                                 timeout=timeout,
                                 files=files,
                                 cookies=cookies)
    try:
        if response.status_code != 200:
            return response.status_code, response.json()
        else:
            return response.status_code, response.json()
    except json.decoder.JSONDecodeError:
        return response.status_code, None
    except simplejson.errors.JSONDecodeError:
        return response.status_code, None
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        raise


def get(headers, address, data, downloadName=None, timeout=8, cookies=None):
    """
    get请求
    :param headers: 请求头
    :param address: 请求地址
    :param data: 请求参数
    :param timeout: 超时时间
    :param downloadName: 下载文件名称
    :param cookies:
    :return:
    """
    response = requests.get(url=address,
                            params=data,
                            headers=headers,
                            timeout=timeout,
                            cookies=cookies)
    if response.status_code == 301:
        response = requests.get(url=response.headers["location"])
    try:
        if downloadName:
            if response.status_code == 200:
                file = download_file(response, downloadName)
                EXT = os.path.splitext(file)[1]
                fileN = os.path.basename(os.path.splitext(file)[0] + EXT)
                with open(file, "rb") as f:
                    context = f.read()
                    allure.attachment_type
                    allure.attach(context, fileN, attachment_type=eval('allure.attachment_type.{}'
                                                                       .format(EXT.strip('.').upper())))
        return response.status_code, response.json()
    except json.decoder.JSONDecodeError:
        return response.status_code, response.text
    except simplejson.errors.JSONDecodeError:
        return response.status_code, response.text
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        raise


def put(headers, address, mime_type, timeout=8, data=None, files=None, cookies=None):
    """
    put请求
    :param headers: 请求头
    :param address: 请求地址
    :param mime_type: 请求参数格式（form_data,raw）
    :param timeout: 超时时间
    :param data: 请求参数
    :param files: 文件路径
    :param cookies:
    :return:
    """
    if mime_type == 'raw':
        data = json.dumps(data)
    elif mime_type == 'application/json':
        data = json.dumps(data)
    response = requests.put(url=address,
                            data=data,
                            headers=headers,
                            timeout=timeout,
                            files=files,
                            cookies=cookies)
    try:
        return response.status_code, response.json()
    except json.decoder.JSONDecodeError:
        return response.status_code, None
    except simplejson.errors.JSONDecodeError:
        return response.status_code, None
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        raise


def delete(headers, address, data, timeout=8, cookies=None):
    """
    delete请求
    :param headers: 请求头
    :param address: 请求地址
    :param data: 请求参数
    :param timeout: 超时时间
    :param cookies:
    :return:
    """
    response = requests.delete(url=address,
                               params=data,
                               headers=headers,
                               timeout=timeout,
                               cookies=cookies)
    try:
        return response.status_code, response.json()
    except json.decoder.JSONDecodeError:
        return response.status_code, None
    except simplejson.errors.JSONDecodeError:
        return response.status_code, None
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        raise


def save_cookie(headers, address, mime_type, timeout=8, data=None, files=None, cookies=None):
    """
    保存cookie信息
    :param headers: 请求头
    :param address: 请求地址
    :param mime_type: 请求参数格式（form_data,raw）
    :param timeout: 超时时间
    :param data: 请求参数
    :param files: 文件路径
    :param cookies:
    :return:
    """
    if 'data' in mime_type:
        response = requests.post(url=address,
                                 data=data,
                                 headers=headers,
                                 timeout=timeout,
                                 files=files,
                                 cookies=cookies)
    else:
        response = requests.post(url=address,
                                 json=data,
                                 headers=headers,
                                 timeout=timeout,
                                 files=files,
                                 cookies=cookies)
    try:
        cookies = response.cookies.get_dict()
        # 读取api配置并写入最新的cookie结果
        aconfig = read_yaml_data(API_CONFIG)
        aconfig[PROJECT_NAME]['cookies'] = cookies
        write_yaml_file(API_CONFIG, aconfig)
        logging.debug("cookies已保存，结果为：{}".format(cookies))
    except json.decoder.JSONDecodeError:
        return response.status_code, None
    except simplejson.errors.JSONDecodeError:
        return response.status_code, None
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        raise


def download_file(res, filename):
    """
    保存请求接口后下载的文件数据
    对于昨天结束前创建的文件进行删除操作
    :param res: 下载接口的返回数据
    :param filename: 下载文件名（包含拓展名）
    :return: 保存的文件路径
    """
    ds = list(os.listdir(DOWNLOAD_DIR))
    for file in ds:
        yesterday_end_time = int(time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d'))) - 1
        create_time = os.path.getctime(DOWNLOAD_DIR + file)
        if create_time < yesterday_end_time:
            os.remove(DOWNLOAD_DIR + file)
    with closing(res) as response:
        fileName = DOWNLOAD_DIR + "{}".format(str(time.time())[:10]) + filename
        with open(fileName, 'wb') as fd:
            for chunk in response.iter_content(128):
                fd.write(chunk)
    return fileName


if __name__ == '__main__':
    pass
