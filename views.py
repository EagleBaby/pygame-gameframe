from warnings import warn

import numpy as np


def d_pos(x, y):
    def Wrapper(_view_type_cls):
        def Inner_Wrapper(*args, **kwargs):
            return _view_type_cls(*args, **kwargs, _pos=(x, y))

        return Inner_Wrapper

    return Wrapper


def d_percent(percent_x, percent_y):
    def Wrapper(_view_type_cls):
        def Inner_Wrapper(*args, **kwargs):
            return _view_type_cls(*args, **kwargs, _percent=(percent_x, percent_y))

        return Inner_Wrapper

    return Wrapper


def d_size(width, height):
    def Wrapper(_view_type_cls):
        def Inner_Wrapper(*args, **kwargs):
            return _view_type_cls(*args, **kwargs, _size=(width, height))

        return Inner_Wrapper

    return Wrapper


def d_layer(layer):
    def Wrapper(_view_type_cls):
        def Inner_Wrapper(*args, **kwargs):
            return _view_type_cls(*args, **kwargs, _layer=layer)

        return Inner_Wrapper

    return Wrapper


def d_show(isShow=True):
    def Wrapper(_view_type_cls):
        def Inner_Wrapper(*args, **kwargs):
            return _view_type_cls(*args, **kwargs, _show=isShow)

        return Inner_Wrapper

    return Wrapper


def d_view(param):
    """
    添加view(只能对同类对象使用)
    :param _views: [[class_View, kwargs], ......]
    :return: None
    """

    def Wrapper(_view_type_cls):
        def Inner_Wrapper(*args, **kwargs):
            return _view_type_cls(*args, **kwargs, _views=param)

        return Inner_Wrapper

    return Wrapper


def d_cp(param):
    """
    添加components
    :param param: [[component_name, kwargs], ......]
    :return: None
    """

    def Wrapper(_view_type_cls):
        def Inner_Wrapper(*args, **kwargs):
            return _view_type_cls(*args, **kwargs, _components=param)

        return Inner_Wrapper

    return Wrapper


def d_ct(param):
    """
    添加controllers
    :param param: [controllers_name, ......]
    :return: None
    """

    def Wrapper(_view_type_cls):
        def Inner_Wrapper(*args, **kwargs):
            return _view_type_cls(*args, **kwargs, _components=param)

        return Inner_Wrapper

    return Wrapper


def _anim(param):
    """
    添加anim(只能对同类对象使用)
    :param param: [[class_Anim, kwargs], ......]
    :return: None
    """

    def Wrapper(_view_type_cls):
        def Inner_Wrapper(*args, **kwargs):
            return _view_type_cls(*args, **kwargs, _anims=param)

        return Inner_Wrapper

    return Wrapper


def d_spirit(param):
    """
    添加spirit
    :param param: [[ArtDef, kwargs], ......]
    :return: None
    """

    def Wrapper(_view_type_cls):
        def Inner_Wrapper(*args, **kwargs):
            return _view_type_cls(*args, **kwargs, _spirits=param)

        return Inner_Wrapper

    return Wrapper


