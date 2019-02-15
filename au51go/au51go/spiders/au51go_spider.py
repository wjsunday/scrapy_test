# -*- coding: utf-8 -*-
import scrapy
from au51go.items import Au51GoItem

class Au51goSpiderSpider(scrapy.Spider):
    name = 'au51go_spider'
    allowed_domains = ['51go.com.au']
    start_urls = [
        'https://www.51go.com.au/Category/women',#女性保健
        'https://www.51go.com.au/Category/men',#男性保健
        'https://www.51go.com.au/Category/senior',#老年保健
        'https://www.51go.com.au/Category/weight-control',#排毒瘦身
        'https://www.51go.com.au/Category/fish-oil',#鱼油
        'https://www.51go.com.au/Category/supplements',#矿物质
        'https://www.51go.com.au/Category/vitamin',#维生素
        'https://www.51go.com.au/Category/honey-products',#蜂产品
        'https://www.51go.com.au/Category/probiotics',#益生菌
        'https://www.51go.com.au/Category/protein',#蛋白粉 膳食纤维
        'https://www.51go.com.au/Category/health-care-basic-other',#基础保健其他
        'https://www.51go.com.au/Category/eye-care',#护眼
        'https://www.51go.com.au/Category/skincare',#护肤
        'https://www.51go.com.au/Category/bath',#沐浴清洁
        'https://www.51go.com.au/Category/sunscreen',#防晒
        'https://www.51go.com.au/Category/makeup',#彩妆
        'https://www.51go.com.au/Category/hair-care',#洗发护发
        'https://www.51go.com.au/Category/fitness',#丰胸减肥
        'https://www.51go.com.au/Category/baby-formula-step-1',#1段
        'https://www.51go.com.au/Category/baby-formula-step-2',#2段
        'https://www.51go.com.au/Category/baby-formula-step-3',#3段
        'https://www.51go.com.au/Category/baby-formula-step-4',#4段
        'https://www.51go.com.au/Category/baby-rice',#米粉
        'https://www.51go.com.au/Category/baby-skincare',#洗护用品
        'https://www.51go.com.au/Category/baby-toothbrush',#牙膏牙刷
        'https://www.51go.com.au/Category/baby-bottle',#奶瓶奶嘴
        'https://www.51go.com.au/Category/baby-skin-protection',#驱蚊防晒
        'https://www.51go.com.au/Category/baby-fish-oil',#婴幼儿鱼油
        'https://www.51go.com.au/Category/dha',#DHA
        'https://www.51go.com.au/Category/baby-honey',#蜂产品
        'https://www.51go.com.au/Category/baby-cure',#感冒止咳
        'https://www.51go.com.au/Category/baby-vitamin',#婴幼儿维生素
        'https://www.51go.com.au/Category/baby-supplements',#婴幼儿矿物质
        'https://www.51go.com.au/Category/baby-probiotics',#婴幼儿益生菌
        'https://www.51go.com.au/Category/mother-products',#孕妇产品
        'https://www.51go.com.au/Category/mother-formula',#孕妇奶粉
        'https://www.51go.com.au/Category/oral',#口腔护理
        'https://www.51go.com.au/Category/personal-care',#个人护理
        'https://www.51go.com.au/Category/household-others',#家居生活其他
        #'https://www.51go.com.au/Category/fresh',#生鲜
        'https://www.51go.com.au/Category/honey',#蜂蜜
        'https://www.51go.com.au/Category/milk',#营养奶粉
        'https://www.51go.com.au/Category/milk-products',#奶制品
        'https://www.51go.com.au/Category/snacks',#零食
        'https://www.51go.com.au/Category/breakfast',#麦片早餐
        'https://www.51go.com.au/Category/food-others',#健康美食其他
        'https://www.51go.com.au/Category/scarf',#围巾
        'https://www.51go.com.au/Category/jellycat',#Jellycat
    ]

    def parse(self, response):
       goods_list = response.xpath("//div[@class='index_con_same']//ul/li")

       for i_item in goods_list:
           au51go_item = Au51GoItem()
           au51go_item['goods_name'] = i_item.xpath(".//p[@class='jingxuan_tl']/a/text()").extract_first()
           au51go_item['goods_img'] = i_item.xpath(".//a[@class='jingxuan_img']/img/@src").extract_first()
           content = i_item.xpath(".//p[@class='jingxuan_money']/text()").extract()
           for i_content in content:
               content_s = "".join(i_content.split())
               au51go_item['goods_price'] = content_s
           au51go_item['goods_url'] = i_item.xpath(".//a[@class='jingxuan_img']/@href").extract_first()
           contentt = i_item.xpath("//div[@class='muying_fenlei']//span//text()").extract()
           for t_content in contentt:
               content_t = "".join(t_content.split())
               au51go_item['gc_name'] = content_t
           yield au51go_item
       next_link = response.xpath("//div[@class='page']/a[@title='下一页']/@href").extract()
       if next_link:
           next_link = next_link[0]
           yield scrapy.Request("https://www.51go.com.au"+next_link,callback=self.parse)