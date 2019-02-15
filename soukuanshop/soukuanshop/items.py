# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SoukuanshopItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    shop_range = scrapy.Field()
    shop_name = scrapy.Field()
    shop_address = scrapy.Field()
    shop_sale = scrapy.Field()
    shop_goods_num = scrapy.Field()
    gc_name = scrapy.Field()