class BaseView(object):
    auto = False

    def __init__(self, data, inst=None, view_id=None, show=True, **kwargs):
        self.inst = inst
        self.data = data
        self.TypeView = None

        self.layer = 0
        if kwargs.get("_layer"):
            self.layer = kwargs["_layer"]

        self.pos = None
        if kwargs.get("_pos"):
            self.pos = kwargs["_pos"]

        self.perpos = (0, 0)
        if kwargs.get("_percent"):
            self.perpos = kwargs["_percent"]

        self.size = data.st.DEFAULT_WINDOW_SIZE
        if kwargs.get("_size"):
            self.size = kwargs["_size"]

        self._show = show
        if kwargs.get("_show"):
            self._show = kwargs["_show"]

        self._wait = []  # [(code_list, per_tick)]
        self._camera_last_pos = data.Support_Part_GetCamera().GetPos()
        self._camera_scale = data.Support_Part_GetCamera().GetScaleRate()
        self._views = dict()
        self._components = dict()
        self._self_id = view_id
        self.task_id = 0
        self._vw_id = 0
        self._cp_id = 0
        self._queue = []
        self.tag = list()

    def GetId(self):
        """
        获取view id
        :return: int view id
        """
        return self._self_id

    def PlaySound(self, name, volume=100):
        """
        播放声音和音乐，如果音乐和音乐处于播放状态，则将在音乐播放完毕后播放。
        Play sound and music,if music and music is on play then will play after music now finish play.
        :param name: string --> filename without .xxx
        :param volume: int --> if it is possible，it will affect sound' s volume.
        :return: None
        """
        self.data.Support_Part_GetSoundManage().AddQueue("SoundEffect", name=name, volume=volume)

    def StopSound(self):
        """
        停止音乐（声音无法停止），将丢失所有等待的音乐。
        Stop music(sound can not be stopped), will lost all waited music.
        :return: None
        """
        self.data.Support_Part_GetSoundManage().AddQueue("SoundStop")

    def PauseSound(self):
        """
        暂停音乐（声音不能暂停），不会丢失等待的音乐。
        Pause music(sound can not be paused), will not lost waited music.
        :return: None
        """
        self.data.Support_Part_GetSoundManage().AddQueue("SoundPause")

    def StartSound(self):
        """
        开始暂停的音乐（无法启动声音）
        Start paused music(sound can not be started)
        :return: None
        """
        self.data.Support_Part_GetSoundManage().AddQueue("SoundStart")

    def GetCenterPos(self, absolute=False):
        """
        获取视图的中心位置
        Get view' s center position
        :param absolute: Bool True-->绝对参考系;False-->相机参考系,默认True
        :return: position tuple(int/float left, int/float top)
        """
        pos = self.GetPos()
        return int(pos[0] + self.size[0] * .5), int(pos[1] + self.size[1] * .5)

    def GetCenterPerPos(self):
        """
        获取当前视图中心点在父视图的相对位置百分比
        Gets the relative position percentage of the current view center point in the parent view
        :return: percent tuple(float --> per_X,float --> per_Y)
        """
        if self.inst:
            size = self.inst.GetSize()
            pos = self.inst.GetPos()
            return (self.pos[0] - pos[0] + self.size[0] * .5) / size[0], (self.pos[1] - pos[1] + self.size[1] * .5) / \
                   size[1]
        else:
            return (self.data.Support_Part_GetScreen().get_width() * self.perpos[0] + self.size[
                0] * .5) / self.data.Support_Part_GetScreen().get_width(), \
                   (self.data.Support_Part_GetScreen().get_height() * self.perpos[0] + self.size[
                       1] * .5) / self.data.Support_Part_GetScreen().get_height()

    def GetPercent(self, axis=None):
        """
        获取当前视图位置在父视图中的相对位置百分比(这个百分比只与自身与父窗口有关，与相机位置无关)
        Gets the relative position percentage of the current view position in the parent view
        :param axis: 0/1 表示仅返回横向百分比或仅返回纵向百分比 Indicates that only horizontal percentage or vertical percentage is returned
        :return: percent tuple(float --> per_X,float --> per_Y) or float --> per_X or float --> per_Y
        """
        if self.pos:
            if self.inst:
                size = self.inst.GetSize()
                pos = self.inst.GetPos()
                temp = (self.pos[0] - pos[0]) / size[0], (self.pos[1] - pos[1]) / size[1]
            else:
                temp = (self.data.Support_Part_GetScreen().get_width() * self.perpos[
                    0]) / self.data.Support_Part_GetScreen().get_width(), \
                       (self.data.Support_Part_GetScreen().get_height() * self.perpos[
                           0]) / self.data.Support_Part_GetScreen().get_height()
        else:
            temp = self.perpos
        if axis is not None:
            return temp[axis]
        return temp

    def SetPercent(self, percent, reset=False):
        """
        设置当前视图在父视图中的百分比
        Sets the percentage of the current view in the parent view
        :param percent: float --> 当前视图在父视图中的百分比 The percentage of the current view in the parent view
        :param reset: bool --> 是否运用到当前视图的当前位置(即立刻改变位置到指定百分比) Whether to apply to the current position of the current view (i.e. immediately change the position to a specified percentage)
        :return: None
        """
        self.perpos = percent
        if reset:
            self.ResetPos()

    def GetPos(self, absolute=False):
        """
        获得当前视图在绝对参考系中或相机参考系中的位置
        Get the location of the current view
        :param absolute: Bool True-->绝对参考系;False-->相机参考系,默认True
        :return: position tuple(int/float --> x,int/float --> y)
        """
        if absolute or not self.pos:
            return self.pos
        else:
            a, b = self.data.Support_Part_GetCamera().GetPos()
            return self.pos[0] - a, self.pos[1] - b

    def __GetPosition(self):
        return self.inst.pos[0] + self.inst.size[0] * self.perpos[0], self.inst.pos[1] + self.inst.size[1] * \
               self.perpos[1]

    def SetPos(self, pos):
        """
        设置当前视图在绝对参考系的位置
        Set the location of the current view
        :param pos: tuple(int/float --> x,int/float --> y)
        :return: None
        """
        self.pos = pos

    def SetCenterPos(self, pos):
        """
        设置当前视图的中心位置
        Set the center location of the current view
        :param pos: tuple(int/float --> x,int/float --> y)
        :return: None
        """

        self.SetPos((pos[0] - int(self.size[0] * .5), pos[1] - int(self.size[1] * .5)))

    def ResetPos(self):
        """
        重置位置为当前视图在父视图中的相对百分比处的位置
        Resets the position to the relative percentage of the current view in the parent view
        :return: None
        """
        self.pos = None

    def GetSize(self):
        """
        获取当前视图的尺寸
        Get the size of the current view
        :return: size tuple(int/float --> width,int/float --> height)
        """
        if self.auto:
            return self.data.st.DEFAULT_WINDOW_SIZE
        return self.size

    def SetSize(self, size):
        """
        设置视图的大小(根视图无法调整大小，若需调整根视图大小，请在设置中调整)
        Set the size of the current view
        :param size: size tuple(int/float --> width,int/float --> height)
        :return: None
        """
        if self.auto:
            raise (Exception("Root View can not SetPos. If you want, please set in settings."))
        self.size = size

    def Hide(self):
        """
        隐藏视图，原先处于显示状态下的视图内绑定的所有对象都会停止工作(原先处于隐藏状态下的视图不受影响)
        Hide the view. All objects bound in the view in the original display state will stop working (the view in the original hidden state will not be affected)
        :return: None
        """
        if self._show:
            self._show = False
            self.data.Support_Part_GetWinManage().AddQueue("HappenDisabled", view=self)

    def Show(self):
        """
        显示视图，原先处于隐藏状态下的视图内绑定的所有对象都会开始工作(原先处于显示状态下的视图不受影响)
        Display view, all objects bound in the view in the previously hidden state will start to work (the view in the previously displayed state will not be affected)
        :return: None
        """
        if not self._show:
            self._show = True
            self.data.Support_Part_GetWinManage().AddQueue("HappenEnabled", view=self)

    def GetStatus(self):
        """
        获取当前视图是否可见
        Get whether the current view is visible
        :return: bool--> 可见:True;不可见:False
        """
        return self._show


