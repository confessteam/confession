import json
import random

import os
import uuid

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


def save_upload_file(filename, avatar, save_path):
    '''保存上传图片'''
    filename = filename + uuid.uuid4().hex
    filepath = os.path.join(settings.BASE_DIR, save_path,filename)
    with open(filepath, 'wb') as fp:
        for chunk in avatar.chunks():
            fp.write(chunk)
    return filepath, filename


def save_images(userId, fileList):
    filenames = []
    if not len(fileList):
        return filenames
    for index, file in enumerate(fileList):
        _, filename = save_upload_file('issue-%s-%s' % (userId, index), file, save_path='static/confessImage')
        filenames.append(filename)
    return filenames


def many_to_dict(objects):
    res_lists = []
    for obj in objects:
        res_lists.append(obj.to_dict())
    return res_lists


def get_first_image_list(confess_list):
    '''获取每组中的第一张图片'''
    image_list = []
    for item in confess_list:
        image_list.append(item.images.split('##')[0])
    length = len(image_list)
    return image_list[0:length//2], image_list[length//2:length]


if __name__ == '__main__':
    print(type(get_code(4)))
