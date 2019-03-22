# -*- coding: utf-8 -*-
import datetime
import hashlib
import json
import re
import os

import math
from random import choice

import oss2
import redis
import requests
import scrapy
import time
from scrapy import Request,FormRequest
from scrapy import Selector
import sys
sys.path.append("../")
from spiders.spec_info import spec_info,url_info
from spiders.wandouip import get_proxy
from soukuan_kfk.items import SoukuanKfkItem
from soukuan_kfk.mylog import MyLog
from soukuan_kfk.settings import image_path,store_id
from soukuan_kfk.settings import Bucket, AccessKeyID, AccessKeySecret, EndPoint, oss_img_path
from soukuan_kfk.settings import redis_host,redis_port,redis_pwd,redis_name

proxy = get_proxy()

class SoukuanwangSpider(scrapy.Spider):
    name = 'soukuanwang'
    allowed_domains = ['www.vvic.com']
    start_urls = ['http://www.vvic.com/']

    def __init__(self):
        self.redis_db = redis.Redis(host=redis_host, port=redis_port, db=redis_name, password=redis_pwd)
        self.spec_info = spec_info
        self.url_info = url_info
        self.mylog = MyLog()
        self.attr = {'颜色':'','尺码':''}

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            }

        # oss配置
        self.auth = oss2.Auth(AccessKeyID, AccessKeySecret)
        self.endpoint = EndPoint
        self.bucket = oss2.Bucket(self.auth, self.endpoint, Bucket)  # 项目名称

    def start_requests(self):
        global proxy
        proxy = proxy if proxy else get_proxy()

        # market_list = ['19', '12', '49', '10', '13', '14', '15', '31', '11', '17', '52', '18', '34', '20', '16', '48','23', '25', '51', '47', '53', '50', '54', '36', '43', '39', '45', '28', '26', '35', '42', '38']
        market_list = ['19']
        for spec_id_3 in self.spec_info:
            pid = self.spec_info[spec_id_3][3]
            for market in market_list:
                url = 'https://www.vvic.com/apic/search/asy?pid={}&spec_id_3={}&bid={}&searchCity=gz&currentPage=1'.format(pid, spec_id_3, market)
                print(url)

                headers = {
                    'user-agent': self.headers,
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'accept-encoding': 'gzip, deflate, br',
                }
                yield Request(url=url,
                              headers=headers,
                              callback=self.get_pages,
                              dont_filter=True,
                              meta={"spec_id_3": spec_id_3,
                                    "pid": pid,
                                    "market": market,
                                    'proxy':choice(proxy)})

    def get_pages(self, response):
        global proxy
        proxy = proxy if proxy else get_proxy()
        proxies = response.meta['proxy']
        if response.status != 200:
            proxy.remove(proxies)

        pid = response.meta["pid"]
        spec_id_3 = response.meta["spec_id_3"]
        market = response.meta["market"]
        json_data = json.loads(response.text)
        pagesize = json_data["data"]["search_page"]["pageSize"]
        recordcound = json_data["data"]["search_page"]["recordCount"]
        pages = math.ceil(int(recordcound) / int(pagesize))
        print(pages)

        for page in range(1, int(pages) + 1):
            url = 'https://www.vvic.com/apic/search/asy?merge=1&isTheft=0&pid={}&spec_id_3={}&bid={}&searchCity=gz&currentPage={}'.format(pid, spec_id_3, market, page)
            print(url)
            if self.redis_db.hexists('soukuan_url', url):
                pass
            else:
                headers = {
                    'user-agent': self.headers,
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'accept-encoding': 'gzip, deflate, br',
                }
                yield Request(url=url,
                              headers=headers,
                              callback=self.get_show_list,
                              meta={"spec_id_3": spec_id_3, "pid": pid, "market": market,'page_url':url,'proxy':choice(proxy)})

    def get_show_list(self, response):
        global proxy
        proxy = proxy if proxy else get_proxy()
        proxies = response.meta['proxy']
        if response.status != 200:
            proxy.remove(proxies)

        page_url = response.meta['page_url']
        self.redis_db.hset('soukuan_url', page_url, 'page')
        json_data = json.loads(response.text)
        data = json_data["data"]["search_page"]["recordList"]
        for i in data:
            id = i["item_id"]
            url = "https://www.vvic.com/item/{}".format(id)
            print(id)

            if self.redis_db.hexists('soukuan_url', url):
                pass
            else:
                headers = {
                    'user-agent': self.headers,
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'accept-encoding': 'gzip, deflate, br',
                }

                yield Request(url=url,
                              headers=headers,
                              callback=self.get_details,
                              # callback=self.select_price,
                              meta={"spec_id_3": response.meta["spec_id_3"],
                                    "pid": response.meta["pid"],
                                    "market": response.meta["market"],
                                    "id": id,
                                    "goods_url": url,
                                    'proxy': choice(proxy)})

    def get_details(self, response):
        global proxy
        proxy = proxy if proxy else get_proxy()
        proxies = response.meta['proxy']
        if response.status != 200:
            proxy.remove(proxies)

        spec_id_3 = response.meta["spec_id_3"]
        goods_url = response.meta["goods_url"]
        self.redis_db.hset('soukuan_url',goods_url,'goods')

        item = SoukuanKfkItem()
        response = Selector(response)

        item['goods_brand'] = '广州女装批发'
        item['goods_name'] = response.xpath("//div[@class='d-name']//strong/text()").extract()[0]

        item['goods_jingle'] = ''
        price = response.xpath("//strong[@class='d-sale']/text()").extract_first()
        try:
            item['goods_price'] = float(price)
        except:
            goods_price = price.split("-")[-1].split()[0]
            item['goods_price'] = float(goods_price)

        item['goods_url'] = goods_url
        item['spec_id_3'] = spec_id_3
        item['goods_storage'] = 100
        item['goods_costprice'] = 0

        # 商品属性
        attr_dd = response.xpath("//dd[@class='fl choice']")
        for i_item in attr_dd:
            try:
                name = i_item.xpath(".//div[@class='name color']/text()").extract()[0]
                print(name)
                value = i_item.xpath('.//div[@class="value color-choice"]//img/@alt').extract()
                print(value)
            except:
                name = i_item.xpath(".//div[@class='name']/text()").extract_first()
                print(name)
                value = i_item.xpath(".//div[@class='value goods-choice']//ul//li/a/text()").extract()
                print(value)


            if name == "颜色":
                self.attr['颜色'] = value
            elif name == "尺码":
                self.attr['尺码'] = value
            else:
                if name and value:
                    self.attr[name] = value

            # if name and value:
            #     self.attr[name] = value
        item['goods_attr'] = self.attr

        shop_info = response.xpath("//div[@class='d-attr clearfix']/ul/li/text()").extract()
        item['shop_info'] = ",".join([str(e).replace("\n", "").replace(' ', '') for e in shop_info])

        item['goods_salenum'] = response.xpath("//p[@class='v-sale-total']/text()").extract_first()
        goods_serial = response.xpath("//div[@class='value ff-arial']/text()").extract_first()
        item['goods_serial'] = goods_serial.replace("\n", "").replace(' ', '')

        shop_name = response.xpath("//h2[contains (@class,'shop-name ')]/span/text()").extract()[0]
        item['shop_name'] = shop_name.replace("\n", "").replace(' ', '')
        try:
            item['shop_range'] = response.xpath("//em[@class='text-top-num']/text()").extract()[0]
        except:
            item['shop_range'] = '0'
        item['shop_ali'] = response.xpath("//div[@class='text']/span[@class='fl']/text()").extract()[0]

        shopinfotmp = response.xpath("//ul[@class='mt10']/li")
        shop_address = shopinfotmp[len(shopinfotmp) - 1].xpath(".//div[@class='text']/text()").extract_first()
        item['shop_address'] = shop_address.replace("\n", "").replace(' ', '')

        # 商品数
        goods_num = response.xpath('//div [contains (@class ,"shop-content")]//ol/@class').extract()
        # print(goods_num)
        nums = []
        for num_ in goods_num:
            try:
                num = re.findall('(\d)', num_)[0]
                # print(num)
                nums.append(num)
            except:
                pass
        shop_goods_num = "".join(nums).strip()
        item['shop_goods_num'] = shop_goods_num

        # 电话
        mobile_list = response.xpath('//li[@class="tel-list"]/div[@class="text"]/p')
        shop_mobile_list = []
        for span in mobile_list:
            mobile = span.xpath('./span[contains (@class,"xx")]/text()').extract()
            # print(mobile)
            shop_mobile_list.append("".join(mobile))
        shop_mobile_list = ",".join(shop_mobile_list)
        item['shop_mobile'] = shop_mobile_list

        # 微信
        shop_wechart_list = []
        try:
            wechart = response.xpath(
                '//div[contains (text(),"微信：")]/following-sibling::div/span[not (@style)]/text()').extract()
            shop_wechart = "".join(wechart)
        except:
            shop_wechart = ""
        item['shop_wechart'] = shop_wechart

        # qq
        shop_qq_list = []
        try:
            qq = response.xpath('//div[contains (text(),"QQ：")]/following-sibling::div/span[@class]/text()').extract()
            shop_qq = "".join(qq)
        except:
            shop_qq = ""
        item['shop_qq'] = shop_qq

        goods_param = []
        param_dd = response.xpath('//div[@class="d-attr clearfix"]/ul/li/text()').extract()
        # print(param_dd)
        for num in param_dd:
            try:
                param = {}
                name = num.split(':\xa0')[0].strip()
                key_1 = re.findall('(尺码|尺寸)', name)
                key_2 = re.findall('(颜色|货号)', name)
                if not (key_1 or key_2):
                    value = num.split(':\xa0')[1].strip().replace('\n', "")
                    key_3 = re.findall('(,)', value)
                    if key_3:
                        value = value.split(',')[0]
                    else:
                        value=value
                    param["name"] = name
                    param["value"] = value
                    goods_param.append(param)
            except:
                try:
                    param = {}
                    name = num.split(':')[0].strip()
                    key_1 = re.findall('(尺码|尺寸)', name)
                    key_2 = re.findall('(颜色|货号)', name)
                    if not (key_1 or key_2):
                        value = num.split(':')[1].strip().replace('\n', "")
                        key_3 = re.findall('(,)', value)
                        if key_3:
                            value = value.split(',')[0]
                        else:
                            value = value
                        param["name"] = name
                        param["value"] = value
                        goods_param.append(param)
                except:
                    pass
        item['goods_param'] = goods_param

        # yield item

