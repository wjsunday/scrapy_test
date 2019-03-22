#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

def get_proxy():
    proxy = []

    url = "http://api.wandoudl.com/api/ip?"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'api.wandoudl.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    }
    query = {
        'app_key': '67055b51734c5d6f2026fd8be9c20f49',
        'pack': '2051',
        # 'pack': '0',
        'num': '5',
        'xy': '1',
        'type': '2',
        'lb': r'\r\n',
        'mr': '1',
    }
    #
    response = requests.get(url=url,
                            headers=headers,
                            params=query,
                            timeout=30)

    html = json.loads(response.text)
    datas = html['data']
    for data in datas:
        ip = data['ip']
        port = data['port']
        print('http://{}:{}'.format(ip, port))
        proxies = 'http://{}:{}'.format(ip,port)
        # requests使用proxy为字典
        # proxy.append({'http': proxies})

        # scrapy使用meta携带proxy
        proxy.append(proxies)

    # proxy = [
    #     {'http': 'http://218.61.231.61:5412'}
    # ]
    return proxy