class View(BaseView):
    """
    mcv中的v部分，显示在屏幕上
    可绑定组件和控制器(c)

    """

    def __init__(self, data, inst=None, __system_calling_trig__=False, view_id=None, **kwargs):
        super().__init__(data, inst, view_id, **kwargs)

        if kwargs.get("_views"):
            for i in kwargs["_views"]:
                self.AddView(i[0], **i[1])

        if kwargs.get("_components"):
            for i in kwargs["_components"]:
                self.AddComponent(i[0], **i[1])

        if kwargs.get("_controllers"):
            for i in kwargs["_controllers"]:
                self.LogController(i)

        self._ctrl_name = dict()
        self._ct_id = 0
        self._task_id = 0
        self._events = dict()  # event_id --> event_func
        self._periods = dict()  # period_id --> [dt,task_func,kwargs]
        self._kwargs = kwargs
        self.__system_calling_trig__ = __system_calling_trig__
        if not __system_calling_trig__:
            self.Loading(**kwargs)
            self.data.Support_Part_GetWinManage().AddQueue("HappenEnabled", view=self)
            if self.inst and self.size == data.st.DEFAULT_WINDOW_SIZE:
                warn(Warning(self.__class__.__name__ + "doesn' t set size, it will use the default size in setting."))

    def GetLayer(self):
        """
        获得view所处的层级
        :return:
        """
        return self.layer

    def system_redo(self):
        """
        系统调用，用户调用可能导致bug
        :return: None
        """
        if self.auto and self.__system_calling_trig__:
            self.Loading(**self._kwargs)
            if self.inst and self.size == data.st.DEFAULT_WINDOW_SIZE:
                warn(Warning(self.__class__.__name__ + "doesn' t set size, it will use the default size in setting."))

    def __call__(self, *args, **kwargs):
        pass

    def GetListenTask(self, event_id):
        """
        按唯一id获取侦听任务（由用户发出）
        Get listen task by unique id(by user)
        :param event_id: int --> event id
        :return: function --> event function
        """
        return self._events[event_id]

    def GetListenTasks(self):
        """
        获取所有侦听任务（由用户发出）
        Get listen tasks(by user)
        :return: function list --> event functions list
        """
        return self._events

    def GetPeriodicTask(self, period_id):
        """
        获取周期事件的函数
        Get function of periodic event
        :param period_id: int --> 周期事件的id
        :return: function --> 周期事件的函数
        """
        return self._periods[period_id]

    def GetPeriodicTasks(self):
        """
        获取所有周期事件的函数
        Get all functions of periodic event
        :return: function list --> 周期事件的函数列表
        """
        return self._periods

    def Loading(self, **kwargs):
        """
        用户在这里写自己的额外的初始化代码
        Users write their own additional initialization code here
        :param kwargs: **dict --> 自动传递__init__中的kwargs
        :return: None 
        """
        pass

    def AddView(self, view, sign=None, **kwargs):
        """
        为当前视图添加一个子视图
        Add a subview to the current view
        :param view: class --> 子视图的类对象 Class object for subview
        :param sign: String 设置子视图在此视图中的变量名称,None表示不添加
        :param kwargs: **dict --> 子视图的类对象的参数键值对 Parameter Key-Value Pairs of Class Objects in Subview
        :return: int --> 子视图的id ID of subview
        """
        if not kwargs.get("inst"):
            kwargs["inst"] = self
        temp = view(self.data, view_id=self._vw_id, **kwargs)
        if not hasattr(temp, "TypeView"):
            raise (TypeError(str(type(view)) + "is not a BaseView object."))
        self._views[self._vw_id] = temp
        if sign:
            setattr(self, sign, self._views[self._vw_id])
        self._vw_id += 1
        return self._vw_id - 1

    def RemoveView(self, view_id):
        """
        移除指定的子视图
        Remove the specified subview
        :param view_id: int --> 子视图的id ID of subview
        :return: None
        """
        self.data.Support_Part_GetWinManage().AddQueue("HappenDisabled", view=self._views[view_id])
        del self._views[view_id]

    def GetView(self, view_id):
        """
        获取指定的子视图
        Gets the specified subview
        :param view_id: int --> 子视图的id ID of subview
        :return: object --> 子视图的实例化对象 Instantiated objects for subviews
        """
        return self._views[view_id]

    def GetViews(self):
        """
        获取所有的子视图
        Get all subviews
        :return: list --> 子视图实例化对象列表 Subview Instantiate Object List
        """
        return self._views.values()

    def LogController(self, controller_name):
        """
        为当前视图注册控制器,视图完成加载后将不再接收此函数
        Register Controller for Current View
        :param controller_name: string --> 控制器的类名 Class name of the controller
        :return: int --> 控制器id Controller ID
        """
        self._ctrl_name[self._ct_id] = controller_name
        self._ct_id += 1
        return self._ct_id

    def CancelController(self, controller_id):
        """
        取消当前视图的一个已注册的控制器,视图完成加载后将不再接收此函数
        Cancel a registered controller for the current view
        :param controller_id: int --> 控制器的id ID of controller
        :return: None
        """
        del self._ctrl_name[controller_id]

    def GetCtrlInfos(self):
        """
        获取所有当前视图的已注册的控制器的注册时的名称信息
        Gets the name information at the time of registration for all registered controllers of the current view
        :return: list --> 控制器的名称信息列表 List of Controller Name Information
        """
        return self._ctrl_name.values()

    def GetCtrlInfo(self, controller_id):
        """
        获取当前视图内指定的已注册的控制器的注册时的名称信息
        Gets the name information for the registered controller specified in the current view at the time of registration
        :param controller_id: int --> 控制器id ID of controller
        :return: string --> 控制器的名称信息 Controller name information
        """
        return self._ctrl_name[controller_id]

    def AddComponent(self, component_name, **kwargs):
        """
        为当前视图添加组件
        Add Components for Current View
        :param component_name: string --> 组件的类名 The class name of the component
        :param kwargs: **dict --> 组件实例化所需的参数的键值对 Key-value pairs of parameters required for component instantiation
        :return: int --> 组件的id ID of component
        """
        self._components[self._cp_id] = getattr(self.data.cp, component_name)(self, **kwargs)
        self._cp_id += 1
        return self._cp_id - 1

    def GetComponents(self):
        """
        获取所有的组件
        Get all _components
        :return: list --> 实例化组件列表 List of instantiated _components
        """
        return self._components.values()

    def GetComponent(self, component_id):
        """
        获取指定的组件
        Gets the specified component
        :param component_id: int --> 组件的id ID of component
        :return: object --> 实例化组件 instantiated component
        """
        return self._components[component_id]

    def RemoveComponent(self, component_id):
        """
        移除指定的组件
        Remove the specified component
        :param component_id: int --> 组件的id ID of component
        :return: None
        """
        self._components[component_id].remove()
        del self._components[component_id]

    def AddQueue(self, func, **kwargs):
        """
        添加队列任务,但是你无法获得返回值
        :param func: String/Func 函数名/函数
        :param kwargs: **dict参数键值对
        :return: None
        """
        self._queue.append((func, kwargs))

    def Update(self):
        """
        更新视图
        Update the current view.
        :return: None
        """
        if self._queue:
            for i in self._queue:
                if isinstance(i[0], str):
                    getattr(self, i[0])(**i[1])
                else:
                    i[0](**i[1])
            self._queue = []

        self.data.Support_Part_GetCore().GetViewAtPosition(self.data, self)
        self.data.Support_Part_GetCore().UpdateView(self.data, self)

    def PushEvent(self, event_name, **kwargs):  # id must > 24
        """
        通过根视图触发指定事件
        Trigger the specified event through the root view
        :param event_name: string --> 事件名称 Event Name
        :param kwargs: **dict --> 事件的参数键值对 Parameter key-value pairs for _events
        :return: None
        """
        if self.inst is not None:
            self.inst.PushEvent(event_name, **kwargs)
        else:
            self.data.Support_Part_GetEveManage().PushEvent(self, event_name, **kwargs)

    def ListenForEvent(self, event_name, func):
        """
        通过根视图监听指定事件
        Listen for specified _events through root view
        :param event_name: string --> 事件名称 Event Name
        :param func: function(eve,data) --> 事件处理函数 Event Handler
        :return: None
        """
        if self.inst is not None:
            self.inst.ListenForEvent(event_name, func)
        else:
            self.data.Support_Part_GetEveManage().ListenForEvent(self, event_name, func)

    def DoPeriodicTask(self, delta_time, func, **kwargs):
        """
        对根视图添加周期任务
        Add cycle task to root view
        :param delta_time: int/float --> 周期任务的周期时间 Cycle time for periodic tasks
        :param func: function(**kwargs) --> 执行函数 Function to be executed
        :param kwargs: **dict --> 执行函数的其他参数的键值对 Key-value pairs for other parameters of the execution function
        :return: int --> 周期任务id ID of Cycle Task
        """
        if self.inst is not None:
            return self.inst.DoPeriodicTask(delta_time, func, **kwargs)
        else:
            return self.data.System_Support_Part_DoPeriodicTask(self, delta_time, func, **kwargs)

    def CancelListen(self, event_name):
        """
        取消根视图对指定事件的监听
        Cancel root view listening to specified _events
        :param event_name: string --> 事件名称 Event Name
        :return: None
        """
        if self.inst is not None:
            return self.inst.CancelListen(event_name)
        else:
            self.data.Support_Part_GetEveManage().CancelListen(self, event_name)

    def CancelPeriod(self, period_id):
        """
        取消根视图指定的周期任务
        Cancel cycle task specified by root view
        :param period_id: int --> 周期事件id ID of Cycle Task
        :return: None
        """
        if self.inst is not None:
            self.inst.CancelPeriod(period_id)
        else:
            self.data.System_Support_Part_CancelPeriodicTask(self, period_id)

    def MapInit(self, shape, view, area=(0., 0., 1., 1.), between=(0, 0), filter=None, **kwargs):
        """
        为视图创建一个views map
        :param shape: tuple(int,int) map的形状
        :param view: View 填充的视图,额外传递矩阵信息x，y(0,0<=x,y<=shape[0],shape[1]),额外设置属性map_pos(x,y)
        :param area: tuple(float，float，float，float) map区域
        :param between: tuple(int,int) 区块间隔
        :param filter: map(Bools...) 选择性填充
        :param kwargs: **dict View的参数
        :return: 2d-array --> Views   返回 _views map
        """
        if self.auto == False and self.size == self.data.st.DEFAULT_WINDOW_SIZE:
            print("-->Warning: In " + self.__class__.__name__ + ", you create the map without .SetSize()")
        if self.auto == False:
            if self.pos is None:
                print("-->Warning: In " + self.__class__.__name__ + ", you create the map without .SetPos()")
                self.SetPos((0, 0))
                trig = True
        else:
            self.SetPos((0, 0))
        if self.auto == False and self.perpos != (0, 0):
            print(
                "-->Warning: In " + self.__class__.__name__ + ", if you want to create a map, the .SetPerpos() will lose it's effect on your map.")
        size = self.GetSize()
        srt = self.GetPos()[0] + int(area[0] * size[0]), self.GetPos()[1] + int(size[1] * area[1])
        end = self.GetPos()[0] + int(area[2] * size[0]), self.GetPos()[1] + int(size[1] * area[3])
        size = [end[0] - srt[0], end[1] - srt[1]]
        size[0], size[1] = (size[0] - (shape[0] - 1) * between[0]) // shape[0], (
                size[1] - (shape[1] - 1) * between[1]) // shape[1]
        self.view_map = []
        self.map = []
        for i in range(shape[0]):
            for j in range(shape[1]):
                if filter is None or filter[i, j]:
                    self.map.append(self.AddView(view, x=i, y=j, **kwargs))
                    self.view_map.append(self.GetView(self.map[-1]))
                    self.view_map[-1].SetSize(size)
                    self.view_map[-1].SetPos(
                        (srt[0] + size[0] * i + between[0] * (i - 1), srt[1] + size[1] * j + between[1] * (j - 1)))
                    self.view_map[-1].map_pos = (i, j)
                else:
                    self.view_map.append(None)
                    self.map.append(None)
        self.map = np.array(self.map).reshape(shape)
        self.view_map = np.array(self.view_map).reshape(shape)

        try:
            a = trig
            self.SetPos(None)
        except:
            pass

        return self.view_map

    def __getitem__(self, item):
        x, y = item
        if hasattr(self, "view_map"):
            return self.view_map[x, y]
        else:
            raise (TypeError("'" + self.__class__.__name__ + "' object is not subscriptable"))

    def __delitem__(self, item):
        x, y = item
        if hasattr(self, "view_map"):
            self.RemoveView(self.map[x, y])
            self.map[x, y] = None
            self.view_map[x, y] = None
        else:
            raise (TypeError("'" + self.__class__.__name__ + "' object is not subscriptable"))


