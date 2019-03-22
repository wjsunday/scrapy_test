#!/usr/bin/env python
# -*- coding: utf-8 -*-


# spec_info = {
#     "20000035": ["女装", "上装/外套", "T恤", "1", "", "", ""],
#     "20000018": ["女装", "上装/外套", "衬衫", "1", "", "", ""],
#     "20000019": ["女装", "上装/外套", "蕾丝衫/雪纺衫", "1", "", "", ""],
#     "20000068": ["女装", "上装/外套", "卫衣/绒衫", "1", "", "", ""],
#     "20000017": ["女装", "上装/外套", "毛衣", "1", "", "", ""],
#     "20000038": ["女装", "上装/外套", "毛针织衫", "1", "", "", ""],
#     "20000037": ["女装", "上装/外套", "毛针织套装", "1", "", "", ""],
#     "20000389": ["女装", "上装/外套", "时尚套装", "1", "", "", ""],
#     "20000025": ["女装", "上装/外套", "休闲运动套装", "1", "", "", ""],
#     "20000024": ["女装", "上装/外套", "其它套装", "1", "", "", ""],
#     "20000129": ["女装", "上装/外套", "短外套", "1", "", "", ""],
#     "20000128": ["女装", "上装/外套", "牛仔短外套", "1", "", "", ""],
#     "20000174": ["女装", "上装/外套", "毛呢外套", "1", "", "", ""],
#     "20000070": ["女装", "上装/外套", "棉衣/棉服", "1", "", "", ""],
#     "20000069": ["女装", "上装/外套", "羽绒服", "1", "", "", ""],
#     "20000175": ["女装", "上装/外套", "羽绒马夹", "1", "", "", ""],
#     "20000071": ["女装", "上装/外套", "风衣", "1", "", "", ""],
#     "20000176": ["女装", "上装/外套", "马夹", "1", "", "", ""],
#     "20000067": ["女装", "上装/外套", "西装", "1", "", "", ""],
#     "20000073": ["女装", "上装/外套", "皮衣", "1", "", "", ""],
#     "20000074": ["女装", "上装/外套", "皮草", "1", "", "", ""],
#     "20000364": ["女装", "上装/外套", "背心吊带", "1", "", "", ""],
#     "20000370": ["女装", "上装/外套", "抹胸", "1", "", "", ""],
#     "20000055": ["女装", "上装/外套", "旗袍", "1", "", "", ""],
#     "20000028": ["女装", "上装/外套", "民族服装/舞台装", "1", "", "", ""],
#     "20000052": ["女装", "上装/外套", "唐装/中式服饰上衣", "1", "", "", ""],
#     "20000072": ["女装", "上装/外套", "学生校服", "1", "", "", ""],
#     "20000027": ["女装", "上装/外套", "礼服/晚装", "1", "", "", ""],
#     "20000131": ["女装", "上装/外套", "酒店工作制服", "1", "", "", ""],
#     "20000005": ["女装", "上装/外套", "大码外套/马甲", "1", "", "", ""],
#     "20000012": ["女装", "上装/外套", "大码毛针织衫", "1", "", "", ""],
#     "20000007": ["女装", "上装/外套", "大码T恤", "1", "", "", ""],
#     "20000013": ["女装", "上装/外套", "大码套装", "1", "", "", ""],
#     "20000008": ["女装", "上装/外套", "大码衬衫", "1", "", "", ""],
#     "20000011": ["女装", "上装/外套", "大码卫衣/绒衫", "1", "", "", ""],
#     "20000002": ["女装", "上装/外套", "大码雪纺衫/雪纺衫", "1", "", "", ""],
#     "20000014": ["女装", "上装/外套", "其他大码女装", "1", "", "", ""],
#     "20000039": ["女装", "上装/外套", "中老年蕾丝衫/雪纺衫", "1", "", "", ""],
#     "20000042": ["女装", "上装/外套", "中老年T恤", "1", "", "", ""],
#     "20000046": ["女装", "上装/外套", "中老年外套/马甲", "1", "", "", ""],
#     "20000048": ["女装", "上装/外套", "中老年套装", "1", "", "", ""],
#     "20000106": ["女装", "裙装", "连衣裙", "1", "", "", ""],
#     "20000006": ["女装", "裙装", "大码连衣裙", "1", "", "", ""],
#     "20000041": ["女装", "裙装", "中老年连衣裙", "1", "", "", ""],
#     "20000001": ["女装", "裙装", "半身裙", "1", "", "", ""],
#     "20000000": ["女装", "裙装", "牛仔半身裙", "1", "", "", ""],
#     "20000010": ["女装", "裙装", "大码半身裙", "1", "", "", ""],
#     "20000044": ["女装", "裙装", "中老年半身裙", "1", "", "", ""],
#     "20000036": ["女装", "裙装", "毛针织裙", "1", "", "", ""],
#     "20000022": ["女装", "裙装", "职业女裙套装", "1", "", "", ""],
#     "20000054": ["女装", "裙装", "唐装/中式服饰裙子", "1", "", "", ""],
#     "20000026": ["女装", "裙装", "婚纱", "1", "", "", ""],
#     "20000021": ["女装", "裤装", "牛仔裤", "1", "", "", ""],
#     "20000020": ["女装", "裤装", "休闲裤", "1", "", "", ""],
#     "20000057": ["女装", "裤装", "打底裤", "1", "", "", ""],
#     "20000009": ["女装", "裤装", "大码裤子", "1", "", "", ""],
#     "20000291": ["女装", "裤装", "西装裤/正装裤", "1", "", "", ""],
#     "20000053": ["女装", "裤装", "唐装/中式服饰裤子", "1", "", "", ""],
#     "20000023": ["女装", "裤装", "职业女裤套装", "1", "", "", ""],
#     "20000040": ["女装", "裤装", "中老年裤子", "1", "", "", ""],
#     "20000340": ["女装", "裤装", "羽绒裤", "1", "", "", ""],
#     "20000341": ["女装", "裤装", "棉裤", "1", "", "", ""],
#     "20000078": ["男装", "上装/外套", "卫衣", "2", "", "", ""],
#     "20000076": ["男装", "上装/外套", "夹克", "2", "", "", ""],
#     "20000034": ["男装", "上装/外套", "针织衫/毛衣", "2", "", "", ""],
#     "20000424": ["男装", "上装/外套", "休闲运动套装", "2", "", "", ""],
#     "20000421": ["男装", "上装/外套", "其他套装", "2", "", "", ""],
#     "20000117": ["男装", "上装/外套", "背心", "2", "", "", ""],
#     "20000116": ["男装", "上装/外套", "马甲", "2", "", "", ""],
#     "20000120": ["男装", "上装/外套", "风衣", "2", "", "", ""],
#     "20000123": ["男装", "上装/外套", "皮衣", "2", "", "", ""],
#     "20000125": ["男装", "上装/外套", "棉衣", "2", "", "", ""],
#     "20000335": ["男装", "上装/外套", "毛呢大衣", "2", "", "", ""],
#     "20000079": ["男装", "上装/外套", "西服", "2", "", "", ""],
#     "20000113": ["男装", "上装/外套", "西服套装", "2", "", "", ""],
#     "20000115": ["男装", "上装/外套", "西装马甲", "2", "", "", ""],
#     "20000127": ["男装", "上装/外套", "羽绒服", "2", "", "", ""],
#     "20000056": ["男装", "上装/外套", "工装制服", "2", "", "", ""],
#     "20000077": ["男装", "上装/外套", "大码卫衣", "2", "", "", ""],
#     "20000033": ["男装", "上装/外套", "大码针织衫/毛衣", "2", "", "", ""],
#     "20000423": ["男装", "上装/外套", "大码休闲运动套装", "2", "", "", ""],
#     "20000420": ["男装", "上装/外套", "大码其他套装", "2", "", "", ""],
#     "20000124": ["男装", "上装/外套", "大码棉衣", "2", "", "", ""],
#     "20000126": ["男装", "上装/外套", "大码羽绒服", "2", "", "", ""],
#     "20000119": ["男装", "上装/外套", "大码风衣", "2", "", "", ""],
#     "20000122": ["男装", "上装/外套", "大码皮衣", "2", "", "", ""],
#     "20000334": ["男装", "上装/外套", "大码毛呢大衣", "2", "", "", ""],
#     "20000075": ["男装", "上装/外套", "中老年夹克", "2", "", "", ""],
#     "20000032": ["男装", "上装/外套", "中老年针织衫/毛衣", "2", "", "", ""],
#     "20000422": ["男装", "上装/外套", "中老年休闲运动套装", "2", "", "", ""],
#     "20000118": ["男装", "上装/外套", "中老年风衣", "2", "", "", ""],
#     "20000031": ["男装", "衬衫/T恤", "T恤", "2", "", "", ""],
#     "20000030": ["男装", "衬衫/T恤", "大码T恤", "2", "", "", ""],
#     "20000029": ["男装", "衬衫/T恤", "中老年T恤", "2", "", "", ""],
#     "20000109": ["男装", "衬衫/T恤", "衬衫", "2", "", "", ""],
#     "20000108": ["男装", "衬衫/T恤", "大码衬衫", "2", "", "", ""],
#     "20000107": ["男装", "衬衫/T恤", "中老年衬衫", "2", "", "", ""],
#     "20000090": ["男装", "衬衫/T恤", "Polo衫", "2", "", "", ""],
#     "20000089": ["男装", "衬衫/T恤", "大码Polo衫", "2", "", "", ""],
#     "20000088": ["男装", "衬衫/T恤", "中老年Polo衫", "2", "", "", ""],
#     "20000016": ["男装", "裤装", "休闲裤", "2", "", "", ""],
#     "20000015": ["男装", "裤装", "大码休闲裤", "2", "", "", ""],
#     "20000081": ["男装", "裤装", "牛仔裤", "2", "", "", ""],
#     "20000080": ["男装", "裤装", "大码牛仔裤", "2", "", "", ""],
#     "20000112": ["男装", "裤装", "西裤", "2", "", "", ""],
#     "20000111": ["男装", "裤装", "皮裤", "2", "", "", ""],
#     "20000339": ["男装", "裤装", "棉裤", "2", "", "", ""],
#     # "10000137": ["鞋", "女鞋", "低帮鞋", "3", "", "", ""],
#     # "10000135": ["鞋", "女鞋", "靴子", "3", "", "", ""],
#     # "10000136": ["鞋", "女鞋", "高帮鞋", "3", "", "", ""],
#     # "10000141": ["鞋", "女鞋", "低帮帆布鞋", "3", "", "", ""],
#     # "10000140": ["鞋", "女鞋", "高帮帆布鞋", "3", "", "", ""],
#     # "10000138": ["鞋", "女鞋", "拖鞋", "3", "", "", ""],
#     # "10000139": ["鞋", "女鞋", "凉鞋", "3", "", "", ""],
#     # "10000133": ["鞋", "女鞋", "雨鞋", "3", "", "", ""],
#     # "10000128": ["鞋", "男鞋", "低帮鞋", "3", "", "", ""],
#     # "10000126": ["鞋", "男鞋", "靴子", "3", "", "", ""],
#     # "10000127": ["鞋", "男鞋", "高帮鞋", "3", "", "", ""],
#     # "10000132": ["鞋", "男鞋", "低帮帆布鞋", "3", "", "", ""],
#     # "10000131": ["鞋", "男鞋", "高帮帆布鞋", "3", "", "", ""],
#     # "10000129": ["鞋", "男鞋", "拖鞋", "3", "", "", ""],
#     # "10000130": ["鞋", "男鞋", "凉鞋", "3", "", "", ""],
#     "20000058": ["内衣/家居", "内衣", "文胸", "4", "", "", ""],
#     "20000059": ["内衣/家居", "内衣", "内裤", "4", "", "", ""],
#     "20000060": ["内衣/家居", "内衣", "文胸套装", "4", "", "", ""],
#     "20000065": ["内衣/家居", "内衣", "抹胸", "4", "", "", ""],
#     "40000154": ["内衣/家居", "内衣", "短袜/打底袜/丝袜/美腿袜", "4", "", "", ""],
#     "20000083": ["内衣/家居", "内衣", "吊带", "4", "", "", ""],
#     "20000085": ["内衣/家居", "内衣", "背心", "4", "", "", ""],
#     "20000082": ["内衣/家居", "内衣", "T恤", "4", "", "", ""],
#     "20000165": ["内衣/家居", "内衣", "睡衣/家居服套装", "4", "", "", ""],
#     "20000064": ["内衣/家居", "内衣", "睡衣上装", "4", "", "", ""],
#     "20000161": ["内衣/家居", "内衣", "睡裤/家居裤", "4", "", "", ""],
#     "20000163": ["内衣/家居", "内衣", "睡裙", "4", "", "", ""],
#     "20000166": ["内衣/家居", "内衣", "睡袍/浴袍", "4", "", "", ""],
#     "20000164": ["内衣/家居", "内衣", "中老年睡衣/家居服套装", "4", "", "", ""],
#     "20000063": ["内衣/家居", "内衣", "中老年睡衣上装", "4", "", "", ""],
#     "20000160": ["内衣/家居", "内衣", "中老年睡裤/家居裤", "4", "", "", ""],
#     "20000162": ["内衣/家居", "内衣", "中老年睡裙", "4", "", "", ""],
#     "20000170": ["内衣/家居", "内衣", "保暖套装", "4", "", "", ""],
#     "20000062": ["内衣/家居", "内衣", "保暖上装", "4", "", "", ""],
#     "20000169": ["内衣/家居", "内衣", "保暖裤", "4", "", "", ""],
#     "20000171": ["内衣/家居", "内衣", "塑身连体衣", "4", "", "", ""],
#     "20000168": ["内衣/家居", "内衣", "塑身分体套装", "4", "", "", ""],
#     "20000061": ["内衣/家居", "内衣", "塑身上衣", "4", "", "", ""],
#     "20000167": ["内衣/家居", "内衣", "塑身美体裤", "4", "", "", ""],
#     "40000015": ["内衣/家居", "内衣", "塑身腰封/腰夹", "4", "", "", ""],
#     "40000169": ["内衣/家居", "内衣", "乳贴", "4", "", "", ""],
#     "40000170": ["内衣/家居", "内衣", "肩带", "4", "", "", ""],
#     "40000171": ["内衣/家居", "内衣", "插片/胸垫", "4", "", "", ""],
#     "20000103": ["儿童用品", "童装", "套装", "5", "", "", ""],
#     "20000158": ["儿童用品", "童装", "亲子装/亲子时装", "5", "", "", ""],
#     "20000374": ["儿童用品", "童装", "连衣裙", "5", "", "", ""],
#     "20000387": ["儿童用品", "童装", "半身裙", "5", "", "", ""],
#     "20000173": ["儿童用品", "童装", "T恤", "5", "", "", ""],
#     "20000096": ["儿童用品", "童装", "衬衫", "5", "", "", ""],
#     "20000102": ["儿童用品", "童装", "毛针织衫", "5", "", "", ""],
#     "20000091": ["儿童用品", "童装", "卫衣/绒衫", "5", "", "", ""],
#     "20000104": ["儿童用品", "童装", "牛仔外套", "5", "", "", ""],
#     "20000105": ["儿童用品", "童装", "普通外套", "5", "", "", ""],
#     "20000141": ["儿童用品", "童装", "风衣", "5", "", "", ""],
#     "20000095": ["儿童用品", "童装", "马甲", "5", "", "", ""],
#     "20000093": ["儿童用品", "童装", "夹克", "5", "", "", ""],
#     "20000092": ["儿童用品", "童装", "皮衣", "5", "", "", ""],
#     "20000094": ["儿童用品", "童装", "呢大衣", "5", "", "", ""],
#     "20000402": ["儿童用品", "童装", "羽绒服", "5", "", "", ""],
#     "20000398": ["儿童用品", "童装", "羽绒马甲", "5", "", "", ""],
#     "20000331": ["儿童用品", "童装", "西服/小西装", "5", "", "", ""],
#     "20000098": ["儿童用品", "童装", "棉袄/棉服", "5", "", "", ""],
#     "20000180": ["儿童用品", "童装", "牛仔裤", "5", "", "", ""],
#     "20000181": ["儿童用品", "童装", "棉裤", "5", "", "", ""],
#     "20000182": ["儿童用品", "童装", "裤子", "5", "", "", ""],
#     "20000345": ["儿童用品", "童装", "背心吊带", "5", "", "", ""],
#     "20000097": ["儿童用品", "童装", "披风/斗篷", "5", "", "", ""],
#     "40000004": ["儿童用品", "童装", "帽子", "5", "", "", ""],
#     "20000369": ["儿童用品", "童装", "家居服套装", "5", "", "", ""],
#     "20000375": ["儿童用品", "童装", "家居裙/睡裙", "5", "", "", ""],
#     "20000352": ["儿童用品", "童装", "内衣套装", "5", "", "", ""],
#     "20000361": ["儿童用品", "童装", "内裤", "5", "", "", ""],
#     "40000141": ["儿童用品", "童装", "儿童袜子(0-16岁)", "5", "", "", ""],
#     "20000099": ["儿童用品", "童装", "连身衣/爬服/哈衣", "5", "", "", ""],
#     "20000190": ["儿童用品", "童装", "婴儿礼盒", "5", "", "", ""],
#     "10000144": ["儿童用品", "童鞋", "皮鞋", "5", "", "", ""],
#     "10000064": ["儿童用品", "童鞋", "跑步鞋", "5", "", "", ""],
#     "10000088": ["儿童用品", "童鞋", "休闲鞋", "5", "", "", ""],
#     "10000143": ["儿童用品", "童鞋", "帆布鞋", "5", "", "", ""],
#     "10000148": ["儿童用品", "童鞋", "靴子", "5", "", "", ""],
#     "10000146": ["儿童用品", "童鞋", "凉鞋", "5", "", "", ""],
#     "10000145": ["儿童用品", "童鞋", "拖鞋", "5", "", "", ""],
#     "10000149": ["儿童用品", "童鞋", "亲子鞋", "5", "", "", ""],
#     "10000150": ["儿童用品", "童鞋", "学步鞋", "5", "", "", ""],
#     "10000065": ["儿童用品", "童鞋", "运动板鞋", "5", "", "", ""],
#     "10000066": ["儿童用品", "童鞋", "运动帆布鞋", "5", "", "", ""],
#     "10000068": ["儿童用品", "童鞋", "运动沙滩鞋/凉鞋", "5", "", "", ""],
#     "10000089": ["儿童用品", "童鞋", "其它运动鞋", "5", "", "", ""],
#     "40000011": ["配件箱包", "服装配饰", "围巾/丝巾/披肩", "6", "", "", ""],
#     "40000016": ["配件箱包", "服装配饰", "帽子", "6", "", "", ""],
#     "40000012": ["配件箱包", "服装配饰", "手套", "6", "", "", ""],
#     "40000017": ["配件箱包", "服装配饰", "耳套", "6", "", "", ""],
#     "40000029": ["配件箱包", "服装配饰", "二件套", "6", "", "", ""],
#     "40000030": ["配件箱包", "服装配饰", "三件套", "6", "", "", ""],
#     "40000014": ["配件箱包", "服装配饰", "腰带/皮带/腰链", "6", "", "", ""],
#     "40000020": ["配件箱包", "服装配饰", "假领", "6", "", "", ""],
#     "30000096": ["配件箱包", "服装配饰", "包挂件", "6", "", "", ""],
#     "40000033": ["配件箱包", "服装配饰", "其他配件", "6", "", "", ""],
#     # "20000246": ["运动户外", "运动", "比基尼", "7", "", "", ""],
#     # "20000250": ["运动户外", "运动", "连体泳衣", "7", "", "", ""],
#     # "20000248": ["运动户外", "运动", "分体泳衣", "7", "", "", ""],
#     # "20000251": ["运动户外", "运动", "男士泳衣", "7", "", "", ""],
#     # "20000252": ["运动户外", "运动", "儿童泳衣/裤", "7", "", "", ""],
#     # "20000249": ["运动户外", "运动", "中老年连体泳衣", "7", "", "", ""],
#     # "20000382": ["运动户外", "运动", "沙滩外套", "7", "", "", ""],
#     # "20000320": ["运动户外", "运动", "沙滩裤", "7", "", "", ""],
#     # "40000102": ["运动户外", "运动", "泳帽", "7", "", "", ""],
#     # "40000101": ["运动户外", "运动", "泳镜", "7", "", "", ""],
#     # "20000255": ["运动户外", "运动", "裹裙/披纱", "7", "", "", ""],
#     # "20000240": ["运动户外", "运动", "瑜伽服", "7", "", "", ""],
#     # "20000225": ["运动户外", "运动", "钢管舞服", "7", "", "", ""],
#     # "20000292": ["运动户外", "运动服", "运动套装", "7", "", "", ""],
#     # "20000139": ["运动户外", "运动服", "运动茄克", "7", "", "", ""],
#     # "20000178": ["运动户外", "运动服", "运动T恤", "7", "", "", ""],
#     # "20000134": ["运动户外", "运动服", "运动卫衣/套头衫", "7", "", "", ""],
#     # "20000293": ["运动户外", "运动服", "运动POLO衫", "7", "", "", ""],
#     # "20000179": ["运动户外", "运动服", "运动连衣裙", "7", "", "", ""],
#     # "20000140": ["运动户外", "运动服", "运动外套", "7", "", "", ""],
#     # "20000135": ["运动户外", "运动服", "运动风衣", "7", "", "", ""],
#     # "20000136": ["运动户外", "运动服", "运动棉衣", "7", "", "", ""],
#     # "20000302": ["运动户外", "运动服", "运动长裤", "7", "", "", ""],
#     # "20000303": ["运动户外", "运动服", "运动中长裤／短裤", "7", "", "", ""],
#     # "20000296": ["运动户外", "运动服", "健身套装", "7", "", "", ""],
#     # "20000294": ["运动户外", "运动服", "健身衣", "7", "", "", ""],
#     # "20000295": ["运动户外", "运动服", "健身裤", "7", "", "", ""],
#     # "20000310": ["运动户外", "运动服", "棒球服", "7", "", "", ""],
#     # "40000142": ["运动户外", "运动服", "运动袜", "7", "", "", ""],
#     # "40000042": ["运动户外", "运动服", "其他服饰配件", "7", "", "", ""],
#     # "10000004": ["户外运动", "运动鞋", "跑步鞋", "7", "", "", ""],
#     # "10000032": ["户外运动", "运动鞋", "休闲鞋", "7", "", "", ""],
#     # "10000031": ["户外运动", "运动鞋", "板鞋", "7", "", "", ""],
#     # "10000007": ["户外运动", "运动鞋", "其它运动鞋", "7", "", "", ""],
#     # "30000050": ["户外运动", "运动包", "单肩背包", "7", "", "", ""],
#     # "30000049": ["户外运动", "运动包", "双肩背包", "7", "", "", ""],
#     # "30000052": ["户外运动", "运动包", "挎包/拎包/休闲包", "7", "", "", ""],
#     # "30000051": ["户外运动", "运动包", "手包", "7", "", "", ""],
#     # "40000126": ["美妆饰品", "美妆", "项链", "8", "", "", ""],
#     # "40000127": ["美妆饰品", "美妆", "项坠/吊坠", "8", "", "", ""],
#     # "40000128": ["美妆饰品", "美妆", "手链", "8", "", "", ""],
#     # "40000129": ["美妆饰品", "美妆", "手镯", "8", "", "", ""],
#     # "40000136": ["美妆饰品", "美妆", "脚链", "8", "", "", ""],
#     # "40000130": ["美妆饰品", "美妆", "戒指/指环", "8", "", "", ""],
#     # "40000132": ["美妆饰品", "美妆", "耳环", "8", "", "", ""],
#     # "40000133": ["美妆饰品", "美妆", "耳钉", "8", "", "", ""],
#     # "40000131": ["美妆饰品", "美妆", "发饰", "8", "", "", ""],
#     # "40000137": ["美妆饰品", "美妆", "胸针", "8", "", "", ""],
#     # "40000139": ["美妆饰品", "美妆", "其它首饰", "8", "", "", ""],
#     # "40000140": ["美妆饰品", "美妆", "其他DIY饰品配件", "8", "", "", ""],
#     "20000144": ["孕妇装", "孕妇装", "连衣裙", "9", "", "", ""],
#     "20000321": ["孕妇装", "孕妇装", "孕妇裤/托腹裤", "9", "", "", ""],
#     "20000148": ["孕妇装", "孕妇装", "套装", "9", "", "", ""],
#     "20000147": ["孕妇装", "孕妇装", "T恤", "9", "", "", ""],
#     "20000145": ["孕妇装", "孕妇装", "毛衣", "9", "", "", ""],
#     "20000146": ["孕妇装", "孕妇装", "针织衫", "9", "", "", ""],
#     "20000151": ["孕妇装", "孕妇装", "卫衣/绒衫", "9", "", "", ""],
#     "20000143": ["孕妇装", "孕妇装", "外套/风衣", "9", "", "", ""],
#     "20000152": ["孕妇装", "孕妇装", "马甲", "9", "", "", ""],
#     "20000325": ["孕妇装", "孕妇装", "棉衣", "9", "", "", ""],
#     "20000324": ["孕妇装", "孕妇装", "羽绒服", "9", "", "", ""],
#     "20000326": ["孕妇装", "孕妇装", "大衣", "9", "", "", ""],
#     "20000323": ["孕妇装", "孕妇装", "半身裙", "9", "", "", ""],
#     "20000150": ["孕妇装", "孕妇装", "衬衫", "9", "", "", ""],
#     "20000153": ["孕妇装", "孕妇装", "吊带/背心", "9", "", "", ""],
#     "20000149": ["孕妇装", "孕妇装", "雪纺衫", "9", "", "", ""],
#     "20000360": ["孕妇装", "孕妇装", "家居服套装", "9", "", "", ""],
#     "20000350": ["孕妇装", "孕妇装", "家居裙", "9", "", "", ""],
#     "20000365": ["孕妇装", "孕妇装", "家居服上装", "9", "", "", ""],
#     "20000383": ["孕妇装", "孕妇装", "家居裤", "9", "", "", ""],
#     "20000380": ["孕妇装", "孕妇装", "家居袍", "9", "", "", ""],
#     "20000328": ["孕妇装", "孕妇装", "其它", "9", "", "", ""],
#     "20000412": ["孕妇装", "孕妇装", "哺乳衣", "9", "", "", ""],
#     "20000243": ["孕妇装", "孕妇装", "哺乳文胸", "9", "", "", ""],
#     "20000348": ["孕妇装", "孕妇装", "哺乳吊带", "9", "", "", ""],
#     "20000157": ["孕妇装", "孕妇装", "防辐射围裙", "9", "", "", ""],
#     "20000156": ["孕妇装", "孕妇装", "防辐射肚兜/护胎宝", "9", "", "", ""],
#     "20000244": ["孕妇装", "孕妇装", "内裤", "9", "", "", ""],
#     "40000155": ["孕妇装", "孕妇装", "孕妇袜/连裤袜/打底袜", "9", "", "", ""],
#     "20000087": ["孕妇装", "孕妇装", "(文胸-内裤)套装", "9", "", "", ""],
#     "20000354": ["孕妇装", "孕妇装", "秋衣裤套装", "9", "", "", ""],
#     "20000384": ["孕妇装", "孕妇装", "秋衣", "9", "", "", ""],
#     "40000163": ["孕妇装", "孕妇装", "束腹带", "9", "", "", ""],
#     "20000385": ["孕妇装", "孕妇装", "塑身裤", "9", "", "", ""],
#     "40000115": ["孕妇装", "孕妇装", "产妇帽", "9", "", "", ""],
#     "20000051": ["孕妇装", "孕妇装", "其它孕妇装", "9", "", "", ""],
#     "30000001": ["配件箱包", "箱包", "女士包袋", "6", "", "", ""],
#     "30000000": ["配件箱包", "箱包", "男士包袋", "6", "", "", ""],
#     "30000009": ["配件箱包", "箱包", "双肩背包", "6", "", "", ""],
#     "30000004": ["配件箱包", "箱包", "钱包", "6", "", "", ""],
#     "30000003": ["配件箱包", "箱包", "旅行袋", "6", "", "", ""],
#     "30000002": ["配件箱包", "箱包", "旅行箱", "6", "", "", ""],
#     "30000006": ["配件箱包", "箱包", "手机包", "6", "", "", ""],
#     "30000005": ["配件箱包", "箱包", "卡包", "6", "", "", ""],
#     "30000007": ["配件箱包", "箱包", "钥匙包", "6", "", "", ""],
#     "30000008": ["配件箱包", "箱包", "证件包", "6", "", "", ""],
#     "30000100": ["配件箱包", "箱包", "箱包相关配件", "6", "", "", ""],
# }

