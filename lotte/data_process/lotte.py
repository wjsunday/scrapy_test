#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import random
from lxml import etree
from urllib.parse import urlencode
import re
import math
import os
import pymysql
import requests
import time
from fake_useragent import UserAgent
from settings import mysql_host,mysql_port,mysql_db_user,mysql_db_pwd,mysql_db_name,mysql_db_charset
from data_process.spec_info import spec_info
from data_process.mylog import MyLog
from data_process.wandouip import get_proxy
# from data_process.lotte_process_kfk import DataProcess
from data_process.lotte_process_sql import DataProcess
from lxml.html import etree
from random import choice

client = pymysql.connect(
            host=mysql_host,
            port=mysql_port,
            user=mysql_db_user,  # 使用自己的用户名
            passwd=mysql_db_pwd,  # 使用自己的密码
            db=mysql_db_name,  # 数据库名
            charset=mysql_db_charset
        )
cur = client.cursor()
mylog = MyLog()

# 返回代理ip列表
proxy = get_proxy()

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
data_process = DataProcess().data_process

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
        }

def start_requests():
    for spec_id_3 in spec_info:
        print('三级分类：{}'.format(spec_id_3))
        print(spec_info[spec_id_3][0], spec_info[spec_id_3][1], spec_info[spec_id_3][2])
        response = get_pages(spec_id_3)

def get_pages(spec_id_3):
    global proxy
    proxy = proxy if proxy else get_proxy()

    url = "http://chn.lottedfs.com/kr/display/GetPrdList?"
    query = {
        'viewType01': '0',
        'lodfsAdltYn': 'N',
        'catNo': spec_id_3,
        'catNm': spec_info[spec_id_3][2],
        'dispShopNo': spec_id_3,
        'sortStdCd': '01',
        'brndNoList': '',
        'prcRngCd': '',
        'genList': '',
        'fvrList': '',
        'prdAttrCdList': '',
        'soExclList': '',
        'svmnUseRtRngList': '',
        'etcFilterList': '',
        'cntPerPage': '60',
        'curPageNo': '1',
        'treDpth': '3',
    }
    query = urlencode(query)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        'Referer': 'http://chn.lottedfs.com/kr/display/category/third?dispShopNo1={}&dispShopNo2={}&dispShopNo3={}&treDpth=3'.format(spec_info[spec_id_3][3], spec_info[spec_id_3][4], spec_id_3),
        'X-Requested-With': 'XMLHttpRequest',
    }

    proxies = choice(proxy)
    # print(proxies)
    response = requests.get(url=url,
                            headers=headers,
                            params=query,
                            timeout=20,
                            proxies=proxies,
                            )
    # print(response.text)
    # print('======================')
    # print(response.status_code)
    proxies = proxy.remove(proxies) and get_pages(spec_id_3) if response.status_code == 403 else proxies

    goods_num = re.findall('var totalCnt = "(\d+)"', response.text)[0]
    pages = math.ceil(int(goods_num) / 60)
    print("pages:{}".format(pages))

    # if pages > 1:
    for page in range(1, int(pages) + 1):
        # for page in range(1,2):
        print('正在爬取{}第{}页'.format(spec_info[spec_id_3][2], page))
        get_goods_list(page, spec_id_3)

def get_goods_list(page,spec_id_3):
    global proxy
    proxy = proxy if proxy else get_proxy()
    query = {
        'viewType01': '0',
        'lodfsAdltYn': 'N',
        'catNo': spec_id_3,
        'catNm': spec_info[spec_id_3][2],
        'dispShopNo': spec_id_3,
        'sortStdCd': '01',
        'brndNoList': '',
        'prcRngCd': '',
        'genList': '',
        'fvrList': '',
        'prdAttrCdList': '',
        'soExclList': '',
        'svmnUseRtRngList': '',
        'etcFilterList': '',
        'cntPerPage': '60',
        'curPageNo': page,
        'treDpth': '3',
    }
    query = urlencode(query)
    proxies = choice(proxy)
    url = "http://chn.lottedfs.com/kr/display/GetPrdList?"
    response = requests.get(url=url,
                            headers=headers,
                            params=query,
                            timeout=20,
                            proxies=proxies
                            )
    proxies = proxy.remove(proxies) and get_goods_list(page,spec_id_3) if response.status_code == 403 else proxies
    if response.status_code == 403:
        proxy.remove(proxies)
        get_goods_list(page, spec_id_3)

    response = response.content.decode('utf-8')
    response = etree.HTML(response)
    goods_ids = response.xpath('//div[@class="imgType"]/ul[@class="listUl"]/li/a/@href')
    # print(goods_ids)
    for ids in goods_ids:
        goods_id = re.findall('(\d+)', ids)[0]
        print(goods_id)
        # 查询商品是否存在
        url = 'http://chn.lottedfs.com/kr/product/productDetail?prdNo={}'.format(goods_id)
        sql_exsits = "select goods_commonid,goods_image,goods_image_old from mall_goods_common where goods_url='%s'" % (url)
        cur.execute(sql_exsits)
        ret = cur.fetchone()
        if ret:
            print("商品已存在：{}".format(goods_id))
            mylog.info(' URL  |  {}  |  {}  |  {}'.format(url.ljust(70),'000', spec_id_3))
            pass
        else:
            # time.sleep(4.5)
            time.sleep(1)
            print("正在爬取：{}".format(goods_id))
            get_detail_html(goods_id,spec_id_3)


