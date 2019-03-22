'''
修复由于重新爬取商品导致自营商城限时活动对应不上goods_id,goods_images
'''
import pymysql
import redis
import math
from settings import mysql_host,mysql_port,mysql_db_user,mysql_db_pwd,mysql_db_name,mysql_db_charset,redis_host,redis_port,redis_pwd,redis_name

class FixXianShi(object):
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

    def oper_item(self):
        '''
        查询限时活动总数，助分页
        :param item:
        :return:
        '''
        sql_count = "select count(1) from mall_p_xianshi_goods"
        self.cur.execute(sql_count)
        ret = self.cur.fetchone()
        page_size = 100
        total_page = math.ceil(ret[0]/page_size);
        for i in range(1,total_page+1):
            start = (i-1)*page_size;
            sql = "SELECT goods_name FROM mall_p_xianshi_goods limit %d,%d" % (start, page_size)
            self.cur.execute(sql)
            results = self.cur.fetchall()
            for row in results:
                goods_name = row[0].replace("'","\\'")
                sql_goods = "SELECT goods_id,goods_price,goods_marketprice,goods_image FROM mall_goods WHERE goods_name='%s' limit 1" % (goods_name)
                self.cur.execute(sql_goods)
                ret_tmp = self.cur.fetchone()
                if not ret_tmp is None:
                    goods_id = ret_tmp[0]
                    goods_price = ret_tmp[1]
                    goods_marketprice = ret_tmp[2]
                    goods_image = ret_tmp[3]
                    rate = round(goods_price/goods_marketprice,1)*10
                    if int(rate) == 10:
                        rate = 0
                    sql_xianshi = "UPDATE mall_p_xianshi_goods SET goods_id='%s',goods_image='%s',goods_price='%s',market_price='%s',xianshi_price='%s',rate='%s' WHERE goods_name = '%s'" % (goods_id,goods_image,goods_price,goods_marketprice,goods_price,rate,goods_name)
                    self.cur.execute(sql_xianshi)
                    print('更新SQL：'+sql_xianshi)
        self.client.commit()


mysql_info = FixXianShi()
mysql_info.oper_item()
