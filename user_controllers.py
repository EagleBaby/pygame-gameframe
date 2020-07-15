# 这是一个用户文件
from pgframe.controllers import *


class MoveUp(KeyCtrl):
    def Loading(self, **kwargs):
        self.SetKey("w")
        self.SetFunc(self.Move)
        self.temp = 0

    def Move(self, eve, **kwargs):
        if kwargs["key_status"]:
            self.data.player.motor.Move("moveUp", 0, -3)
        else:
            self.data.player.motor.Stop("moveUp")


class MoveDown(KeyCtrl):
    def Loading(self, **kwargs):
        self.SetKey("s")
        self.SetFunc(self.Move)

    def Move(self, eve, **kwargs):
        if kwargs["key_status"]:
            self.data.player.motor.Move("moveDown", 0, 3)
        else:
            self.data.player.motor.Stop("moveDown")


class MoveLeft(KeyCtrl):
    def Loading(self, **kwargs):
        self.SetKey("a")
        self.SetFunc(self.Move)

    def Move(self, eve, **kwargs):
        if kwargs["key_status"]:
            self.data.player.motor.Move("moveLeft", -3, 0)
        else:
            self.data.player.motor.Stop("moveLeft")


class MoveRight(KeyCtrl):
    def Loading(self, **kwargs):
        self.SetKey("d")
        self.SetFunc(self.Move)

    def Move(self, eve, **kwargs):
        if kwargs["key_status"]:
            self.data.player.motor.Move("moveRight", 3, 0)
        else:
            self.data.player.motor.Stop("moveRight")


class Hello(Click):
    def Loading(self, **kwargs):
        self.SetFunc(self.Hello)

    def Hello(self, eve, **kwargs):
        print(self.inst.PushEvent("test"))


class Move(MouseMove):
    def Loading(self, **kwargs):
        self.SetFunc(self.Move)

    def Move(self, eve, **kwargs):
        print(eve.pos)
