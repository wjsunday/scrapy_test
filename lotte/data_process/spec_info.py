#!/usr/bin/env python
# -*- coding: utf-8 -*-

spec_info = {
    '1200009': ['护肤', '基础护肤', '保湿喷雾', '1200001', '1200002', '', ''],
    '10007919': ['护肤', '基础护肤', '护肤套装', '1200001', '1200002', '', ''],
    '1200003': ['护肤', '基础护肤', '化妆水', '1200001', '1200002', '', ''],
    '1200005': ['护肤', '基础护肤', '精华', '1200001', '1200002', '', ''],
    '1200007': ['护肤', '基础护肤', '脸部精油', '1200001', '1200002', '', ''],
    '1200010': ['护肤', '基础护肤', '面膜', '1200001', '1200002', '', ''],
    '1200006': ['护肤', '基础护肤', '面霜', '1200001', '1200002', '', ''],
    '1200004': ['护肤', '基础护肤', '乳液', '1200001', '1200002', '', ''],
    '10007872': ['护肤', '基础护肤', '​特殊护理', '1200001', '1200002', '', ''],
    '1200008': ['护肤', '基础护肤', '眼部/颈部护理', '1200001', '1200002', '', ''],
    '10009475': ['护肤', '洁面', '美容用品', '1200001', '1200018', '', ''],
    '1200026': ['护肤', '洁面', '磨砂/去角质', '1200001', '1200018', '', ''],
    '10007877': ['护肤', '洁面', '特殊护理', '1200001', '1200018', '', ''],
    '1200022': ['护肤', '洁面', '洗面奶', '1200001', '1200018', '', ''],
    '1200025': ['护肤', '洁面', '香皂', '1200001', '1200018', '', ''],
    '1200021': ['护肤', '洁面', '卸妆乳/霜', '1200001', '1200018', '', ''],
    '1200024': ['护肤', '洁面', '卸妆湿巾', '1200001', '1200018', '', ''],
    '1200020': ['护肤', '洁面', '卸妆油', '1200001', '1200018', '', ''],
    '1200023': ['护肤', '洁面', '卸妆啫喱/水', '1200001', '1200018', '', ''],
    '1200019': ['护肤', '洁面', '眼部/唇部卸妆', '1200001', '1200018', '', ''],
    '1200014': ['护肤', '防晒', '防晒棒', '1200001', '1200011', '', ''],
    '1200013': ['护肤', '防晒', '防晒喷雾', '1200001', '1200011', '', ''],
    '1200015': ['护肤', '防晒', '防晒气垫粉 ', '1200001', '1200011', '', ''],
    '1200012': ['护肤', '防晒', '防晒霜', '1200001', '1200011', '', ''],
    '1200017': ['护肤', '防晒', '美黑产品', '1200001', '1200011', '', ''],
    '1200016': ['护肤', '防晒', '晒后修复', '1200001', '1200011', '', ''],
    '1200047': ['护肤', '美容工具', '按摩仪', '1200001', '1200045', '', ''],
    '1200048': ['护肤', '美容工具', '皮脂/角质护理', '1200001', '1200045', '', ''],
    '1200049': ['护肤', '美容工具', '洁面器', '1200001', '1200045', '', ''],
    '1200046': ['护肤', '美容工具', '剃须刀', '1200001', '1200045', '', ''],
    '1200033': ['护肤', '男士护肤', '唇部护理', '1200001', '1200027', '', ''],
    '1200035': ['护肤', '男士护肤', '防晒', '1200001', '1200027', '', ''],
    '10007920': ['护肤', '男士护肤', '护肤套装', '1200001', '1200027', '', ''],
    '1200454': ['护肤', '男士护肤', '化妆品', '1200001', '1200027', '', ''],
    '1200028': ['护肤', '男士护肤', '化妆水', '1200001', '1200027', '', ''],
    '1200030': ['护肤', '男士护肤', '精华', '1200001', '1200027', '', ''],
    '1200034': ['护肤', '男士护肤', '面膜', '1200001', '1200027', '', ''],
    '1200031': ['护肤', '男士护肤', '面霜', '1200001', '1200027', '', ''],
    '1200038': ['护肤', '男士护肤', '美体/美发', '1200001', '1200027', '', ''],
    '1200029': ['护肤', '男士护肤', '乳液', '1200001', '1200027', '', ''],
    '10007873': ['护肤', '男士护肤', '特殊护理', '1200001', '1200027', '', ''],
    '1200036': ['护肤', '男士护肤', '剃须/须后护理', '1200001', '1200027', '', ''],
    '1200037': ['护肤', '男士护肤', '洗面奶', '1200001', '1200027', '', ''],
    '1200032': ['护肤', '男士护肤', '眼部/颈部护理', '1200001', '1200027', '', ''],
    '1200043': ['护肤', '婴幼儿护肤', '防晒霜', '1200001', '1200039', '', ''],
    '10007878': ['护肤', '婴幼儿护肤', '洁面', '1200001', '1200039', '', ''],
    '1200044': ['护肤', '婴幼儿护肤', '沐浴液/洗发液', '1200001', '1200039', '', ''],
    '1200040': ['护肤', '婴幼儿护肤', '润肤乳', '1200001', '1200039', '', ''],
    '1200041': ['护肤', '婴幼儿护肤', '润肤霜/护臀霜', '1200001', '1200039', '', ''],
    '1200042': ['护肤', '婴幼儿护肤', '润肤油', '1200001', '1200039', '', ''],
    '10007874': ['护肤', '婴幼儿护肤', '​特殊护理', '1200001', '1200039', '', ''],
    # '1200052': ['彩妆', '底妆', 'BB/CC霜', '1200050', '1200051', '', ''],
    # '1200058': ['彩妆', '底妆', '粉底液', '1200050', '1200051', '', ''],
    # '1200056': ['彩妆', '底妆', '两用粉饼/粉饼', '1200050', '1200051', '', ''],
    # '1200054': ['彩妆', '底妆', '蜜粉', '1200050', '1200051', '', ''],
    # '1200057': ['彩妆', '底妆', '气垫粉', '1200050', '1200051', '', ''],
    # '1200059': ['彩妆', '底妆', '阴影/腮红/高光', '1200050', '1200051', '', ''],
    # '1200053': ['彩妆', '底妆', '妆前乳/隔离霜', '1200050', '1200051', '', ''],
    # '1200055': ['彩妆', '底妆', '遮瑕膏', '1200050', '1200051', '', ''],
    # '1200067': ['彩妆', '唇妆', '唇彩', '1200050', '1200065', '', ''],
    # '1200070': ['彩妆', '唇妆', '唇膏笔/唇线笔', '1200050', '1200065', '', ''],
    # '1200066': ['彩妆', '唇妆', '口红', '1200050', '1200065', '', ''],
    # '1200068': ['彩妆', '唇妆', '润唇膏', '1200050', '1200065', '', ''],
    # '1200069': ['彩妆', '唇妆', '染唇液', '1200050', '1200065', '', ''],
    # '1200064': ['彩妆', '眼妆', '睫毛膏', '1200050', '1200060', '', ''],
    # '1200061': ['彩妆', '眼妆', '眉笔', '1200050', '1200060', '', ''],
    # '1200063': ['彩妆', '眼妆', '眼线', '1200050', '1200060', '', ''],
    # '1200062': ['彩妆', '眼妆', '眼影', '1200050', '1200060', '', ''],
    # '1200073': ['彩妆', '套装/综合彩盘', '眼妆套装', '1200050', '1200071', '', ''],
    # '1200075': ['彩妆', '套装/综合彩盘', '综合彩盘', '1200050', '1200071', '', ''],
    # '1200072': ['彩妆', '套装/综合彩盘', '底妆套装', '1200050', '1200071', '', ''],
    # '1200074': ['彩妆', '套装/综合彩盘', '唇妆套装', '1200050', '1200071', '', ''],
    # '1200084': ['彩妆', '化妆工具/空盒', '化妆刷', '1200050', '1200082', '', ''],
    # '1200083': ['彩妆', '化妆工具/空盒', '粉扑/海绵', '1200050', '1200082', '', ''],
    # '1200085': ['彩妆', '化妆工具/空盒', '睫毛夹', '1200050', '1200082', '', ''],
    # '10011308': ['彩妆', '化妆工具/空盒', '化妆包', '1200050', '1200082', '', ''],
    # '1200086': ['彩妆', '化妆工具/空盒', '化妆棉/吸油纸', '1200050', '1200082', '', ''],
    # '1200455': ['彩妆', '化妆工具/空盒', '化妆品空盒', '1200050', '1200082', '', ''],
    # '1200089': ['彩妆', '化妆工具/空盒', '口红盒/眼影盒', '1200050', '1200082', '', ''],
    # '1200087': ['彩妆', '化妆工具/空盒', '镜子', '1200050', '1200082', '', ''],
    # '1200088': ['彩妆', '化妆工具/空盒', '削笔刀/镊子', '1200050', '1200082', '', ''],
    # '1200090': ['彩妆', '化妆工具/空盒', '蜜粉盒/粉底盒', '1200050', '1200082', '', ''],
    # '1200077': ['彩妆', '美甲', '指甲油', '1200050', '1200076', '', ''],
    # '1200078': ['彩妆', '美甲', '护甲油', '1200050', '1200076', '', ''],
    # '1200081': ['彩妆', '美甲', '美甲套装', '1200050', '1200076', '', ''],
    # '1200080': ['彩妆', '美甲', '美甲工具', '1200050', '1200076', '', ''],
    # '1200079': ['彩妆', '美甲', '洗甲水', '1200050', '1200076', '', ''],
    '1200093': ['香水/美体/美发', '女士香水', '~30ml', '1200091', '1200092', '', ''],
    '1200094': ['香水/美体/美发', '女士香水', '31~50ml', '1200091', '1200092', '', ''],
    '1200095': ['香水/美体/美发', '女士香水', '51~100ml', '1200091', '1200092', '', ''],
    '1200096': ['香水/美体/美发', '女士香水', '101ml~', '1200091', '1200092', '', ''],
    '1200097': ['香水/美体/美发', '女士香水', '套装', '1200091', '1200092', '', ''],
    '1200129': ['香水/美体/美发', '美发', '洗发露', '1200091', '1200128', '', ''],
    '1200132': ['香水/美体/美发', '美发', '护发喷雾/护发精油', '1200091', '1200128', '', ''],
    '1200133': ['香水/美体/美发', '美发', '美发造型', '1200091', '1200128', '', ''],
    '1200462': ['香水/美体/美发', '美发', '头皮/脱发护理', '1200091', '1200128', '', ''],
    '1200130': ['香水/美体/美发', '美发', '护发素/护发营养', '1200091', '1200128', '', ''],
    '1200131': ['香水/美体/美发', '美发', '精华液/发膜', '1200091', '1200128', '', ''],
    '1200134': ['香水/美体/美发', '美发', '洗护套装', '1200091', '1200128', '', ''],
    '1200126': ['香水/美体/美发', '美体', '护手/护足', '1200091', '1200119', '', ''],
    '1200127': ['香水/美体/美发', '美体', '口腔用品', '1200091', '1200119', '', ''],
    '1200121': ['香水/美体/美发', '美体', '磨砂膏', '1200091', '1200119', '', ''],
    '1200461': ['香水/美体/美发', '美体', '美体套装', '1200091', '1200119', '', ''],
    '1200120': ['香水/美体/美发', '美体', '沐浴露', '1200091', '1200119', '', ''],
    '1200122': ['香水/美体/美发', '美体', '润肤乳/润肤霜', '1200091', '1200119', '', ''],
    '1200460': ['香水/美体/美发', '美体', '剃毛用品', '1200091', '1200119', '', ''],
    '1200125': ['香水/美体/美发', '美体', '体香剂', '1200091', '1200119', '', ''],
    '1200124': ['香水/美体/美发', '美体', '纤体乳', '1200091', '1200119', '', ''],
    '1200123': ['香水/美体/美发', '美体', '滋润油/喷雾', '1200091', '1200119', '', ''],
    '1200099': ['香水/美体/美发', '男士香水', '~30ml', '1200091', '1200098', '', ''],
    '1200100': ['香水/美体/美发', '男士香水', '31~50ml', '1200091', '1200098', '', ''],
    '1200101': ['香水/美体/美发', '男士香水', '51~100ml', '1200091', '1200098', '', ''],
    '1200102': ['香水/美体/美发', '男士香水', '101ml~', '1200091', '1200098', '', ''],
    '1200103': ['香水/美体/美发', '男士香水', '套装', '1200091', '1200098', '', ''],
    '1200105': ['香水/美体/美发', '中性香水', '~30ml', '1200091', '1200104', '', ''],
    '1200106': ['香水/美体/美发', '中性香水', '31~50ml', '1200091', '1200104', '', ''],
    '1200107': ['香水/美体/美发', '中性香水', '51~100ml', '1200091', '1200104', '', ''],
    '1200108': ['香水/美体/美发', '中性香水', '101ml~', '1200091', '1200104', '', ''],
    '1200109': ['香水/美体/美发', '中性香水', '套装', '1200091', '1200104', '', ''],

}