class Label(View):
    def Loading(self, **kwargs):
        l, t, w, h = kwargs.get('left', 0), kwargs.get('top', 0), kwargs.get('width', 60), kwargs.get('height', 20)
        text, pic = kwargs.get('text', ''), kwargs.get('pic', '')
        font_size, font = kwargs.get('font', (30, None))
        font_color = kwargs.get('fg', (255, 255, 255))
        font_bold, font_italic = kwargs.get('bold', False), kwargs.get('italic', False)
        pic_size = str(kwargs.get('scale', 100))

        pic_justify, text_justify = kwargs.get('p_just', (0, 0)), kwargs.get('t_just', (0, 0))

        focus = kwargs.get('focus', '')
        cover = kwargs.get('cover', '')
        cover_size, cover_justify = kwargs.get('c_scale', '100'), kwargs.get('c_just', (0, 0))

        self.SetPos((l, t))
        self.SetSize((w, h))
        if pic != '':
            self.AddComponent('Pic', ArtDef=pic, scale=pic_size, justify=pic_justify, sign='pic')
        if cover != '':
            self.AddComponent('Pic', ArtDef=cover, scale=cover_size, justify=cover_justify, sign='cover',
                              show=False)  # cover默认隐藏
        if text != '':
            self.AddComponent('Text', text=text, size=font_size, font=font, color=font_color, show=True,
                              italic=font_bold, bold=font_italic, justify=text_justify, sign='text')
        if focus != '':
            self.LogController(focus)


