from django.db import models


class BaseMode(models.Model):
    class Meta:
        abstract = True

    def to_dict(self):
        pass


class User(BaseMode):
    class Meta:
        db_table = 'user'

    SEX = (
        ('男性', '男性'),
        ('女性', '女性'),
        ('保密', '保密'),
    )
    u_name = models.CharField(max_length=30, default='默认用户')
    password = models.CharField(max_length=256)
    phone = models.CharField(max_length=11, unique=True)
    icon = models.CharField(max_length=256)
    sex = models.CharField(max_length=4, choices=SEX)
    age = models.IntegerField(default=18)

