import requests
import json
from multiprocessing import Queue
from handel_mysql import mysql_info
from concurrent.futures import ThreadPoolExecutor
#创建队列
queue_list = Queue()

def handel_request(url, data):
    header = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "appids":"srh_WbCH4sVmLE9rDJ5W",
        "Connection":"keep-alive",
        "Content-Length":"11",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie":"JSESSIONID=8b8a70f3-d269-4061-a207-ddb4700fafb1; Hm_lvt_4799f3a6bc2cf71582db80a438f0cdc6=1548657045; Hm_lpvt_4799f3a6bc2cf71582db80a438f0cdc6=1548657336",
        "Host":"ai.shenronghui.net",
        "Origin":"http://ai.shenronghui.net",
        "Referer":"http://ai.shenronghui.net/pharmacy//zhuantiLevel2.html?labelId=164&srh=1",
        "signs":"5da4658bceeb3ded6e3e1a04d06956d30f1129f86df729fda5b60dd4f230844e",
        "timestamps":"1548657367539",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest",
    }

    response = requests.post(url=url,headers=header,data=data)
    return response

def handle_index():
    url = 'http://ai.shenronghui.net/pharmacy/srh_api/getSectionHome2List'
    data = {
        "labelid":"164"
    }

    response = handel_request(url=url,data=data)
    index_response_dict = json.loads(response.text)
    for key in index_response_dict['data']:
        for index_item_i in index_response_dict['data'][key]:
            for item in index_item_i['goodsList']:
                data_2 = {
                    "goodsId":item['goodsId']
                }
                queue_list.put(data_2)

def handle_shenrong_list(data):
    shenrong_list_url = 'http://ai.shenronghui.net/pharmacy/srh_api/getGoodsById'
    shenrong_list_response = handel_request(url=shenrong_list_url,data=data)
    shenrong_response_dict = json.loads(shenrong_list_response.text)
    data_list = shenrong_response_dict['data']
    print('当前入库的商品是：',data_list['name'])
    mysql_info.oper_item(data_list)


handle_index()
# pool = ThreadPoolExecutor(max_workers=20)
while queue_list.qsize() > 0:
    # pool.submit(handle_shenrong_list,queue_list.get())
    handle_shenrong_list(queue_list.get())