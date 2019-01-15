from datetime import datetime
from django.db import models


class BaseMode(models.Model):
    class Meta:
        abstract = True

    def to_dict(self, *ignore_fileds):
        '''将一个 model 转换成一个 dict'''
        attr_dict = {}
        for field in self._meta.fields:  # 遍历所有字段
            name = field.attname  # 取出字段名称
            if name not in ignore_fileds:  # 检查是否是需要忽略的字段
                tem_attr = getattr(self, name)
                if isinstance(tem_attr, datetime):
                    attr_dict[name] = tem_attr.strftime("%Y-%m-%d %X")  # 获取字段对应的值
                else:
                    attr_dict[name] = getattr(self, name)  # 获取字段对应的值
        return attr_dict

    def datetime_to_string(self, datetime):
        pass



class User(BaseMode):
    '''用户表'''
    class Meta:
        db_table = 'user'

    SEX = (
        ('男性', '男性'),
        ('女性', '女性'),
        ('保密', '保密'),
    )
    u_name = models.CharField(max_length=30, default='默认用户')
    password = models.CharField(max_length=256, default='123456')
    phone = models.CharField(max_length=11, unique=True, null=False)
    icon = models.CharField(max_length=256)
    sex = models.CharField(max_length=4, choices=SEX, default='男性')
    age = models.IntegerField(default=18)
    province = models.CharField(max_length=64, default='山西省')
    city = models.CharField(max_length=64, default='太原市')
    school = models.CharField(max_length=256, default='山西大学')


class Confess(BaseMode):
    '''贴子表'''
    STATE = (
        ('待审核', '待审核'),
        ('通过', '通过'),
        ('未通过', '未通过')
    )

    class Meta:
        db_table = 'confess'

    userID = models.IntegerField()
    context = models.TextField(default='', null=True)
    image1 = models.CharField(max_length=256, null=True)
    image2 = models.CharField(max_length=256, null=True)
    image3 = models.CharField(max_length=256, null=True)
    userName = models.CharField(max_length=30)
    state = models.CharField(max_length=50, choices=STATE, default='待审核')
    release_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)


class Comment(BaseMode):
    class Meta:
        db_table = 'comment'

    userID = models.IntegerField()
    confessID = models.IntegerField()
    context = models.TextField(null=True)
    comment_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)









