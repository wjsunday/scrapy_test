import pymysql
import redis
import time
import os
import hashlib
import requests
from settings import mysql_host,mysql_port,mysql_db_user,mysql_db_pwd,mysql_db_name,mysql_db_charset,redis_host,redis_port,redis_pwd,redis_name

class Connect_mysql(object):
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

    def oper_item(self,item):
        now_time = int(time.time())
        if 'code' in item:
            goods_serial = item['code']
        else:
            goods_serial = item['title']
        goods_name = item['name']
        goods_image = item['mainImage']
        self.img_url = goods_image
        goods_url = ''
        if 'reason' in item:
            goods_jingle = item['reason']
        else:
            goods_jingle = ''
        goods_desc = item['introduction'].replace("'","\\'")
        goods_marketprice = round(item['discountprice'] * 1.2,2)
        rate = round(item['discountprice']/goods_marketprice,2)*10
        goods_price = item['discountprice']
        shop_info = ''
        address = item['address']
        goods_weight = item['weights']
        goods_salenum = item['buyquantity']
        #判断商品是否存在
        sql_exsits = "select goods_commonid,goods_image,goods_image_old from mall_goods_common where goods_serial='%s'" % (goods_serial)
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
            sqlupdatecommon = "UPDATE mall_goods_common SET goods_name='%s',goods_image='%s',goods_price='%s',goods_jingle_other='%s',goods_body='%s',mobile_body='%s',goods_marketprice='%s',goods_costprice='%s',shop_info='%s',goods_image_old='%s', goods_serial='%s' WHERE goods_commonid = '%s'" % (goods_name,goods_image,goods_price,goods_jingle,goods_desc,goods_desc,goods_marketprice,goods_price,shop_info,self.img_url,goods_serial,ret[0])
            self.cur.execute(sqlupdatecommon)
            #更新店铺信息
            if address != '':
                self.oper_shop(ret[0],address)
            #更新goods
            sqlgoods = "SELECT goods_id FROM mall_goods WHERE goods_commonid='%s'" % (ret[0])
            self.cur.execute(sqlgoods)
            results = self.cur.fetchall()
            for row in results:
                sqlupdategoods = "UPDATE mall_goods SET goods_name='%s',goods_image='%s',goods_storage='%s',goods_price='%s',goods_jingle_other='%s',goods_edittime='%s',goods_tradeprice='%s',goods_promotion_price='%s',goods_marketprice='%s',goods_salenum='%s' WHERE goods_id=%s" % (goods_name,goods_image,100,goods_price,goods_jingle,now_time,goods_price,goods_price,goods_marketprice,goods_salenum,row[0])
                self.cur.execute(sqlupdategoods)
                common_key = str(ret[0])
                goods_key = str(row[0])
                #更新mall_p_xianshi_goods
                sql_xianshi = "UPDATE mall_p_xianshi_goods SET goods_image='%s',goods_price='%s',market_price='%s',xianshi_price='%s',rate='%s' WHERE goods_id = %s" % (goods_image,goods_price,goods_marketprice,goods_price,rate,row[0])
                self.cur.execute(sql_xianshi)
                self.r.delete('ppxMall_goods_common'+common_key)
                self.r.delete('ppxMall_goods'+goods_key)
                self.r.delete('ppxMall_goods_xianshi'+goods_key)
                goods_key_tmp = 'ppxMall_goods_image'+goods_key+'|*'
                if len(self.r.keys(pattern=goods_key_tmp)):
                    self.r.delete(*self.r.keys(pattern=goods_key_tmp))
            self.client.commit()
        else:
            goods_image = self.down_img()
            #mall_goods_common
            sqlcommon = 'insert into mall_goods_common' \
                        '(goods_name,goods_image,goods_price,goods_jingle,mobile_body,gc_id,gc_id_1,gc_id_2,gc_id_3,gc_name,store_id,store_name,spec_name,spec_value,brand_id,brand_name,goods_attr,goods_body,goods_state,goods_verify,goods_addtime,goods_selltime,goods_specname,goods_marketprice,goods_costprice,goods_discount,goods_serial,goods_storage_alarm,areaid_1,areaid_2,appoint_satedate,presell_deliverdate,goods_url,goods_jingle_other,shop_info,goods_image_old) ' \
                        'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            liscommon = (goods_name,goods_image,goods_price,goods_jingle,goods_desc,'131','131','0','0','滋补','1','拼拼侠','N;','N;','7','参茸滋补','N;',goods_desc,'1','1',now_time,now_time,'N;',goods_marketprice,goods_price,'100',goods_serial,'1','1','1',now_time,now_time,goods_url,goods_jingle,shop_info,self.img_url)
            self.cur.execute(sqlcommon,liscommon)
            common_id = int(self.client.insert_id())
            if common_id:
                #更新店铺信息
                if address != '':
                    self.oper_shop(common_id,address)
                #处理商品相册
                goods_image_list = item['banner'].split(",")
                if not goods_image_list is None:
                    mgi_insert = 'insert into mall_goods_images (goods_commonid,store_id,color_id,goods_image,goods_image_sort,is_default) values (%s,%s,%s,%s,%s,%s)'
                    for goods_images_v in goods_image_list:
                        if goods_images_v != '':
                            goods_images_v = self.down_imgs(goods_images_v)
                            lismgi = (common_id,1,0,goods_images_v,0,0)
                            self.cur.execute(mgi_insert,lismgi)

                #mall_goods
                sqlgoods = 'insert into mall_goods(goods_commonid,goods_name,goods_jingle,store_id,store_name,gc_id,gc_id_1,gc_id_2,gc_id_3,brand_id,goods_price,goods_tradeprice,goods_promotion_price,goods_promotion_type,goods_marketprice,goods_serial,goods_storage_alarm,goods_click,goods_salenum,goods_collect,goods_spec,goods_storage,goods_image,goods_state,goods_verify,goods_addtime,goods_edittime,areaid_1,areaid_2,color_id,transport_id,goods_freight,goods_vat,goods_commend,goods_stcids,evaluation_good_star,evaluation_count,is_virtual,virtual_indate,virtual_limit,virtual_invalid_refund,is_fcode,is_appoint,is_presell,have_gift,is_own_shop,distribution_price_1,distribution_price_2,distribution_price_3,commission_percent,goods_jingle_other,goods_weight)' \
                            'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                lisgoods = (common_id,goods_name,goods_jingle,'1','拼拼侠','131','131','0','0','7',goods_price,goods_price,goods_price,'0',goods_marketprice,goods_serial,'1','1',goods_salenum,'1','N;',100,goods_image,'1','1',now_time,now_time,'1','1','0','0','0','0','0','1','5','0','0','0','0','0','0','0','0','0','0','0','0','0','0',goods_jingle,goods_weight)
                self.cur.execute(sqlgoods,lisgoods)
                self.client.commit()


    def down_img(self):
        url = self.img_url
        print(url)
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

    def oper_shop(self,common_id,shop_address):
        ms_select = "select * from mall_shop where goods_commonid='%s'"
        ms_insert = 'insert into mall_shop (shop_address,goods_commonid) values (%s,%s)'
        sql_ms = ms_select % (common_id)
        self.cur.execute(sql_ms)
        ms_info = self.cur.fetchone()
        if not ms_info is None:
            sqlupdategoods = "UPDATE mall_shop SET shop_address='%s' WHERE shop_id=%s" % (shop_address,ms_info[0])
            self.cur.execute(sqlupdategoods)
            sp_id = ms_info[0]
        else:
            lisms = (shop_address,common_id)
            self.cur.execute(ms_insert,lisms)
            sp_id = int(self.client.insert_id())

        return sp_id

mysql_info = Connect_mysql()