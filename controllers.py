import pygame as pg
from pgframe.base import *

"""
        self.data = data
        self.inst = inst
        self.func = self.template
        self.kwargs = {}
        self.type = None
        
        def template(self, eve, **kwargs): # 空白的控制类生效调用方法
            pass
            
        Loading(self, **kwargs):
            pass # 在这里写你的加载方法

        SetFunc(self, func, **kwargs) # 设置调用函数
"""


class Controller:
    def __init__(self, data, inst):
        self.inst = inst
        self.data = data
        self.func = None
        self.kwargs = {}
        self.type = None
        self.Loading()
        self._block = False
        if self.func is None:
            self.func = self.template

    def template(self, eve, **kwargs):
        pass

    def Loading(self, **kwargs):
        pass

    def SetFunc(self, func, **kwargs):
        self.func = func
        self.kwargs = kwargs

    def GetFunc(self):
        return self.func

    def BindInst(self, inst):
        self.inst = inst

    def Block(self):
        self._block = True

    def GetBlock(self):
        return self._block

    def ResetBlock(self):
        self._block = False

    def effect(self, eve, **kwargs):
        """
        系统调用函数
        :param eve: Object 事件
        :param kwargs: **dict 参数键值对
        :return: return .GetFunc()(eve,**kwargs)
        """

        if self.IsAbled():
            return self.GetFunc()(eve, **kwargs)

    def IsAbled(self):
        temp = self.inst
        while True:
            if not temp.GetStatus():
                return
            elif temp.inst:
                temp = temp.inst
            else:
                break
        return True


class KeyCtrl(Controller):
    TypeKey = None
    auto = True

    def SetKey(self, key_name):
        try:
            self.type = getattr(pg, "K_" + key_name)
        except:
            raise (Exception("key " + key_name + " does not exist."))

    def effect(self, eve, **kwargs):
        if self.IsAbled() and eve.key == self.type:
            return self.GetFunc()(eve, **kwargs)


class MouseCtrl(Controller):
    LEFT = pg.BUTTON_LEFT
    MID = pg.BUTTON_MIDDLE
    RIGHT = pg.BUTTON_RIGHT
    UP = pg.BUTTON_WHEELUP
    DOWN = pg.BUTTON_WHEELDOWN

    TypeMouse = None
    auto = True

    def SetMouseKey(self, mouse_key_name):
        try:
            self.type = getattr(self, mouse_key_name.upper())
        except:
            raise (Exception("Mouse key " + mouse_key_name + " does not exist."))

    def effect(self, eve, **kwargs):
        if self.IsAbled() and eve.button == self.type:
            return self.GetFunc()(eve, **kwargs)


class MouseMove(Controller):
    TypeMouseMove = None
    auto = True

    def SetMouseKey(self, now_is_unvalued):
        pass

    def effect(self, eve, **kwargs):
        if self.IsAbled():
            return self.GetFunc()(eve, **kwargs)


# -----------------------内置控制器(默认)-----------------------
class Click(MouseCtrl):
    def __init__(self, data, inst):
        super().__init__(data, inst)
        self.SetMouseKey("LEFT")

    def effect(self, eve, **kwargs):
        if self.IsAbled() and eve.button == self.type and kwargs["key_status"] and IsClickActive(self.inst,
                                                                                                 eve.pos):
            return self.GetFunc()(eve, **kwargs)


class RightClick(MouseCtrl):
    def __init__(self, data, inst):
        super().__init__(data, inst)
        self.SetMouseKey("Right")

    def effect(self, eve, **kwargs):
        if self.IsAbled() and eve.button == self.type and kwargs["key_status"] and IsClickActive(self.inst,
                                                                                                 eve.pos):
            return self.GetFunc()(eve, **kwargs)


class Focus(MouseMove):
    """
    eve,focus
    """

    def effect(self, eve, **kwargs):
        if self.IsAbled():
            return self.GetFunc()(eve, focus=IsFocusActive(self.inst, eve.pos), **kwargs)
