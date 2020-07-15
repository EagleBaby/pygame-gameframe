from pgframe.core import *


class Component(object):
    """
    基本的组件，可以被视图添加
    """

    def __init__(self, inst, sign=None):
        """
        可以被View调动的具有组合性质的组件基类，可以完成很多事情
        :param inst: View 调动者(通用解释:实体)
        :param sign: String 设置组件在inst中的变量名称,None表示不添加
        """
        self.inst = inst
        self.data = inst.data
        self.inst.tag.append(self.__class__.__name__)
        self.sign = sign
        if sign:
            setattr(self.inst, sign, self)

    def GetSign(self):
        """
        获得标记的名称
        :return: String
        """
        return self.sign

    def remove(self):
        """
        移除组件，一般为系统调用
        如果用户自行调用，可能导致没能完全移除，导致bug
        :return: None
        """
        self.inst.tag.remove(self.__class__.__name__)

    def effect(self, **kwargs):
        """
        获得标记的名称
        :return: String
        """
        pass


class Area(Component):
    """
    通过一确定的矩形、圆形区域，确定inst视图下处于该区域内的视图，并可对其进行操作
    需要事先指定rect(矩形区域)，shape(区域形状,只支持rect和circle，默认rect)，mode(检测模式，只支持point(只看view的中心点是否在区域中)和area，默认point)，ban(舍弃的view list)，aim(目标视图list)
    使用GetFliter来获取所有满足条件的view
    设置func(view,**kwargs)(对处于区域中的视图的进行操作的函数)，tim(函数每多少帧执行一次)
    """

    def __init__(self, inst, sign=None, rect=(0, 0, 1, 1), shape="rect", mode="point", aim=(), ban=(), tim=0,
                 func=None):
        """
        确定一个区域，并检索区域内的view
        :param sign: String 设置组件在inst中的变量名称,None表示不添加
        :param rect: (x,y,w,h)/rect Area 区域
        :param shape: String 区域形状，rect 和 circle
        :param mode: String 检测模式，point 和 area 两种模式
        :param aim: tuple(_views...) 目标视图列表
        :param ban: tuple(_views...) 舍弃目标试图
        :param tim: 函数执行间隔帧，每一定帧数时自动检测并执行操作函数，默认为0
        :param func: function(view,**kwargs) 操作函数，默认为None(不检测且不执行)
        """
        super().__init__(inst, sign=sign)
        self.rect = pg.Rect(rect)
        self.shape = shape
        self.aim = aim
        self.ban = ban

        self.tick = Tick(tim)
        self.func = func

    def SetShape(self, shape):
        """
        设置区域形状
        :param shape: String 区域形状，rect 和 circle
        :return: None
        """
        self.shape = shape

    def GetShape(self):
        """
        获取区域形状
        :return: String
        """
        return self.shape

    def SetRect(self, rect):
        """
        设置区域
        :param rect: (x,y,w,h)/rect Area 区域
        :return: None
        """
        self.rect = pg.Rect(rect)

    def GetRect(self):
        """
        获得区域
        :return: rect
        """
        return self.rect

    def AdjustToInst(self):
        """
        设置area与inst相同
        :return: None
        """
        self.rect.left, self.rect.top = self.inst.GetPos()
        self.rect.width, self.rect.height = self.inst.GetSize()

    def SetFilter(self, aim=(), ban=()):
        """
        设置过滤器
        :param aim: view list 筛选下来的view类型列表
        :param ban: view list 舍弃的view类型列表
        :return: None
        """
        self.aim = aim
        self.ban = ban

    def __is_view_in_area__(self, view):
        """
        系统函数
        :param view:
        :return:
        """
        if self.shape == "rect":
            if self.mode == "point":
                return IsInArea(view.GetCenterPos(), (self.rect.left, self.rect.top),
                                (self.rect.width, self.rect.height))
            elif self.mode == "area":
                return self.rect.colliderect(
                    pg.Rect(view.GetPos()[0], view.GetPos()[1], view.GetSize()[0], view.GetSize()[1]))
            else:
                raise (Exception("don't support mode " + self.mode + "."))
        elif self.shape == "circle":
            if self.mode == "point":
                return IsInCircle(view.GetCenterPos(), (self.rect.centerx, self.rect.centery),
                                  min(self.rect.width, self.rect.height))
            elif self.mode == "area":
                return GetPointsDistance(view.GetCenterPos(), (self.rect.centerx, self.rect.centery)) < min(
                    self.rect.width, self.rect.height) + min(view.GetSize()[0], view.GetSize()[1])
            else:
                raise (Exception("don't support mode " + self.mode + "."))
        else:
            raise (Exception("don't support shape " + self.shape + "."))

    def GetFilter(self):
        """
        进行筛选
        :return: view list 符合条件的视图列表
        """
        return self.__check_sub__(self.inst)

    def __check_sub__(self, view):
        """
        系统函数
        :param view:
        :return:
        """
        temp = []
        for view in view.GetViews():
            if view not in self.ban and self.__is_view_in_area__(view) and view in self.aim:
                temp += [view]
            temp += self.__check_sub__(view)
        return temp

    def effect(self, **kwargs):
        """
        系统函数
        :param kwargs:
        :return:
        """
        if self.func and self.tick.tick():
            for i in self.GetFilter():
                self.func(i, **kwargs)


