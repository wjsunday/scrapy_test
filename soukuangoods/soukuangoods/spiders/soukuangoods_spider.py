# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
import pymysql
from soukuangoods.items import SoukuangoodsItem
from soukuangoods.settings import mysql_host,mysql_port,mysql_db_user,mysql_db_pwd,mysql_db_name,mysql_db_charset


class SoukuangoodsSpiderSpider(scrapy.Spider):
    name = 'soukuangoods_spider'
    allowed_domains = ['vvic.com']
    start_urls = []
    goods_info = dict()
    attr = dict()

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
        sql = "SELECT goods_name, goods_url, gc_name FROM mall_51go_list WHERE goods_source=2"
        self.cur.execute(sql)
        results = self.cur.fetchall()
        url = 'https://www.vvic.com'
        for row in results:
            self.start_urls.append(url+row[1])
            self.goods_info[url+row[1]] = {'goods_name':row[0], 'goods_url':url+row[1], 'gc_name':row[2]}

    def parse(self, response):
        urltmp = urllib.parse.unquote(response.url)
        goods = SoukuangoodsItem()
        #商品基本信息
        goods['goods_name'] = response.xpath("//div[@class='d-name']//strong/text()").extract_first()
        goods['goods_brand'] = '广州女装批发'
        goods['goods_image'] = response.xpath("//div[@class='tb-pic-main']/a/@href").extract_first()
        goods['goods_jingle'] = ''
        goods['goods_price'] = float(response.xpath("//strong[@class='d-sale']/text()").extract_first())
        goods['goods_desc'] = response.xpath("//div[@class='fr con-info j-con-info']").extract_first()
        if urltmp in self.goods_info:
            goods['goods_url'] = self.goods_info[urltmp]['goods_url']
            goods['gc_name'] = self.goods_info[urltmp]['gc_name']
        goods['goods_storage'] = 100
        goods['goods_costprice'] = response.xpath("//strong[@class='d-sale']/text()").extract_first()
        #商品属性
        attr_dd = response.xpath("//dd[@class='fl choice']")
        for i_item in attr_dd:
            #处理特殊样式
            name = i_item.xpath(".//div[@class='name color']/text()").extract_first()
            if not name is None:
                value = i_item.xpath(".//div[@class='value color-choice']/ul/li/a/img/@alt").extract()
            else:
                name = i_item.xpath(".//div[@class='name']/text()").extract_first()
                value = i_item.xpath(".//div[@class='value goods-choice']//ul//li/a/text()").extract()
            self.attr[name] = value
        goods['goods_attr'] = self.attr
        goods_desc_img = response.xpath("//script[@id='descTemplate']/text()").extract_first()
        goods['goods_desc'] = goods['goods_desc'] + goods_desc_img
        shop_info = response.xpath("//div[@class='d-attr clearfix']/ul/li/text()").extract()
        goods['shop_info'] = ",".join([str(e).replace("\n","").replace(' ','') for e in shop_info])
        goods['goods_images'] = response.xpath("//div[@class='thumbnail']//div[@class='tb-thumb-item ']/a/img/@mid").extract()
        goods['goods_salenum'] = response.xpath("//p[@class='v-sale-total']/text()").extract_first()
        goods['goods_serial'] = response.xpath("//div[@class='value ff-arial']/text()").extract_first()
        #获取商铺的其它信息
        goods['shop_name'] = response.xpath("//h2[@class='shop-name ']/span/text()").extract_first()
        goods['shop_range'] = response.xpath("//em[@class='text-top-num']/text()").extract_first()
        goods['shop_ali'] = response.xpath("//div[@class='text']/span[@class='fl']/text()").extract_first()
        shop_mobile_list = response.xpath("//li[@class='tel-list']/div[@class='text']/p//span[@class]/text()").extract()
        goods['shop_mobile'] = "".join([str(e) for e in shop_mobile_list])
        shopinfotmp = response.xpath("//ul[@class='mt10']/li")
        goods['shop_address'] = shopinfotmp[len(shopinfotmp)-1].xpath(".//div[@class='text']/text()").extract_first()
        # weixinall = shopinfotmp[4].xpath(".//div[@class='text']/span/text()").extract()
        # weixinhas = shopinfotmp[4].xpath(".//div[@class='text']/span[@style]/text()").extract()
        # weixin = list(set(weixinhas).difference(set(weixinall)))
        # print(weixinall)
        # print(weixinhas)
        # print(weixin)
        yield goods