spec_info = {
    # "20000035": ["女装", "上装/外套", "T恤", "1", "", "", ""],
    # "20000018": ["女装", "上装/外套", "衬衫", "1", "", "", ""],
    "20000068": ["女装", "上装/外套", "卫衣/绒衫", "1", "", "", ""],
}

url_info ={
    # T恤
    "20000035":[
        # 'https://www.vvic.com/item/8419573',
        # 'https://www.vvic.com/item/8351228',
        # 'https://www.vvic.com/item/9815764',
        # 'https://www.vvic.com/item/8419574',
        # 'https://www.vvic.com/item/9164794',
        # 'https://www.vvic.com/item/13275990',
        # 'https://www.vvic.com/item/13175701',
        # 'https://www.vvic.com/item/8435498',
        # 'https://www.vvic.com/item/8419585',
        # 'https://www.vvic.com/item/9053521',
        # 'https://www.vvic.com/item/9972639',
        # 'https://www.vvic.com/item/8419580',
        # 'https://www.vvic.com/item/8599477',
        # 'https://www.vvic.com/item/8583809',
        # 'https://www.vvic.com/item/12876377',
        # 'https://www.vvic.com/item/8505640',
        # 'https://www.vvic.com/item/8435509',
        # 'https://www.vvic.com/item/13086807',
        # 'https://www.vvic.com/item/13404526',
        # 'https://www.vvic.com/item/8435520',
        # 'https://www.vvic.com/item/13077195',
        # 'https://www.vvic.com/item/13366507',
        'https://www.vvic.com/item/13089675',
        'https://www.vvic.com/item/13233028',
        'https://www.vvic.com/item/10804200',
        'https://www.vvic.com/item/9833069',
        'https://www.vvic.com/item/13295126',
        'https://www.vvic.com/item/13107174',
        'https://www.vvic.com/item/4158512',
        'https://www.vvic.com/item/13257953',
        'https://www.vvic.com/item/13389385',
        'https://www.vvic.com/item/10085269',
        # 'https://www.vvic.com/item/12626160',
        # 'https://www.vvic.com/item/12968918',
        # 'https://www.vvic.com/item/8299280',
        # 'https://www.vvic.com/item/13167827',
        # 'https://www.vvic.com/item/13098127',
        # 'https://www.vvic.com/item/11764311',
        # 'https://www.vvic.com/item/13532275',
        # 'https://www.vvic.com/item/9204737',
        # 'https://www.vvic.com/item/12467599',
        # 'https://www.vvic.com/item/8593023',
        # 'https://www.vvic.com/item/3752054',
        # 'https://www.vvic.com/item/13171981',
        # 'https://www.vvic.com/item/13171244 ',
        # 'https://www.vvic.com/item/8811471',
        # 'https://www.vvic.com/item/13360728',
        # 'https://www.vvic.com/item/10913225',
        # 'https://www.vvic.com/item/13303087',
        # 'https://www.vvic.com/item/13446789',
        # 'https://www.vvic.com/item/13101664',
        # 'https://www.vvic.com/item/10635224',
        # 'https://www.vvic.com/item/12351958',
        # 'https://www.vvic.com/item/13168836',
        # 'https://www.vvic.com/item/13523008',
    #     'https://www.vvic.com/item/9084016',
    #     'https://www.vvic.com/item/12432465',
    #     'https://www.vvic.com/item/13468022',
    #     'https://www.vvic.com/item/12737443',
    #     'https://www.vvic.com/item/9281788',
    #     'https://www.vvic.com/item/13035236',
    #     'https://www.vvic.com/item/13271144',
    #     'https://www.vvic.com/item/13053666',
    #     'https://www.vvic.com/item/13220284',
    #     'https://www.vvic.com/item/13479424',
    #     'https://www.vvic.com/item/13395603',
    #     'https://www.vvic.com/item/13411013',
    #     'https://www.vvic.com/item/13196651',
    #     'https://www.vvic.com/item/10011300',
    #     'https://www.vvic.com/item/13314319',
    #     'https://www.vvic.com/item/13402585',
    #     'https://www.vvic.com/item/13552259',
    #     'https://www.vvic.com/item/8618333',
    #     'https://www.vvic.com/item/13109084',
    #     'https://www.vvic.com/item/12948320',
    #     'https://www.vvic.com/item/13485932',
    #     'https://www.vvic.com/item/13507674',
    #     'https://www.vvic.com/item/13558702',
    #     'https://www.vvic.com/item/13165073',
    #     'https://www.vvic.com/item/13159164',
    #     'https://www.vvic.com/item/13468086',
    #     'https://www.vvic.com/item/13414376',
    #     'https://www.vvic.com/item/13378317',
    #     'https://www.vvic.com/item/12832620',
    #     'https://www.vvic.com/item/12755598',
    #     'https://www.vvic.com/item/13407225',
    #     'https://www.vvic.com/item/13370438',
    #     'https://www.vvic.com/item/12223503',
    #     'https://www.vvic.com/item/12937462',
    #     'https://www.vvic.com/item/13473199',
    #     'https://www.vvic.com/item/12992681',
    #     'https://www.vvic.com/item/13535678',
    #     'https://www.vvic.com/item/10642655',
    #     'https://www.vvic.com/item/12839160',
    #     'https://www.vvic.com/item/13303087',
    #     'https://www.vvic.com/item/13280475',
    #     'https://www.vvic.com/item/13301387',
        # 'https://www.vvic.com/item/5065433',
        # 'https://www.vvic.com/item/7596395',
    ],

    # 半身裙
    "20000001":[
        # 'https://www.vvic.com/item/12378211',
        # 'https://www.vvic.com/item/8916145',
        # 'https://www.vvic.com/item/13222346',
        # 'https://www.vvic.com/item/12323846',
        # 'https://www.vvic.com/item/12945600',
    #     'https://www.vvic.com/item/13113488',
    #     'https://www.vvic.com/item/12285561',
    #     'https://www.vvic.com/item/8895858',
    #     'https://www.vvic.com/item/12489101',
    #     'https://www.vvic.com/item/3085246',
    #
    ],

    #背心
    # "20000364": [
    #     'https://www.vvic.com/item/12929262',
    #     'https://www.vvic.com/item/12914156',
    #     'https://www.vvic.com/item/13068174',
    #     'https://www.vvic.com/item/9190545',
    #
    #
    # ],
    # 衬衫
    "20000018": [
        # 'https://www.vvic.com/item/10074545',
        # 'https://www.vvic.com/item/12049125',
        # 'https://www.vvic.com/item/12165625',
        # 'https://www.vvic.com/item/12685899',
    #
    ],
    # #打底裤
    # "20000057": [
    #     'https://www.vvic.com/item/11641624',
    # ],
    #短裤
    # "21000003": [
    #     'https://www.vvic.com/item/13211639',
    # ],
    #蕾丝衫
    # "20000039": [
    #     'https://www.vvic.com/item/13107523',
    #     'https://www.vvic.com/item/13044522',
    # ],
    # 连衣裙
    "20000106": [
        # 'https://www.vvic.com/item/11567923',
        # 'https://www.vvic.com/item/12711724',
        # 'https://www.vvic.com/item/13125773',
        # 'https://www.vvic.com/item/13494908',
        # 'https://www.vvic.com/item/11485509',
        # 'https://www.vvic.com/item/13581910',
        # 'https://www.vvic.com/item/13578588',
        # 'https://www.vvic.com/item/12296474',
        # 'https://www.vvic.com/item/10791089',
        # 'https://www.vvic.com/item/13527199',
        # 'https://www.vvic.com/item/10225707',
        # 'https://www.vvic.com/item/12967756',
        # 'https://www.vvic.com/item/13107541',
        # 'https://www.vvic.com/item/7635234',
        # 'https://www.vvic.com/item/13018527',
        # 'https://www.vvic.com/item/13230810',
    ],
    #抹胸
    # "20000370": [
    #     'https://www.vvic.com/item/12958908',
    #     'https://www.vvic.com/item/8094606',
    #     'https://www.vvic.com/item/7763163',
    #     'https://www.vvic.com/item/13208583',
    #     'https://www.vvic.com/item/9494386',
    #     'https://www.vvic.com/item/8198603',
    #
    # ],
    #牛仔裤
    "20000021": [
        # 'https://www.vvic.com/item/13041394',
        # 'https://www.vvic.com/item/12919664',
        # 'https://www.vvic.com/item/10204941',
    #     'https://www.vvic.com/item/11174538',
    #     'https://www.vvic.com/item/13262966',
    #     'https://www.vvic.com/item/10213437',
    ],
    # #配饰、袜子
    # "20000004": [
    #     'https://www.vvic.com/item/10007348',
    #     'https://www.vvic.com/item/9623542',
    #     'https://www.vvic.com/item/9826841',
    #     'https://www.vvic.com/item/10341502',
    #
    # ],

    #套装
    "20000389": [
        # 'https://www.vvic.com/item/9021504',
        # 'https://www.vvic.com/item/13027870',
        # 'https://www.vvic.com/item/13293482',
        # 'https://www.vvic.com/item/13370850',
        # 'https://www.vvic.com/item/5409120',
        # 'https://www.vvic.com/item/13389847',
    #     'https://www.vvic.com/item/10249701',
    # #     'https://www.vvic.com/item/9495941',
    # #     'https://www.vvic.com/item/13332525',
    # #     'https://www.vvic.com/item/13487907',
    ],

    #卫衣
    "20000068": [
        # 'https://www.vvic.com/item/11120648',
    ],
    #西装
    "20000067": [
        # 'https://www.vvic.com/item/13303892',
        # 'https://www.vvic.com/item/13495677',
        # 'https://www.vvic.com/item/12872802',
        # 'https://www.vvic.com/item/13129062',
        # 'https://www.vvic.com/item/13171444',
        # 'https://www.vvic.com/item/13029127',
        # 'https://www.vvic.com/item/13115734',
        # 'https://www.vvic.com/item/13365518',
        # 'https://www.vvic.com/item/13416829',
        # 'https://www.vvic.com/item/13568937',
        # 'https://www.vvic.com/item/13399631',
        # 'https://www.vvic.com/item/10140462',
        # 'https://www.vvic.com/item/13188812',
        # 'https://www.vvic.com/item/13553522',
        # 'https://www.vvic.com/item/13413167',
        # 'https://www.vvic.com/item/13375614',
        # 'https://www.vvic.com/item/10818078',
        # 'https://www.vvic.com/item/13447555',
        # 'https://www.vvic.com/item/13129062',
        # 'https://www.vvic.com/item/13522575',
        # 'https://www.vvic.com/item/10463927',
        # 'https://www.vvic.com/item/13110927',
    ],

    #小衫
    "21000001": [
        # 'https://www.vvic.com/item/9558086',
        # 'https://www.vvic.com/item/13169697',
    ],

    # 休闲裤
    "20000020": [
        # 'https://www.vvic.com/item/9750308',
        # 'https://www.vvic.com/item/9859155',
        # 'https://www.vvic.com/item/11502310',
        # 'https://www.vvic.com/item/12847822',
        # 'https://www.vvic.com/item/8220806',
        # 'https://www.vvic.com/item/9779101',
        # 'https://www.vvic.com/item/10449122',
        # 'https://www.vvic.com/item/12899357',
        # 'https://www.vvic.com/item/13274640',
        # 'https://www.vvic.com/item/11137090',
        # 'https://www.vvic.com/item/11776727',
        # 'https://www.vvic.com/item/13021789',
        # 'https://www.vvic.com/item/6327663',
        # 'https://www.vvic.com/item/7892576',
        # 'https://www.vvic.com/item/11117204',
        # 'https://www.vvic.com/item/12449800',
        # 'https://www.vvic.com/item/8264227',
        # 'https://www.vvic.com/item/6678591',
        # 'https://www.vvic.com/item/4965553',
        # 'https://www.vvic.com/item/4845402',
        # 'https://www.vvic.com/item/7565158',
        # 'https://www.vvic.com/item/7892576',
        # 'https://www.vvic.com/item/7873630',
        # 'https://www.vvic.com/item/5518833',
    #     'https://www.vvic.com/item/11049768',
    #     'https://www.vvic.com/item/12605873',
    #     'https://www.vvic.com/item/6613511',
    #     'https://www.vvic.com/item/13178914',
    #     'https://www.vvic.com/item/12966507',
    #     'https://www.vvic.com/item/7877794',
    ],

    }