def get_detail_html(goods_id,spec_id_3):
    global proxy
    proxy = proxy if proxy else get_proxy()

    url = "http://chn.lottedfs.com/kr/product/productDetail?prdNo={}".format(goods_id)
    print("goods_url:{}".format(url))
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'chn.lottedfs.com',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    }
    proxies = choice(proxy)
    response = requests.get(url=url,
                            headers=headers,
                            timeout=20,
                            proxies=proxies,
                            )
    # print("code:{}".format(response.status_code))
    code = response.status_code
    if code == 200:
        get_details(response.text, goods_id, spec_id_3, proxies)
    elif code == 403:
        proxy.remove(proxies)
        get_detail_html(goods_id, spec_id_3)
    else:
        pass
    # proxies = proxies if code == 200 else (proxy.remove(proxies) and get_detail_html(goods_id,spec_id_3) lotte_proxy else choice(proxy))

    mylog.info(' URL  |  {}  |  {}  |  {}'.format(url.ljust(70),code, spec_id_3))


def get_details(response,goods_id,spec_id_3,proxies):
    global proxy
    proxy = proxy if proxy else get_proxy()

    response_1 = re.findall('var prd =(.*?)		', response, re.S)[0]
    prdno = re.findall('"prdNo":"(.*?)",', response_1)[0]
    # print(prdno)
    prdoptno = re.findall('"prdOptNo":"(.*?)",', response_1)[0]
    # print(prdoptno)

    try:
        file_path = re.findall('"prdImgFilePathNm":"(.*?)",', response_1)[0].replace('\\', '')
        img_name = re.findall('"prdImgNm":"(.*?)",', response_1)[0]
        img_url = "http://static.lottedfs.com"
        goods_image_url = "".join([img_url, file_path, img_name])
    except:
        goods_image_url = ''

    goods_item = get_goods_body(goods_id,spec_id_3, prdno, prdoptno, goods_image_url,proxies)

    goods_item['goods_image'] = goods_image_url
    goods_item['spec_id_3'] = spec_id_3
    goods_item['goods_jingle'] = ''
    goods_item['goods_storage'] = 100         # 库存
    goods_item['goods_costprice'] = '0'
    goods_item['goods_attr'] = ''
    goods_item['shop_info'] = ''
    goods_item['goods_salenum'] = '0'
    goods_item['goods_serial'] = ''   # 货号
    goods_item['shop_name'] = ''
    goods_item['shop_range'] = ''
    goods_item['shop_ali'] = ''
    goods_item['shop_mobile'] = ''
    goods_item['shop_address'] = ''
    goods_item['shop_wechart'] = ''
    goods_item['shop_qq'] = ''
    goods_item['shop_goods_num'] = ''
    # 商品基本信息
    try:
        goods_item['goods_brand'] = re.findall('"dispShopNm":"(.*?)",', response_1)[0].encode().decode('unicode_escape')
        # print(goods_item['goods_brand'])
    except:
        goods_item['goods_brand'] = ''

    try:
        goods_item['goods_name'] = re.findall('"prdNm":"(.*?)",', response_1)[0].encode().decode('unicode_escape')
        # print(goods_item['goods_name'])
    except:
        goods_item['goods_name'] = ''

    goods_item['goods_url'] = "http://chn.lottedfs.com/kr/product/productDetail?prdNo={}".format(goods_id)
    # print(goods_item['goods_url'])

    try:
        file_path = re.findall('"prdImgFilePathNm":"(.*?)",', response_1)[0].replace('\\', '')
        img_name = re.findall('"prdImgNm":"(.*?)",', response_1)[0]
        img_url = "http://static.lottedfs.com"
        goods_item['goods_image'] = "".join([img_url, file_path, img_name])
    except:
        goods_item['goods_image'] = ''
    # print('image_url:{}'.format(goods_item['goods_image']))

    try:
        price = re.findall('"saleUntPrcGlbl":"(.*?)",', response_1)[0]
        goods_item['goods_price'] = float(price)
        # print('goods_price:{}'.format(goods_item['goods_price']))
    except:
        goods_item['goods_price'] = ''

    data_process(goods_item)
    # print('data_process:{}'.format(data_process))


