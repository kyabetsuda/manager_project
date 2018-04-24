from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from manager.managers import PersonManager

class Person(AbstractBaseUser):
    objects = PersonManager()

    # アカウント名
    identifier = models.CharField(max_length=64, unique=True, blank=False)
    # 名前
    name = models.CharField(max_length=128)

    is_active = models.BooleanField(default=True)

    # hijack機能の実装に必要
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'identifier'


class Article(models.Model):

    # 人
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    # スレッド
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE)
    # タイトル
    title = models.CharField(max_length=100)
    # 日付
    insymd = models.DateTimeField()
    # 本文
    text = models.CharField(max_length=100)

class Thread(models.Model):

    # タイトル
    title = models.CharField(max_length=100)
    # 日付
    insymd = models.DateTimeField()
