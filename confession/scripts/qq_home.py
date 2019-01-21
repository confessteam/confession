#coding=utf8
from lxml import etree

import requests
import re

url ='''https://h5.qzone.qq.com/proxy/domain/ic2.qzone.qq.com/cgi-bin/feeds/feeds_html_act_all?uin=2094531487&hostuin=3185948277&scope=0&filter=all&flag=1&refresh=0&firstGetGroup=0&mixnocache=0&scene=0&begintime=undefined&icServerTime=&start=20&count=10&sidomain=qzonestyle.gtimg.cn&useutf8=1&outputhtmlfeed=1&refer=2&r=0.8956716993342928&g_tk=1445203692&qzonetoken=5b8291666fe8c64bc91e9650b15d0e5c04a821de00dce560b3301d5754bb36acb031aa814bc6a472ff23&g_tk=1445203692'''
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'cookie':'''pgv_pvi=4587480064; pgv_pvid=7663623423; RK=1jzpLOp5Vg; ptcz=5f4879138b14cbe4baf30d19cfbb9d1d88a8c2a8d7a804355f8be6edbb7f8679; QZ_FE_WEBP_SUPPORT=1; __Q_w_s__QZN_TodoMsgCnt=1; __Q_w_s_hat_seed=1; cpu_performance_v8=29; ptui_loginuin=2094531487; zzpaneluin=; zzpanelkey=; pgv_si=s8964029440; _qpsvr_localtk=0.5245727354066003; ptisp=cnc; pgv_info=ssid=s4767496354; uin=o2094531487; skey=@0gvCWoKIM; p_uin=o2094531487; pt4_token=QYae0fY1cmlBPOWnZ913wNsiwqoBzhNzEteIbshRNVQ_; p_skey=c*I1WAYwJ06eBDJzDjqKtoTYqUwnTm*mb1QWW4k8tkU_; rv2=800CE7EAC8DD7CC882B442FFA8B3E8F9CD5877339E83CAC31B; property20=B59BA47C3CD3F48031A968E11D71E14A5B53214726BCF0BC8FC30DD6636B58F6ECD24E815CD9A189'''
}
res = requests.get(url, headers=headers)
data = res.text
print(data)



# 抓取所有的feedstime
feedstime_lists = re.findall(r"feedstime:'(.*?)'", data)
print(feedstime_lists)

# 获取所有的abstime
abstime_lists = re.findall(r"abstime:'(.*?)'", data)
print(abstime_lists)

# 抓取所有html
htmls = re.findall(r"html:'([\s\S]*?)'", data)
# 将所有特殊字符替换
res_html = [x.replace('\\x22', '"').replace('\\x3C', '<').replace('\\', '') for x in htmls]

# 将三者结合起来组成每个tuple
res = zip(feedstime_lists, abstime_lists, res_html)
# print(len(list(res)))

selector = etree.HTML(res_html[3])

print(selector.xpath('//div[@class="f-info"]//text()'))
print(selector.xpath('//span[@class="f-like-cnt"]//text()'))

images = [x for x in selector.xpath('//img/@src') if x.startswith('http://a')]
print(images)

