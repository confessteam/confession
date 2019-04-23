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

from user_app.models import Confess


def clear_collectCount():
    '''清空所有收藏数'''
    for confess in Confess.objects.all():
        confess.collectCount = 0
        confess.likeCount = 0
        confess.commentCount = 0
        confess.save()



if __name__ == '__main__':
    clear_collectCount()