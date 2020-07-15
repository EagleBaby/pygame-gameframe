import math
import os


class Tick(object):
    def __init__(self, tim):
        """
        设置间隔工作机制
        :param tim: int 间隔帧
        """
        self.tim_set = tim
        self.tim_rec = 0
        self._able = True

    def GetStatus(self):
        return self._able

    def Enabled(self):
        self._able = True

    def Disabled(self):
        self._able = False

    def SetTim(self, tim, reset=False):
        """
        设置间隔
        :param tim: int 间隔数
        :param reset: Bool 是否重置
        :return: None
        """
        if reset:
            self.tim_rec = 0
        self.tim_set = tim

    def tick(self):
        """
        时钟tick
        :return: Bool 是否达到时间点
        """
        if self._able:
            if self.tim_rec >= self.tim_set:
                self.tim_rec = 0
                return True
            else:
                self.tim_rec += 1
        return False

    def __call__(self, *args, **kwargs):
        return self.tick()


def IsClickActive(aim_view, pos):
    aim = aim_view.GetPos()
    if aim:
        size = aim_view.GetSize()
        return IsInArea(pos, aim, size)


def IsFocusActive(aim_view, pos):
    aim = aim_view.GetPos()
    if aim:
        size = aim_view.GetSize()
        return IsInArea(pos, aim, size)


def IsInArea(pos, area_pos, area_size):
    return area_pos[0] < pos[0] < area_pos[0] + area_size[0] and area_pos[1] < pos[1] < area_pos[1] + area_size[1]


def IsInCircle(pos, circle_center, circle_radius):
    return GetPointsDistance(pos, circle_center) < circle_radius


def GetPointsDistance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** .5


def GetDirect(self_pos, aim_pos):
    """
    y轴向下
    :param self_pos:
    :param aim_pos:
    :return:
    """
    if self_pos[0] > aim_pos[0]:
        a = Vector(0, 1)
        direct = 180
    else:
        a = Vector(0, -1)
        direct = 0
    b = Vector(aim_pos[0] - self_pos[0], aim_pos[1] - self_pos[1])
    return int(math.degrees(math.acos(a.GetCos(b)))) + direct


class Vector(object):
    def __init__(self, *array):
        self.array = array

    def Dot(self, other):
        if len(self.array) != len(other.array):
            raise (Exception("只有同维向量才能做点积."))
        temp = 0
        for i, j in zip(self.array, other.array):
            temp += i * j
        return temp

    def Length(self):
        temp = 0
        for i in self.array:
            temp += i ** 2
        return temp ** .5

    def __getitem__(self, item):
        return self.array[item]

    def Multiply(self, other):
        return self.Length() * other.Length() * math.sin(math.acos(self.GetCos()))

    def Add(self, other):
        temp = []
        for i, j in zip(self.array, other.array):
            temp += [i + j]
        return Vector(temp)

    def Sub(self, other):
        temp = []
        for i, j in zip(self.array, other.array):
            temp += [i - j]
        return Vector(temp)

    def __sub__(self, other):
        return self.Sub(other)

    def __add__(self, other):
        return self.Add(other)

    def __mul__(self, other):
        return self.Multiply(other)

    def __eq__(self, other):
        return self.array == other.array

    def __len__(self):
        return self.Length()

    def GetCos(self, other):
        try:
            return self.Dot(other) / (self.Length() * other.Length())
        except ZeroDivisionError:
            return 1


def GetRectSide(collide, collide_):
    """
    获取是collide的那个面与collide_发生碰撞
    :param collide: collide self
    :param collide_: collide other
    :return: "up""down""left""right"
    """
    rect = collide.GetRect()
    rect_ = collide_.GetRect()
    temp = rect.clip(rect_)
    pos = collide.inst.GetPos()
    if temp.width > temp.height:
        if rect.centery > rect_.bottom:
            collide.inst.SetPos((collide.inst.GetPos()[0], rect_.bottom - 1))
            return "up"
        else:
            collide.inst.SetPos((collide.inst.GetPos()[0], rect_.top - rect.height + 1))
            return "down"
    elif temp.width < temp.height:
        if rect.centerx > rect_.right:
            collide.inst.SetPos((rect_.right - 1, collide.inst.GetPos()[1]))
            return "left"
        else:
            collide.inst.SetPos((rect_.left - rect.width + 1, collide.inst.GetPos()[1]))
            return "right"
    else:
        return None


def UpdateModelData(data, auto=False):
    if not (data.st.AUTO_UPDATE_MODEL or auto):
        return
    for model in os.listdir(data.st.PATH_SET["datum"]):
        if os.path.isdir(os.path.join(data.st.PATH_SET["datum"], model)):
            for datum in os.listdir(os.path.join(data.st.PATH_SET["datum"], model)):
                if datum[len(datum) - 5:] == ".data":
                    datum = datum[:len(datum) - 5]
                    getattr(data.md, model)(datum).save()