class Button(Label):
    def Loading(self, **kwargs):
        super().Loading(**kwargs)
        self.LogController(kwargs['ctrl'])


class Anim(BaseView):
    """
    一个特殊的View，失去了大部分view的功能，然后添加了一些View所不具有的特性
    比View更精简，有利于节约程序资源
    与View相比，Anim
    *不能参与event和periodic task
    *不能参与控制器响应
    *取消AddComponent、GetComponent、GetComponents、RemoveComponent函数，取而代之的是AddSpirit、GetSpirit、GetSpirits、RemoveSpirit
    *只支持Pic组件(Spirit在本质上是一个Pic组件)
    *取消AddView、GetView、GetViews、RemoveView函数，取而代之的是AddAnim、GetAnim、GetAnims、RemoveAnim
    *只支持Anim视图(Anim在本质上是一个View对象)
    """

    def __init__(self, data, inst=None, __system_calling_trig__=False, view_id=None, **kwargs):
        super().__init__(data, inst, view_id, **kwargs)

        if kwargs.get("_anims"):
            for i in kwargs["_anims"]:
                self.AddAnim(i[0], **i[1])

        if kwargs.get("_spirits"):
            for i in kwargs["_spirits"]:
                self.AddSpirit(i[0], **i[1])

        self.TypeView = "Anim"
        self.layer = -1
        self._kwargs = kwargs
        self.__system_calling_trig__ = __system_calling_trig__
        if not __system_calling_trig__:
            self.Loading(**kwargs)
            self.data.Support_Part_GetWinManage().AddQueue("HappenEnabled", view=self)
            if self.inst and self.size == data.st.DEFAULT_WINDOW_SIZE:
                warn(Warning(self.__class__.__name__ + "doesn' t set size, it will use the default size in setting."))

    def Default(self):
        """
        Anim特殊状态设置函数，设置动画的默认状态
        当Anim被创建完成后自动执行，将动画调整为默认状态
        :return:
        """
        pass

    def system_redo(self):
        """
        系统调用，用户调用可能导致bug
        :return: None
        """
        if self.auto and self.__system_calling_trig__:
            self.Loading(**self._kwargs)
            if self.inst and self.size == data.st.DEFAULT_WINDOW_SIZE:
                warn(Warning(self.__class__.__name__ + "doesn' t set size, it will use the default size in setting."))

    def __call__(self, *args, **kwargs):
        pass

    def Loading(self, **kwargs):
        """
        用户在这里写自己的额外的初始化代码
        Users write their own additional initialization code here
        :param kwargs: **dict --> 自动传递__init__中的kwargs
        :return: None
        """
        pass

    def DoThingsInTick(self, codes, tick):
        """
        Anim特殊方法，可以按行匀速执行code中的代码，环境在self下
        :param codes: list(Str...) 程序代码，记得用\n换行
        :param tick: Int 总帧数(在多少帧内完成这段代码)
        :return: None
        """
        code_split = codes
        per_tick = (tick / len(code_split) + .5) // 1
        self._wait += [(code_split, per_tick)]

    def AddQueue(self, func, **kwargs):
        """
        添加队列任务,但是你无法获得返回值
        :param func: String/Func 函数名/函数
        :param kwargs: **dict参数键值对
        :return: None
        """
        self._queue.append((func, kwargs))

    def AddAnim(self, anim, sign=None, **kwargs):
        """
        为当前动画视图添加一个子动画视图
        Add a subview to the current view
        :param anim: class --> 子动画视图的类对象 Class object for subanim
        :param sign: String 设置子视图在此视图中的变量名称,None表示不添加
        :param kwargs: **dict --> 子视图的类对象的参数键值对 Parameter Key-Value Pairs of Class Objects in Subview
        :return: int --> 子视图的id ID of subview
        """
        if not kwargs.get("inst"):
            kwargs["inst"] = self
        temp = anim(self.data, view_id=self._vw_id, **kwargs)
        if not hasattr(temp, "TypeView"):
            raise (TypeError(str(type(anim)) + "is not a BaseView object."))
        elif anim.TypeView != "Anim":
            raise (TypeError(str(type(anim)) + "is not a Anim object."))
        self._views[self._vw_id] = temp

        if sign:
            setattr(self, sign, self._views[self._vw_id])
        self._vw_id += 1
        return self._vw_id - 1

    def RemoveAnim(self, anim_id):
        """
        移除指定的子动画视图
        Remove the specified subview
        :param anim_id: int --> 子动画视图的id ID of subview
        :return: None
        """
        self.data.Support_Part_GetWinManage().AddQueue("HappenDisabled", view=self._views[anim_id])
        del self._views[anim_id]

    def GetAnim(self, anim_id):
        """
        获取指定的子动画视图
        Gets the specified subanim
        :param anim_id: int --> 子动画视图的id ID of subanim
        :return: object --> 子动画视图的实例化对象 Instantiated objects for subanims
        """
        return self._views[anim_id]

    def GetAnims(self):
        """
        获取所有的子动画视图
        Get all subviews
        :return: list --> 子动画视图实例化对象列表 Subanim Instantiate Object List
        """
        return self._views.values()

    def AddSpirit(self, ArtDef, sign=None, show=True, scale="100", rotate="000", hflip="0", vflip="0", tim=0,
                  keep_tim=0,
                  justify=(0, 0), end_func=None, center=True):
        """
        为当前视图添加图片元素
        Add spirit for Current Anim
        :param ArtDef: 艺术数据名String
        :param sign: String 设置图片元素在inst中的变量名称,None表示不添加
        :param show: Bool 设置图片元素是否可见
        :param scale: 缩放倍率Int 0~100 (100->100%, 10->10%)(传入String类型能减少程序资源占用)
        :param rotate: 旋转角度Int 0~360 (向上为0, 顺时针旋转)(传入String类型能减少程序资源占用)
        :param hflip: 水平翻转Int 0/1(1表示水平翻转)(传入String类型能减少程序资源占用)
        :param vflip: 竖直翻转Int 0/1(1表示竖直翻转)(传入String类型能减少程序资源占用)
        :param tim: 图片间隔帧Int(只适用于多图片,控制图片播放时间隔的帧数)
        :param keep_tim: 持续帧数Int(显示多少帧，大于此数时，该组件会被隐藏)
        :param justify: Tuple(int, int) 图片位置微调
        :param end_func: function(pic= Pic Components) 允许Pic即将Hide时激活函数
        :param center: 是否以中心为基准点Bool(传入False能减少程序资源占用), 默认True
        :return: int --> 元素的id ID of spirit
        """
        self._components[self._cp_id] = getattr(self.data.cp, "Pic")(self, ArtDef=ArtDef, scale=scale, rotate=rotate,
                                                                     hflip=hflip, vflip=vflip, tim=tim,
                                                                     keep_tim=keep_tim, justify=justify, sign=sign,
                                                                     end_func=end_func, center=center)
        if not show:
            self._components[self._cp_id].Hide()
        self._cp_id += 1
        return self._cp_id - 1

    def GetSpirits(self):
        """
        获取所有的图片元素
        Get all _spirits
        :return: list --> 实例化图片元素列表 List of instantiated _spirits
        """
        return self._components.values()

    def GetSpirit(self, spirit_id):
        """
        获取指定的图片元素
        Gets the specified spirit
        :param spirit_id: int --> 图片元素的id ID of spirit
        :return: object --> 实例化图片元素 instantiated spirit
        """
        return self._components[spirit_id]

    def RemoveSpirit(self, spirit_id):
        """
        移除指定的图片元素
        Remove the specified spirit
        :param spirit_id: int --> 组件的id ID of spirit
        :return: None
        """
        self._components[spirit_id].remove()
        del self._components[spirit_id]

    def Update(self):
        """
        更新视图
        Update the current view.
        :return: None
        """
        if self._queue:
            for i in self._queue:
                if isinstance(i[0], str):
                    getattr(self, i[0])(**i[1])
                else:
                    i[0](**i[1])
            self._queue = []

        for i in self._wait:
            codes, p_rick = i
            if not codes:
                self._wait.remove(i)
                continue
            if self.data.Support_Part_GetTick() % p_rick == 0:
                eval(codes.pop(0))

        self.data.Support_Part_GetCore().GetViewAtPosition(self.data, self)
        self.data.Support_Part_GetCore().UpdateView(self.data, self)

    # 代码生成器
    class Generator(object):
        def __init__(self, Pic):
            self.inst = Pic

        def generate(self, command, aim, **kwargs):
            code = ""
            if command == "scale":
                return "self." + aim + ".Scale(" + kwargs["value"] + ")"
