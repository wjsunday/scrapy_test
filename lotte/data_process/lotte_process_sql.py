#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import os
import pymysql
import time
import re
# from kafka import KafkaProducer
from settings import mysql_host, mysql_port, mysql_db_user, mysql_db_pwd, mysql_db_name, mysql_db_charset
from data_process.spec_info import spec_info
from data_process.mylog import MyLog
from settings import image_path

class DataProcess(object):
    def __init__(self):
        self.client = pymysql.connect(
            host=mysql_host,
            port=mysql_port,
            user=mysql_db_user,  # 使用自己的用户名
            passwd=mysql_db_pwd,  # 使用自己的密码
            db=mysql_db_name,  # 数据库名
            charset=mysql_db_charset
        )
        self.cur = self.client.cursor()
        self.mylog = MyLog()

        # self.producer = KafkaProducer(bootstrap_servers=['192.168.148.81:9092', '192.168.148.82:9092', '192.168.148.83:9092'])
        # self.topic = 'lotte'
        self.spec_info = spec_info
        self.spec_info = spec_info
        self.store_name = '韩国免税批发仓'
        self.store_id = '6'
        self.type_name = "韩国乐天"
        self.type_id = "8"
        self.transport_title = "拼拼侠通用运费模板"
        self.transport_id = "11"

    def data_process(self,item):
        now_time = int(time.time())

        price = item['goods_price']

        goods_price = round(price * 0.8)  # 拼拼侠售价
        goods_marketprice = price  # 拼拼侠市场价

        goods_brand = item['goods_brand']
        goods_name = item['goods_name']
        goods_image = item['goods_image']
        goods_jingle = item['goods_jingle']
        goods_desc = item['goods_desc']
        goods_url = item['goods_url']
        spec_id_3 = item['spec_id_3']
        goods_storage = item['goods_storage']
        goods_costprice = item['goods_costprice']
        goods_attr = item['goods_attr']
        goods_images = item['goods_images']
        shop_info = item['shop_info']
        goods_salenum = item['goods_salenum']
        goods_serial = item['goods_serial']
        shop_name = item['shop_name']
        shop_range = item['shop_range']
        shop_ali = item['shop_ali']
        shop_mobile = item['shop_mobile']
        shop_address = item['shop_address']
        shop_wechart = item['shop_wechart']
        shop_qq = item['shop_qq']
        goods_param = item['goods_param']
        shop_goods_num = item['shop_goods_num']

        # 入库
        # 判断商品是否存在
        sql_exsits = "select goods_commonid from mall_goods_common where goods_url='%s'" % (goods_url)
        self.cur.execute(sql_exsits)
        ret = self.cur.fetchone()
        if ret:
            pass
        else:
            # 增加
            # 三级分类判断
            goods_image = self.down_img(goods_image)

            # 处理商品分类 没有添加，有使用
            gc_select = "select * from mall_goods_class where gc_name='%s'"
            gc_insert = 'insert into mall_goods_class (gc_name,type_id,type_name,gc_parent_id,commis_rate,gc_sort,gc_virtual,gc_title,gc_keywords,gc_description)' \
                        'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

            sql_gc1 = gc_select % (spec_info[spec_id_3][0])
            self.cur.execute(sql_gc1)
            gc1_info = self.cur.fetchone()
            if gc1_info:
                gc1_id = gc1_info[0]
            else:
                lisgc1 = (spec_info[spec_id_3][0], '8', '韩国乐天', '0', '0', '0', '0', '', '', '')
                self.cur.execute(gc_insert, lisgc1)
                gc1_id = int(self.client.insert_id())

            sql_gc2 = gc_select % (spec_info[spec_id_3][1])
            self.cur.execute(sql_gc2)
            gc2_info = self.cur.fetchone()
            if gc2_info:
                gc2_id = gc2_info[0]
            else:
                lisgc2 = (spec_info[spec_id_3][1], '8', '韩国乐天', gc1_id, '0', '0', '0', '', '', '')
                self.cur.execute(gc_insert, lisgc2)
                gc2_id = int(self.client.insert_id())

            sql_gc3 = gc_select % (spec_info[spec_id_3][2])
            self.cur.execute(sql_gc3)
            gc3_info = self.cur.fetchone()
            if gc3_info:
                gc3_id = gc3_info[0]
            else:
                lisgc3 = (spec_info[spec_id_3][2], '8', '韩国乐天', gc2_id, '0', '0', '0', '', '', '')
                self.cur.execute(gc_insert, lisgc3)
                gc3_id = int(self.client.insert_id())

            # 商品品牌

            brand_select = "select * from mall_brand where brand_name='%s'"
            brand_insert = 'insert into mall_brand (brand_name,brand_initial,brand_class,brand_pic,brand_sort,brand_recommend,store_id,brand_apply,class_id,show_type)' \
                           'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            sql_brand = brand_select % (goods_brand)
            self.cur.execute(sql_brand)
            brand_info = self.cur.fetchone()
            if brand_info:
                brand_id = brand_info[0]
            else:
                lisbrand = (goods_brand, 'l', '韩国乐天', '', '0', '0', '4', '1', gc3_id, '1')
                self.cur.execute(brand_insert, lisbrand)
                brand_id = int(self.client.insert_id())

            # 添加商品
            sql_common = 'insert into mall_goods_common' \
                         '(goods_name,goods_jingle,gc_id,gc_id_1,gc_id_2,gc_id_3,gc_name,store_id,store_name,spec_name,spec_value,brand_id,brand_name,type_id,goods_image,goods_attr,goods_body,mobile_body,goods_state,goods_stateremark,goods_verify,goods_verifyremark,goods_lock,goods_addtime,goods_selltime,goods_specname,goods_price,goods_tradeprice,goods_marketprice,goods_costprice,goods_discount,goods_serial,goods_storage_alarm,transport_id,transport_title,goods_commend,goods_freight,goods_vat,areaid_1,areaid_2,goods_stcids,is_virtual,virtual_invalid_refund,is_fcode,is_appoint,appoint_satedate,is_presell,presell_deliverdate,is_own_shop,is_support_voucher,is_vip_buy,commission_ratio,goods_url,goods_jingle_other,shop_info,goods_image_old) ' \
                         'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            lis_common = (goods_name, goods_jingle, gc3_id, gc1_id, gc2_id, gc3_id, spec_info[spec_id_3][2], self.store_id, self.store_name, 'N;','N;', brand_id, goods_brand, self.type_id, goods_image, 'N;', goods_desc, goods_desc, '1', '', '1', '', '0',now_time, now_time, 'N;', goods_price, '0', goods_marketprice, '0', '100', 'N;', '1', '11', '拼拼侠通用运费模板', '0','0', '0', '1', '1', '', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', goods_url, '', shop_info,goods_image)
            self.cur.execute(sql_common, lis_common)
            common_id = int(self.client.insert_id())
            print('入库common_id：{}'.format(common_id))
            # print(common_id)

            # 添加sku
            if common_id:
                sql_goods = 'insert into mall_goods(goods_commonid,goods_name,goods_jingle,store_id,store_name,gc_id,gc_id_1,gc_id_2,gc_id_3,brand_id,goods_price,goods_tradeprice,goods_promotion_price,goods_promotion_type,goods_marketprice,goods_serial,goods_storage_alarm,goods_click,goods_salenum,goods_collect,goods_spec,goods_storage,goods_image,goods_state,goods_verify,goods_addtime,goods_edittime,areaid_1,areaid_2,color_id,transport_id,goods_weight,goods_freight,goods_vat,goods_commend,goods_stcids,is_virtual,virtual_indate,virtual_limit,virtual_invalid_refund,is_fcode,is_appoint,is_presell,have_gift,is_own_shop,distribution_price_1,distribution_price_2,distribution_price_3,commission_percent,goods_jingle_other)' \
                            'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                lis_goods = (common_id, goods_name, goods_jingle, self.store_id, self.store_name, gc3_id, gc1_id, gc2_id, gc3_id, brand_id,goods_price, '0', '0', '0', goods_marketprice, '', '1', '1', '0', '1', '', '100', goods_image, '1', '1',now_time, now_time, '1', '1', '0', '11', '0', '0', '0', '0', '', '0', '0', '0', '0', '0', '0', '0', '0','1', '0', '0', '0', '0', '')
                self.cur.execute(sql_goods, lis_goods)
                goods_id = int(self.client.insert_id())
                print('入库goods_id：{}'.format(goods_id))
            self.client.commit()

        return item

    def down_img(self,url):
        import requests
        datenow = time.strftime("%Y%m%d", time.localtime())
        arr = os.path.splitext(url)
        ext = re.findall(r".*?(.jpg|.png|.JPG|.PNG|.jpeg)", url)[0]
        hashname = hashlib.md5(url.encode(encoding='UTF-8')).hexdigest()
        filename = datenow + 'zz' + hashname + ext
        root = image_path
        path = root + '/6_' + filename
        try:
            if not os.path.exists(root):
                os.makedirs(root)
            if not os.path.exists(path):
                r = requests.get(url, timeout=20)
                code = r.status_code
                try:
                    with open(path, "wb") as f:
                        f.write(r.content)
                    print("爬取完成:{}".format(url))
                    self.mylog.info(' IMG  |  {}  |  {}  |  {}'.format(('1_' + filename).ljust(70), code, url))
                    return '6_' + filename
                except:
                    print("爬取失败:{}".format(url))
                    self.mylog.error(' IMG  |  {}  |  {}'.format(code, url))
                    return url
            else:
                print("文件已存在")
                self.mylog.info(' IMG  |  {}  |  {}  |  {}'.format(('1_' + filename).ljust(70), "000", url))
                return '6_' + filename
        except Exception as e:
            print("爬取失败:" + str(e))
            return url