# -*- coding: utf-8 -*-
import pymysql
import redis
import time
import phpserialize
import itertools
import os
import hashlib
from soukuangoods.settings import mysql_host,mysql_port,mysql_db_user,mysql_db_pwd,mysql_db_name,mysql_db_charset,redis_host,redis_port,redis_pwd,redis_name
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SoukuangoodsPipeline(object):
    brand_info = dict()
    cat_info = dict()
    img_url = ""

    def __init__(self):
        self.client = pymysql.connect(
            host=mysql_host,
            port=mysql_port,
            user=mysql_db_user,  #使用自己的用户名
            passwd=mysql_db_pwd,  # 使用自己的密码
            db=mysql_db_name,  # 数据库名
            charset=mysql_db_charset
        )
        self.r = redis.Redis(host=redis_host,port=redis_port,db=redis_name,password=redis_pwd)
        self.cur = self.client.cursor()
        self.brand_info = {'广州女装批发':'6'}
        self.cat_info = {
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000035&merge=1':{'gc_id':'T恤','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'T恤'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000018&merge=1':{'gc_id':'寸衫','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'寸衫'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000129&merge=1':{'gc_id':'短外套','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'短外套'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000025&merge=1':{'gc_id':'休闲运动','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'休闲运动'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000038&merge=1':{'gc_id':'毛织针衫','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'毛织针衫'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000071&merge=1':{'gc_id':'风衣','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'风衣'},
            'https://www.vvic.com/gz/search/index.html?q=%E6%83%85%E4%BE%A3%E8%A3%85&merge=1&merge=1':{'gc_id':'情侣装','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'情侣装'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000017&merge=1':{'gc_id':'毛衣','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'毛衣'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000055&merge=1':{'gc_id':'旗袍','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'旗袍'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000067&merge=1':{'gc_id':'西装','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'西装'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000389&merge=1':{'gc_id':'时尚套装','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'时尚套装'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000019&merge=1':{'gc_id':'蕾丝雪纺','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'蕾丝雪纺'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000006&merge=1':{'gc_id':'大码连衣裙','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'大码连衣裙'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000364&merge=1':{'gc_id':'背心吊带','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'背心吊带'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000068&merge=1':{'gc_id':'卫衣绒衫','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'卫衣绒衫'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000041&merge=1':{'gc_id':'中老年连衣裙','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'中老年连衣裙'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000176&merge=1':{'gc_id':'马甲','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'马甲'},
            'https://www.vvic.com/gz/list/index.html?merge=1&pid=9#J_main&merge=1':{'gc_id':'孕妇装','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'孕妇装'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000069&merge=1':{'gc_id':'羽绒服','gc_id_1':'女装','gc_id_2':'上装/外套','gc_id_3':'羽绒服'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000106&merge=1':{'gc_id':'连衣裙','gc_id_1':'女装','gc_id_2':'裙装','gc_id_3':'连衣裙'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000001&merge=1':{'gc_id':'半身裙','gc_id_1':'女装','gc_id_2':'裙装','gc_id_3':'半身裙'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000022&merge=1':{'gc_id':'职业女裙套装','gc_id_1':'女装','gc_id_2':'裙装','gc_id_3':'职业女裙套装'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000021&merge=1':{'gc_id':'牛仔裤','gc_id_1':'女装','gc_id_2':'裤装','gc_id_3':'牛仔裤'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000020&merge=1':{'gc_id':'休闲裤','gc_id_1':'女装','gc_id_2':'裤装','gc_id_3':'休闲裤'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000057&merge=1':{'gc_id':'打底裤','gc_id_1':'女装','gc_id_2':'裤装','gc_id_3':'打底裤'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000291&merge=1':{'gc_id':'西装裤/正装裤','gc_id_1':'女装','gc_id_2':'裤装','gc_id_3':'西装裤/正装裤'},
            'https://www.vvic.com/gz/list/index.html?pid=1&vcid=20000023&merge=1':{'gc_id':'职业女裤套装','gc_id_1':'女装','gc_id_2':'裤装','gc_id_3':'职业女裤套装'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000078&merge=1':{'gc_id':'卫衣','gc_id_1':'男装','gc_id_2':'上装/外套','gc_id_3':'卫衣'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000034&merge=1':{'gc_id':'针织衫','gc_id_1':'男装','gc_id_2':'上装/外套','gc_id_3':'针织衫'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000077&merge=1':{'gc_id':'大码卫衣','gc_id_1':'男装','gc_id_2':'上装/外套','gc_id_3':'大码卫衣'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000116&merge=1':{'gc_id':'马甲','gc_id_1':'男装','gc_id_2':'上装/外套','gc_id_3':'马甲'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000117&merge=1':{'gc_id':'背心','gc_id_1':'男装','gc_id_2':'上装/外套','gc_id_3':'背心'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000076&merge=1':{'gc_id':'夹克','gc_id_1':'男装','gc_id_2':'上装/外套','gc_id_3':'夹克'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000424&merge=1':{'gc_id':'运动套装','gc_id_1':'男装','gc_id_2':'上装/外套','gc_id_3':'运动套装'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000120&merge=1':{'gc_id':'风衣','gc_id_1':'男装','gc_id_2':'上装/外套','gc_id_3':'风衣'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000125&merge=1':{'gc_id':'棉衣','gc_id_1':'男装','gc_id_2':'上装/外套','gc_id_3':'棉衣'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000421&merge=1':{'gc_id':'其他套装','gc_id_1':'男装','gc_id_2':'上装/外套','gc_id_3':'其他套装'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000031&merge=1':{'gc_id':'T恤','gc_id_1':'男装','gc_id_2':'寸衫/T恤','gc_id_3':'T恤'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000109&merge=1':{'gc_id':'寸衫','gc_id_1':'男装','gc_id_2':'寸衫/T恤','gc_id_3':'寸衫'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000030&merge=1':{'gc_id':'大码T恤','gc_id_1':'男装','gc_id_2':'寸衫/T恤','gc_id_3':'大码T恤'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000090&merge=1':{'gc_id':'Polo衫','gc_id_1':'男装','gc_id_2':'寸衫/T恤','gc_id_3':'Polo衫'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000029&merge=1':{'gc_id':'中老年人T恤','gc_id_1':'男装','gc_id_2':'寸衫/T恤','gc_id_3':'中老年人T恤'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000108&merge=1':{'gc_id':'大码寸衫','gc_id_1':'男装','gc_id_2':'寸衫/T恤','gc_id_3':'大码寸衫'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000016&merge=1':{'gc_id':'休闲裤','gc_id_1':'男装','gc_id_2':'裤装','gc_id_3':'休闲裤'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000081&merge=1':{'gc_id':'牛仔裤','gc_id_1':'男装','gc_id_2':'裤装','gc_id_3':'牛仔裤'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000015&merge=1':{'gc_id':'大码休闲裤','gc_id_1':'男装','gc_id_2':'裤装','gc_id_3':'大码休闲裤'},
            'https://www.vvic.com/gz/list/index.html?pid=2&vcid=20000080&merge=1':{'gc_id':'大码牛仔裤','gc_id_1':'男装','gc_id_2':'裤装','gc_id_3':'大码牛仔裤'},
        }

    def process_item(self, item, spider):
        now_time = int(time.time())
        goods_url = item['goods_url']
        goods_name = item['goods_name'].replace("'","\\'")
        goods_jingle = item['goods_jingle'].replace("'","\\'")
        goods_desc = item['goods_desc'].replace("'","\\'").replace("\n","")
        goods_marketprice = item['goods_price'] * 1.2
        rate = round(item['goods_price']/goods_marketprice,2)*10
        goods_image = 'https:'+item['goods_image']
        self.img_url = goods_image
        shop_info = item['shop_info']
        goods_serial = item['goods_serial'].replace("\n","").replace(' ','')
        if not item['shop_name'] is None:
            shop_name = item['shop_name'].replace("\n","").replace(' ','')
        else:
            shop_name = ''
        if not item['shop_range'] is None:
            shop_range = item['shop_range']
        else:
            shop_range = '0'
        if not item['shop_ali'] is None:
            shop_ali = item['shop_ali']
        else:
            shop_ali = ''
        if not item['shop_mobile'] is None:
            shop_mobile = item['shop_mobile']
        else:
            shop_mobile = ''
        if not item['shop_address'] is None:
            shop_address = item['shop_address'].replace(' ','')
        else:
            shop_address = ''
        if not item['goods_salenum'] is None:
            goods_salenum = item['goods_salenum']
        else:
            goods_salenum = '0'
        #判断商品是否存在
        sql_exsits = "select goods_commonid,goods_image,goods_image_old from mall_goods_common where goods_url='%s'" % (goods_url)
        self.cur.execute(sql_exsits)
        ret = self.cur.fetchone()
        if not ret is None:
            #处理图片问题
            root = "/image/1/"
            path = root +ret[1]
            #当原始图片不存在时候直接下载
            curPath = os.path.abspath(os.path.dirname(__file__))+path
            if not os.path.exists(curPath):
                goods_image = self.down_img()
            else:
                #当存在的时候
                if self.img_url != ret[2]:
                    os.remove(path)
                    goods_image = self.down_img()
                else:
                    goods_image = ret[2]

            #更新
            sqlupdatecommon = "UPDATE mall_goods_common SET goods_name='%s',goods_image='%s',goods_price='%s',goods_jingle_other='%s',goods_body='%s',mobile_body='%s',goods_marketprice='%s',goods_costprice='%s',shop_info='%s',goods_image_old='%s', goods_serial='%s' WHERE goods_commonid = '%s'" % (goods_name,goods_image,item['goods_price'],goods_jingle,goods_desc,goods_desc,goods_marketprice,item['goods_costprice'],shop_info,self.img_url,goods_serial,ret[0])
            self.cur.execute(sqlupdatecommon)
            #更新店铺信息
            self.oper_shop(shop_name,shop_range,shop_ali,ret[0],shop_mobile,shop_address)
            #更新goods
            sqlgoods = "SELECT goods_id FROM mall_goods WHERE goods_commonid='%s'" % (ret[0])
            self.cur.execute(sqlgoods)
            results = self.cur.fetchall()
            for row in results:
                sqlupdategoods = "UPDATE mall_goods SET goods_name='%s',goods_image='%s',goods_storage='%s',goods_price='%s',goods_jingle_other='%s',goods_edittime='%s',goods_tradeprice='%s',goods_promotion_price='%s',goods_marketprice='%s',goods_salenum='%s' WHERE goods_id=%s" % (goods_name,goods_image,item['goods_storage'],item['goods_price'],goods_jingle,now_time,item['goods_price'],item['goods_price'],goods_marketprice,goods_salenum,row[0])
                self.cur.execute(sqlupdategoods)
                common_key = str(ret[0])
                goods_key = str(row[0])
                #更新mall_p_xianshi_goods
                sql_xianshi = "UPDATE mall_p_xianshi_goods SET goods_image='%s',goods_price='%s',market_price='%s',xianshi_price='%s',rate='%s' WHERE goods_id = %s" % (goods_image,item['goods_price'],goods_marketprice,item['goods_price'],rate,row[0])
                self.cur.execute(sql_xianshi)
                self.r.delete('ppxMall_goods_common'+common_key)
                self.r.delete('ppxMall_goods'+goods_key)
                self.r.delete('ppxMall_goods_xianshi'+goods_key)
                goods_key_tmp = 'ppxMall_goods_image'+goods_key+'|*'
                if len(self.r.keys(pattern=goods_key_tmp)):
                    self.r.delete(*self.r.keys(pattern=goods_key_tmp))
            self.client.commit()
        else:
            #新增
            if item['gc_name'] in self.cat_info:
                #爬取图片
                goods_image = self.down_img()
                #处理商品分类 没有添加，有使用
                gc_select = "select * from mall_goods_class where gc_name='%s'"
                gc_insert = 'insert into mall_goods_class (gc_name,type_id,type_name,gc_parent_id,commis_rate,gc_sort,gc_virtual,gc_title,gc_keywords,gc_description)' \
                            'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

                sql_gc1 = gc_select % (self.cat_info[item['gc_name']]['gc_id_1'])
                self.cur.execute(sql_gc1)
                gc1_info = self.cur.fetchone()
                if not gc1_info is None:
                    gc1_id = gc1_info[0]
                else:
                    lisgc1 = (self.cat_info[item['gc_name']]['gc_id_1'],6,'服装',0,0,0,0,'','','')
                    self.cur.execute(gc_insert,lisgc1)
                    gc1_id = int(self.client.insert_id())

                sql_gc2 = gc_select % (self.cat_info[item['gc_name']]['gc_id_2'])
                self.cur.execute(sql_gc2)
                gc2_info = self.cur.fetchone()
                if not gc2_info is None:
                    gc2_id = gc2_info[0]
                else:
                    lisgc2 = (self.cat_info[item['gc_name']]['gc_id_2'],6,'服装',gc1_id,0,0,0,'','','')
                    self.cur.execute(gc_insert,lisgc2)
                    gc2_id = int(self.client.insert_id())

                sql_gc3 = gc_select % (self.cat_info[item['gc_name']]['gc_id_3'])
                self.cur.execute(sql_gc3)
                gc3_info = self.cur.fetchone()
                if not gc3_info is None:
                    gc3_id = gc3_info[0]
                else:
                    lisgc3 = (self.cat_info[item['gc_name']]['gc_id_3'],6,'服装',gc2_id,0,0,0,'','','')
                    self.cur.execute(gc_insert,lisgc3)
                    gc3_id = int(self.client.insert_id())

                #添加属性，规格
                ms_select = "select * from mall_spec where sp_name='%s' and class_id='%s'"
                ms_insert = 'insert into mall_spec (sp_name,sp_sort,class_id,class_name) values (%s,%s,%s,%s)'
                msv_select = "select * from mall_spec_value where sp_value_name='%s' and sp_id='%s' and gc_id='%s'"
                msv_insert = 'insert into mall_spec_value (sp_value_name,sp_id,gc_id,store_id,sp_value_color,sp_value_sort) values (%s,%s,%s,%s,%s,%s)'
                mts_select = "select * from mall_type_spec where type_id='%s' and sp_id='%s'"
                mts_insert = 'insert into mall_type_spec (type_id,sp_id) values (%s,%s)'
                sp_name = dict()
                sp_val = dict()
                sp_val_list = dict()
                for i_item in item['goods_attr']:
                    if i_item is None:
                        continue
                    sql_ms = ms_select % (i_item, gc3_id)
                    self.cur.execute(sql_ms)
                    ms_info = self.cur.fetchone()
                    if not ms_info is None:
                        sp_id = ms_info[0]
                    else:
                        lisms = (i_item,0,gc3_id,self.cat_info[item['gc_name']]['gc_id_3'])
                        self.cur.execute(ms_insert,lisms)
                        sp_id = int(self.client.insert_id())
                    sp_name[sp_id] = i_item
                    #添加类型规格关系表
                    sql_mts = mts_select % ('6',sp_id)
                    self.cur.execute(sql_mts)
                    mts_info = self.cur.fetchone()
                    if mts_info is None:
                        lismts = ('6',sp_id)
                        self.cur.execute(mts_insert,lismts)
                    #添加规格的值
                    for c_item in item['goods_attr'][i_item]:
                        sql_msv = msv_select % (c_item, sp_id, gc3_id)
                        self.cur.execute(sql_msv)
                        msv_info = self.cur.fetchone()
                        if not msv_info is None:
                            sp_value_id = msv_info[0]
                        else:
                            lismsv = (c_item,sp_id,gc3_id,1,'',0)
                            self.cur.execute(msv_insert,lismsv)
                            sp_value_id = int(self.client.insert_id())
                        if sp_id in sp_val:
                            sp_val[sp_id].update({sp_value_id:c_item})
                            sp_val_list[sp_value_id] = c_item
                        else:
                            sp_val[sp_id] = {sp_value_id:c_item}
                            sp_val_list[sp_value_id] = c_item

                #开始添加商品了
                #mall_goods_common
                sp_name_tmp = phpserialize.dumps(sp_name).decode('utf-8')
                sp_val_tmp = phpserialize.dumps(sp_val).decode('utf-8')
                sqlcommon = 'insert into mall_goods_common' \
                        '(goods_name,goods_image,goods_price,goods_jingle,mobile_body,gc_id,gc_id_1,gc_id_2,gc_id_3,gc_name,store_id,store_name,spec_name,spec_value,brand_id,brand_name,goods_attr,goods_body,goods_state,goods_verify,goods_addtime,goods_selltime,goods_specname,goods_marketprice,goods_costprice,goods_discount,goods_serial,goods_storage_alarm,areaid_1,areaid_2,appoint_satedate,presell_deliverdate,goods_url,goods_jingle_other,shop_info,goods_image_old) ' \
                        'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                liscommon = (goods_name,goods_image,item['goods_price'],'',goods_desc,gc3_id,gc1_id,gc2_id,gc3_id,self.cat_info[item['gc_name']]['gc_id_3'],'1','拼拼侠',sp_name_tmp,sp_val_tmp,self.brand_info[item['goods_brand']],item['goods_brand'],'N;',goods_desc,'1','1',now_time,now_time,item['goods_brand'],goods_marketprice,item['goods_costprice'],'100',goods_serial,'1','1','1',now_time,now_time,item['goods_url'],goods_jingle,shop_info,self.img_url)
                self.cur.execute(sqlcommon,liscommon)
                common_id = int(self.client.insert_id())
                if common_id:
                    #更新店铺信息
                    self.oper_shop(shop_name,shop_range,shop_ali,common_id,shop_mobile,shop_address)

                    #处理商品相册
                    if not item['goods_images'] is None:
                        mgi_insert = 'insert into mall_goods_images (goods_commonid,store_id,color_id,goods_image,goods_image_sort,is_default) values (%s,%s,%s,%s,%s,%s)'
                        for goods_images_v in item['goods_images']:
                            goods_images_v = 'https:'+goods_images_v
                            goods_images_v = self.down_imgs(goods_images_v)
                            lismgi = (common_id,1,0,goods_images_v,0,0)
                            self.cur.execute(mgi_insert,lismgi)

                    sp_tmp = dict()
                    i = 1
                    for sp_val_item in sp_val:
                        sp_tmp[i] = sp_val[sp_val_item]
                        i += 1
                    for x in itertools.product(sp_tmp[1],sp_tmp[2]):
                        goods_sku_name = goods_name
                        sp_value = dict()
                        for x_i in x:
                            sp_value[x_i] = sp_val_list[x_i]
                            goods_sku_name += ' ' + sp_val_list[x_i]
                        sp_value_serilize = phpserialize.dumps(sp_value).decode('utf-8')
                        #mall_goods
                        sqlgoods = 'insert into mall_goods(goods_commonid,goods_name,goods_jingle,store_id,store_name,gc_id,gc_id_1,gc_id_2,gc_id_3,brand_id,goods_price,goods_tradeprice,goods_promotion_price,goods_promotion_type,goods_marketprice,goods_serial,goods_storage_alarm,goods_click,goods_salenum,goods_collect,goods_spec,goods_storage,goods_image,goods_state,goods_verify,goods_addtime,goods_edittime,areaid_1,areaid_2,color_id,transport_id,goods_freight,goods_vat,goods_commend,goods_stcids,evaluation_good_star,evaluation_count,is_virtual,virtual_indate,virtual_limit,virtual_invalid_refund,is_fcode,is_appoint,is_presell,have_gift,is_own_shop,distribution_price_1,distribution_price_2,distribution_price_3,commission_percent,goods_jingle_other)' \
                                   'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                        lisgoods = (common_id,goods_sku_name,'','1','拼拼侠',gc3_id,gc1_id,gc2_id,gc3_id,self.brand_info[item['goods_brand']],item['goods_price'],item['goods_price'],item['goods_price'],'0',goods_marketprice,'','1','1',goods_salenum,'1',sp_value_serilize,item['goods_storage'],goods_image,'1','1',now_time,now_time,'1','1','0','0','0','0','0','1','5','0','0','0','0','0','0','0','0','0','0','0','0','0','0',goods_jingle)
                        self.cur.execute(sqlgoods,lisgoods)
                    self.client.commit()

        return item

    def down_img(self):
        import requests
        url = self.img_url
        datenow = time.strftime("%Y%m%d", time.localtime())
        arr = os.path.splitext(self.img_url)
        ext = arr[len(arr) - 1]
        hashname = hashlib.md5(self.img_url.encode(encoding='UTF-8')).hexdigest()
        filename = datenow+'zz'+hashname+ext
        root = "./image/1/"
        path = root + '1_'+filename
        try:
            if not os.path.exists(root):
                os.makedirs(root)
            if not os.path.exists(path):
                r = requests.get(url)
                r.raise_for_status()
                #使用with语句可以不用自己手动关闭已经打开的文件流
                with open(path,"wb") as f: #开始写文件，wb代表写二进制文件
                    f.write(r.content)
                print("爬取完成")
                return '1_'+filename
            else:
                print("文件已存在")
                return '1_'+filename
        except Exception as e:
            print("爬取失败:"+str(e))
            return self.img_url

    def down_imgs(self,goods_images_v):
        import requests
        url = goods_images_v
        datenow = time.strftime("%Y%m%d", time.localtime())
        arr = os.path.splitext(goods_images_v)
        ext = arr[len(arr) - 1]
        hashname = hashlib.md5(goods_images_v.encode(encoding='UTF-8')).hexdigest()
        filename = datenow+'zz'+hashname+ext
        root = "./image/1/"
        path = root + '1_'+filename
        try:
            if not os.path.exists(root):
                os.makedirs(root)
            if not os.path.exists(path):
                r = requests.get(url)
                r.raise_for_status()
                #使用with语句可以不用自己手动关闭已经打开的文件流
                with open(path,"wb") as f: #开始写文件，wb代表写二进制文件
                    f.write(r.content)
                print("爬取完成")
                return '1_'+filename
            else:
                print("文件已存在")
                return '1_'+filename
        except Exception as e:
            print("爬取失败:"+str(e))
            return goods_images_v

    def oper_shop(self,shop_name,shop_range,shop_ali,common_id,shop_mobile,shop_address):
        ms_select = "select * from mall_shop where goods_commonid='%s'"
        ms_insert = 'insert into mall_shop (shop_name,shop_range,shop_ali,shop_mobile,shop_wechat,shop_qq,shop_product,shop_address,goods_commonid) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        sql_ms = ms_select % (common_id)
        self.cur.execute(sql_ms)
        ms_info = self.cur.fetchone()
        if not ms_info is None:
            sqlupdategoods = "UPDATE mall_shop SET shop_name='%s',shop_range='%s',shop_ali='%s',shop_mobile='%s',shop_address='%s' WHERE shop_id=%s" % (shop_name,shop_range,shop_ali,shop_mobile,shop_address,ms_info[0])
            self.cur.execute(sqlupdategoods)
            sp_id = ms_info[0]
        else:
            lisms = (shop_name,shop_range,shop_ali,shop_mobile,'','','',shop_address,common_id)
            self.cur.execute(ms_insert,lisms)
            sp_id = int(self.client.insert_id())

        return sp_id


