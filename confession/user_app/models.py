from datetime import datetime
from time import time
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


class User(BaseMode):
    '''用户表'''

    class Meta:
        verbose_name_plural = '用户'
        db_table = 'user'

    SEX = (
        ('男性', '男性'),
        ('女性', '女性'),
        ('保密', '保密'),
    )
    u_name = models.CharField(max_length=30, default='默认用户', verbose_name="用户昵称")
    signature = models.CharField(max_length=64, default="我就是我，不一样的烟火", verbose_name="个性签名")
    password = models.CharField(max_length=256, default='123456', verbose_name="密码")
    phone = models.CharField(max_length=11, unique=True, null=False, verbose_name="手机号")
    icon = models.CharField(max_length=256, verbose_name="用户头像")
    sex = models.CharField(max_length=4, choices=SEX, default='男性', verbose_name="性别")
    birthday = models.DateField(auto_now=True, verbose_name="出生年月日")
    province = models.CharField(max_length=64, default='山西省', verbose_name="学校所在省")
    city = models.CharField(max_length=64, default='太原市', verbose_name="学校所在市")
    school = models.CharField(max_length=256, default='山西大学', verbose_name="学校名称")
    create_time = models.TimeField(auto_now_add=True, verbose_name="用户创建时间")
    action_time = models.TimeField(auto_now=True, verbose_name="修改时间")

    @property
    def age(self):
        '''计算年龄'''
        # 用户出生时间到当前时间一共有多少天
        days = (datetime.now() - datetime(self.birthday.year, self.birthday.month, self.birthday.day)).days
        ages = days / 365
        return ages


class Confess(BaseMode):
    '''贴子表'''
    STATE = (
        ('待审核', '待审核'),
        ('通过', '通过'),
        ('未通过', '未通过')
    )
    TYPE = (
        (1, '表白'),
        (2, '失物招领'),
        (3, '二手商品'),
        (4, '其他'),
    )

    class Meta:
        verbose_name_plural = '内容'
        db_table = 'confess'

    userID = models.IntegerField(default=1, verbose_name="用户ID")
    userName = models.CharField(max_length=30, default='表白墙', verbose_name="用户昵称")
    context = models.TextField(default='', null=True, verbose_name="发表内容")  # 使用%@#分割每张图的说明
    images = models.TextField(default='', verbose_name="发表配图")  # 使用##来分割每张图片
    state = models.CharField(max_length=50, choices=STATE, default='待审核', verbose_name="审核状态")
    release_time = models.CharField(max_length=256, default=str(int(time())), verbose_name="发布时间")
    # contentType = models.IntegerField(default=1, verbose_name="内容类型（1:表白、2：失物招领、3：二手商品、4：其他）")
    contentType = models.IntegerField(default=1, verbose_name="内容类型", choices=TYPE)
    likeCount = models.IntegerField(default=0, verbose_name='关注数')
    collectCount = models.IntegerField(default=0, verbose_name='收藏数')
    commentCount = models.IntegerField(default=0, verbose_name='评论数')
    is_delete = models.BooleanField(default=False, verbose_name="是否被删除")


class Comment(BaseMode):
    class Meta:
        verbose_name_plural = '评论'
        db_table = 'comment'

    userID = models.IntegerField()
    confessID = models.IntegerField()
    context = models.TextField(null=True)
    comment_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)


class Collection(BaseMode):
    class Meta:
        verbose_name_plural = '收藏'
        db_table = 'collection'

    userID = models.IntegerField()
    confessID = models.IntegerField()
    is_delete = models.BooleanField(default=False)


class Care(BaseMode):
    class Meta:
        verbose_name_plural = '关注'
        db_table = 'care'

    userID = models.IntegerField()
    caredUserId = models.IntegerField()
    is_delete = models.BooleanField(default=False)


class Notice(BaseMode):
    class Meta:
        verbose_name_plural = '消息'
        db_table = "notice"

    userId = models.IntegerField()
    messageType = models.CharField(max_length=10, default="系统") # 系统、用户
    messageState = models.CharField(max_length=10, default="未读") # 已读、未读
    message = models.TextField(null=True)


