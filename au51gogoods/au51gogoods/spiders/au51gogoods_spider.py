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
        sql = """SELECT goods_name, goods_url, gc_name FROM mall_51go_list WHERE goods_id in(598,785,786,787,788,789,790,791,792,793,794,795,796,797,798,799,800,801,802,803,804,805,806,807,808,809,810,811,812,813,814,815,816,817,818,819,820,821,822,823,824,825,826,827,828,829,830,831,832,833,834,835,836,837,838,839,840,841,842,843,844,845,846,847,848,849,850,851,852,853,854,855,856,857,858,859,860,861,862,863,864,865,866,867,868,869,870,871,872,873,874,875,876,877,878,879,880,881,882,883,884,885,886,887,888,889,890,891,892,893,894,895,896,897,898,899,900,901,902,903,904,905,906,907,908,909,910,911,912,913,914,915,916,917,918,919,920,921,922,923,924,925,926,927,928,929,930,931,932,933,934,935,936,937,938,939,940,941,942,943,944,945,946,947,948,949,950,951,952,953,954,955,956,957,958,959,960,961,962,963,964,965,966,967,968,969,970,971,972,973,974,975,976,977,978,979,980,981,982,983,984,985,986,987,988,989,990,991,992,993,994,995,996,997,998,999,1000,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,1016,1017,1018,1019,1020,117698,117699,117700,117701,117702,117703,117704,117705,117706,117707,117708,117709,117710,164575,164576,164577,164578,164579,164580,164581,164582,178088,178089,239688,239689,239690,239691,239692,239693,239694,239695,239696,239697,239698,239699,239700,239701,239702,239703,239704,239705)"""
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