class Progress(Component):
    """
    创建一个进度条，必须依附于inst视图的形状和位置
    可以调整位置，默认显示
    可以设定边框，进度条本体，渐变条，背景条的颜色和透明度
    """

    def __init__(self, inst, max, now=0, color=(20, 190, 160), sub=False, sub_color=(255, 75, 75), sub_tick=20, bd=0,
                 show=True, bd_color=(100, 100, 100), bg_color=(125, 125, 125, 125), sign=None, justify=(0, 0)):
        """
        Progress组件，用于显示进度，只能横着显示
        :param max: Int 进度条最大值
        :param now: Int 进度条当前值
        :param show: Bool 是否可以显示，默认为True
        :param color: Tuple(Int R, Int G, Int B [, int alpha) 进度条的颜色
        :param sub: Bool 是否允许进度条渐变
        :param sub_color: Tuple(Int R, Int G, Int B [, int alpha)渐变颜色
        :param sub_tick: Int 渐变等待帧
        :param bd: Int 进度条边框厚度
        :param bd_color: Tuple(Int R, Int G, Int B [, int alpha): Int 进度条边框颜色
        :param bg_color: Tuple(Int R, Int G, Int B [, int alpha): Int 进度条背景颜色
        :param justify: Tuple(int, int) 进度条位置微调
        :param sign: String 设置组件在inst中的变量名称,默认None
        """
        super().__init__(inst, sign)
        self._max = max
        self._now = now
        self._bd = bd
        self._bd_color = bd_color
        self._bg_color = bg_color
        self._color = color

        self.sub = sub
        self.sub_color = sub_color
        self.sub_tick = sub_tick
        self.sub_rec = 0
        self.last = self._now

        self.__show__ = show
        self.rect = pg.Rect(0, 0, 1, 1)
        self.justify = justify

    def GetSubTick(self):
        """
        获取渐变帧设定值
        :return: Int
        """
        return self.sub_tick

    def GetSubTickNow(self):
        """
        获取渐变帧已等待当前值
        :return: Int
        """
        return self.sub_rec

    def GetSubStatus(self):
        """
        获取是否渐变状态
        :return: Bool
        """
        return self.sub

    def GetSubColor(self):
        """
        获取渐变颜色
        :return: Tuple(Int R, Int G, Int B [, int alpha)
        """
        return self.sub_color

    def SetSubTick(self, sub_tick):
        """
        设置渐变帧设定值
        :param sub_tick: Int 渐变等待帧
        :return:
        """
        self.sub_tick = sub_tick

    def SetSubTickNow(self, sub_rec):
        """
        设置渐变帧当前已等待的数值
        :param sub_rec: Int 渐变已等待帧
        :return: None
        """

        self.sub_rec = sub_rec

    def SetSubColor(self, sub_color):
        """
        设置渐变颜色
        :param sub_color: Tuple(Int R, Int G, Int B [, int alpha)
        :return: None
        """
        self.sub_color = sub_color

    def SetSub(self, sub):
        """
        设置是否渐变
        :param sub: Bool 是否允许进度条渐变
        :return: None
        """

        self.sub = sub

    def SetMax(self, max):
        """
        设置进度条最大值
        :param max: Int 进度条最大值
        :return: None
        """
        self._max = max

    def __justify__(self):
        self.rect.left += self.justify[0]
        self.rect.top += self.justify[1]

    def Justify(self, justify=(0, 0)):
        """
        设置偏移量
        :param justify: Tuple（int，int） 偏移量
        :return: None
        """
        self.justify = justify

    def GetJustify(self):
        """
        获取偏移量
        :return: Tuple(int, int) 偏移量
        """
        return self.justify

    def SetNow(self, now=0):
        """
        设置进度条当前值
        :param now: Int 进度条当前值
        :return: None
        """
        self._now = now
        if self.sub:
            self.sub_rec += 10

    def SetBd(self, bd=1):
        """
        设置进度条边框厚度
        :param bd: Int 进度条边框厚度
        :return: None
        """
        self._bd = bd

    def SetColor(self, color=(20, 190, 160)):
        """
        设置进度条的颜色
        :param color: Tuple(Int R, Int G, Int B [, int alpha) 进度条的颜色
        :return: None
        """
        self._color = color

    def GetBdColor(self):
        """
        获取边框的颜色
        :return: Tuple(Int R, Int G, Int B [, int alpha)
        """
        return self._bd_color

    def GetBgColor(self):
        """
        获取背景的颜色
        :return: Tuple(Int R, Int G, Int B [, int alpha)
        """
        return self._bg_color

    def SetBdColor(self, bd_color=(100, 100, 100)):
        """
        设置边框的颜色
        :param bd_color: Tuple(Int R, Int G, Int B [, int alpha) 边框的颜色
        :return: None
        """
        self._bd_color = bd_color

    def SetBgColor(self, bg_color=(125, 125, 125, 125)):
        """
        设置背景的颜色
        :param bd_color: Tuple(Int R, Int G, Int B [, int alpha) 背景的颜色
        :return: None
        """
        self._bg_color = bg_color

    def GetMax(self):
        """
        获得进度条的最大值
        :return: Int 进度条的最大值
        """
        return self._max

    def GetNow(self):
        """
        获得进度条的当前值
        :return: Int 进度条的当前值
        """
        return self._now

    def Get(self):
        """
        获得进度条的当前值
        :return: Int 进度条的当前值
        """
        return self._now

    def UpdateSize(self):
        """
        更新组件的尺寸，一般为系统调用
        :return: None
        """
        self.rect.left, self.rect.top = self.inst.GetPos()
        self.rect.width, self.rect.height = self.inst.GetSize()
        self.__justify__()

    def Show(self):
        """
        隐藏Progress组件，这将使Progress组件不可见并且停止工作
        :return: None
        """
        self.__show__ = True

    def Hide(self):
        """
        显示Progress组件，这将使Progress组件可见并且开始工作
        :return:
        """
        self.__show__ = False

    def GetStatus(self):
        """
        获取Progress组件是否可见
        :return: Bool --> True:可见/False:不可见
        """
        return self.__show__

    def GetRect(self):
        """
        获取组件有效的矩形区域
        :return: Rect
        """
        return self.rect

    def __GetNowTuple(self):
        """
        系统方法
        :return: tuple(x,y,z,w)
        """
        return self.rect.left, self.rect.top, int(self.rect.width * self._now / self._max), self.rect.height

    def __GetLastTuple(self):
        """
        系统方法
        :return: tuple(x,y,z,w)
        """
        return self.rect.left, self.rect.top, int(self.rect.width * self.last / self._max), self.rect.height

    def effect(self, **kwargs):
        """
        系统调用函数
        :param kwargs: 系统参数
        :return: None
        """
        self.UpdateSize()
        pg.draw.rect(self.data.Support_Part_GetScreen(), self._bg_color, self.rect)
        if self.sub and self.last != self._now:
            pg.draw.rect(self.data.Support_Part_GetScreen(), self.sub_color, self.__GetLastTuple())
            if self.sub_rec >= self.sub_tick:
                self.last = self._now
                self.sub_rec = 0
            else:
                self.sub_rec += 1
        pg.draw.rect(self.data.Support_Part_GetScreen(), self._color, self.__GetNowTuple())
        if self._bd:
            pg.draw.rect(self.data.Support_Part_GetScreen(), self._bd_color, self.rect, self._bd)
        pass  # 在这里绘制进度条


