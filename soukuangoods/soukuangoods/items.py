# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SoukuangoodsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #商品基本信息
    goods_brand = scrapy.Field()
    goods_name = scrapy.Field()
    goods_image = scrapy.Field()
    goods_jingle = scrapy.Field()
    goods_price = scrapy.Field()
    goods_desc = scrapy.Field()
    goods_url = scrapy.Field()
    gc_name = scrapy.Field()
    goods_storage = scrapy.Field()
    goods_costprice = scrapy.Field()
    goods_attr = scrapy.Field()
    goods_images = scrapy.Field()
    shop_info = scrapy.Field()
    goods_salenum = scrapy.Field()
    goods_serial = scrapy.Field()
    shop_name = scrapy.Field()
    shop_range = scrapy.Field()
    shop_ali = scrapy.Field()
    shop_mobile = scrapy.Field()
    shop_address = scrapy.Field()