# ##################################################
# ##################################################

        # 图片上传至oss
        goods_image = response.xpath("//div[@class='tb-pic-main']/a/@href").extract()[0]
        if re.findall("(http)", goods_image):
            img_name, img_url = self.down_image(goods_image.strip())
            item['goods_image'] = img_name

        else:
            img_name, img_url = self.down_image('http:' + goods_image.strip())
            item['goods_image'] = img_name


        # 详情图片下载并上传至oss，返回绝对路径

        goods_desc_body = response.xpath("//div[@class='fr con-info j-con-info']").extract_first()

        goods_desc_images = []
        desc_images = response.xpath("//script[@id='descTemplate']/text()").extract()[0]
        images = re.findall('(http.*?jpg|http.*?png|http.*?JPG|http.*?PNG)', desc_images)
        # images = re.findall('src="(.*?)"', desc_images)[0]
        for img_url_sk in images:
            print('img_url_sk:{}'.format(img_url_sk))
            # goods_image_oss = self.down_image(img_url_sk)
            img_name,img_url = self.down_image(img_url_sk)
            # goods_image_oss = ''.join([EndPoint,'/',oss_img_path,'/',goods_image_oss])
            # 下载至本地，上传至oss返回图片路径，图片路径添加进html，组合形成goods_body
            goods_desc_images.append('<p><img align="absmiddle" src="{}"></p>'.format(img_url))
        goods_desc_img = ''.join(goods_desc_images)
        item['goods_desc'] = goods_desc_body + goods_desc_img

        # 商品附图下载并上传至oss，返回相对路径

        goods_images_list = []
        images = response.xpath("//div[@class='thumbnail']//div[@class='tb-thumb-item ']/a/img/@mid").extract()
        for imgs_url_sk in images:
            imgs_url_sk = re.findall("(.*?jpg|.*?JPG|.*?PNG|.*?png)", imgs_url_sk)[0]
            # imgs_url_sk = re.findall('src="(.*?)"', imgs_url_sk)[0]
            if re.findall("(http)", imgs_url_sk):
                img_name, img_url = self.down_image(imgs_url_sk)

            else:
                imgs_url_sk = 'http:' + imgs_url_sk
                img_name, img_url = self.down_image(imgs_url_sk)

            if not goods_images_list:

                images = {"name": img_name,
                          "default": "1"}
            else:
                images = {"name": img_name,
                          "default": "0"}

            goods_images_list.append(images)
        item['goods_images'] = goods_images_list


        yield item

