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
                attr_dict[name] = getattr(self, name)  # 获取字段对应的值
        return attr_dict


class User(BaseMode):
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
    STATE = (
        ('待审核', '待审核'),
        ('通过', '通过'),
        ('未通过', '未通过')
    )

    class Meta:
        db_table = 'confess'

    userID = models.IntegerField()
    context = models.TextField()
    image1 = models.CharField(max_length=256, null=True)
    image2 = models.CharField(max_length=256, null=True)
    image3 = models.CharField(max_length=256, null=True)
    userName = models.CharField(max_length=30)
    state = models.CharField(max_length=50, choices=STATE, default='待审核')










