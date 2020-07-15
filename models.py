from pgframe.base import *
import os
import pickle as pick
import tkinter.messagebox as message

_data = None


def System_Model_Part_Init(__data):
    global _data
    _data = __data


model_class_base = ["TypeModel", "path", "Loading", "Get", "SetMainKey", "save", "GetAttrs", "GetAttrsValues", "All"]


class Model(object):  # 一个Model类会产生一个文件夹，文件夹下存放此类所有数据，文件夹的名称由类名控制，每份数据的名称由主键决定
    def __init__(self, *args, **kwargs):
        if _data is None:
            raise (Exception("Before you create model,you need init pgframe first."))
        self.main_key = None if not hasattr(self, "main_key") else self.main_key
        self.TypeModel = None
        path = _data.st.PATH_SET["datum"]
        name = self.__class__.__name__
        self.__get_from_file__ = None
        for i in os.listdir(path):
            if i == name and os.path.isdir(os.path.join(path, i)):
                self.path = os.path.join(path, i)
                break
        if not hasattr(self, "path"):
            os.makedirs(os.path.join(path, name))
            self.path = os.path.join(path, name)
        self.Loading(**kwargs)
        for attr_name in dir(self):
            if attr_name not in model_class_base and kwargs.get(attr_name):
                self.__dict__[attr_name] = kwargs[attr_name]
        if self.main_key not in dir(self):
            message.showerror("主键错误:", "In model " + self.__class__.__name__ + ", main_key is not correct.")
            raise (Exception("In model " + self.__class__.__name__ + ", main_key is not correct."))
        if len(args) == 1 and self.main_key is not None:
            setattr(self, self.main_key, args[0])
            if self.Get() and len(kwargs) != 0:
                message.showwarning("警告:", "你正在试图向一个已存在的data(" + self.__class__.__name__ + ":" + getattr(self,
                                                                                                         self.main_key) + ")写入数据，重写数据动作可能没有成功.")
                self.__get_from_file__ = True

    def Loading(self, **kwargs):
        pass

    def All(self):
        temp = {}
        for file in os.listdir(self.path):
            temp[file[:len(file) - 5]] = self.__class__(file[:len(file) - 5])
        return temp

    def GetAttrs(self, binary=False):
        attrs = []
        for attr in dir(self):
            if attr[:2] != "__" and attr not in model_class_base:
                if binary and attr in ["main_key"]:
                    continue
                attrs.append(attr)
        return attrs

    def GetAttrsValues(self, binary=False):
        values = []
        for attr in self.GetAttrs(binary):
            values.append(self.__getattribute__(attr))
        return values

    def Get(self):
        temp = {}
        trig = False
        for i in os.listdir(self.path):
            # print(os.path.isfile(os.path.join(self.path, i)),getattr(self,"main_key"),os.path.splitext(i)[0]) # debug
            if os.path.isfile(os.path.join(self.path, i)) and getattr(self, self.main_key) == os.path.splitext(i)[0]:
                with open(os.path.join(self.path, i), "rb") as f:
                    try:
                        temp = pick.load(f)
                    except EOFError:
                        message.showwarning("异常:", "一个不能被识别的data文件:" + i + "\n系统将对其进行自动修复")
                        trig = True
                        continue
                    if not isinstance(temp, dict):
                        message.showwarning("异常:", "检测到一个异常的文件" + i + "\n系统将对其进行自动修复")
                        trig = True
                        continue
                    if len(temp) < 2:
                        message.showerror("错误:", "你成功的打开了一个文件，但获得了一个严重错误的数据，以至于不能被系统自动修复"
                                                 "\n请联系程序员以解决问题")
                        raise (Exception("你成功的打开了一个文件，但没有获得正常的数据，判定为载入异常"
                                         "\n请联系程序员以解决问题"))
                for attr in self.GetAttrs():
                    if not temp.get(attr):
                        continue
                    self.__dict__[attr] = temp[attr]
                if trig:
                    self.save()
                return True
        return False

    def __call__(self, *args, **kwargs):
        pass

    def SetMainKey(self, main_key):
        self.main_key = main_key

    def save(self):
        if self.main_key is None:
            message.showerror("error:",
                              "Before saving data, you need use function '.SetMainKey(main_key)' or set the value of attribute '.main_key' to set the main key first.")
            raise (Exception(
                "Before saving data, you need use function '.SetMainKey(main_key)' or set the value of attribute '.main_key' to set the main key first."))
        elif not hasattr(self, self.main_key):
            message.showerror("error:",
                              "\"" + self.__class__.__name__ + "\" doesn't have main key \"" + self.main_key + "\"")
            raise (Exception("\"" + self.__class__.__name__ + "\" doesn't have main key \"" + self.main_key + "\""))
        elif not self.__get_from_file__ and os.path.exists(
                os.path.join(self.path, self.__class__.__name__, self.main_key + ".data")):
            message.showerror("错误:", "你创建的新数据的主键与已有数据重复!")
            raise (Exception("你创建的新数据的主键与已有数据重复!"))
        temp = {}
        for attr in self.GetAttrs():
            temp[attr] = getattr(self, attr)
        with open(os.path.join(self.path, getattr(self, self.main_key) + ".data"), "wb") as f:
            pick.dump(temp, f)
            f.close()


"""
from user_models import *
from main import *
a = main_init(None, None, None, None, None, None)
p=Player("ea")
p=Player(name="ea",hp=500,mp=200)
"""
