# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import re
import redis
import time
import phpserialize
import itertools
import os
import hashlib
import sys
sys.path.append("../")
from Fix.settings import mysql_host,mysql_port,mysql_db_user,mysql_db_pwd,mysql_db_name,mysql_db_charset
from Fix.settings import redis_host,redis_port,redis_pwd,redis_name
from Fix.settings import image_path,store_id
from mylog import MyLog

mylog = MyLog()

class FixPipeline(object):
    brand_info = dict()
    cat_info = dict()
    img_url = ""


    def __init__(self):
        self.client = pymysql.connect(
            host=mysql_host,
            port=mysql_port,
            user=mysql_db_user,  # 使用自己的用户名
            passwd=mysql_db_pwd,  # 使用自己的密码
            db=mysql_db_name,  # 数据库名
            charset=mysql_db_charset
        )
        self.r = redis.Redis(host=redis_host, port=redis_port, db=redis_name, password=redis_pwd)
        self.cur = self.client.cursor()
        self.brand_info = {'广州女装批发': '6'}

        self.cat_info = {
            "21000001": ["女装", "上装/外套", "小衫", "", "", "", ""],
            "21000002": ["女装", "上装/外套", "马甲", "", "", "", ""],
            "21000003": ["女装", "裤装", "短裤", "", "", "", ""],
            "20000004": ["内衣/家居", "内衣", "配饰", "", "", "", ""],
            "20000035": ["女装", "上装/外套", "T恤", "1", "", "", ""],
            "20000018": ["女装", "上装/外套", "衬衫", "1", "", "", ""],
            "20000019": ["女装", "上装/外套", "蕾丝衫/雪纺衫", "1", "", "", ""],
            "20000068": ["女装", "上装/外套", "卫衣/绒衫", "1", "", "", ""],
            "20000017": ["女装", "上装/外套", "毛衣", "1", "", "", ""],
            "20000038": ["女装", "上装/外套", "毛针织衫", "1", "", "", ""],
            "20000037": ["女装", "上装/外套", "毛针织套装", "1", "", "", ""],
            "20000389": ["女装", "上装/外套", "时尚套装", "1", "", "", ""],
            "20000025": ["女装", "上装/外套", "休闲运动套装", "1", "", "", ""],
            "20000024": ["女装", "上装/外套", "其它套装", "1", "", "", ""],
            "20000129": ["女装", "上装/外套", "短外套", "1", "", "", ""],
            "20000128": ["女装", "上装/外套", "牛仔短外套", "1", "", "", ""],
            "20000174": ["女装", "上装/外套", "毛呢外套", "1", "", "", ""],
            "20000070": ["女装", "上装/外套", "棉衣/棉服", "1", "", "", ""],
            "20000069": ["女装", "上装/外套", "羽绒服", "1", "", "", ""],
            "20000175": ["女装", "上装/外套", "羽绒马夹", "1", "", "", ""],
            "20000071": ["女装", "上装/外套", "风衣", "1", "", "", ""],
            "20000176": ["女装", "上装/外套", "马夹", "1", "", "", ""],
            "20000067": ["女装", "上装/外套", "西装", "1", "", "", ""],
            "20000073": ["女装", "上装/外套", "皮衣", "1", "", "", ""],
            "20000074": ["女装", "上装/外套", "皮草", "1", "", "", ""],
            "20000364": ["女装", "上装/外套", "背心吊带", "1", "", "", ""],
            "20000370": ["女装", "上装/外套", "抹胸", "1", "", "", ""],
            "20000055": ["女装", "上装/外套", "旗袍", "1", "", "", ""],
            "20000028": ["女装", "上装/外套", "民族服装/舞台装", "1", "", "", ""],
            "20000052": ["女装", "上装/外套", "唐装/中式服饰上衣", "1", "", "", ""],
            "20000072": ["女装", "上装/外套", "学生校服", "1", "", "", ""],
            "20000027": ["女装", "上装/外套", "礼服/晚装", "1", "", "", ""],
            "20000131": ["女装", "上装/外套", "酒店工作制服", "1", "", "", ""],
            "20000005": ["女装", "上装/外套", "大码外套/马甲", "1", "", "", ""],
            "20000012": ["女装", "上装/外套", "大码毛针织衫", "1", "", "", ""],
            "20000007": ["女装", "上装/外套", "大码T恤", "1", "", "", ""],
            "20000013": ["女装", "上装/外套", "大码套装", "1", "", "", ""],
            "20000008": ["女装", "上装/外套", "大码衬衫", "1", "", "", ""],
            "20000011": ["女装", "上装/外套", "大码卫衣/绒衫", "1", "", "", ""],
            "20000002": ["女装", "上装/外套", "大码雪纺衫/雪纺衫", "1", "", "", ""],
            "20000014": ["女装", "上装/外套", "其他大码女装", "1", "", "", ""],
            "20000039": ["女装", "上装/外套", "中老年蕾丝衫/雪纺衫", "1", "", "", ""],
            "20000042": ["女装", "上装/外套", "中老年T恤", "1", "", "", ""],
            "20000046": ["女装", "上装/外套", "中老年外套/马甲", "1", "", "", ""],
            "20000048": ["女装", "上装/外套", "中老年套装", "1", "", "", ""],
            "20000106": ["女装", "裙装", "连衣裙", "1", "", "", ""],
            "20000006": ["女装", "裙装", "大码连衣裙", "1", "", "", ""],
            "20000041": ["女装", "裙装", "中老年连衣裙", "1", "", "", ""],
            "20000001": ["女装", "裙装", "半身裙", "1", "", "", ""],
            "20000000": ["女装", "裙装", "牛仔半身裙", "1", "", "", ""],
            "20000010": ["女装", "裙装", "大码半身裙", "1", "", "", ""],
            "20000044": ["女装", "裙装", "中老年半身裙", "1", "", "", ""],
            "20000036": ["女装", "裙装", "毛针织裙", "1", "", "", ""],
            "20000022": ["女装", "裙装", "职业女裙套装", "1", "", "", ""],
            "20000054": ["女装", "裙装", "唐装/中式服饰裙子", "1", "", "", ""],
            "20000026": ["女装", "裙装", "婚纱", "1", "", "", ""],
            "20000021": ["女装", "裤装", "牛仔裤", "1", "", "", ""],
            "20000020": ["女装", "裤装", "休闲裤", "1", "", "", ""],
            "20000057": ["女装", "裤装", "打底裤", "1", "", "", ""],
            "20000009": ["女装", "裤装", "大码裤子", "1", "", "", ""],
            "20000291": ["女装", "裤装", "西装裤/正装裤", "1", "", "", ""],
            "20000053": ["女装", "裤装", "唐装/中式服饰裤子", "1", "", "", ""],
            "20000023": ["女装", "裤装", "职业女裤套装", "1", "", "", ""],
            "20000040": ["女装", "裤装", "中老年裤子", "1", "", "", ""],
            "20000340": ["女装", "裤装", "羽绒裤", "1", "", "", ""],
            "20000341": ["女装", "裤装", "棉裤", "1", "", "", ""],
            "20000078": ["男装", "上装/外套", "卫衣", "2", "", "", ""],
            "20000076": ["男装", "上装/外套", "夹克", "2", "", "", ""],
            "20000034": ["男装", "上装/外套", "针织衫/毛衣", "2", "", "", ""],
            "20000424": ["男装", "上装/外套", "休闲运动套装", "2", "", "", ""],
            "20000421": ["男装", "上装/外套", "其他套装", "2", "", "", ""],
            "20000117": ["男装", "上装/外套", "背心", "2", "", "", ""],
            "20000116": ["男装", "上装/外套", "马甲", "2", "", "", ""],
            "20000120": ["男装", "上装/外套", "风衣", "2", "", "", ""],
            "20000123": ["男装", "上装/外套", "皮衣", "2", "", "", ""],
            "20000125": ["男装", "上装/外套", "棉衣", "2", "", "", ""],
            "20000335": ["男装", "上装/外套", "毛呢大衣", "2", "", "", ""],
            "20000079": ["男装", "上装/外套", "西服", "2", "", "", ""],
            "20000113": ["男装", "上装/外套", "西服套装", "2", "", "", ""],
            "20000115": ["男装", "上装/外套", "西装马甲", "2", "", "", ""],
            "20000127": ["男装", "上装/外套", "羽绒服", "2", "", "", ""],
            "20000056": ["男装", "上装/外套", "工装制服", "2", "", "", ""],
            "20000077": ["男装", "上装/外套", "大码卫衣", "2", "", "", ""],
            "20000033": ["男装", "上装/外套", "大码针织衫/毛衣", "2", "", "", ""],
            "20000423": ["男装", "上装/外套", "大码休闲运动套装", "2", "", "", ""],
            "20000420": ["男装", "上装/外套", "大码其他套装", "2", "", "", ""],
            "20000124": ["男装", "上装/外套", "大码棉衣", "2", "", "", ""],
            "20000126": ["男装", "上装/外套", "大码羽绒服", "2", "", "", ""],
            "20000119": ["男装", "上装/外套", "大码风衣", "2", "", "", ""],
            "20000122": ["男装", "上装/外套", "大码皮衣", "2", "", "", ""],
            "20000334": ["男装", "上装/外套", "大码毛呢大衣", "2", "", "", ""],
            "20000075": ["男装", "上装/外套", "中老年夹克", "2", "", "", ""],
            "20000032": ["男装", "上装/外套", "中老年针织衫/毛衣", "2", "", "", ""],
            "20000422": ["男装", "上装/外套", "中老年休闲运动套装", "2", "", "", ""],
            "20000118": ["男装", "上装/外套", "中老年风衣", "2", "", "", ""],
            "20000031": ["男装", "衬衫/T恤", "T恤", "2", "", "", ""],
            "20000030": ["男装", "衬衫/T恤", "大码T恤", "2", "", "", ""],
            "20000029": ["男装", "衬衫/T恤", "中老年T恤", "2", "", "", ""],
            "20000109": ["男装", "衬衫/T恤", "衬衫", "2", "", "", ""],
            "20000108": ["男装", "衬衫/T恤", "大码衬衫", "2", "", "", ""],
            "20000107": ["男装", "衬衫/T恤", "中老年衬衫", "2", "", "", ""],
            "20000090": ["男装", "衬衫/T恤", "Polo衫", "2", "", "", ""],
            "20000089": ["男装", "衬衫/T恤", "大码Polo衫", "2", "", "", ""],
            "20000088": ["男装", "衬衫/T恤", "中老年Polo衫", "2", "", "", ""],
            "20000016": ["男装", "裤装", "休闲裤", "2", "", "", ""],
            "20000015": ["男装", "裤装", "大码休闲裤", "2", "", "", ""],
            "20000081": ["男装", "裤装", "牛仔裤", "2", "", "", ""],
            "20000080": ["男装", "裤装", "大码牛仔裤", "2", "", "", ""],
            "20000112": ["男装", "裤装", "西裤", "2", "", "", ""],
            "20000111": ["男装", "裤装", "皮裤", "2", "", "", ""],
            "20000339": ["男装", "裤装", "棉裤", "2", "", "", ""],
            "10000137": ["鞋", "女鞋", "低帮鞋", "3", "", "", ""],
            "10000135": ["鞋", "女鞋", "靴子", "3", "", "", ""],
            "10000136": ["鞋", "女鞋", "高帮鞋", "3", "", "", ""],
            "10000141": ["鞋", "女鞋", "低帮帆布鞋", "3", "", "", ""],
            "10000140": ["鞋", "女鞋", "高帮帆布鞋", "3", "", "", ""],
            "10000138": ["鞋", "女鞋", "拖鞋", "3", "", "", ""],
            "10000139": ["鞋", "女鞋", "凉鞋", "3", "", "", ""],
            "10000133": ["鞋", "女鞋", "雨鞋", "3", "", "", ""],
            "10000128": ["鞋", "男鞋", "低帮鞋", "3", "", "", ""],
            "10000126": ["鞋", "男鞋", "靴子", "3", "", "", ""],
            "10000127": ["鞋", "男鞋", "高帮鞋", "3", "", "", ""],
            "10000132": ["鞋", "男鞋", "低帮帆布鞋", "3", "", "", ""],
            "10000131": ["鞋", "男鞋", "高帮帆布鞋", "3", "", "", ""],
            "10000129": ["鞋", "男鞋", "拖鞋", "3", "", "", ""],
            "10000130": ["鞋", "男鞋", "凉鞋", "3", "", "", ""],
            "20000058": ["内衣/家居", "内衣", "文胸", "4", "", "", ""],
            "20000059": ["内衣/家居", "内衣", "内裤", "4", "", "", ""],
            "20000060": ["内衣/家居", "内衣", "文胸套装", "4", "", "", ""],
            "20000065": ["内衣/家居", "内衣", "抹胸", "4", "", "", ""],
            "40000154": ["内衣/家居", "内衣", "短袜/打底袜/丝袜/美腿袜", "4", "", "", ""],
            "20000083": ["内衣/家居", "内衣", "吊带", "4", "", "", ""],
            "20000085": ["内衣/家居", "内衣", "背心", "4", "", "", ""],
            "20000082": ["内衣/家居", "内衣", "T恤", "4", "", "", ""],
            "20000165": ["内衣/家居", "内衣", "睡衣/家居服套装", "4", "", "", ""],
            "20000064": ["内衣/家居", "内衣", "睡衣上装", "4", "", "", ""],
            "20000161": ["内衣/家居", "内衣", "睡裤/家居裤", "4", "", "", ""],
            "20000163": ["内衣/家居", "内衣", "睡裙", "4", "", "", ""],
            "20000166": ["内衣/家居", "内衣", "睡袍/浴袍", "4", "", "", ""],
            "20000164": ["内衣/家居", "内衣", "中老年睡衣/家居服套装", "4", "", "", ""],
            "20000063": ["内衣/家居", "内衣", "中老年睡衣上装", "4", "", "", ""],
            "20000160": ["内衣/家居", "内衣", "中老年睡裤/家居裤", "4", "", "", ""],
            "20000162": ["内衣/家居", "内衣", "中老年睡裙", "4", "", "", ""],
            "20000170": ["内衣/家居", "内衣", "保暖套装", "4", "", "", ""],
            "20000062": ["内衣/家居", "内衣", "保暖上装", "4", "", "", ""],
            "20000169": ["内衣/家居", "内衣", "保暖裤", "4", "", "", ""],
            "20000171": ["内衣/家居", "内衣", "塑身连体衣", "4", "", "", ""],
            "20000168": ["内衣/家居", "内衣", "塑身分体套装", "4", "", "", ""],
            "20000061": ["内衣/家居", "内衣", "塑身上衣", "4", "", "", ""],
            "20000167": ["内衣/家居", "内衣", "塑身美体裤", "4", "", "", ""],
            "40000015": ["内衣/家居", "内衣", "塑身腰封/腰夹", "4", "", "", ""],
            "40000169": ["内衣/家居", "内衣", "乳贴", "4", "", "", ""],
            "40000170": ["内衣/家居", "内衣", "肩带", "4", "", "", ""],
            "40000171": ["内衣/家居", "内衣", "插片/胸垫", "4", "", "", ""],
            "20000103": ["儿童用品", "童装", "套装", "5", "", "", ""],
            "20000158": ["儿童用品", "童装", "亲子装/亲子时装", "5", "", "", ""],
            "20000374": ["儿童用品", "童装", "连衣裙", "5", "", "", ""],
            "20000387": ["儿童用品", "童装", "半身裙", "5", "", "", ""],
            "20000173": ["儿童用品", "童装", "T恤", "5", "", "", ""],
            "20000096": ["儿童用品", "童装", "衬衫", "5", "", "", ""],
            "20000102": ["儿童用品", "童装", "毛针织衫", "5", "", "", ""],
            "20000091": ["儿童用品", "童装", "卫衣/绒衫", "5", "", "", ""],
            "20000104": ["儿童用品", "童装", "牛仔外套", "5", "", "", ""],
            "20000105": ["儿童用品", "童装", "普通外套", "5", "", "", ""],
            "20000141": ["儿童用品", "童装", "风衣", "5", "", "", ""],
            "20000095": ["儿童用品", "童装", "马甲", "5", "", "", ""],
            "20000093": ["儿童用品", "童装", "夹克", "5", "", "", ""],
            "20000092": ["儿童用品", "童装", "皮衣", "5", "", "", ""],
            "20000094": ["儿童用品", "童装", "呢大衣", "5", "", "", ""],
            "20000402": ["儿童用品", "童装", "羽绒服", "5", "", "", ""],
            "20000398": ["儿童用品", "童装", "羽绒马甲", "5", "", "", ""],
            "20000331": ["儿童用品", "童装", "西服/小西装", "5", "", "", ""],
            "20000098": ["儿童用品", "童装", "棉袄/棉服", "5", "", "", ""],
            "20000180": ["儿童用品", "童装", "牛仔裤", "5", "", "", ""],
            "20000181": ["儿童用品", "童装", "棉裤", "5", "", "", ""],
            "20000182": ["儿童用品", "童装", "裤子", "5", "", "", ""],
            "20000345": ["儿童用品", "童装", "背心吊带", "5", "", "", ""],
            "20000097": ["儿童用品", "童装", "披风/斗篷", "5", "", "", ""],
            "40000004": ["儿童用品", "童装", "帽子", "5", "", "", ""],
            "20000369": ["儿童用品", "童装", "家居服套装", "5", "", "", ""],
            "20000375": ["儿童用品", "童装", "家居裙/睡裙", "5", "", "", ""],
            "20000352": ["儿童用品", "童装", "内衣套装", "5", "", "", ""],
            "20000361": ["儿童用品", "童装", "内裤", "5", "", "", ""],
            "40000141": ["儿童用品", "童装", "儿童袜子(0-16岁)", "5", "", "", ""],
            "20000099": ["儿童用品", "童装", "连身衣/爬服/哈衣", "5", "", "", ""],
            "20000190": ["儿童用品", "童装", "婴儿礼盒", "5", "", "", ""],
            "10000144": ["儿童用品", "童鞋", "皮鞋", "5", "", "", ""],
            "10000064": ["儿童用品", "童鞋", "跑步鞋", "5", "", "", ""],
            "10000088": ["儿童用品", "童鞋", "休闲鞋", "5", "", "", ""],
            "10000143": ["儿童用品", "童鞋", "帆布鞋", "5", "", "", ""],
            "10000148": ["儿童用品", "童鞋", "靴子", "5", "", "", ""],
            "10000146": ["儿童用品", "童鞋", "凉鞋", "5", "", "", ""],
            "10000145": ["儿童用品", "童鞋", "拖鞋", "5", "", "", ""],
            "10000149": ["儿童用品", "童鞋", "亲子鞋", "5", "", "", ""],
            "10000150": ["儿童用品", "童鞋", "学步鞋", "5", "", "", ""],
            "10000065": ["儿童用品", "童鞋", "运动板鞋", "5", "", "", ""],
            "10000066": ["儿童用品", "童鞋", "运动帆布鞋", "5", "", "", ""],
            "10000068": ["儿童用品", "童鞋", "运动沙滩鞋/凉鞋", "5", "", "", ""],
            "10000089": ["儿童用品", "童鞋", "其它运动鞋", "5", "", "", ""],
            "40000011": ["配件箱包", "服装配饰", "围巾/丝巾/披肩", "6", "", "", ""],
            "40000016": ["配件箱包", "服装配饰", "帽子", "6", "", "", ""],
            "40000012": ["配件箱包", "服装配饰", "手套", "6", "", "", ""],
            "40000017": ["配件箱包", "服装配饰", "耳套", "6", "", "", ""],
            "40000029": ["配件箱包", "服装配饰", "二件套", "6", "", "", ""],
            "40000030": ["配件箱包", "服装配饰", "三件套", "6", "", "", ""],
            "40000014": ["配件箱包", "服装配饰", "腰带/皮带/腰链", "6", "", "", ""],
            "40000020": ["配件箱包", "服装配饰", "假领", "6", "", "", ""],
            "30000096": ["配件箱包", "服装配饰", "包挂件", "6", "", "", ""],
            "40000033": ["配件箱包", "服装配饰", "其他配件", "6", "", "", ""],
            "20000246": ["运动户外", "运动", "比基尼", "7", "", "", ""],
            "20000250": ["运动户外", "运动", "连体泳衣", "7", "", "", ""],
            "20000248": ["运动户外", "运动", "分体泳衣", "7", "", "", ""],
            "20000251": ["运动户外", "运动", "男士泳衣", "7", "", "", ""],
            "20000252": ["运动户外", "运动", "儿童泳衣/裤", "7", "", "", ""],
            "20000249": ["运动户外", "运动", "中老年连体泳衣", "7", "", "", ""],
            "20000382": ["运动户外", "运动", "沙滩外套", "7", "", "", ""],
            "20000320": ["运动户外", "运动", "沙滩裤", "7", "", "", ""],
            "40000102": ["运动户外", "运动", "泳帽", "7", "", "", ""],
            "40000101": ["运动户外", "运动", "泳镜", "7", "", "", ""],
            "20000255": ["运动户外", "运动", "裹裙/披纱", "7", "", "", ""],
            "20000240": ["运动户外", "运动", "瑜伽服", "7", "", "", ""],
            "20000225": ["运动户外", "运动", "钢管舞服", "7", "", "", ""],
            "20000292": ["运动户外", "运动服", "运动套装", "7", "", "", ""],
            "20000139": ["运动户外", "运动服", "运动茄克", "7", "", "", ""],
            "20000178": ["运动户外", "运动服", "运动T恤", "7", "", "", ""],
            "20000134": ["运动户外", "运动服", "运动卫衣/套头衫", "7", "", "", ""],
            "20000293": ["运动户外", "运动服", "运动POLO衫", "7", "", "", ""],
            "20000179": ["运动户外", "运动服", "运动连衣裙", "7", "", "", ""],
            "20000140": ["运动户外", "运动服", "运动外套", "7", "", "", ""],
            "20000135": ["运动户外", "运动服", "运动风衣", "7", "", "", ""],
            "20000136": ["运动户外", "运动服", "运动棉衣", "7", "", "", ""],
            "20000302": ["运动户外", "运动服", "运动长裤", "7", "", "", ""],
            "20000303": ["运动户外", "运动服", "运动中长裤／短裤", "7", "", "", ""],
            "20000296": ["运动户外", "运动服", "健身套装", "7", "", "", ""],
            "20000294": ["运动户外", "运动服", "健身衣", "7", "", "", ""],
            "20000295": ["运动户外", "运动服", "健身裤", "7", "", "", ""],
            "20000310": ["运动户外", "运动服", "棒球服", "7", "", "", ""],
            "40000142": ["运动户外", "运动服", "运动袜", "7", "", "", ""],
            "40000042": ["运动户外", "运动服", "其他服饰配件", "7", "", "", ""],
            "10000004": ["户外运动", "运动鞋", "跑步鞋", "7", "", "", ""],
            "10000032": ["户外运动", "运动鞋", "休闲鞋", "7", "", "", ""],
            "10000031": ["户外运动", "运动鞋", "板鞋", "7", "", "", ""],
            "10000007": ["户外运动", "运动鞋", "其它运动鞋", "7", "", "", ""],
            "30000050": ["户外运动", "运动包", "单肩背包", "7", "", "", ""],
            "30000049": ["户外运动", "运动包", "双肩背包", "7", "", "", ""],
            "30000052": ["户外运动", "运动包", "挎包/拎包/休闲包", "7", "", "", ""],
            "30000051": ["户外运动", "运动包", "手包", "7", "", "", ""],
            "40000126": ["美妆饰品", "美妆", "项链", "8", "", "", ""],
            "40000127": ["美妆饰品", "美妆", "项坠/吊坠", "8", "", "", ""],
            "40000128": ["美妆饰品", "美妆", "手链", "8", "", "", ""],
            "40000129": ["美妆饰品", "美妆", "手镯", "8", "", "", ""],
            "40000136": ["美妆饰品", "美妆", "脚链", "8", "", "", ""],
            "40000130": ["美妆饰品", "美妆", "戒指/指环", "8", "", "", ""],
            "40000132": ["美妆饰品", "美妆", "耳环", "8", "", "", ""],
            "40000133": ["美妆饰品", "美妆", "耳钉", "8", "", "", ""],
            "40000131": ["美妆饰品", "美妆", "发饰", "8", "", "", ""],
            "40000137": ["美妆饰品", "美妆", "胸针", "8", "", "", ""],
            "40000139": ["美妆饰品", "美妆", "其它首饰", "8", "", "", ""],
            "40000140": ["美妆饰品", "美妆", "其他DIY饰品配件", "8", "", "", ""],
            "20000144": ["孕妇装", "孕妇装", "连衣裙", "9", "", "", ""],
            "20000321": ["孕妇装", "孕妇装", "孕妇裤/托腹裤", "9", "", "", ""],
            "20000148": ["孕妇装", "孕妇装", "套装", "9", "", "", ""],
            "20000147": ["孕妇装", "孕妇装", "T恤", "9", "", "", ""],
            "20000145": ["孕妇装", "孕妇装", "毛衣", "9", "", "", ""],
            "20000146": ["孕妇装", "孕妇装", "针织衫", "9", "", "", ""],
            "20000151": ["孕妇装", "孕妇装", "卫衣/绒衫", "9", "", "", ""],
            "20000143": ["孕妇装", "孕妇装", "外套/风衣", "9", "", "", ""],
            "20000152": ["孕妇装", "孕妇装", "马甲", "9", "", "", ""],
            "20000325": ["孕妇装", "孕妇装", "棉衣", "9", "", "", ""],
            "20000324": ["孕妇装", "孕妇装", "羽绒服", "9", "", "", ""],
            "20000326": ["孕妇装", "孕妇装", "大衣", "9", "", "", ""],
            "20000323": ["孕妇装", "孕妇装", "半身裙", "9", "", "", ""],
            "20000150": ["孕妇装", "孕妇装", "衬衫", "9", "", "", ""],
            "20000153": ["孕妇装", "孕妇装", "吊带/背心", "9", "", "", ""],
            "20000149": ["孕妇装", "孕妇装", "雪纺衫", "9", "", "", ""],
            "20000360": ["孕妇装", "孕妇装", "家居服套装", "9", "", "", ""],
            "20000350": ["孕妇装", "孕妇装", "家居裙", "9", "", "", ""],
            "20000365": ["孕妇装", "孕妇装", "家居服上装", "9", "", "", ""],
            "20000383": ["孕妇装", "孕妇装", "家居裤", "9", "", "", ""],
            "20000380": ["孕妇装", "孕妇装", "家居袍", "9", "", "", ""],
            "20000328": ["孕妇装", "孕妇装", "其它", "9", "", "", ""],
            "20000412": ["孕妇装", "孕妇装", "哺乳衣", "9", "", "", ""],
            "20000243": ["孕妇装", "孕妇装", "哺乳文胸", "9", "", "", ""],
            "20000348": ["孕妇装", "孕妇装", "哺乳吊带", "9", "", "", ""],
            "20000157": ["孕妇装", "孕妇装", "防辐射围裙", "9", "", "", ""],
            "20000156": ["孕妇装", "孕妇装", "防辐射肚兜/护胎宝", "9", "", "", ""],
            "20000244": ["孕妇装", "孕妇装", "内裤", "9", "", "", ""],
            "40000155": ["孕妇装", "孕妇装", "孕妇袜/连裤袜/打底袜", "9", "", "", ""],
            "20000087": ["孕妇装", "孕妇装", "(文胸-内裤)套装", "9", "", "", ""],
            "20000354": ["孕妇装", "孕妇装", "秋衣裤套装", "9", "", "", ""],
            "20000384": ["孕妇装", "孕妇装", "秋衣", "9", "", "", ""],
            "40000163": ["孕妇装", "孕妇装", "束腹带", "9", "", "", ""],
            "20000385": ["孕妇装", "孕妇装", "塑身裤", "9", "", "", ""],
            "40000115": ["孕妇装", "孕妇装", "产妇帽", "9", "", "", ""],
            "20000051": ["孕妇装", "孕妇装", "其它孕妇装", "9", "", "", ""],
            "30000001": ["配件箱包", "箱包", "女士包袋", "6", "", "", ""],
            "30000000": ["配件箱包", "箱包", "男士包袋", "6", "", "", ""],
            "30000009": ["配件箱包", "箱包", "双肩背包", "6", "", "", ""],
            "30000004": ["配件箱包", "箱包", "钱包", "6", "", "", ""],
            "30000003": ["配件箱包", "箱包", "旅行袋", "6", "", "", ""],
            "30000002": ["配件箱包", "箱包", "旅行箱", "6", "", "", ""],
            "30000006": ["配件箱包", "箱包", "手机包", "6", "", "", ""],
            "30000005": ["配件箱包", "箱包", "卡包", "6", "", "", ""],
            "30000007": ["配件箱包", "箱包", "钥匙包", "6", "", "", ""],
            "30000008": ["配件箱包", "箱包", "证件包", "6", "", "", ""],
            "30000100": ["配件箱包", "箱包", "箱包相关配件", "6", "", "", ""],
        }

    def process_item(self, item, spider):

        if item["goods_price"]:
            now_time = int(time.time())
            goods_url = item['goods_url']
            goods_name = item['goods_name'].replace("'", "\\'")
            goods_jingle = item['goods_jingle'].replace("'", "\\'")
            goods_desc = item['goods_desc'].replace("'", "\\'").replace("\n", "")

            # 价格判断
            price = int(item['goods_price'])  # 采集价格
            if price <= 100:
                item['goods_price'] = round(price * 1.25 + 2)  # 拼拼侠售价
                goods_marketprice = price * 3  # 拼拼侠市场价
            elif price >= 500:
                item['goods_price'] = round(price * 1.15 + 2)
                goods_marketprice = price * 1.5
            else:
                item['goods_price'] = round(price * 1.25 + 2)
                goods_marketprice = price * 2.5

            # item['goods_price'] = round(item['goods_price'] * 1.25 + 2)
            # goods_marketprice = item['goods_price'] * 2

            rate = round(item['goods_price'] / goods_marketprice, 1) * 10
            if int(rate) == 10:
                rate = 0

            goods_image = 'https:' + item['goods_image']
            self.img_url = goods_image
            shop_info = item['shop_info']
            goods_serial = item['goods_serial'].replace("\n", "").replace(' ', '')
            if not item['shop_name'] is None:
                shop_name = item['shop_name'].replace("\n", "").replace(' ', '')
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
                shop_address = item['shop_address'].replace(' ', '')
            else:
                shop_address = ''
            if not item['goods_salenum'] is None:
                goods_salenum = item['goods_salenum']
            else:
                goods_salenum = '0'
            # 判断商品是否存在
            sql_exsits = "select goods_commonid,goods_image,goods_image_old from mall_goods_common where goods_url='%s'" % (goods_url)
            self.cur.execute(sql_exsits)
            ret = self.cur.fetchone()
            if not ret is None:
                # 处理图片问题
                root = image_path
                path = root +'/'+ ret[1]
                # 当原始图片不存在时候直接下载
                curPath = os.path.abspath(os.path.dirname(__file__)) + path
                if self.img_url:
                    if not os.path.exists(curPath):
                        goods_image = self.down_img()
                    else:
                        pass
                        # 当存在的时候
                        # if self.img_url != ret[2]:
                        #     os.remove(path)
                        #     goods_image = self.down_img()
                        # else:
                        #     goods_image = ret[1]

                # 更新
                """
                sqlupdatecommon = "UPDATE mall_goods_common SET goods_name='%s',goods_image='%s',goods_price='%s',goods_jingle_other='%s',goods_body='%s',mobile_body='%s',goods_marketprice='%s',shop_info='%s',goods_image_old='%s',goods_serial='%s',transport_id='%s',transport_title='%s',is_support_voucher='%s' WHERE goods_commonid = '%s'" % (goods_name,goods_image,item['goods_price'],goods_jingle,goods_desc,goods_desc,goods_marketprice,shop_info,self.img_url,goods_serial,'11','拼拼侠通用运费模板','1',ret[0])
                self.cur.execute(sqlupdatecommon)
                # 更新店铺信息
                self.oper_shop(shop_name, shop_range, shop_ali, ret[0], shop_mobile, shop_address)
                # 更新goods
                sqlgoods = "SELECT goods_id FROM mall_goods WHERE goods_commonid='%s'" % (ret[0])
                self.cur.execute(sqlgoods)
                results = self.cur.fetchall()
                for row in results:
                    sqlupdategoods = "UPDATE mall_goods SET goods_image='%s',goods_storage='%s',goods_price='%s',goods_jingle_other='%s',goods_edittime='%s',goods_promotion_price='%s',goods_marketprice='%s',goods_salenum='%s',transport_id='%s' WHERE goods_id=%s" % (goods_image,item['goods_storage'],item['goods_price'],goods_jingle,now_time,item['goods_price'],goods_marketprice,goods_salenum,'11',row[0])
                    self.cur.execute(sqlupdategoods)
                    common_key = str(ret[0])
                    goods_key = str(row[0])
                    # 更新mall_p_xianshi_goods
                    sql_xianshi = "UPDATE mall_p_xianshi_goods SET goods_image='%s',goods_price='%s',market_price='%s',xianshi_price='%s',rate='%s' WHERE goods_id = %s" % (goods_image,item['goods_price'],goods_marketprice,item['goods_price'],rate,row[0])
                    self.cur.execute(sql_xianshi)
                    self.r.delete('ppxMall_goods_common' + common_key)
                    self.r.delete('ppxMall_goods' + goods_key)
                    self.r.delete('ppxMall_goods_xianshi' + goods_key)
                    goods_key_tmp = 'ppxMall_goods_image' + goods_key + '|*'
                    if len(self.r.keys(pattern=goods_key_tmp)):
                        self.r.delete(*self.r.keys(pattern=goods_key_tmp))
                self.client.commit()
                
                """
            else:
                # 新增
                if item['gc_name'] in self.cat_info:
                    # 爬取图片
                    goods_image = self.down_img()
                    # 处理商品分类 没有添加，有使用
                    gc_select = "select * from mall_goods_class where gc_name='%s'"
                    gc_insert = 'insert into mall_goods_class (gc_name,type_id,type_name,gc_parent_id,commis_rate,gc_sort,gc_virtual,gc_title,gc_keywords,gc_description)' \
                                'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    sql_gc1 = gc_select % (self.cat_info[item['gc_name']][0])
                    self.cur.execute(sql_gc1)
                    gc1_info = self.cur.fetchone()
                    if not gc1_info is None:
                        gc1_id = gc1_info[0]
                    else:
                        lisgc1 = (self.cat_info[item['gc_name']][0], 6, '服装', 0, 0, 0, 0, '', '', '')
                        self.cur.execute(gc_insert, lisgc1)
                        gc1_id = int(self.client.insert_id())

                    sql_gc2 = gc_select % (self.cat_info[item['gc_name']][1])
                    self.cur.execute(sql_gc2)
                    gc2_info = self.cur.fetchone()
                    if not gc2_info is None:
                        gc2_id = gc2_info[0]
                    else:
                        lisgc2 = (self.cat_info[item['gc_name']][1], 6, '服装', gc1_id, 0, 0, 0, '', '', '')
                        self.cur.execute(gc_insert, lisgc2)
                        gc2_id = int(self.client.insert_id())

                    sql_gc3 = gc_select % (self.cat_info[item['gc_name']][2])
                    self.cur.execute(sql_gc3)
                    gc3_info = self.cur.fetchone()
                    if not gc3_info is None:
                        gc3_id = gc3_info[0]
                    else:
                        lisgc3 = (self.cat_info[item['gc_name']][2], 6, '服装', gc2_id, 0, 0, 0, '', '', '')
                        self.cur.execute(gc_insert, lisgc3)
                        gc3_id = int(self.client.insert_id())

                    # 添加属性，规格
                    ms_select = "select * from mall_spec where sp_name='%s'"
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
                        sql_ms = ms_select % (i_item)
                        self.cur.execute(sql_ms)
                        ms_info = self.cur.fetchone()
                        if not ms_info is None:
                            sp_id = ms_info[0]
                        else:
                            lisms = (i_item, 0, 0, '')
                            self.cur.execute(ms_insert, lisms)
                            sp_id = int(self.client.insert_id())
                        sp_name[sp_id] = i_item
                        # 添加类型规格关系表
                        sql_mts = mts_select % ('6', sp_id)
                        self.cur.execute(sql_mts)
                        mts_info = self.cur.fetchone()
                        if mts_info is None:
                            lismts = ('6', sp_id)
                            self.cur.execute(mts_insert, lismts)
                        # 添加规格的值
                        for c_item in item['goods_attr'][i_item]:
                            sql_msv = msv_select % (c_item, sp_id, gc3_id)
                            self.cur.execute(sql_msv)
                            msv_info = self.cur.fetchone()
                            if not msv_info is None:
                                sp_value_id = msv_info[0]
                            else:
                                lismsv = (c_item, sp_id, gc3_id, 1, '', 0)
                                self.cur.execute(msv_insert, lismsv)
                                sp_value_id = int(self.client.insert_id())
                            if sp_id in sp_val:
                                sp_val[sp_id].update({sp_value_id: c_item})
                                sp_val_list[sp_value_id] = c_item
                            else:
                                sp_val[sp_id] = {sp_value_id: c_item}
                                sp_val_list[sp_value_id] = c_item

                    # 开始添加商品了
                    # mall_goods_common
                    sp_name_tmp = phpserialize.dumps(sp_name).decode('utf-8')
                    sp_val_tmp = phpserialize.dumps(sp_val).decode('utf-8')
                    sqlcommon = 'insert into mall_goods_common' \
                                '(goods_name,goods_image,goods_price,goods_jingle,mobile_body,gc_id,gc_id_1,gc_id_2,gc_id_3,gc_name,store_id,store_name,spec_name,spec_value,brand_id,brand_name,goods_attr,goods_body,goods_state,goods_verify,goods_addtime,goods_selltime,goods_specname,goods_marketprice,goods_costprice,goods_discount,goods_serial,goods_storage_alarm,areaid_1,areaid_2,appoint_satedate,presell_deliverdate,goods_url,goods_jingle_other,shop_info,goods_image_old,is_support_voucher,transport_id,transport_title) ' \
                                'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    liscommon = (goods_name,goods_image,item['goods_price'],'',goods_desc,gc3_id,gc1_id,gc2_id,gc3_id,self.cat_info[item['gc_name']][2],'1','拼拼侠',sp_name_tmp,sp_val_tmp,self.brand_info[item['goods_brand']],item['goods_brand'],'N;',goods_desc,'1','1',now_time,now_time,item['goods_brand'],goods_marketprice,'0','100',goods_serial,'1','1','1',now_time,now_time,item['goods_url'],goods_jingle,shop_info,self.img_url,'1','11','拼拼侠通用运费模板')
                    self.cur.execute(sqlcommon, liscommon)
                    common_id = int(self.client.insert_id())
                    if common_id:
                        # 更新店铺信息
                        self.oper_shop(shop_name, shop_range, shop_ali, common_id, shop_mobile, shop_address)
                        # 处理商品相册
                        if not item['goods_images'] is None:
                            mgi_insert = 'insert into mall_goods_images (goods_commonid,store_id,color_id,goods_image,goods_image_sort,is_default) values (%s,%s,%s,%s,%s,%s)'
                            for goods_images_v in item['goods_images']:
                                goods_images_v = 'https:' + goods_images_v
                                # goods_images_v = self.down_imgs(goods_images_v)
                                goods_images_v = self.down_img(goods_images_v)
                                lismgi = (common_id, 1, 0, goods_images_v, 0, 0)
                                self.cur.execute(mgi_insert, lismgi)

                        sp_tmp = dict()
                        i = 1
                        for sp_val_item in sp_val:
                            sp_tmp[i] = sp_val[sp_val_item]
                            i += 1
                        for x in itertools.product(sp_tmp[1], sp_tmp[2]):
                            goods_sku_name = goods_name
                            sp_value = dict()
                            for x_i in x:
                                sp_value[x_i] = sp_val_list[x_i]
                                goods_sku_name += ' ' + sp_val_list[x_i]
                            sp_value_serilize = phpserialize.dumps(sp_value).decode('utf-8')
                            # mall_goods
                            sqlgoods = 'insert into mall_goods(goods_commonid,goods_name,goods_jingle,store_id,store_name,gc_id,gc_id_1,gc_id_2,gc_id_3,brand_id,goods_price,goods_tradeprice,goods_promotion_price,goods_promotion_type,goods_marketprice,goods_serial,goods_storage_alarm,goods_click,goods_salenum,goods_collect,goods_spec,goods_storage,goods_image,goods_state,goods_verify,goods_addtime,goods_edittime,areaid_1,areaid_2,color_id,goods_freight,goods_vat,goods_commend,goods_stcids,evaluation_good_star,evaluation_count,is_virtual,virtual_indate,virtual_limit,virtual_invalid_refund,is_fcode,is_appoint,is_presell,have_gift,is_own_shop,distribution_price_1,distribution_price_2,distribution_price_3,commission_percent,goods_jingle_other,transport_id)' \
                                       'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                            lisgoods = (common_id,goods_sku_name,'','1','拼拼侠',gc3_id,gc1_id,gc2_id,gc3_id,self.brand_info[item['goods_brand']],item['goods_price'],'0','0','0',goods_marketprice,'','1','1',goods_salenum,'1',sp_value_serilize,item['goods_storage'],goods_image,'1','1',now_time,now_time,'1','1','0','0','0','0','1','5','0','0','0','0','0','0','0','0','0','0','0','0','0','0',goods_jingle,'11')
                            self.cur.execute(sqlgoods, lisgoods)
                        self.client.commit()

        return item

    def down_img(self):
        import requests
        url = self.img_url
        datenow = time.strftime("%Y%m%d", time.localtime())
        arr = os.path.splitext(self.img_url)
        ext = re.findall(r".*?(.jpg|.png|.JPG|.PNG)", url)[0]
        hashname = hashlib.md5(self.img_url.encode(encoding='UTF-8')).hexdigest()
        filename = datenow + 'zz' + hashname + ext

        image_name = '{}_'.format(store_id) + filename
        path = image_path + '/' + image_name
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        if not os.path.exists(path):

            r = requests.get(url)
            code = r.status_code
            r.raise_for_status()
            try:
                # 使用with语句可以不用自己手动关闭已经打开的文件流
                with open(path, "wb") as f:  # 开始写文件，wb代表写二进制文件
                    f.write(r.content)
                print("爬取完成:{}".format(url))
                mylog.info(' INFO  |  {}  |  {}  |  {}'.format(image_name, code, url))
                return image_name
            except:
                print("爬取失败:{}".format(url))
                mylog.info(' ERROR  |  {}  |  {}  '.format(code, url))
                return self.img_url
        else:
            print("文件已存在")
            mylog.info(' INFO  |  {}  |  {}  |  {}'.format(image_name, '000', url))
            return image_name

    def down_imgs(self, goods_images_v):
        import requests
        url = goods_images_v
        datenow = time.strftime("%Y%m%d", time.localtime())
        arr = os.path.splitext(goods_images_v)
        ext = re.findall(r".*?(.jpg|.png|.JPG|.PNG)", url)[0]
        hashname = hashlib.md5(goods_images_v.encode(encoding='UTF-8')).hexdigest()
        filename = datenow + 'zz' + hashname + ext
        image_name = '{}_'.format(store_id) + filename
        path = image_path + '/' + image_name
        try:
            if not os.path.exists(image_path):
                os.makedirs(image_path)
            if not os.path.exists(path):
                r = requests.get(url)
                code = r.status_code
                r.raise_for_status()
                try:
                    # 使用with语句可以不用自己手动关闭已经打开的文件流
                    with open(path, "wb") as f:  # 开始写文件，wb代表写二进制文件
                        f.write(r.content)
                    print("爬取完成:{}".format(url))
                    mylog.info(' INFO  |  {}  |  {}  |  {}'.format(image_name, code, url))
                    return image_name
                except:
                    print("爬取失败:{}".format(url))
                    mylog.info(' ERROR  |  {}  |  {}  '.format(code, url))
                    return goods_images_v
            else:
                print("文件已存在")
                mylog.info(' INFO  |  {}  |  {}  |  {}'.format(image_name, '000', url))
                return image_name
        except Exception as e:
            # print("爬取失败:" + str(e))
            return goods_images_v

    def oper_shop(self, shop_name, shop_range, shop_ali, common_id, shop_mobile, shop_address):
        ms_select = "select * from mall_shop where goods_commonid='%s'"
        ms_insert = 'insert into mall_shop (shop_name,shop_range,shop_ali,shop_mobile,shop_wechat,shop_qq,shop_product,shop_address,goods_commonid) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        sql_ms = ms_select % (common_id)
        self.cur.execute(sql_ms)
        ms_info = self.cur.fetchone()
        if not ms_info is None:
            sqlupdategoods = "UPDATE mall_shop SET shop_name='%s',shop_range='%s',shop_ali='%s',shop_mobile='%s',shop_address='%s' WHERE shop_id=%s" % (shop_name, shop_range, shop_ali, shop_mobile, shop_address, ms_info[0])
            self.cur.execute(sqlupdategoods)
            sp_id = ms_info[0]
        else:
            lisms = (shop_name, shop_range, shop_ali, shop_mobile, '', '', '', shop_address, common_id)
            self.cur.execute(ms_insert, lisms)
            sp_id = int(self.client.insert_id())

        return sp_id