class Text(Component):
    """
    在inst视图上添加一个surface对象，用于渲染文本。
    可以调整位置，默认隐藏不显示
    """

    def __init__(self, inst, text="", color=(255, 255, 255), font=None, show=True, size=30, bold=False, italic=False,
                 equality=False, auto=False, sign=None, justify=(0, 0)):
        """
        Text组件，用于显示文本
        :param text: String 用于显示的文本
        :param color: Tuple(Int R, Int G, Int B) 文本的颜色
        :param font: String 字体(可以是字体名(如simhei)，也可以是字体路径)，None表示使用默认字体
        :param show: Bool 是否显示
        :param size: Int 字体大小
        :param bold: Bool 是否为黑体
        :param italic: Bool 是否为斜体
        :param equality: Bool 是否开启高质量模式(高质量模式下不能设置透明度)
        :param auto: Bool 是否自动换行(自动换行会使程序占用相当资源)
        :param justify: Tuple(int, int) 字体位置微调
        :param sign: String 设置组件在inst中的变量名称,None表示不添加
        """
        super().__init__(inst, sign)
        if not pg.font.get_init():
            raise (Exception("Not Init:before using ", self.__class__.__name__, " component, please init game first."))
        self.__show__ = show

        if font is None or "." in font:
            self.font = pg.font.Font(font, size)
            if bold:
                self.font.set_bold(True)
            if italic:
                self.font.set_italic(True)
        elif font in pg.font.get_fonts():
            self.font = pg.font.SysFont(font, size, bold, italic)
        self.equality = equality
        self.color = color
        self.auto = auto
        self.justify = justify
        self.SetText(text)

    def __justify__(self):
        self.rect.left += self.justify[0]
        self.rect.top += self.justify[1]

    def SetBold(self, value):
        """
        设置是否粗体
        :param value: Bool 是否为粗体
        :return: None
        """
        self.font.set_bold(value)

    def SetItalic(self, value):
        """
        设置是否斜体
        :param value: Bool 是否为斜体
        :return: None
        """
        self.font.set_italic(value)

    def GetBold(self):
        """
        获取是否为粗体
        :return: Bool 是否为粗体
        """
        return self.font.get_bold()

    def GetItalic(self):
        """
        获取是否为斜体
        :return: 是否为斜体
        """
        return self.font.get_italic()

    def Justify(self, justify=(0, 0)):
        """
        设置偏移量
        :param justify: Tuple（int，int） 偏移量
        :return: None
        """
        self.justify = justify

    def GetJustify(self):
        """
        获取偏移量
        :return: Tuple(int, int) 偏移量
        """
        return self.justify

    def SetText(self, text, color=None, equality=None, auto=None):
        """
        设置用于显示的文字
        :param text: String用于显示的文本
        :param color: Tuple(Int R, Int G, Int B) 文本的颜色
        :param equality: Bool是否精细化,精细化后无法调整透明度
        :param auto: Bool 是否自动换行(自动换行会使程序占用相当资源)
        :return:None
        """
        self.text = text
        if auto is None:
            auto = self.auto
        if color is not None:
            self.color = color
        if auto:
            size = self.inst.GetSize()
            width = self.font.metrics("一")[0][4]
            line = size[0] // width
            self.render = []
            trig = -2
            while trig != -1:
                trig = text.find("\n")
                temp = text[:trig]
                text = text[trig + 1:]
                while temp:
                    self.render.append(self.font.render(temp[:line], self.equality if equality is None else equality,
                                                        self.color if color is None else color))
                    temp = temp[line:]
            self.rect = self.render[0].get_rect()


        else:
            self.render = self.font.render(self.text, self.equality if equality is None else equality,
                                           self.color if color is None else color)
            self.rect = self.render.get_rect()

    def GetText(self):
        """
        获取用于显示的文本
        :return: String
        """
        return self.text

    def Show(self):
        """
        隐藏Text组件，这将使Text组件不可见并且停止工作
        :return: None
        """
        self.__show__ = True

    def Hide(self):
        """
        显示Text组件，这将使Text组件可见并且开始工作
        :return:
        """
        self.__show__ = False

    def GetStatus(self):
        """
        获取Text组件是否可见
        :return: Bool --> True:可见/False:不可见
        """
        return self.__show__

    def __update_Position__(self):
        self.rect.left = self.inst.GetPos()[0]
        self.rect.top = self.inst.GetPos()[1]
        self.__justify__()

    def effect(self, **kwargs):
        """
        系统调用函数
        :param kwargs: 系统参数
        :return: None
        """
        if self.__show__:
            self.__update_Position__()
            try:
                if isinstance(self.render, (list, tuple)):
                    for i in self.render:
                        self.inst.data.Support_Part_GetScreen().blit(i, self.rect)
                        self.rect.top += self.rect.height
                else:
                    self.inst.data.Support_Part_GetScreen().blit(self.render, self.rect)
            except pg.error:
                pass


