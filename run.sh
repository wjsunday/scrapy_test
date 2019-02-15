#!/bin/bash

echo -n "\n ############ 爬取 商品列表（au51go） ################### \n"
cd /app/au51go/au51go/ && python main.py ;

echo -n "\n ############ 爬取 商品详情（au51gogoods） ############## \n"
cd /app/au51gogoods/au51gogoods && python main.py


echo -n "\n ############ 爬取 商品列表（soukuan） ################### \n"
cd /app/soukuan/soukuan/ && python main.py ;

echo -n "\n ############ 爬取 商品详情（soukuangoods） ############## \n"
cd /app/soukuangoods/soukuangoods && python main.py


echo -n "\n ############ 爬取 参茸（shenrong） ############## \n"
cd /app/shenrong && python shenrong_spider.py

