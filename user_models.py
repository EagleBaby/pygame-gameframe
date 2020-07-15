# 这是一个用户文件
from pgframe.models import *


class Player(Model):
    lv = 1
    hp = 100
    mp = 50
    exp = 0
    name = ""
    main_key = "name"


class Enemy(Model):
    hp = 100
    mp = 50
    name = ""
    main_key = "name"


class Money(Model):
    gold = 100
    diamond = 50
    owner = ""
    main_key = "owner"
