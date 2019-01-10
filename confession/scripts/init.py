#!/usr/bin/env python

import os
import sys
import random
import django

# 设置环境
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "confession.settings")
django.setup()

# =======================user表=====================================

last_names = (
    '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨'
    '朱秦尤许何吕施张孔曹严华金魏陶姜'
    '戚谢邹喻柏水窦章云苏潘葛奚范彭郎'
    '鲁韦昌马苗凤花方俞任袁柳酆鲍史唐'
    '费廉岑薛雷贺倪汤滕殷罗毕郝邬安常'
    '乐于时傅皮卞齐康伍余元卜顾孟平黄'
)

first_names = {
    '男性': [
        '致远', '俊驰', '雨泽', '烨磊', '晟睿',
        '天佑', '文昊', '修洁', '黎昕', '远航',
        '旭尧', '鸿涛', '伟祺', '荣轩', '越泽',
        '浩宇', '瑾瑜', '皓轩', '浦泽', '绍辉',
        '绍祺', '升荣', '圣杰', '晟睿', '思聪'
    ],
    '女性': [
        '沛玲', '欣妍', '佳琦', '雅芙', '雨婷',
        '韵寒', '莉姿', '雨婷', '宁馨', '妙菱',
        '心琪', '雯媛', '诗婧', '露洁', '静琪',
        '雅琳', '灵韵', '清菡', '溶月', '素菲',
        '雨嘉', '雅静', '梦洁', '梦璐', '惠茜'
    ]
}

from user_app.models import User, Confess

password_template = '0123456789'
address_template = [
    ('山西省', '太原市', '山西大学'),
    ('山西省', '大同市', '大同大学'),
    ('山西省', '临汾市', '临汾师范'),
    ('山西省', '长治市', '长治学院'),
]


def get_name_sex():
    l_name = random.choice(last_names)
    sex = random.choice(['男性', '女性'])
    f_name = random.choice(first_names[sex])
    data = {
        'name': l_name + f_name,
        'sex': sex
    }
    return data


def init_user():
    '''初始化user表中数据'''
    for i in range(1, 21):
        user = User()
        n_s = get_name_sex()
        user.u_name, user.sex = n_s['name'], n_s['sex']
        user.password = ''.join(random.choices(password_template, k=6))
        user.phone = '13' + ''.join(random.choices(password_template, k=9))
        user.icon = 'avatar-%s' % i
        user.age = random.randint(18, 30)
        user.province, user.city, user.school = random.choice(address_template)
        user.save()
    print('*' * 10, 'user添加完成')


# =======================confess表=====================================

context_templates = [
    '这是谁的书，丢在了综合楼',
    '辣个女孩的名字叫什么？急急急！！！',
    '高数考什么，求指教。',
    '什么时候放寒假',
]


def init_confess():
    '''初始化confesss表数据'''
    for i in range(1, 1001):
        user = User.objects.get(pk=random.randint(1, 20))
        confess = Confess()
        confess.userID = user.id
        confess.userName = user.u_name
        confess.context = random.choice(context_templates)
        confess.image1 = user.icon + '-1'
        confess.image2 = user.icon + '-2'
        confess.image3 = user.icon + '-3'
        confess.state = '待审核'
        confess.save()
    print('*' * 10, 'confess添加完成')


if __name__ == '__main__':
    # init_user()
    init_confess()
