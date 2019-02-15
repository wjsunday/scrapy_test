# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SoukuanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    goods_name = scrapy.Field()
    goods_img = scrapy.Field()
    goods_price = scrapy.Field()
    goods_url = scrapy.Field()
    gc_name = scrapy.Field()
