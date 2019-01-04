import json
import random
import string

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse

from third_part.sms import SendMessage
from user_app.user_settings import TEXT

'''
视图函数中的逻辑部分
'''


def render_json(data, code):
    '''
    返回格式如下Response：
    result = {
        "code":code,
        "data":data,
    }
    '''
    result = {
        "code":code,
        "data":data,
    }
    if settings.DEBUG:
        result_json = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)
        return HttpResponse(result_json)
    result_json = json.dumps(result, ensure_ascii=False, separators=[':', ','])
    return HttpResponse(result_json)


def get_code(length):
    '''生成length长度的验证码'''
    chr_template = '0123456789'
    code = ''.join(random.choices(chr_template, k=length))
    return code


def check_vcode(phonenum, vcode):
    '''检查验证码是否正确'''
    cache_code = cache.get('Vcode-%s' % phonenum)
    return cache_code == vcode


def send_msg(phone, vcode):
    text = TEXT % vcode
    sender = SendMessage(text=text, mobile=phone)
    res = sender.send_sms()
    return res





if __name__ == '__main__':
    print(type(get_code(4)))
