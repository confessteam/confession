#!/usr/bin/env python

import os
import sys
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

from user_app.models import Confess, User, Notice, Comment, Collection, Care


def init():
    '''初始化'''
    for confess in Confess.objects.all():  # 初始化confess表
        confess.collectCount = 0
        confess.likeCount = 0
        confess.commentCount = 0
        confess.userID = 1
        confess.userName = '墙'
        confess.contentType = 1
        confess.save()

    User.objects.all().delete()  # 清空用户表
    Notice.objects.all().delete()  # 清空notice表
    Comment.objects.all().delete()  # 清空评论表
    Collection.objects.all().delete()  # 清空收藏表
    Care.objects.all().delete()  # 清空收关注表


if __name__ == '__main__':
    init()
