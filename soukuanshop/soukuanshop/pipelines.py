# -*- coding: utf-8 -*-
import pymysql
from soukuanshop.settings import mysql_host,mysql_port,mysql_db_user,mysql_db_pwd,mysql_db_name,mysql_db_charset
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SoukuanshopPipeline(object):
    def __init__(self):
        self.client = pymysql.connect(
            host=mysql_host,
            port=mysql_port,
            user=mysql_db_user,  #使用自己的用户名
            passwd=mysql_db_pwd,  # 使用自己的密码
            db=mysql_db_name,  # 数据库名
            charset=mysql_db_charset
        )
        self.cur = self.client.cursor()

    def process_item(self, item, spider):
        #判断商品是否存在
        sql_exsits = "select shop_id from mall_shop_top where shop_name='%s' and gc_name='%s'" % (item['shop_name'],item['gc_name'])
        self.cur.execute(sql_exsits)
        ret = self.cur.fetchone()
        if not ret is None:
            #更新
            sqlgz = "UPDATE mall_shop_top SET shop_range='%s',shop_name='%s',shop_address='%s',shop_sale='%s',shop_goods_num='%s', gc_name='%s' WHERE shop_id = '%s'" % (item['shop_range'],item['shop_name'],item['shop_address'],item['shop_sale'],item['shop_goods_num'],item['gc_name'],ret[0])
            print(sqlgz)
            self.cur.execute(sqlgz)
            self.client.commit()
        else:
            sql = 'insert into mall_shop_top(shop_range,shop_name,shop_address,shop_sale,shop_goods_num,gc_name) VALUES (%s,%s,%s,%s,%s,%s)'
            lis = (item['shop_range'],item['shop_name'],item['shop_address'],item['shop_sale'],item['shop_goods_num'],item['gc_name'])
            self.cur.execute(sql,lis)
            self.client.commit()

        return item
