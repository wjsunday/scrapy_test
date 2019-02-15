# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
import pymysql
from au51gogoods.items import Au51GogoodsItem
from au51gogoods.settings import mysql_host,mysql_port,mysql_db_user,mysql_db_pwd,mysql_db_name,mysql_db_charset


class Au51gogoodsSpiderSpider(scrapy.Spider):
    name = 'au51gogoods_spider'
    allowed_domains = ['51go.com.au']
    start_urls = []
    goods_info = dict()
    exchange_rate_us = 1.03
    exchange_rate_world = 4.8881


    def __init__(self):
        self.client = pymysql.connect(
            host=mysql_host,
            port=mysql_port,
            user=mysql_db_user,  #使用自己的用户名
            passwd=mysql_db_pwd,  # 使用自己的密码
            db=mysql_db_name,  # 数据库名
            charset=mysql_db_charset
        )
        self.cur = self.client.cursor()
        sql = "SELECT goods_name, goods_url, gc_name FROM mall_51go_list WHERE goods_source=1"
        self.cur.execute(sql)
        results = self.cur.fetchall()
        url = 'https://www.51go.com.au'
        for row in results:
            self.start_urls.append(url+row[1])
            self.goods_info[url+row[1]] = {'goods_name':row[0], 'goods_url':url+row[1], 'gc_name':row[2]}

    def parse(self, response):
        urltmp = urllib.parse.unquote(response.url)
        goods = Au51GogoodsItem()
        str = response.xpath("//div[@class='right pro_con_t_rt']//span[@class='left']/text()").extract_first()
        x = str.split("：", 1)
        goods['goods_brand'] = x[1]
        y = response.xpath("//div[@class='pro_con_t_rt_tl']/text()").extract()
        for i_content in y:
            content_s = "".join(i_content.split())
            goods['goods_name'] = content_s
        if urltmp in self.goods_info:
            goods['goods_url'] = self.goods_info[urltmp]['goods_url']
            goods['gc_name'] = self.goods_info[urltmp]['gc_name']
        goods['goods_image'] = response.xpath("//div[@class='jqzoom']/img/@src").extract_first()
        z = response.xpath("//div[@class='pro_con_t_rt_xinx']/text()").extract()
        for j_content in z:
            content_k = "".join(j_content.split())
            goods['goods_jingle'] = content_k
        p = response.xpath("//span[@class='color_red bold']/text()").extract_first()
        v = p.split("$", 1)
        goods['goods_price'] = round(float(v[1])*self.exchange_rate_us*self.exchange_rate_world,2)
        goods['goods_costprice'] = v[1]
        goods['goods_desc'] = response.xpath("//div[@class='pro_con_b_rt_main']").extract_first()
        goods_weight = response.xpath("//div[@class='clearfix yunfei']/span/text()").extract_first()
        if not goods_weight is None:
            goods_weight_tmp = goods_weight.split('：')
            goods['goods_weight'] = goods_weight_tmp[1].replace(' 千克','')
        else:
            goods['goods_weight'] = ''
        goods_storage = response.xpath("//a[@id='addtocart']").extract_first()
        if not goods_storage is None:
            goods['goods_storage'] = 100
        else:
            goods['goods_storage'] = 0
        yield goods