class Collide(pg.sprite.Sprite):
    """
    为inst视图绑定碰撞属性，使其参与碰撞检测
    inst会被加入group_name所带指的碰撞组中，与aim_name所带指的碰撞组进行检测(aim_name为None时会忽略检测，节省资源)(建议不要设置太多的aim_group)
    可以指定碰撞的检测方法collide_func(function(collide,group_list)):return: Bool 来判断是否碰撞(只对aim_group不为空的情况才有效)
    发生指定类型的碰撞后执行func(collide,collided_list)
    """

    def __init__(self, inst, group_name, aim_name=None, func=None, collide_func=None, sign=None):
        """
        Collide组件，用于监听碰撞发生
        :param group_name: String该组件的组别，认为本组件是这个组下的一员
        :param aim_name: String目标组别，当该组件与目标组别发生碰撞时会调用func
        :param func: function(collide,group)发生碰撞时被调用的函数(collide=自己，group=List --> 发生碰撞的组件)
        :param collide_func: function(?)碰撞检测函数，用于检测是否发生碰撞
        :param sign: String 设置组件在inst中的变量名称,None表示不添加
        :param push: Bool是否在碰撞时推动一个系统默认事件{"Collide",collide=...,group=...}
        """
        super().__init__()
        self.inst = inst
        self.inst.tag.append(self.__class__.__name__)
        self.func = func
        self.collide_func = collide_func
        self.group_name = group_name
        self.group = self.inst.data.Support_Part_GetGroupManage().GetGroup(self.group_name)
        self.inst.data.Support_Part_GetGroupManage().AddCollider(self)
        self.aim_name = aim_name
        self.aim_group = self.inst.data.Support_Part_GetGroupManage().GetGroup(
            self.aim_name) if self.aim_name is not None else None
        self.rect = pg.Rect(0, 0, 0, 0)
        self.new = True
        self.sign = sign
        if sign:
            setattr(self.inst, sign, self)
        self.radius = 0

    def GetSign(self):
        """
        获得标记的名称
        :return: String
        """
        return self.sign

    def UpdateSize(self):
        """
        更新组件的尺寸，一般为系统调用
        :return: None
        """
        self.rect.left, self.rect.top = self.inst.GetPos()
        self.rect.width, self.rect.height = self.inst.GetSize()
        self.radius = min(self.rect.height, self.rect.width) // 2

    def SetGroup(self, group_name):
        """
        设置组件组别
        :param group_name: String组件组别的名称
        :return: None
        """
        self.group_name = group_name
        self.group = self.inst.data.Support_Part_GetGroupManage().GetGroup(self.group_name)

    def SetAim(self, aim_name):
        """
        设置目标组别
        :param aim_name: String目标组别的名称
        :return: None
        """
        self.aim_name = aim_name
        self.aim_group = self.inst.data.Support_Part_GetGroupManage().GetGroup(aim_name)

    def GetGroupName(self):
        """
        获取组件组别的组名
        :return: String
        """
        return self.group_name

    def GetAimName(self):
        """
        获取目标组别的组名
        :return: String
        """
        return self.aim_name

    def SetCollideFunc(self, func):
        """
        设置碰撞检测函数
        :param func: function(?)碰撞检测函数
        :return: None
        """
        self.collide_func = func

    def GetRect(self):
        """
        获取组件有效的矩形区域
        :return: Rect
        """
        return self.rect

    def remove(self):
        """
        移除组件，一般为系统调用
        如果用户自行调用，可能导致没能完全移除，导致bug
        :return: None
        """
        self.inst.tag.remove(self.__class__.__name__)
        self.inst.data.Support_Part_GetGroupManage().RemoveCollider(self)

    def effect(self, **kwargs):
        """
        系统调用函数
        :param kwargs: 系统参数
        :return: None
        """
        if self.new:
            self.UpdateSize()
        if self.aim_name is not None:
            rec = pg.sprite.spritecollide(self, self.aim_group, False, self.collide_func)
            if len(rec) > 0:
                if self.func:
                    self.func(self, rec)


