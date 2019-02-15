# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from urllib import parse
import requests
import json
from soukuan.items import SoukuanItem


class SoukuanSpiderSpider(scrapy.Spider):
    name = 'soukuan_spider'
    allowed_domains = ['vvic.com']
    start_urls = [
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000035&merge=1',#女装->上装/外套->T恤
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000018&merge=1',#女装->上装/外套->寸衫
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000129&merge=1',#女装->上装/外套->短外套
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000025&merge=1',#女装->上装/外套->休闲运动
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000038&merge=1',#女装->上装/外套->毛织针衫
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000071&merge=1',#女装->上装/外套->风衣
        'https://www.vvic.com/gz/search/index.html?q=%E6%83%85%E4%BE%A3%E8%A3%85&merge=1&merge=1',#女装->上装/外套->情侣装
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000017&merge=1',#女装->上装/外套->毛衣
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000055&merge=1',#女装->上装/外套->旗袍
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000067&merge=1',#女装->上装/外套->西装
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000389&merge=1',#女装->上装/外套->时尚套装
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000019&merge=1',#女装->上装/外套->蕾丝雪纺
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000006&merge=1',#女装->上装/外套->大码连衣裙
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000364&merge=1',#女装->上装/外套->背心吊带
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000068&merge=1',#女装->上装/外套->卫衣绒衫
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000041&merge=1',#女装->上装/外套->中老年连衣裙
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000176&merge=1',#女装->上装/外套->马甲
        'https://www.vvic.com/gz/list/index.html?merge=1&pid=9#J_main&merge=1',#女装->上装/外套->孕妇装
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000069&merge=1',#女装->上装/外套->羽绒服
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000106&merge=1',#女装->裙装->连衣裙
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000001&merge=1',#女装->裙装->半身裙
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000022&merge=1',#女装->裙装->职业女裙套装
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000021&merge=1',#女装->裤装->牛仔裤
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000020&merge=1',#女装->裤装->休闲裤
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000057&merge=1',#女装->裤装->打底裤
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000291&merge=1',#女装->裤装->西装裤/正装裤
        'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000023&merge=1',#女装->裤装->职业女裤套装
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000078&merge=1',#男装->上装/外套->卫衣
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000034&merge=1',#男装->上装/外套->针织衫
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000077&merge=1',#男装->上装/外套->大码卫衣
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000116&merge=1',#男装->上装/外套->马甲
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000117&merge=1',#男装->上装/外套->背心
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000076&merge=1',#男装->上装/外套->夹克
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000424&merge=1',#男装->上装/外套->运动套装
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000120&merge=1',#男装->上装/外套->风衣
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000125&merge=1',#男装->上装/外套->棉衣
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000421&merge=1',#男装->上装/外套->其他套装
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000031&merge=1',#男装->寸衫/T恤->T恤
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000109&merge=1',#男装->寸衫/T恤->寸衫
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000030&merge=1',#男装->寸衫/T恤->大码T恤
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000090&merge=1',#男装->寸衫/T恤->Polo衫
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000029&merge=1',#男装->寸衫/T恤->中老年人T恤
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000108&merge=1',#男装->寸衫/T恤->大码寸衫
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000016&merge=1',#男装->裤装->休闲裤
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000081&merge=1',#男装->裤装->牛仔裤
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000015&merge=1',#男装->裤装->大码休闲裤
        'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000080&merge=1',#男装->裤装->大码牛仔裤
    ]

    def parse(self, response):
        urltmp = urllib.parse.unquote(response.url)
        goods_list = response.xpath("//div[@class='goods-list clearfix']//ul/li")
        for i_item in goods_list:
            soukuan_item = SoukuanItem()
            content = i_item.xpath(".//div[@class='title']//a/text()").extract()
            for i_content in content:
                content_s = "".join(i_content.split())
                soukuan_item['goods_name'] = content_s
            soukuan_item['goods_img'] = ''
            content_p = i_item.xpath(".//div[@class='fl price']/text()").extract()
            for p_content in content_p:
                content_pp = "".join(p_content.split())
                soukuan_item['goods_price'] = content_pp
            soukuan_item['goods_url'] = i_item.xpath(".//div[@class='item']/div[@class='pic ']/a/@href").extract_first()
            soukuan_item['gc_name'] = urltmp
            yield soukuan_item

        param = parse.urlparse(urltmp)
        paramdict = parse.parse_qs(param.query)
        vcid = paramdict['vcid'][0]
        for n in range(2, 101):
            url = 'https://www.vvic.com/apic/search/asy?merge=1&pid=1&vcid='+str(vcid)+'&searchCity=gz&currentPage='+str(n)
            responsepage = requests.get(url, verify=False)
            index_response_dict = json.loads(responsepage.text)
            for index_item in index_response_dict['data']['search_page']['recordList']:
                soukuan_item['goods_name'] = index_item['title']
                soukuan_item['goods_img'] = index_item['index_img_url']
                soukuan_item['goods_price'] = index_item['price']
                soukuan_item['goods_url'] = "/item/"+str(index_item['item_id'])
                soukuan_item['gc_name'] = urltmp
                yield soukuan_item












