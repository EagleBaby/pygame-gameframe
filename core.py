import inspect as ins

import pygame as pg

draw = pg.draw
transform = pg.transform
display = pg.display
image = pg.image
event = pg.event
# import pgframe.dataframe as dataframe
from pgframe.base import *


# dict = dataframe.Dict
# list = dataframe.List
# 事实上，python 原生数据结构更快
# ndict = dataframe.ndict


# template_ndict = ndict()


class Core(object):
    def __init__(self):
        self.camera = None

    def call(self, *args, **kwargs):
        pass

    def ImportImgs(self, data, path, format=("png",)):  # 连续图片放在有__init__.py的文件夹下,此文件夹的名字即为连续图片组的名字
        if not data.Support_Part_GetImgManage():
            raise (Exception("before you import imgs, you must ImgManage() in Data at first."))
        temp = dict()
        hasdir = list()
        for name in os.listdir(path):  # 所有图片的格式必须相同
            if not os.path.isdir(os.path.join(path, name)):
                if name[len(name) - 3:] in format:  # 文件名去格式作为name
                    # "scale", "rotate", "hflip", "vflip", "name"
                    temp["100" + "000" + "0" + "0" + name[:len(name) - 4]] = {
                        "default": image.load(os.path.join(path, name))}
            else:  # 目录
                if not os.path.exists(os.path.join(path, name, "__init__.py")):
                    hasdir.append(name)
                else:
                    itemp = list()
                    for iname in os.listdir(os.path.join(path, name)):
                        if (not os.path.isdir(iname)) and iname[len(iname) - 3:] in format:
                            itemp.append(image.load(os.path.join(path, name, iname)))
                    temp["100" + "000" + "0" + "0" + name] = {"default": itemp}

        # for 循环结束
        data.Support_Part_GetImgManage().UpdateImg(temp)
        if len(hasdir):
            for i in hasdir:
                self.ImportImgs(data, os.path.join(path, i), format)

    def ImportWins(self, data):
        temp = dict()
        for vw in dir(data.vw):
            if vw[:2] != "__" and ins.isclass(getattr(data.vw, vw)) and issubclass(getattr(data.vw, vw),
                                                                                   getattr(data.vw,
                                                                                           "View")) and vw not in [
                "View", "MapView"]:
                # print(isinstance(getattr(data.vw, vw), getattr(data.vw, "View")))
                vtemp = getattr(data.vw, vw)(data, __system_calling_trig__=True)
                if vtemp and hasattr(vtemp, "TypeView") and vtemp.auto:
                    vtemp.system_redo()
                    temp[vw] = vtemp
        data.Support_Part_GetWinManage().UpdateWin(temp)

    def ImportCtrls(self, data):
        temp_key = dict()
        temp_mouse = dict()
        temp_mousemove = dict()
        for ct in dir(data.ct):
            if ct[:2] != "" and ct not in ["Controller", "KeyCtrl", "MouseCtrl", "MouseMove", "pg"] and hasattr(
                    getattr(data.ct, ct), "__class__"):
                ctemp = getattr(data.ct, ct)
                if ctemp and hasattr(ctemp, "TypeKey") and ctemp.auto:
                    temp_key[ct] = ctemp
                elif ctemp and hasattr(ctemp, "TypeMouse") and ctemp.auto:
                    temp_mouse[ct] = ctemp
                elif ctemp and hasattr(ctemp, "TypeMouseMove") and ctemp.auto:
                    temp_mousemove[ct] = ctemp

        data.Support_Part_GetCtrlManage().UpdateKeyCtrl(temp_key)
        data.Support_Part_GetCtrlManage().UpdateMouseCtrl(temp_mouse)
        data.Support_Part_GetCtrlManage().UpdateMouseMoveCtrl(temp_mousemove)

    def ImportMods(self, data):
        temp = dict()
        for md in dir(data.md):
            if md[:2] != "" and md not in ["Model"] and hasattr(getattr(data.md, md), "__class__"):
                temp[md] = getattr(data.md, md)
        data.GetModManage().UpdateMod(temp)

    def ImportSounds(self, data, path, format="ogg"):
        if not data.Support_Part_GetImgManage():
            raise (Exception("before you import sounds, you must SoundManage() in Data at first."))
        temp = dict()
        for name in os.listdir(path):  # 所有音乐的格式必须相同
            if not os.path.isdir(os.path.join(path, name)):
                if name[len(name) - 3:] == format:  # 文件名去格式作为name
                    temp[name[:len(name) - 4]] = pg.mixer.Sound(os.path.join(path, name))
                elif data.st.AUTO_TIDY["sound"]:
                    data.inst.TidySoundFiles()
                    self.ImportSounds(data, path, format)
                    return
                else:
                    raise (Exception(format, " does not be supported.Please use Game.TidySoundFiles() to tidy format"))
        # for 循环结束
        data.Support_Part_GetSoundManage().UpdateSound(temp)

    # def CheackForCameraScaleChange(self,data):
    #     if not hasattr(self,'camera'):
    #         self.camera = data.Support_Part_GetCamera()
    #         self._last_scale_rate = self.camera.GetScaleRate()
    #     if self._last_scale_rate != self.camera.GetScaleRate():
    #         self.ResetAllObjectScale(data)
    #         self._last_scale_rate = self.camera.GetScaleRate()

    def CreateAndLogFromImage(self, data, name, scale, rotate, hflip, vflip):
        try:
            test = scale[2] + rotate[2]
        except:
            raise (Exception("scale and rotate must have three numbers."))
        try:
            get = data.Support_Part_GetAllImg()["10000000" + name]["default"]
        except:
            raise (Exception("Base img " + name + " isn't be logged in."))
        if scale != "100":
            get = self.ScaleImage(data, get, name, "100", "000", "0", "0", scale)
        if rotate != "000":
            get = self.RotateImage(data, get, name, scale, "000", "0", "0", rotate)
        if hflip != "0" or vflip != "0":
            get = self.FlipImage(data, get, name, scale, rotate, "0", "0", hflip, vflip)
        return get

    def ScaleImage(self, data, get, name, scale, rotate, hflip, vflip, newScale):
        if data.Support_Part_GetAllImg().get(newScale + rotate + hflip + vflip + name):
            return data.Support_Part_GetAllImg()[newScale + rotate + hflip + vflip + name]
        trans = int(newScale) / int(scale)
        if isinstance(get, dict):
            get = get["default"]
        if not isinstance(get, (list, tuple)):
            temp = transform.scale(get, (int(get.get_width() * trans), int(get.get_height() * trans)))
        else:
            temp = list()
            for i in get:
                temp.append(transform.scale(i, (int(i.get_width() * trans), int(i.get_height() * trans))))
        data.Support_Part_GetAllImg()[newScale + rotate + hflip + vflip + name] = {"default": temp}
        return temp

    def RotateImage(self, data, get, name, scale, rotate, hflip, vflip, newRotate):
        if data.Support_Part_GetAllImg().get(scale + newRotate + hflip + vflip + name):
            return data.Support_Part_GetAllImg()[scale + newRotate + hflip + vflip + name]
        if isinstance(get, dict):
            get = get["default"]
        if not isinstance(get, (list, tuple)):
            temp = transform.rotate(get, int(rotate) - int(newRotate))
        else:
            temp = list()
            for i in get:
                temp.append(transform.rotate(i, int(rotate) - int(newRotate)))
        data.Support_Part_GetAllImg()[scale + newRotate + hflip + vflip + name] = {"default": temp}
        return temp

    def FlipImage(self, data, get, name, scale, rotate, hflip, vflip, newHflip, newVflip):
        if data.Support_Part_GetAllImg().get(scale + rotate + newHflip + newVflip + name):
            return data.Support_Part_GetAllImg()[scale + rotate + newHflip + newVflip + name]
        if isinstance(get, dict):
            get = get["default"]
        if not isinstance(get, (list, tuple)):
            temp = transform.flip(get, newHflip == "1", newVflip == "1")
        else:
            temp = list()
            for i in get:
                temp.append(transform.flip(i, newHflip == "1", newVflip == "1"))
        data.Support_Part_GetAllImg()[scale + rotate + newHflip + newVflip + name] = {"default": temp}
        return temp

    def GetViewAtPosition(self, data, view):
        if not view.GetPos():
            if view.inst:
                r_x, r_y = view.inst.GetSize()[0] * view.GetPercent(0), view.inst.GetSize()[1] * view.GetPercent(1)
                view.SetPos((r_x + view.inst.GetPos()[0], r_y + view.inst.GetPos()[1]))
            else:
                view.SetPos(
                    (data.Support_Part_GetScreen().get_width() * view.GetPercent(0),
                     data.Support_Part_GetScreen().get_height() * view.GetPercent(1)))
            return view.GetPos()

    def UpdateView(self, data, view):
        for comp in view.GetComponents() if view.TypeView is None else view.GetSpirits():
            comp.effect()
        for vw in view.GetViews() if view.TypeView is None else view.GetAnims():
            if vw.GetStatus():
                vw.Update()

    def CtrlHandler(self, data, eve):
        if eve.type == pg.KEYDOWN or eve.type == pg.KEYUP:
            # print("按下了一个键")
            for ctrl in data.Support_Part_GetCtrlManage().GetWinKeyCtrl():
                if ctrl.inst.layer == data.Support_Part_GetWinManage().GetTopLayer():
                    ctrl.effect(eve=eve, key_status=eve.type == pg.KEYDOWN)
                    if ctrl.GetBlock():
                        ctrl.ResetBlock()
                        break
        elif eve.type == pg.MOUSEBUTTONDOWN or eve.type == pg.MOUSEBUTTONUP:
            for ctrl in data.Support_Part_GetCtrlManage().GetWinMouseCtrl():
                if ctrl.inst.layer == data.Support_Part_GetWinManage().GetTopLayer():
                    ctrl.effect(eve=eve, key_status=eve.type == pg.MOUSEBUTTONDOWN)
                    if ctrl.GetBlock():
                        ctrl.ResetBlock()
                        break
        elif eve.type == pg.MOUSEMOTION:
            for ctrl in data.Support_Part_GetCtrlManage().GetWinMouseMoveCtrl():
                if ctrl.inst.layer == data.Support_Part_GetWinManage().GetTopLayer():
                    ctrl.effect(eve=eve, key_status=False)
                    if ctrl.GetBlock():
                        ctrl.ResetBlock()
                        break

    def PeriodTaskHandler(self, data):
        win = data.Support_Part_GetWindow()
        for i in win.GetPeriodicTasks().values():
            try:
                if data.Support_Part_GetTick() % i["_move_tick"] == 0:
                    i["func"](**i["kwargs"])
            except ZeroDivisionError:
                raise (Exception("period delta time can not to be small."))

    def EventHandler(self, data, eve):
        win = data.Support_Part_GetWindow()
        temp = win.GetListenTasks()
        for i in temp:
            if i == eve.type:
                temp[i](eve, data)


core = Core()


def GetCore():
    return core
