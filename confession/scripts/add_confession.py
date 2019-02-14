#!/usr/bin/env python

import os
import sys
import random
import re

import time
import uuid
from urllib.parse import urljoin

from lxml import etree
import requests
import django

# 设置环境
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "confession.settings")
django.setup()

from user_app.models import Confess


class GetCofession(object):
    # base_url、headers需要时时跟新
    base_url = '''https://h5.qzone.qq.com/proxy/domain/ic2.qzone.qq.com/cgi-bin/feeds/feeds_html_act_all?uin=2094531487&hostuin=3185948277&scope=0&filter=all&flag=1&refresh=0&firstGetGroup=0&mixnocache=0&scene=0&begintime=undefined&icServerTime=&start=%d&count=%d&sidomain=qzonestyle.gtimg.cn&useutf8=1&outputhtmlfeed=1&refer=2&r=0.6598675730229324&g_tk=45245881&qzonetoken=24014f8eded068265a6ae915f4a98c169b4ef38bd14f1319d5c3359f2e41f7027d3537a6185bdf&g_tk=45245881'''
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'cookie': '''pgv_pvid=2942223597; pgv_info=ssid=s314747112; zzpaneluin=; zzpanelkey=; pgv_pvi=1444548608; pgv_si=s9418597376; _qpsvr_localtk=0.8774627654124492; uin=o2094531487; skey=@QNld8s6Ph; RK=OizhKspoXg; ptcz=6d4fbe3e08321772765f3cd7d6d197bf7a9bb16af0079fba658e52b963563d00; p_uin=o2094531487; pt4_token=k291S9LKqocB4-rPT3E8P6x26KfgOHw7W4eWSKiKdAk_; p_skey=ayHByNNovJkmkugUkQMrdItR0L*y5ZTtSMftnV5kcCQ_; rv2=806403F17A023B4802CC56AF092AA6E3A41DC52032B9D83CB7; property20=701501B315228225D5F857000DFDAF59CDD0F85E8A64A2C7CDF3A751BD7AEC6F4892F557CFB32AC0'''
    }
    start = 0
    step = 40
    HOST = "http://192.168.1.101:8000/static/confessImage/"

    def get_data(self):
        '''发起请求'''
        for i in range(2):  # range中的取值计算 (可抓总条数 - 10) // step
            url = self.base_url % (self.start + (self.step * i), self.step)
            print("*******开始********：%s" % str(self.start + (self.step * i)))
            res = requests.get(url, headers=self.headers)
            data = res.text
            data_list = self.parse_data(data)
            self.save_data(data_list)
            time.sleep(2)

    def parse_data(self, data):
        '''解析数据'''
        data_list = []
        # # 抓取所有的feedstime
        # feedstime_lists = re.findall(r"feedstime:'(.*?)'", data)
        # print(feedstime_lists)

        # 抓取用户昵称
        nick_name_list = re.findall(r"nickname:'(.*?)'", data)
        print(nick_name_list)

        # 获取所有的abstime
        abstime_lists = re.findall(r"abstime:'(.*?)'", data)
        print(abstime_lists)

        # 抓取用户头像
        logimg_list = re.findall(r"logimg:'(.*?)'", data)
        print(logimg_list)

        # 抓取所有html
        htmls = re.findall(r"html:'([\s\S]*?)'", data)
        # 将所有特殊字符替换
        res_html_list = [x.replace('\\x22', '"').replace('\\x3C', '<').replace('\\', '') for x in htmls]

        # 将三者结合起来组成每个tuple
        res = zip(nick_name_list, logimg_list, abstime_lists, res_html_list)
        for name, logimg, abstime, res_html in res:
            res_data = {}
            res_data['uid'] = 1  # 规定墙的id是1
            res_data['nick_name'] = name
            res_data['logimg'] = logimg
            res_data['abstime'] = abstime
            res_data['content'], res_data['imgs'], res_data['zan'] = self.parse_html(res_html)
            data_list.append(res_data)
        return data_list

    def parse_html(self, html):
        '''解析html数据'''
        selector = etree.HTML(html)
        content_list = selector.xpath('//div[@class="f-info"]//text()')
        img_list = [x for x in selector.xpath('//img/@src') if x.startswith('http://a')]
        # 将图片保存在本地
        img_list = self.download_images(img_list)
        zan_list = selector.xpath('//span[@class="f-like-cnt"]//text()')
        content_str = '%@#'.join(content_list)
        img_str = '##'.join(img_list)
        zan_str = ''.join(zan_list)
        return content_str, img_str, zan_str

    def save_data(self, data_list):
        '''存库'''
        for item in data_list:
            confess = Confess()
            confess.userID = item['uid']
            confess.userName = item['nick_name']
            confess.images = item['imgs']
            confess.context = item['content']
            confess.release_time = item['abstime']
            confess.save()

    def download_images(self, image_list):
        bas_dir = os.path.join(BASE_DIR, 'static/confessImage')
        images = []
        for url in image_list:
            filename = uuid.uuid4().hex
            path = os.path.join(bas_dir, filename)
            with open(path, 'wb') as fp:
                res = requests.get(url, headers=self.headers)
                fp.write(res.content)
            res_url = urljoin(self.HOST, filename)
            images.append(res_url)
            print(images)
        return images


if __name__ == '__main__':
    GetCofession().get_data()