# ##################################################
# ##################################################

    # 图片下载至本地固定路径，返回图片文件名
    def down_image(self, url):
        datenow = time.strftime("%Y%m%d", time.localtime())
        ext = re.findall(r".*?(.jpg|.png|.JPG|.PNG)", url)[0]
        hashname = hashlib.md5(url.encode(encoding='UTF-8')).hexdigest()
        filename = datenow + 'zz' + hashname + ext

        image_name = '{}_'.format(store_id) + filename
        path = image_path + '/' + image_name

        # 测试时不下载图片，直接返回路径
        # return image_name,image_name

        if not os.path.exists(image_path):
            os.makedirs(image_path)
        if not os.path.exists(path):
            r = requests.get(url=url,
                             headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36', },
                             )
            code = r.status_code
            try:
                with open(path, "wb") as f:
                    f.write(r.content)
                print("爬取完成:{}".format(url))
                self.mylog.info(' INFO  |  {}  |  {}  |  {}'.format(image_name, code, url))
                oss_url_name = self.post_img_oss(image_name)
                return oss_url_name
            except:
                print("爬取失败:{}".format(url))
                self.mylog.info(' ERROR  |  {}  |  {}  '.format(code, url))
                return url
        else:
            print("文件已存在")
            self.mylog.info(' INFO  |  {}  |  {}  |  {}'.format(image_name, '000', url))
            oss_url_name = self.post_img_oss(image_name)
            return oss_url_name

    # 图片上传至oss，返回图片url
    def post_img_oss(self, image_name):
        try:
            # result = self.bucket.put_object_from_file(r"goods/1/{}".format(filename), image_path + '/' + filename)
            result = self.bucket.put_object_from_file(r"{}/{}".format(oss_img_path, image_name),image_path + '/' + image_name)  # (上传后文件名，当前地址）
            print('http status: {0}'.format(result.status))  # 打印上传的返回值 200成功
            jpg_url = self.bucket.sign_url('GET', r"{}/{}".format(oss_img_path, image_name), 10000)
            # jpg_url = self.bucket.sign_url('GET', r"goods/1/{}".format(filename), 10000)
            jpg_url = str(jpg_url).split("?")[0].replace("%2F", "/")
            print("post_oss_url:{}".format(jpg_url))
            # return image_name
            return image_name,jpg_url
        except:
            return image_name,""


