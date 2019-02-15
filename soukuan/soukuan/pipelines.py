# -*- coding: utf-8 -*-
import pymysql
from soukuan.settings import mysql_host,mysql_port,mysql_db_user,mysql_db_pwd,mysql_db_name,mysql_db_charset
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SoukuanPipeline(object):
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
        goods_name = item['goods_name'].replace("'","\\'")
        sql_exsits = "select goods_id from mall_51go_list where goods_url='%s'" % (item['goods_url'])
        self.cur.execute(sql_exsits)
        ret = self.cur.fetchone()
        if not ret is None:
            #更新
            sqlgz = "UPDATE mall_51go_list SET goods_name='%s',goods_img='%s',goods_price='%s',goods_url='%s',gc_name='%s' WHERE goods_id = '%s'" % (goods_name,item['goods_img'],item['goods_price'],item['goods_url'],item['gc_name'],ret[0])
            print(sqlgz)
            self.cur.execute(sqlgz)
            self.client.commit()
        else:
            sql = 'insert into mall_51go_list(goods_name,goods_img,goods_price,goods_url,gc_name,goods_source) VALUES (%s,%s,%s,%s,%s,%s)'
            lis = (goods_name,item['goods_img'],item['goods_price'],item['goods_url'],item['gc_name'],2)
            self.cur.execute(sql,lis)
            self.client.commit()

        return item
