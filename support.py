import time
import tkinter.messagebox as message
import time
try:
    class FalseData:
        pass


    import pgframe.user_models as md
    import pgframe.user_settings as st

    _data = FalseData()
    _data.md, _data.st = md, st
    md.System_Model_Part_Init(_data)
    import pgframe.user_views as vw
    import pgframe.user_components as cp
    import pgframe.user_controllers as ct
    import pgframe.user_events as ev
except Exception as error:
    message.showerror("你的某个文件出现了错误：", "在一个用户文件中有一个错误:\n" + str(error))
from pgframe.core import *
from threading import *


class GameThread(Thread):
    def __init__(self, name=None, daemon=True, tick=60):
        super().__init__(name=name, daemon=daemon)
        self.queue = []  # (name:kwargs)
        self.tick = tick
        self.delta = 1 / self.tick
        self.ready = False

    def SetTick(self, tick):
        self.tick = tick
        self.delta = 1 / self.tick

    def GetQueue(self):
        if self.queue:
            temp = self.queue
            self.queue = []
            return temp
        return self.queue

    def AddQueue(self, task_name, **task_parm):
        self.queue.append((task_name, task_parm))

    def Ready(self):
        self.ready = True


class Data(object):
    game___init__ = False
    BaseInfo = list(["md", "st", "vw", "cp", "ct", "ev"])
    screen = None
    inst = None
    md = None
    st = None
    vw = None
    cp = None
    ct = None
    ev = None

    class System_Support_Part_GroupManage(GameThread):
        def __init__(self, data):
            super().__init__(name="group_thread", daemon=True)
            self.data = data
            self.group = {}

        def CreateNewGroup(self, group_name):
            self.group[group_name] = pg.sprite.Group()
            return self.group[group_name]

        def GetGroup(self, group_name):
            temp = self.group.get(group_name)
            if temp:
                return temp
            else:
                return self.CreateNewGroup(group_name)

        def AddCollider(self, item):
            self.GetGroup(item.GetGroupName()).add(item)

        def RemoveCollider(self, item):
            self.GetGroup(item.GetGroupName()).remove(item)

        def run(self):
            while True:
                time.sleep(self.delta)
                if self.ready:
                    for i in self.GetQueue():
                        getattr(self, i[0])(**i[1])

    class System_Support_Part_CtrlManage(GameThread):
        def __init__(self, data):
            super().__init__(name="controller_thread", daemon=True)
            self.data = data
            self.key_ctrl = dict()  # key:eve_name values:eve_func
            self.mouse_ctrl = dict()
            self.mousemove_ctrl = dict()
            self._key_ctrl = dict()
            self._mouse_ctrl = dict()
            self._mousemove_ctrl = dict()
            self._id = 0

        def CtrlHandler(self, data, eve):
            self.data.Support_Part_GetCore().CtrlHandler(data, eve)

        def EnpowerWinCtrl(self, win, _id=0, _key_ctrl={}, _mouse_ctrl={}, _mousemove_ctrl={}):
            if win.TypeView is not None:
                return
            self._id = _id
            self._key_ctrl = _key_ctrl
            self._mouse_ctrl = _mouse_ctrl
            self._mousemove_ctrl = _mousemove_ctrl
            for name in win.GetCtrlInfos():
                try:
                    temp = self.GetKeyController(name)
                except:
                    try:
                        temp = self.GetMouseController(name)
                    except:
                        temp = self.GetMouseMoveController(name)
                if hasattr(temp, "TypeKey"):
                    self._key_ctrl[self._id] = temp(self.data, win)
                elif hasattr(temp, "TypeMouse"):
                    self._mouse_ctrl[self._id] = temp(self.data, win)
                elif hasattr(temp, "TypeMouseMove"):
                    self._mousemove_ctrl[self._id] = temp(self.data, win)
                self._id += 1
            for i in win.GetViews():
                self.EnpowerWinCtrl(i, self._id, self._key_ctrl, self._mouse_ctrl, self._mousemove_ctrl)

        def GetWinKeyCtrl(self):
            return self._key_ctrl.values()

        def GetWinMouseCtrl(self):
            return self._mouse_ctrl.values()

        def GetWinMouseMoveCtrl(self):
            return self._mousemove_ctrl.values()

        def GetAllKeyCtrl(self):
            return self.key_ctrl.values()

        def GetAllMouseCtrl(self):
            return self.mouse_ctrl.values()

        def GetAllMouseMoveCtrl(self):
            return self.mousemove_ctrl.values()

        def GetKeyController(self, name):
            try:
                return self.key_ctrl[name]
            except:
                raise (Exception(
                    "Can't find key_controller named " + name + "."))

        def GetMouseController(self, name):
            try:
                return self.mouse_ctrl[name]
            except:
                raise (Exception(
                    "Can't find mouse_controller named " + name + "."))

        def GetMouseMoveController(self, name):
            try:
                return self.mousemove_ctrl[name]
            except:
                raise (Exception(
                    "Can't find mousemove_controller named " + name + "."))

        def UpdateKeyCtrl(self, key_ctrl_dict):
            self.key_ctrl.update(key_ctrl_dict)

        def UpdateMouseCtrl(self, mouse_ctrl_dict):
            self.mouse_ctrl.update(mouse_ctrl_dict)

        def UpdateMouseMoveCtrl(self, mousemove_ctrl_dict):
            self.mousemove_ctrl.update(mousemove_ctrl_dict)

        def run(self):
            while True:
                time.sleep(self.delta)
                if self.ready:
                    for i in self.GetQueue():
                        getattr(self, i[0])(**i[1])

    class System_Support_Part_EveManage(GameThread):
        def __init__(self, data):
            super().__init__(name="event_thread", daemon=True)
            self.data = data
            self.eve_id = 24
            self.eve = dict()  # key:eve_name values:event_id

        def DoPeriodicTask(self, maker, delta_tick, func, task_id, kwargs):
            maker.GetPeriodicTasks()[task_id] = {"_move_tick": delta_tick, "func": func, "kwargs": kwargs}

        def CancelPeriodicTask(self, maker, period_id):
            if maker.GetPeriodicTasks().get(period_id):
                del maker.GetPeriodicTasks()[period_id]

        def EventHandler(self, data, eve):
            self.data.Support_Part_GetCore().EventHandler(data, eve)

        def PeriodTaskHandler(self, data):
            self.data.Support_Part_GetCore().PeriodTaskHandler(data)

        def GetAllEveId(self):
            return self.eve.values()

        def GetAllEveName(self):
            return self.eve.keys()

        def ListenForEvent(self, maker, event_name, func):
            if not hasattr(maker, "_events"):
                raise (Exception("This inst can't make listen for event."))
            maker.events[self.GetEventId(event_name)] = func  # 对应的view 里储存event_id-->函数信息,由core处理

        def CancelListen(self, maker, event_name):
            del maker.events[self.GetEventId(event_name)]

        def PushEvent(self, maker, event_name, **kwargs):
            id = self.GetEventId(event_name)
            kwargs["maker"] = maker
            event.post(event.Event(id, **kwargs))

        def GetEventId(self, event_name):
            try:
                return self.eve[event_name]
            except:
                return self.AddNewEvent(event_name)

        def AddNewEvent(self, event_name):
            self.eve_id += 1
            self.eve[event_name] = self.eve_id
            return self.eve_id

        def UpdateEve(self, eve_dict):
            self.eve.update(eve_dict)

        def run(self):
            while True:
                time.sleep(self.delta)
                if self.ready:
                    for i in self.GetQueue():
                        getattr(self, i[0])(**i[1])

    class System_Support_Part_ImgManage(GameThread):
        def __init__(self, data):
            super().__init__(name="image_thread", daemon=True)
            self.data = data
            self.img = dict()  # key="name" value=dict([dict("scale","rotate","hflip","vflip","num")],[list(surfaces)])

            #    "name"          , 0~100,0~360,0/1,0/1,number

        def GetAllImgs(self):
            return self.img.values()

        def GetAllImg(self):
            return self.img

        def UpdateImg(self, img_dict):
            self.img.update(img_dict)

        def __tidy__(self, scale, rotate, hflip, vflip):
            if not isinstance(scale, str):
                scale = str(scale)
                if len(scale) <= 2:
                    scale = "0" + scale
                    if len(scale) == 2:
                        scale = "0" + scale
            if not isinstance(rotate, str):
                rotate = str(rotate)
                if len(rotate) <= 2:
                    rotate = "0" + rotate
                    if len(rotate) == 2:
                        rotate = "0" + rotate
            if not isinstance(hflip, str):
                hflip = str(hflip)
            if not isinstance(vflip, str):
                vflip = str(vflip)
            return scale, rotate, hflip, vflip

        def GetImage(self, name, scale="100", rotate="000", hflip="0", vflip="0"):
            scale, rotate, hflip, vflip = self.__tidy__(scale, rotate, hflip, vflip)
            key = scale + rotate + hflip + vflip + name
            if key in self.img:
                return self.img[key]["default"]
            else:
                return self.data.Support_Part_GetCore().CreateAndLogFromImage(self.data, name, scale, rotate, hflip,
                                                                              vflip)

        def run(self):
            while True:
                time.sleep(self.delta)
                if self.ready:
                    for i in self.GetQueue():
                        getattr(self, i[0])(**i[1])

    class System_Support_Part_WinManage(GameThread):
        def __init__(self, data):
            super().__init__(name="window_thread", daemon=True)
            self.data = data
            self.win = dict()  # key:win_name # values:window_view object

            self.top_targets = list()
            self.top_layer = -1

            self.target = None

        def UpdateGameWindow(self):
            self.data.screen.fill((10, 10, 10))
            self.data.Support_Part_GetWindow().Update()
            display.update()

        def HappenDisabled(self, view):
            if view.layer == self.top_layer and view in self.top_targets:
                self.top_targets.remove(view)
                if not self.top_targets:
                    self.UpdateTopWindow()

        def HappenEnabled(self, view):
            if view.layer > self.top_layer:
                self.top_targets = [view]
                self.top_layer = view.layer
            elif view.layer == self.top_layer:
                self.top_targets += [view]

        def GetTopLayer(self):
            return self.top_layer

        def GetTopTargets(self):
            return self.top_targets

        def UpdateTopWindow(self):
            self.top_layer = -1
            for i in self.GetTarget().GetViews():
                if i.GetStatus():
                    if i.layers > self.top_layer:
                        self.top_targets = [i]
                        self.top_layer = i.layers
                    elif i.layers == self.top_layer:
                        self.top_targets += [i]

        def GetAllWin(self):
            return self.win.values()

        def UpdateWin(self, win_dict):
            self.win.update(win_dict)

        def SetTarget(self, target_name):
            self.target = self.GetWindow(target_name)
            self.data.Support_Part_GetCtrlManage().EnpowerWinCtrl(self.target)

        def GetTarget(self):
            return self.target

        def GetWindow(self, name):
            try:
                return self.win[name]
            except:
                raise (Exception(
                    "Can't find window named " + name + "."))

        def run(self):
            while True:
                time.sleep(self.delta)
                if self.ready:
                    for i in self.GetQueue():
                        getattr(self, i[0])(**i[1])

    class System_Support_Part_SoundManage(GameThread):
        def __init__(self, data):
            super().__init__(name="music_thread", daemon=True)
            self.data = data
            self.sound = dict()  # key:sound_name values:sound_obj
            self.music_queue = []
            self.rec = 0
            # self.music = dict()  # music won't be load pre game

        def GetAllSound(self):
            return self.sound.values()

        def GetSound(self, name):
            try:
                return self.sound[name]
            except:
                raise (Exception(
                    "Can't find sound named " + name + "."))

        def SoundEffect(self, name, volume):
            if name not in self.sound.keys():  # 说明是个音乐文件
                path = os.path.join(self.data.st.PATH_SET["sound"], "music", name + ".ogg")
                if os.path.exists(path):
                    self.music_queue.append(pg.mixer.Sound(path))
                else:
                    raise (Exception("Does not find file " + path + " in music."))
            else:
                self.sound[name].play()

        def SoundStop(self):
            pg.mixer.music.stop()

        def SoundPause(self):
            pg.mixer.music.pause()

        def SoundStart(self):
            pg.mixer.music.unpause()

        def UpdateSound(self, sound_dict):
            self.sound.update(sound_dict)

        def MusicQueueHandler(self):
            if self.rec <= 0:
                if len(self.music_queue):
                    self.music_queue[0].play()
                    self.rec = self.music_queue[0].get_length() * self.data.st.FREQUENCY
                    self.music_queue.pop(0)
            else:
                self.rec -= 1

        def run(self):
            time.sleep(1)
            while True:
                time.sleep(self.delta)
                if self.ready:
                    for i in self.GetQueue():
                        getattr(self, i[0])(**i[1])

    class System_Support_Part_Camera:
        def __init__(self, data):
            self.data = data
            self._pos = [0, 0]
            self._height = 50
            self._min_height, self._max_height = 50, 200
            self.delta_pos = [0, 0]
            self.floor_pos = [0, 0]
            self.delta_height = 0
            self._move_tick, self._scale_tick = Tick(0), Tick(0)
            self._move_tick.Disabled()
            self._scale_tick.Disabled()

        def SetHeight(self, height):
            self._height = self._max_height if height > self._max_height else (
                self._min_height if height < self._min_height else height)

        def SetPos(self, pos):
            self._pos = pos

        def GetHeight(self):
            return self._height

        def GetScaleRate(self):
            return 100 / self._height

        def GetPos(self):
            return self._pos

        def Transfer(self, pos):
            return self._pos[0] + pos[0], self._pos[1] + pos[1]

        def LiftCamera(self, _to_height, tick):
            self._scale_tick.Enabled()
            self._scale_tick.SetTim(tick)
            self.delta_height = (_to_height - self._height) / tick

        def MoveCamera(self, desc_pos, tick):
            self._move_tick.Enabled()
            self._move_tick.SetTim(tick)
            self.delta_pos = [(desc_pos[0] - self._pos[0]) / tick, (desc_pos[1] - self._pos[1]) / tick]
            self.floor_pos = self._pos.copy()

        def CameraMoveUpdate(self):
            if self._move_tick.GetStatus():
                if self._move_tick.tick():
                    self._move_tick.Disabled()
                else:
                    self.floor_pos[0] += self.delta_pos[0]
                    self.floor_pos[1] += self.delta_pos[1]
                    self._pos = int(self.floor_pos[0]), int(self.floor_pos[1])

        def CameraScaleUpdate(self):
            if self._scale_tick.GetStatus():
                if self._scale_tick.tick():
                    self._scale_tick.Disabled()
                else:
                    self.SetHeight(self._height + self.delta_height)

        def CameraUpdate(self):
            self.CameraMoveUpdate()
            self.CameraScaleUpdate()

    def __init__(self):
        self.system_support_part_img_manage = self.System_Support_Part_ImgManage(self)
        self.system_support_part_eve_manage = self.System_Support_Part_EveManage(self)
        self.system_support_part_win_manage = self.System_Support_Part_WinManage(self)
        self.system_support_part_ctrl_manage = self.System_Support_Part_CtrlManage(self)
        self.system_support_part_group_manage = self.System_Support_Part_GroupManage(self)
        self.system_support_part_sound_manage = self.System_Support_Part_SoundManage(self)
        self.system_support_part_camera = self.System_Support_Part_Camera(self)
        self.system_support_part_target_win = None
        self.system_support_part_tick = 0

    def Support_Part_GetTick(self):
        return self.system_support_part_tick

    def System_Support_Part_SetTick(self, tick):
        self.system_support_part_tick = tick

    def System_Support_Part_TickIadd(self):
        self.system_support_part_tick += 1

    def System_Support_Part_TickSetProcess(self):
        self.System_Support_Part_TickIadd()
        if self.Support_Part_GetTick() >= 65536 - 1:
            self.System_Support_Part_SetTick(0)

    def System_Support_Part_GetThingsReady(self, srt_window):
        if not self.game___init__:
            raise (Exception("you need init first."))
        for i in self.BaseInfo:
            if not hasattr(self, i):
                raise (Exception(
                    "pgframe need init first.So check whether your parameters are full or not."))
        self.core = GetCore()
        self.System_Support_Part_LoadCtrl()
        self.System_Support_Part_LoadImg()
        self.System_Support_Part_LoadEve()
        self.System_Support_Part_LoadWin()
        self.System_Support_Part_LoadSound()
        self.Support_Part_GetWinManage().SetTarget(srt_window)
        self.system_support_part_target_win = self.Support_Part_GetWinManage().GetTarget()

        UpdateModelData(self)

    def System_Support_Part_LoadSound(self):
        pg.mixer.init(frequency=self.st.AUDIO_BIT, buffer=self.st.AUDIO_BUFFER)
        self.system_support_part_sound_manage.start()
        self.Support_Part_GetSoundManage().SetTick(self.st.FREQUENCY)
        self.Support_Part_GetCore().ImportSounds(self, os.path.join(self.st.PATH_SET["sound"], "sound"))
        self.Support_Part_GetSoundManage().Ready()

    def System_Support_Part_LoadCtrl(self):
        self.system_support_part_ctrl_manage.start()
        self.Support_Part_GetCtrlManage().SetTick(self.st.FREQUENCY)
        self.Support_Part_GetCore().ImportCtrls(self)
        self.Support_Part_GetCtrlManage().Ready()

    def System_Support_Part_LoadEve(self):
        self.system_support_part_eve_manage.start()
        self.Support_Part_GetEveManage().SetTick(self.st.FREQUENCY)
        for i in self.ev.LogEveLoading():
            self.Support_Part_GetEveManage().AddNewEvent(i)
        self.Support_Part_GetEveManage().Ready()

    def System_Support_Part_LoadImg(self):
        self.system_support_part_img_manage.start()
        self.Support_Part_GetImgManage().SetTick(self.st.FREQUENCY)
        self.Support_Part_GetCore().ImportImgs(self, self.st.PATH_SET["img"])
        self.Support_Part_GetSoundManage().Ready()

    def System_Support_Part_LoadWin(self):
        self.system_support_part_win_manage.start()
        self.Support_Part_GetWinManage().SetTick(self.st.FREQUENCY)
        self.Support_Part_GetCore().ImportWins(self)
        self.Support_Part_GetWinManage().Ready()

    def System_Support_Part_DoPeriodicTask(self, maker, delta_time, func, **kwargs):
        delta_tick = (delta_time * self.st.FREQUENCY) // 1
        self.Support_Part_GetEveManage().AddQueue("DoPeriodicTask", maker=maker, delta_tick=delta_tick, func=func,
                                                  task_id=maker.task_id, kwargs=kwargs)
        maker.task_id += 1
        return maker.task_id - 1

    def System_Support_Part_CancelPeriodicTask(self, maker, period_id):
        self.Support_Part_GetEveManage().AddQueue("CancelPeriodicTask", maker=maker, period_id=period_id)

    def Support_Part_GetWindow(self):
        """
        获取当前根视图
        Get the current root view
        :return: object --> 实例化视图对象 Instantiate View Object
        """
        return self.system_support_part_target_win

    def Support_Part_GetCore(self):
        """
        获取核心对象
        Get Core Objects
        :return: object --> 核心对象 Core Objects
        """
        return self.core

    def Support_Part_GetAllWin(self):
        """
        获取当前已注册的所有视图
        Get all currently registered _views
        :return: list --> 视图列表 _views list
        """
        return self.system_support_part_win_manage.GetAllWin()

    def Support_Part_GetAllImg(self):
        """
        获取当前已注册的所有图片
        Get all currently registered p_images
        :return: list --> 图片列表 p_images list
        """
        return self.system_support_part_img_manage.GetAllImg()

    def Support_Part_GetAllEve(self):
        """
        获取当前已注册的所有事件
        Get all currently registered _events
        :return: list --> 事件列表 _events list
        """
        return self.system_support_part_eve_manage.GetAllEveName()

    def Support_Part_GetAllEveId(self):
        """
        获取当前已注册的所有事件id
        Get all currently registered _events' id
        :return: list --> 事件id列表 _events' id list
        """
        return self.system_support_part_eve_manage.GetAllEveId()

    def Support_Part_GetImgManage(self):
        """
        获取图片管理器
        Get Image Manager
        :return: object --> 图片管理器 Image Manager
        """
        return self.system_support_part_img_manage

    def Support_Part_GetEveManage(self):
        """
        获取事件管理器
        Get Event Manager
        :return: object --> 事件管理器 Event Manager
        """
        return self.system_support_part_eve_manage

    def Support_Part_GetWinManage(self):
        """
        获取视图管理器
        Get View Manager
        :return: object --> 视图管理器 View Manager
        """
        return self.system_support_part_win_manage

    def Support_Part_GetCtrlManage(self):
        """
        获取控制管理器
        Get Controller Manager
        :return: object --> 控制管理器 Controller Manager
        """
        return self.system_support_part_ctrl_manage

    def Support_Part_GetGroupManage(self):
        """
        获取分组管理器
        Get Group Manager
        :return: object --> 分组管理器 Group Manager
        """
        return self.system_support_part_group_manage

    def Support_Part_GetCamera(self):
        """
        获取相机
        Get Camera
        :return: object --> 相机 Camera
        """
        return self.system_support_part_camera

    def Support_Part_MoveCamera(self, aim_pos, tick):
        """
        移动相机
        :param aim_pos: tuple(int,int) 目标点
        :param tick: int 间隔帧
        :return: None
        """
        self.Support_Part_GetCamera().MoveCamera(aim_pos, tick)

    def Support_Part_GetSoundManage(self):
        """
        获取声音管理器
        Get Sound Manager
        :return: object --> 声音管理器 Sound Manager
        """
        return self.system_support_part_sound_manage

    def Support_Part_GetScreen(self):
        """
        获取显示屏幕
        Get Display Screen
        :return: object --> 显示区域的屏幕 Display Screen
        """
        return self.screen
