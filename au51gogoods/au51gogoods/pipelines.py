# -*- coding: utf-8 -*-
import pymysql
import redis
import time
from au51gogoods.settings import mysql_host,mysql_port,mysql_db_user,mysql_db_pwd,mysql_db_name,mysql_db_charset,redis_host,redis_port,redis_pwd,redis_name
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Au51GogoodsPipeline(object):
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
        self.brand_info = {'澳新':'5'}
        self.cat_info = {
            '彩妆':{'gc_id':'16','gc_id_1':'1','gc_id_2':'16','gc_id_3':'0'},
            '护肤':{'gc_id':'55','gc_id_1':'1','gc_id_2':'55','gc_id_3':'0'},
            '沐浴清洁':{'gc_id':'56','gc_id_1':'1','gc_id_2':'56','gc_id_3':'0'},
            '防晒':{'gc_id':'57','gc_id_1':'1','gc_id_2':'57','gc_id_3':'0'},
            '洗发护发':{'gc_id':'58','gc_id_1':'1','gc_id_2':'58','gc_id_3':'0'},
            '丰胸减肥':{'gc_id':'59','gc_id_1':'1','gc_id_2':'59','gc_id_3':'0'},
            '女性保健':{'gc_id':'60','gc_id_1':'4','gc_id_2':'60','gc_id_3':'0'},
            '男性保健':{'gc_id':'61','gc_id_1':'4','gc_id_2':'61','gc_id_3':'0'},
            '老年保健':{'gc_id':'62','gc_id_1':'4','gc_id_2':'62','gc_id_3':'0'},
            '排毒瘦身':{'gc_id':'63','gc_id_1':'4','gc_id_2':'63','gc_id_3':'0'},
            '鱼油':{'gc_id':'65','gc_id_1':'4','gc_id_2':'64','gc_id_3':'65'},
            '矿物质':{'gc_id':'66','gc_id_1':'4','gc_id_2':'64','gc_id_3':'66'},
            '维生素':{'gc_id':'67','gc_id_1':'4','gc_id_2':'64','gc_id_3':'67'},
            '蜂产品':{'gc_id':'68','gc_id_1':'4','gc_id_2':'64','gc_id_3':'68'},
            '益生菌':{'gc_id':'69','gc_id_1':'4','gc_id_2':'64','gc_id_3':'69'},
            '蛋白粉膳食纤维':{'gc_id':'70','gc_id_1':'4','gc_id_2':'64','gc_id_3':'70'},
            '护眼':{'gc_id':'71','gc_id_1':'4','gc_id_2':'64','gc_id_3':'71'},
            '基础保健其他':{'gc_id':'72','gc_id_1':'4','gc_id_2':'64','gc_id_3':'72'},
            '1段':{'gc_id':'79','gc_id_1':'73','gc_id_2':'74','gc_id_3':'79'},
            '2段':{'gc_id':'80','gc_id_1':'73','gc_id_2':'74','gc_id_3':'80'},
            '3段':{'gc_id':'81','gc_id_1':'73','gc_id_2':'74','gc_id_3':'81'},
            '4段':{'gc_id':'82','gc_id_1':'73','gc_id_2':'74','gc_id_3':'82'},
            '米粉':{'gc_id':'83','gc_id_1':'73','gc_id_2':'75','gc_id_3':'83'},
            '洗护用品':{'gc_id':'84','gc_id_1':'73','gc_id_2':'76','gc_id_3':'84'},
            '牙膏牙刷':{'gc_id':'85','gc_id_1':'73','gc_id_2':'76','gc_id_3':'85'},
            '奶瓶奶嘴':{'gc_id':'86','gc_id_1':'73','gc_id_2':'76','gc_id_3':'86'},
            '驱蚊防晒':{'gc_id':'87','gc_id_1':'73','gc_id_2':'76','gc_id_3':'87'},
            '婴幼儿鱼油':{'gc_id':'88','gc_id_1':'73','gc_id_2':'77','gc_id_3':'88'},
            'DHA':{'gc_id':'89','gc_id_1':'73','gc_id_2':'77','gc_id_3':'89'},
            '蜂产品':{'gc_id':'90','gc_id_1':'73','gc_id_2':'77','gc_id_3':'90'},
            '感冒止咳':{'gc_id':'91','gc_id_1':'73','gc_id_2':'77','gc_id_3':'91'},
            '婴幼儿维生素':{'gc_id':'92','gc_id_1':'73','gc_id_2':'77','gc_id_3':'92'},
            '婴幼儿矿物质':{'gc_id':'93','gc_id_1':'73','gc_id_2':'77','gc_id_3':'93'},
            '婴幼儿益生菌':{'gc_id':'94','gc_id_1':'73','gc_id_2':'77','gc_id_3':'94'},
            '孕妇产品':{'gc_id':'95','gc_id_1':'73','gc_id_2':'78','gc_id_3':'95'},
            '孕妇奶粉':{'gc_id':'96','gc_id_1':'73','gc_id_2':'78','gc_id_3':'96'},
            '口腔护理':{'gc_id':'98','gc_id_1':'97','gc_id_2':'98','gc_id_3':'0'},
            '个人护理':{'gc_id':'99','gc_id_1':'97','gc_id_2':'99','gc_id_3':'0'},
            '家居生活其他':{'gc_id':'100','gc_id_1':'97','gc_id_2':'100','gc_id_3':'0'},
            '蜂蜜':{'gc_id':'102','gc_id_1':'101','gc_id_2':'102','gc_id_3':'0'},
            '营养奶粉':{'gc_id':'103','gc_id_1':'101','gc_id_2':'103','gc_id_3':'0'},
            '奶制品':{'gc_id':'104','gc_id_1':'101','gc_id_2':'104','gc_id_3':'0'},
            '零食':{'gc_id':'105','gc_id_1':'101','gc_id_2':'105','gc_id_3':'0'},
            '麦片早餐':{'gc_id':'106','gc_id_1':'101','gc_id_2':'106','gc_id_3':'0'},
            '健康美食其他':{'gc_id':'107','gc_id_1':'101','gc_id_2':'107','gc_id_3':'0'},
            '围巾':{'gc_id':'109','gc_id_1':'108','gc_id_2':'109','gc_id_3':'0'},
            'Jellycat':{'gc_id':'110','gc_id_1':'108','gc_id_2':'110','gc_id_3':'0'},
        }

    def process_item(self, item, spider):
        now_time = int(time.time())
        goods_url = item['goods_url']
        goods_name = item['goods_name'].replace("'","\\'")
        goods_jingle = item['goods_jingle'].replace("'","\\'")
        goods_desc = item['goods_desc'].replace("'","\\'").replace("//img","https://img")
        goods_weight = float(item['goods_weight']) * 1000
        goods_marketprice = item['goods_price'] * 1.2
        rate = round(item['goods_price']/goods_marketprice,2)*10
        goods_image = 'https:'+item['goods_image']
        self.img_url = goods_image
        goods_image = self.down_img()
        shop_info = ''
        #判断商品是否存在
        sql_exsits = "select goods_commonid from mall_goods_common where goods_url='%s'" % (goods_url)
        self.cur.execute(sql_exsits)
        ret = self.cur.fetchone()
        if not ret is None:
            #更新
            sqlupdatecommon = "UPDATE mall_goods_common SET goods_name='%s',goods_image='%s',goods_price='%s',goods_jingle_other='%s',goods_body='%s',mobile_body='%s',goods_marketprice='%s',goods_costprice='%s' WHERE goods_commonid = '%s'" % (goods_name,goods_image,item['goods_price'],goods_jingle,goods_desc,goods_desc,goods_marketprice,item['goods_costprice'],ret[0])
            self.cur.execute(sqlupdatecommon)
            #if self.cur.rowcount:
            sqlupdategoods = "UPDATE mall_goods SET goods_name='%s',goods_image='%s',goods_storage='%s',goods_price='%s',goods_jingle_other='%s',goods_edittime='%s',goods_tradeprice='%s',goods_promotion_price='%s',goods_marketprice='%s',goods_weight='%s' WHERE goods_commonid=%s" % (goods_name,goods_image,item['goods_storage'],item['goods_price'],goods_jingle,now_time,item['goods_price'],item['goods_price'],goods_marketprice,goods_weight,ret[0])
            self.cur.execute(sqlupdategoods)
            #清除redis缓存
            sql_goods_exsits = "select goods_id from mall_goods where goods_commonid='%s'" % (ret[0])
            self.cur.execute(sql_goods_exsits)
            retgoods = self.cur.fetchone()
            common_key = str(ret[0])
            goods_key = str(retgoods[0])
            #更新mall_p_xianshi_goods
            sql_xianshi = "UPDATE mall_p_xianshi_goods SET goods_image='%s',goods_price='%s',market_price='%s',xianshi_price='%s',rate='%s' WHERE goods_id = %s" % (goods_image,item['goods_price'],goods_marketprice,item['goods_price'],rate,retgoods[0])
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
            #mall_goods_common
            sqlcommon = 'insert into mall_goods_common' \
                  '(goods_name,goods_image,goods_price,goods_jingle,mobile_body,gc_id,gc_id_1,gc_id_2,gc_id_3,gc_name,store_id,store_name,spec_name,spec_value,brand_id,brand_name,goods_attr,goods_body,goods_state,goods_verify,goods_addtime,goods_selltime,goods_specname,goods_marketprice,goods_costprice,goods_discount,goods_serial,goods_storage_alarm,areaid_1,areaid_2,appoint_satedate,presell_deliverdate,goods_url,goods_jingle_other,shop_info) ' \
                  'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            liscommon = (goods_name,goods_image,item['goods_price'],'',goods_desc,self.cat_info[item['gc_name']]['gc_id'],self.cat_info[item['gc_name']]['gc_id_1'],self.cat_info[item['gc_name']]['gc_id_2'],self.cat_info[item['gc_name']]['gc_id_3'],item['gc_name'],'1','拼拼侠','N;','N;',self.brand_info[item['goods_brand']],item['goods_brand'],'N;',goods_desc,'1','1',now_time,now_time,item['goods_brand'],goods_marketprice,item['goods_costprice'],'100','','1','1','1',now_time,now_time,item['goods_url'],goods_jingle,shop_info)
            self.cur.execute(sqlcommon,liscommon)
            common_id = int(self.client.insert_id())
            if common_id:
                #mall_goods
                sqlgoods = 'insert into mall_goods(goods_commonid,goods_name,goods_jingle,store_id,store_name,gc_id,gc_id_1,gc_id_2,gc_id_3,brand_id,goods_price,goods_tradeprice,goods_promotion_price,goods_promotion_type,goods_marketprice,goods_serial,goods_storage_alarm,goods_click,goods_salenum,goods_collect,goods_spec,goods_storage,goods_image,goods_state,goods_verify,goods_addtime,goods_edittime,areaid_1,areaid_2,color_id,transport_id,goods_freight,goods_vat,goods_commend,goods_stcids,evaluation_good_star,evaluation_count,is_virtual,virtual_indate,virtual_limit,virtual_invalid_refund,is_fcode,is_appoint,is_presell,have_gift,is_own_shop,distribution_price_1,distribution_price_2,distribution_price_3,commission_percent,goods_jingle_other,goods_weight)' \
                           'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                lisgoods = (common_id,goods_name,'','1','拼拼侠',self.cat_info[item['gc_name']]['gc_id'],self.cat_info[item['gc_name']]['gc_id_1'],self.cat_info[item['gc_name']]['gc_id_2'],self.cat_info[item['gc_name']]['gc_id_3'],self.brand_info[item['goods_brand']],item['goods_price'],item['goods_price'],item['goods_price'],'0',goods_marketprice,'','1','1','1','1','',item['goods_storage'],goods_image,'1','1',now_time,now_time,'1','1','0','0','0','0','0','1','5','0','0','0','0','0','0','0','0','0','0','0','0','0','0',goods_jingle,goods_weight)
                self.cur.execute(sqlgoods,lisgoods)
                self.client.commit()

        return item

    def down_img(self):
        import requests
        import os
        url = self.img_url
        root = "./image/1/"
        path = root + '1_'+url.split("/")[-1]
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
                return '1_'+url.split("/")[-1]
            else:
                print("文件已存在")
                return '1_'+url.split("/")[-1]
        except Exception as e:
            print("爬取失败:"+str(e))
            return self.img_url