class Locomotor(Component):  # mode = border/center ,collide_act = func/"keep"
    """
    控制inst视图的运动的一个组件，建议在需要复杂控制时才使用(比如玩家的控制)，因为使用此组件比使用view.SetPos等方法更占用资源
    设置frequency的值来控制运动频率(单位:hz，意味着每秒运动多少次)
    设置mode来指明控制的位置是inst视图的border(左上方)还是center(中心点)
    使用Move添加一个运动矢量，使用Stop来停止一个指定的运动矢量
    使用Lock来锁住一个或多个方向上的运动
    """

    def __init__(self, inst, frequency=20, mode="border", sign="locomotor"):
        """
        Locomotor组件, 标准的移动组件，控制视图的移动(允许你用矢量叠加的形式控制组件移动)
        :param frequency: Int 运动频率，应当小于你设置中的FREQUENCY
        :param mode: String (border或center)运动模式，表示以边缘对齐或中心对齐(pgframe中几乎所有的组件和视图都是边缘对齐，使用中心对齐会略微增加程序资源占用)
        :param sign: String 设置组件在inst中的变量名称,默认locomotor
        :param collide_act: function(eve,data) {eve.collide, eve.group}碰撞生效函数，可选参数"keep"(碰撞停下)，None(不监听碰撞)
        """
        super().__init__(inst, sign)
        if sign is None:
            raise (Exception("Locomotor' s sign can not be None!"))
        if self.inst.inst is None and self.inst.auto:
            raise (Exception("Root view can not have component Locomotor."))
        self.mode = int(mode == "center")
        self.dx, self.dy = 0, 0

        self.move = False
        self.move_id = None
        self.moves = dict()
        self.move_lock = dict(up=False, left=False, right=False, down=False)
        self.lock_time = dict(up=0, left=0, right=0, down=0)
        self.frequency = frequency

        self.__setsize__()

    def GetFreq(self):
        """
        获取运动频率
        :return: Int
        """
        return self.frequency

    def SetFreq(self, freq):
        """
        设置运动频率。请勿大量重复的设置频率，因为该方法稍微更占用资源.
        :param freq: 频率
        :return: None
        """
        self.frequency = freq
        if not self.failed and self.move_id:
            self.inst.CancelPeriod(self.move_id)
            self.move_id = self.inst.DoPeriodicTask(1 / self.frequency, self.System_Component_Class_MoveOne)

    # def SetCollideAction(self, collide_act):
    #     """
    #     设置碰撞生效函数
    #     :param collide_act: function(eve,data) {eve.collide, eve.group}碰撞生效函数，可选参数"keep"(碰撞停下)，None(不监听碰撞)
    #     :return: None
    #     """
    #     try:
    #         self.inst.CancelListen("collide")
    #     except:
    #         pass
    #     if collide_act:
    #         if collide_act == "keep":
    #             collide_act = self.CollideKeepAction
    #         self.inst.ListenForEvent("collide", collide_act)
    #
    # def CollideKeepAction(self, eve, data):
    #     """
    #     系统函数
    #     :param eve: 事件
    #     :param data: 全局栈区
    #     :return: None
    #     """
    #     for i in eve.group:
    #         self.Lock(GetRectSide(eve.collide, i), self.frequency / 10)

    def Lock(self, direct=None, continue_time=None):
        """
        锁住指定的方向
        :param direct: None/String/List-->String 要锁住的方向，None不进行操作，String锁住指定的方向("all"锁住所有方向)，List-->String，锁住List中的方向
        :param continue_time: Int 锁住的帧数，None只锁住瞬间帧，Int在指定帧数内保持锁住
        :return:
        """
        if direct is not None:
            if isinstance(direct, (list, tuple)):
                for i in direct:
                    self.move_lock[i] = True
                    if continue_time:
                        self.lock_time[i] = continue_time
            else:
                if direct == "all":
                    self.move_lock["up"] = True
                    self.move_lock["right"] = True
                    self.move_lock["down"] = True
                    self.move_lock["left"] = True
                    if continue_time:
                        self.lock_time["up"] = continue_time
                        self.lock_time["right"] = continue_time
                        self.lock_time["down"] = continue_time
                        self.lock_time["left"] = continue_time
                else:
                    self.move_lock[direct] = True
                    if continue_time:
                        self.lock_time[direct] = continue_time

    def remove(self):
        """
        移除组件，一般为系统调用
        如果用户自行调用，可能导致没能完全移除，导致bug
        :return: None
        """
        super().remove()
        self.inst.CancelListen("collide")

    def __setsize__(self):
        if self.inst:
            size = self.inst.GetSize()
            self.size = size
            self.x_migration = self.mode * self.size[0] * .5
            self.y_migration = self.mode * self.size[1] * .5
            if self.inst.inst:
                i_size = self.inst.inst.GetSize()
                self.can_percent = True
            else:
                i_size = (1, 1)
                self.can_percent = False
            self.x_per_migration = self.mode * self.size[0] * .5 / i_size[0]
            self.y_per_migration = self.mode * self.size[1] * .5 / i_size[1]
            self.move_id = self.inst.DoPeriodicTask(1 / self.frequency, self.System_Component_Class_MoveOne)
            self.failed = False
        else:
            self.failed = True

    def SetPosition(self, x, y):
        """
        设置位置(x,y 表示视图border/center的位置)
        :param x: Int x
        :param y: Int y
        :return: None
        """
        if not self.failed:
            self.inst.SetPos((x - self.x_migration, y - self.y_migration))
        else:
            print("-->An Error happen:Locomotor is failed<--")

    def GetPosition(self):
        """
        获取border/center的位置
        :return: Tuple(Int x,Int y)
        """
        if not self.failed:
            x, y = self.inst.GetPos()
            return x - self.x_migration, y - self.y_migration
        else:
            print("-->An Error happen:Locomotor is failed<--")
            return 0, 0

    def SetPercent(self, per_X=None, per_Y=None, reset=False):
        """
        设置视图(border/center)基准点在上级视图中的百分比
        :param per_X: float 0~1百分比x
        :param per_Y: float 0~1百分比y
        :param reset: Bool 是否立刻重置位置
        :return: None
        """
        if not self.can_percent:
            print("-->An Error happen:Root view can not SetPercent<--")
        if not self.failed:
            x, y = self.inst.GetPercent()
            x = x if per_X is None else per_X - self.x_per_migration
            y = y if per_Y is None else per_Y - self.y_per_migration
            self.inst.SetPercent((x, y), reset)
        else:
            print("-->An Error happen:Locomotor is failed<--")

    def GetPercent(self):
        """
        获取视图(border/center)基准点在上级视图中的百分比
        :return: Tuple(float x，float y)
        """
        if not self.can_percent:
            print("-->An Error happen:Root view can not GetPercent<--")
        if not self.failed:
            x, y = self.inst.GetPercent()
            return x + self.x_per_migration, y + self.y_per_migration
        else:
            print("-->An Error happen:Locomotor is failed<--")
            return 0, 0

    def System_Component_Class_MoveOne(self):
        """
        系统方法，请用户勿自行调用，否则可能出现bug
        :return:
        """
        if len(self.moves) and (self.dx or self.dy):
            dx, dy = self.dx, self.dy
            if True in self.move_lock.values():
                if self.move_lock["up"] and dy < 0:
                    if self.lock_time["up"] == 0:
                        self.move_lock["up"] = False
                    else:
                        self.lock_time["up"] -= 1
                    dy = 0
                if self.move_lock["down"] and dy > 0:
                    if self.lock_time["down"] == 0:
                        self.move_lock["down"] = False
                    else:
                        self.lock_time["down"] -= 1
                    dy = 0
                if self.move_lock["left"] and dx < 0:
                    if self.lock_time["left"] == 0:
                        self.move_lock["left"] = False
                    else:
                        self.lock_time["left"] -= 1
                    dx = 0
                if self.move_lock["right"] and dx > 0:
                    if self.lock_time["right"] == 0:
                        self.move_lock["right"] = False
                    else:
                        self.lock_time["right"] -= 1
                    dx = 0

            x, y = self.GetPosition()
            self.SetPosition(x + dx, y + dy)

    def Move(self, name, dx=0, dy=0):
        """
        添加运动速度矢量
        :param name: String速度矢量名称
        :param dx: Int 速度的x分量
        :param dy: Int 速度的y分量
        :return: None
        """
        if not self.failed:
            self.moves[name] = (dx, dy)
            self.dx += dx
            self.dy += dy

    def Stop(self, name):
        """
        停止某一运动速度矢量
        :param name: String速度矢量名称
        :return: None
        """
        if not self.failed and self.move_id is not None:
            temp = self.moves.pop(name)
            self.dx -= temp[0]
            self.dy -= temp[1]

    def effect(self, **kwargs):
        """
        系统调用函数
        :param kwargs: 系统参数
        :return: None
        """
        if self.failed or self.size != self.inst.GetSize():
            self.__setsize__()