def get_goods_body(goods_id,spec_id_3, prdno, prdoptno, goods_image_url,proxies):
    goods_item = {}
    url = "http://chn.lottedfs.com/kr/product/productDetailBtmInfoAjax?"
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Referer': 'http://chn.lottedfs.com/kr/product/productDetail?prdNo='.format(goods_id),
        'User-Agent': user_agent,
        'X-Requested-With': 'XMLHttpRequest',
    }

    query = {
        'prdNo': prdno,
        'prdOptNo': prdoptno,
        'previewYn': '', }

    response = requests.get(url=url,
                            headers=headers,
                            params=query,
                            timeout=20,
                            proxies=proxies)
    print("{}商品详情获取成功".format(goods_id))
    code = response.status_code

    response = response.content.decode('utf-8')
    mylog.info(' BODY |  {}  |  {}  |  {} |  {} |  {} '.format(url.ljust(70),code, goods_id,prdno,prdoptno))

    response_2 = etree.HTML(response)

    des_1 = '<div class="box-collateral box-additional"><h2>商品参数</h2><p> </p><table id="product-attribute-specs-table" class="data-table"><colgroup><col width="99"><col></colgroup><tbody>'
    des_2 = '</tbody></table></div>'
    des_3 = '<div class="box-collateral box-description"><a name="description"></a><h2> </h2><h2>商品详情</h2><p> </p>'
    des_4 = '</div>'

    desc_param = []
    goods_desc_body = []
    t_body = response_2.xpath('//tbody [@name="{}"]/tr'.format(prdno))
    # print(t_body)
    for item in t_body:
        # print('t_body-item:{}'.format(item))
        desc_name = item.xpath('./th[@scope="row"]/text()')[0]
        # desc_name = item.xpath('./th[@scope="row"]/text()').extract()[0]
        # print(desc_name)
        desc_body = item.xpath('./th[@scope="row"]/following-sibling::td/text()')[0].replace(' ', '')
        # print(desc_body)

        key_1 = re.findall('(质量保证标准)', desc_name)
        key_2 = re.findall('(产品咨询)', desc_name)
        key_3 = re.findall('(全部成分)', desc_name)
        key_4 = re.findall('(保质期)', desc_name)
        if key_1 or key_2:
            pass
        elif key_3:
            desc_body = item.xpath('./th[@scope="row"]/following-sibling::td/div/text()')[0]
            desc_body = ''.join(desc_body).replace(r'\r', '').replace(r'\n', '').replace(r'\t', '')
            desc_param.append({"name": '全部成分', "value": desc_body})

            desc_body_1 = item.xpath('./th[@scope="row"]/following-sibling::td/div/text()')[0].replace(' ', '')
            goods_desc_body.append('<tr class="even"><th class="label">{}</th><td class="data last">{}</td></tr>'.format('全部成分', desc_body_1))

        elif key_4:
            desc_body = '生产日期随时更新，不便于标识。'
            desc_param.append({"name": '保质期', "value": desc_body})
            goods_desc_body.append('<tr class="even"><th class="label">{}</th><td class="data last">{}</td></tr>'.format('保质期', desc_body))
        else:
            desc_param.append({"name": desc_name, "value": desc_body})
            goods_desc_body.append('<tr class="even"><th class="label">{}</th><td class="data last">{}</td></tr>'.format(desc_name, desc_body))
    # print(desc_param)
    # print('type:{}'.format(type(desc_param)))
    goods_item['goods_param'] = desc_param
    goods_desc_body = ''.join(goods_desc_body)

    desc_image = []
    images = response_2.xpath('//div[@class="productDesc"]/img/@src')
    # print(images)
    if images:
        for img in images:
            if re.findall("(http)", img):
                goods_images = img.strip()

            else:
                goods_images = 'http:' + img.strip()

            dic_img = {"name": goods_images,"default": "0"}
            desc_image.append('<p><img src="/images/loading.svg" class="img-product-desc" data-src="{}"></p>'.format(img))
            desc_image.append(dic_img)
            goods_item['goods_images'] = desc_image
    else:
        goods_item['goods_images'] = ''

    desc_image = []
    try:
        images = response_2.xpath('//div[@class="productDesc"]/img/@src').extract()
        # print(images)
        if images:
            for img in images:
                desc_image.append('<p><img src="/images/loading.svg" class="img-product-desc" data-src="{}"></p>'.format(img))
            goods_desc_3 = ''.join(desc_image)
        else:
            goods_desc_3 = '<p><img src="/images/loading.svg" class="img-product-desc" data-src="{}"></p>'.format(goods_image_url)
    except:
        goods_desc_3 = '<p><img src="/images/loading.svg" class="img-product-desc" data-src="{}"></p>'.format(goods_image_url)

    if goods_desc_body and goods_desc_3:
        goods_body = ''.join([des_1, goods_desc_body, des_2, des_3, goods_desc_3, des_4])
        # print(goods_body)
    elif goods_desc_body:
        goods_body = ''.join([des_1, goods_desc_body, des_2, ])
    else:
        goods_body = ''.join([des_3, goods_desc_3, des_4])
        # print(goods_body)

    goods_item['goods_desc'] = goods_body
    return goods_item

