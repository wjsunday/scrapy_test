# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import json
import time
import os
import re
import redis
import requests
import oss2
from spiders.spec_info import spec_info
from kafka import KafkaProducer
from soukuan_kfk.settings import image_path
from soukuan_kfk.settings import bootstrap_servers,kfk_topic
from mylog import MyLog
from soukuan_kfk.settings import Bucket, AccessKeyID, AccessKeySecret, EndPoint
from soukuan_kfk.settings import redis_host,redis_port,redis_pwd,redis_name

class SoukuanKfkPipeline(object):
    def __init__(self):

        self.r = redis.Redis(host=redis_host, port=redis_port, db=redis_name, password=redis_pwd)

        # kafka配置
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        self.topic = kfk_topic

        # oss配置
        self.auth = oss2.Auth(AccessKeyID, AccessKeySecret)
        self.endpoint = EndPoint
        self.bucket = oss2.Bucket(self.auth, self.endpoint, Bucket)  # 项目名称

        self.spec_info = spec_info
        self.brand_name = '广州女装批发'
        self.brand_id = '6'
        self.store_name = '拼拼侠'
        self.store_id = '1'
        self.type_name = "服装"
        self.type_id = "6"
        self.transport_title = "拼拼侠通用运费模板"
        self.transport_id = "11"
        self.mylog = MyLog()

    def process_item(self, item, spider):

        price = item['goods_price']
        try:
            if price <= 100:
                goods_price = round(price * 1.25 + 2)  # 拼拼侠售价
                goods_marketprice = price * 3  # 拼拼侠市场价
            elif price >= 500:
                goods_price = round(price * 1.15 + 2)
                goods_marketprice = price * 1.5
            else:
                goods_price = round(price * 1.25 + 2)
                goods_marketprice = price * 2.5
        except:
            goods_price = '0'
            goods_marketprice = '0'

        goods_image = item['goods_image']
        # goods_image = self.down_image(goods_image_url)

        goods_brand = item['goods_brand']
        goods_name = item['goods_name']
        goods_jingle = item['goods_jingle']
        goods_desc = item['goods_desc']
        goods_url = item['goods_url']
        spec_id_3 = item['spec_id_3']
        goods_storage = item['goods_storage']
        goods_costprice = item['goods_costprice']
        goods_attr = item['goods_attr']
        goods_images = item['goods_images']
        shop_info = item['shop_info']
        goods_salenum = item['goods_salenum']
        goods_serial = item['goods_serial']
        shop_name = item['shop_name']
        shop_range = item['shop_range']
        shop_ali = item['shop_ali']
        shop_mobile = item['shop_mobile']
        shop_address = item['shop_address']
        shop_wechart = item['shop_wechart']
        shop_qq = item['shop_qq']
        goods_param = item['goods_param']
        shop_goods_num = item['shop_goods_num']

        if goods_price:
            data = {
                "goods_name": goods_name,
                "goods_cat": {
                    "gc_id": spec_info[spec_id_3][2],
                    "gc_id_1": spec_info[spec_id_3][0],
                    "gc_id_2": spec_info[spec_id_3][1],
                    "gc_id_3": spec_info[spec_id_3][2],
                },
                "is_suport_voucher": "1", # 是否支持优惠券1支持;2不支持
                "brand_id": self.brand_id,
                "brand_name": self.brand_name,
                "goods_image": goods_image,
                "goods_price": goods_price,
                "goods_marketprice": goods_marketprice,
                "goods_body": goods_desc,
                "mobile_body": goods_desc,
                "store_id": self.store_id,
                "store_name": self.store_name,
                "goods_weight": "0.00",     # 商品重量
                "goods_salenum": goods_salenum,     # 商品销量
                "goods_storage": goods_storage,     # 商品库存
                "goods_images": goods_images,
                "goods_attr": goods_attr,
                "goods_param": goods_param,
                "shop_info": {
                    "shop_name": shop_name,
                    "shop_range": shop_range,
                    "shop_ali": shop_ali,
                    "shop_goods_num": shop_goods_num,
                    "shop_mobile": shop_mobile,
                    "shop_wechat": shop_wechart,
                    "shop_qq": shop_qq,
                    "shop_product": '广东省 广州',
                    "shop_address": shop_address,
                },
                "goods_url": goods_url,
                "goods_serial": goods_serial,
                "type_id": self.type_id,
                "type_name": self.type_name,
                "transport_id": self.transport_id,
                "transport_title": self.transport_title,
            }

            data = json.dumps(data)
            self.producer.send(topic=self.topic, value=data.encode('utf-8'), partition=None)
            self.r.hset('soukuan_kfk', goods_url, 1)
            # self.producer.close()

        return item