class Pic(Component):
    """
    用于显示图片或图片组的组件(传入ArtDef参数的值为某图片或图片组的名字)，须注意的是，它不会以inst视图的大小来安排图片，只使用inst的GetPos确定位置(可以设置center=True以使用view.GetCenterPos确定位置)
    更多帮助查看help(Pic.__init__)
    """

    def __init__(self, inst, ArtDef, scale="100", rotate="000", hflip="0", vflip="0", center=False, tim=0, keep_tim=0,
                 sign=None, justify=(0, 0), end_func=None, show=True):
        """
        Pic组件，用于显示图片或图片组
        :param ArtDef: 艺术数据名String
        :param scale: 缩放倍率Int 0~100 (100->100%, 10->10%)(传入String类型能减少程序资源占用)
        :param rotate: 旋转角度Int 0~360 (向上为0, 顺时针旋转)(传入String类型能减少程序资源占用)
        :param hflip: 水平翻转Int 0/1(1表示水平翻转)(传入String类型能减少程序资源占用)
        :param vflip: 竖直翻转Int 0/1(1表示竖直翻转)(传入String类型能减少程序资源占用)
        :param center: 是否以中心为基准点Bool(传入False能减少程序资源占用)
        :param tim: 图片间隔帧Int(只适用于多图片,控制图片播放时间隔的帧数)
        :param keep_tim: 持续帧数Int(显示多少帧，大于此数时，该组件会被隐藏)
        :param justify: Tuple(int, int) 图片位置微调
        :param end_func: function(pic= Pic Components) 允许Pic即将Hide时激活函数
        :param sign: String 设置组件在inst中的变量名称,None表示不添加
        """
        super().__init__(inst, sign)
        self.ArtDef = ArtDef
        self.center = center
        self._camera_scale = self.inst.data.Support_Part_GetCamera().GetScaleRate()
        self._scale = scale
        self._rotate = rotate
        self._hflip = hflip
        self._vflip = vflip
        self.pic = self.inst.data.Support_Part_GetImgManage().GetImage(ArtDef, int(int(scale) * self._camera_scale),
                                                                       rotate, hflip, vflip)
        self.__show__ = show
        self.keep_rec = 0
        self.keep_tim = keep_tim
        self.__sequence_pics_Sets__(tim)
        self.tim_set = tim
        self.justify = justify
        self.func = end_func

    def __justify__(self):
        self.rect.left += self.justify[0]
        self.rect.top += self.justify[1]

    def Rotate(self, rotate):
        self.SetPic(self.GetPicName(), self._scale, rotate, self._hflip, self._vflip)

    def Scale(self, scale):
        self.SetPic(self.GetPicName(), scale, self._rotate, self._hflip, self._vflip)

    def Hflip(self, hflip):
        self.SetPic(self.GetPicName(), self._scale, self._rotate, hflip, self._vflip)

    def Vflip(self, vflip):
        self.SetPic(self.GetPicName(), self._scale, self._rotate, self._hflip, vflip)

    def SetKeep(self, keep):
        """
        设置持续帧
        :param keep: 持续帧数Int(显示多少帧，大于此数时，该组件会被隐藏)
        :return: None
        """
        self.keep_tim = keep

    def GetKeep(self):
        """
        获得持续帧设置值
        :return: Int 持续帧
        """
        return self.keep_tim

    def __sequence_pics_Sets__(self, tim=0, keep=False):
        if isinstance(self.pic, (list, tuple)):
            # for i in self.pic:
            #     i.set_alpha(self.alpha)
            if not keep:
                self.tim_rec = 0
                if tim != False:
                    self.tim_set = tim
                self.rec = 0
            self.rect = self.pic[0].get_rect()
        else:
            # self.pic.set_alpha(self.alpha)
            self.rec = None
            self.rect = self.pic.get_rect()

    def Justify(self, justify=(0, 0)):
        """
        设置偏移量
        :param justify: Tuple（int，int） 偏移量
        :return: None
        """
        self.justify = justify

    def GetJustify(self):
        """
        获取偏移量
        :return: Tuple(int, int) 偏移量
        """
        return self.justify

    def SetPic(self, ArtDef, scale='None', rotate="None", hflip="None", vflip="None", tim=False, keep=False):
        """
        为Pic组件设置艺术数据名
        :param ArtDef: 艺术数据名String
        :param scale: 缩放倍率Int 0~100 (100->100%, 10->10%)(传入String类型能减少程序资源占用)
        :param rotate: 旋转角度Int 0~360 (向上为0, 顺时针旋转)(传入String类型能减少程序资源占用)
        :param hflip: 水平翻转Int 0/1(1表示水平翻转)(传入String类型能减少程序资源占用)
        :param vflip: 竖直翻转Int 0/1(1表示竖直翻转)(传入String类型能减少程序资源占用)
        :param tim: 图片间隔帧Int(只适用于多图片,控制图片播放时间隔的帧数)
        :param keep: 是否保持原先播放位置 Bool
        :return: None
        """
        self._scale = scale if scale != 'None' else self._scale
        self._rotate = rotate if rotate != 'None' else self._rotate
        self._hflip = hflip if hflip != 'None' else self._hflip
        self._vflip = vflip if vflip != 'None' else self._vflip
        self.pic = self.inst.data.Support_Part_GetImgManage().GetImage(ArtDef, int(int(self._scale) * self._camera_scale),
                                                                       self._rotate, self._hflip, self._vflip)
        self.ArtDef = ArtDef
        self.__sequence_pics_Sets__(tim, keep)

    def GetPic(self):
        """
        获得Pic组件的艺术数据
        :return: Surface or List of Surfaces
        """
        return self.pic

    def GetPicName(self):
        """
        获得Pic组件艺术数据的名称
        :return: String
        """
        return self.ArtDef

    def Hide(self):
        """
        隐藏Pic组件，这将使Pic组件不可见并且停止工作
        :return: None
        """
        if self.func:
            self.func(self)
        self.__show__ = False

    def Show(self):
        """
        显示Pic组件，这将使Pic组件可见并且开始工作
        :return: None
        """
        self.__show__ = True
        if self.keep_tim:
            self.keep_rec = 0

    def GetStatus(self):
        """
        获取Pic组件是否可见
        :return: Bool --> True:可见/False:不可见
        """
        return self.__show__

    def SetTim(self, tim):
        """
        设置图片组的显示间隔(单位:帧)
        :param tim: 图片间隔帧Int(只适用于多图片,控制图片播放时间隔的帧数)
        :return: None
        """
        self.tim_set = tim

    def GetTimSet(self):
        """
        获取图片组的显示间隔(单位:帧)
        :return: Int
        """
        return self.tim_set

    def GetTimRec(self):
        """
        获取图片组的显示间隔时已经等待的帧数
        :return: Int
        """
        return self.tim_rec

    def ResetKeep(self):
        self.keep_rec = 0

    def GetRect(self):
        """
        获取组件有效的矩形区域
        :return: Rect
        """
        return self.rect

    def effect(self, **kwargs):
        """
        系统调用函数
        :param kwargs: 系统参数
        :return: None
        """
        if self.__show__:
            if self.keep_tim:
                if self.keep_rec >= self.keep_tim:
                    self.Hide()
                    return
                else:
                    self.keep_rec += 1
            if self._camera_scale != self.inst.data.Support_Part_GetCamera().GetScaleRate():
                self._camera_scale = self.inst.data.Support_Part_GetCamera().GetScaleRate()
                self.SetPic(self.GetPicName(), self._scale, self._rotate, self._hflip, self._vflip)
            if self.center:
                temp = self.inst.GetCenterPos()
                self.rect.centerx = temp[0]
                self.rect.centery = temp[1]
            else:
                self.rect.left = self.inst.GetPos()[0]
                self.rect.top = self.inst.GetPos()[1]
            self.__justify__()
            if self.rec is not None:
                while True:
                    try:
                        self.data.Support_Part_GetScreen().blit(self.pic[self.rec], self.rect)
                        break
                    except pg.error:
                        pass
                if self.tim_rec >= self.tim_set:
                    self.tim_rec = 0
                    if len(self.pic) - 1 == self.rec:
                        self.rec = 0
                    else:
                        self.rec += 1
                else:
                    self.tim_rec += 1
            else:
                try:
                    self.data.Support_Part_GetScreen().blit(self.pic, self.rect)
                except pg.error:
                    pass
