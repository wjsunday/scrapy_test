# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from urllib import parse
import requests
import json
from soukuanshop.items import SoukuanshopItem


class SoukuanshopSpiderSpider(scrapy.Spider):
    name = 'soukuanshop_spider'
    allowed_domains = ['vvic.com']
    start_urls = [
        'https://www.vvic.com/gz/rank/10000?tjtime=month&t=top',#排行总榜
        'https://www.vvic.com/gz/rank/10001?tjtime=month&t=top',#新档口帮
        'https://www.vvic.com/gz/rank/1?tjtime=month&t=top',#连衣裙
        'https://www.vvic.com/gz/rank/8?tjtime=month&t=top',#T恤
        'https://www.vvic.com/gz/rank/15?tjtime=month&t=top',#套装
        'https://www.vvic.com/gz/rank/21?tjtime=month&t=top',#毛衣/针织衫
        'https://www.vvic.com/gz/rank/14?tjtime=month&t=top',#蕾丝衫/雪纺衫
        'https://www.vvic.com/gz/rank/9?tjtime=month&t=top',#衬衫
        'https://www.vvic.com/gz/rank/3?tjtime=month&t=top',#牛仔裤
        'https://www.vvic.com/gz/rank/28?tjtime=month&t=top',#孕妇装
        'https://www.vvic.com/gz/rank/4?tjtime=month&t=top',#休闲裤/打底裤
        'https://www.vvic.com/gz/rank/6?tjtime=month&t=top',#短外套/马甲
        'https://www.vvic.com/gz/rank/18?tjtime=month&t=top',#大码女装
        'https://www.vvic.com/gz/rank/2?tjtime=month&t=top',#半身裙
        'https://www.vvic.com/gz/rank/10003?tjtime=month&t=top',#民族风棉麻榜
        'https://www.vvic.com/gz/rank/10002?tjtime=month&t=top',#外贸榜
        'https://www.vvic.com/gz/rank/24?tjtime=month&t=top',#男装
        'https://www.vvic.com/gz/rank/10?tjtime=month&t=top',#卫衣/绒衫
        'https://www.vvic.com/gz/rank/7?tjtime=month&t=top',#棉服/羽绒
        'https://www.vvic.com/gz/rank/10005?tjtime=month&t=top',#毛呢/风衣/皮衣
        'https://www.vvic.com/gz/rank/10004?tjtime=month&t=top',#亲子情侣装
    ]

    def parse(self, response):
        urltmp = urllib.parse.unquote(response.url)
        shop_list = response.xpath("//tbody/tr")
        gc_name = response.xpath("//h1/text()").extract_first()
        param = parse.urlparse(urltmp)
        paramdict = parse.parse_qs(param.query)
        if 'currentPage' in paramdict:
            page = int(paramdict['currentPage'][0])
        else:
            page = 1
        for i_item in shop_list:
            soukuanshop_item = SoukuanshopItem()
            soukuanshop_item['shop_range'] = i_item.xpath(".//td/div[@class='rank-tab-td-01']/em/text()").extract_first().replace(' ','').replace("\n","")
            soukuanshop_item['shop_name'] = i_item.xpath(".//td[@class='rank-shop-info']//a[@class='rank-shop-word j-vda']/text()").extract_first()
            soukuanshop_item['shop_address'] = i_item.xpath(".//td[@class='rank-shop-info']//p[@class='rank-shop-address']/text()").extract_first()
            shop_sale = i_item.xpath(".//p[@class='rank-shop-sell']/span")
            soukuanshop_item['shop_sale'] = shop_sale[0].xpath(".//em/text()").extract_first()
            soukuanshop_item['shop_goods_num'] = shop_sale[1].xpath(".//em/text()").extract_first()
            soukuanshop_item['gc_name'] = gc_name.replace(' ','').replace("\n","")
            yield soukuanshop_item
        if page <= 100:
            pageold = page
            page += 1
            if '&currentPage=' in urltmp:
                url = urltmp.replace('&currentPage='+str(pageold), '&currentPage='+str(page))
            else:
                url = urltmp + '&currentPage=' + str(page)
            yield scrapy.Request(url,callback=self.parse)
