# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
@File    : main.py
@Time    : 2020/10/4 19:321
@Author  : iBoy
@Email   : iboy@iboy.tech
@Description : 
@Software: PyCharm
"""
import os
import requests
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

keys = os.environ['KEY'].split("#")

api = os.environ['API']

# 采集网易云的接口


def get_163_info():
    headers = {
        "authority": "api.uomg.com",
        "path": "/api/comments.163?format = json",
        "scheme": "https",
        "accept": "text / html, application / xhtml + xml, application / xml;    q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9",
        "accept-encoding": "gzip, deflate, braccept - language: zh - CN, zh;q = 0.9, en;q = 0.8",
        "cache-control": "no - cache",
        "cookie": "Hm_lvt_697a67a1161cac5798b4cf766ef2b3b0 = 1601308892, 1601342651;PHPSESSID = 40p60bvvkj8c3mgfa60dparog1;Hm_lpvt_697a67a1161cac5798b4cf766ef2b3b0 = 1601342664",
        "pragma": "no - cache",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 80.0.3987.163Safari / 537.36",
    }
    url = "http://api.uomg.com/api/rand.music?sort=%E7%83%AD%E6%AD%8C%E6%A6%9C&format=json"
    data = requests.get(url, headers=headers).json().get('data')
    try:
        id = data["url"].replace(
            "http://music.163.com/song/media/outer/url?id=", "")
        data['music'] = "[CQ:music,type=163,id={}]".format(id)
        for key in keys:
            msg = {
                "group_id": key,
                "message": data['music'].encode('utf-8')
            }
            requests.post(api, msg)
    except Exception as e:
        print(str(e))
        return get_163_info()


# 获取词霸
def get_iciba_everyday():
    icbapi = 'http://open.iciba.com/dsapi/'
    eed = requests.get(icbapi)
    english = eed.json()['content']
    zh_CN = eed.json()['note']
    str1 = '【每日一句】\n' + english + '\n' + zh_CN
    return str1+"[CQ:image,file={}]".format(eed.json()['fenxiang_img']), eed.json()['tts']

# 主函数


def main(*args):
    ciba = get_iciba_everyday()
    for key in keys:
        msg1 = {
            "group_id": key,
            "message": ciba[0]
        }
        # 把天气数据转换成UTF-8格式，不然要报错。
        msg2 = {
            "group_id": key,
            "message": "[CQ:record,file={}]".format(ciba[1])
        }
        requests.post(api, msg1)
        requests.post(api, msg2)
    get_163_info()


if __name__ == '__main__':
    main()
