import os
import pickle as pick
from ast import literal_eval as tidy_tuple
from pgframe.base import *
import tkinter as tk
import inspect as ins
import tkinter.messagebox as message
import random

adj = ["无奈的", "委屈的", "无可奈何的", "略有沉思的", "试探性的", "理直气壮的", "随意的"]
exclude_attr = ["main_key"]


class FalseData:
    pass


class EnterUnable(Exception):
    pass


class CanNotFindAnyModel(Exception):
    pass


class DataManager(object):
    def __init__(self, model, st):
        self.md = model
        self._false_data = FalseData()
        self._false_data.md = model
        self._false_data.st = st
        self.md.System_Model_Part_Init(self._false_data)
        self.model_list = []
        self.path = st.PATH_SET["datum"]
        self.win = tk.Tk()
        self.win.protocol('WM_DELETE_WINDOW', self.__on_closing__)
        self.win.title("DataManager(回车表示添加项(第二个框框)/保存退出(第四个框框)，点击\"X\"退出时也会自动保存)Delete删除选中(第二个框框)")
        self.win.minsize(1285, 640)
        self.win.maxsize(1285, 640)

        UpdateModelData(self._false_data, True)

        self.model = None  # 当前选中模型
        self.datum = None  # 当前选中数据
        self.data = None  # 当前数据对象
        self._change = False
        self.__data_init__()
        self.__create_window__()
        self.__init_at_box_txt__()
        self.__init_datum_box__()

    def Start(self):
        self.win.mainloop()

    def GetModelDatum(self, index):
        name_list = []
        model_list = []
        # a = self.model_list[index]
        return name_list, model_list

    def __data_init__(self):
        """
        初始化几个数据变量
        :return:
        """
        """
        self.md_box = []
        self.dt_box = []
        self.at_box = []
        self.at_txt = []
        """
        self._at_box = []  # 原始数据

        self.md_box = tk.StringVar(self.win)
        self.dt_box = tk.StringVar(self.win)
        self.at_box = tk.StringVar(self.win)
        self.__md_box__()
        # self.__dt_box__() # 选中model后出现
        # self.__at_box__() # 选中data后出现
        # self.__at_txt__() # 选中data后出现

    def __md_box__(self):

        """
        get infos for md_box
        :return:
        """

        temp = []
        for i in dir(self.md):
            if i[:2] != "__" and i != "Model" and ins.isclass(getattr(self.md, i)) and issubclass(getattr(self.md, i),
                                                                                                  self.md.Model):
                temp.append(i)

        if len(temp) == 0:
            message.showerror("DataManager" + random.sample(adj, 1)[0] + "告诉你：", "*DataManager 找不到任何的model")
            raise (CanNotFindAnyModel("*DataManager 找不到任何的model"))

        self.md_box.set(temp)

    def __init_datum_box__(self):
        if self._change and self.data:
            self._save_data()
        self.datum_box.delete(0, "end")
        self.datum_box.insert("end", "...waiting...")
        self.datum_box.config(state=tk.DISABLED)
        self.model = None

    def __init_at_box_txt__(self):
        if self._change and self.data:
            self._save_data()
        self.data = None
        self.attrs_box.delete(0, "end")
        self.attrs_txt.delete(1.0, "end")
        self.attrs_box.insert("end", "...waiting...")
        self.attrs_txt.insert("end", "...waiting...")
        self.attrs_box.config(state=tk.DISABLED)
        self.attrs_txt.config(state=tk.DISABLED)
        self.datum = None

    def __dt_box__(self, widget):
        if not widget.curselection():
            return
        else:
            which = widget.get(widget.curselection()[0])
        """
        get infos for dt_box
        :return:
        """

        if self.model != which:
            self.datum_box.config(state=tk.NORMAL)
            temp = []
            if not os.path.exists(os.path.join(self.path, which)):
                os.makedirs(os.path.join(self.path, which))
            for f_name in os.listdir(os.path.join(self.path, which)):
                if f_name.find(".") != -1 and f_name[len(f_name) - 4:] == "data":
                    temp.append(f_name[:len(f_name) - 5])
            self.dt_box.set(temp)
            self.model = which

    def __at_box__(self, widget):
        if not widget.curselection():
            return
        which = widget.get(widget.curselection()[0])
        """
        get infos for at_box
        :return:
        """
        if self.datum != which:
            self.attrs_box.config(state=tk.NORMAL)
            temp = []
            self.data = pick.load(open(os.path.join(self.path, self.model, which + ".data"), "rb"))
            for attr in self.data:
                if attr not in exclude_attr:
                    temp.append(attr)
            self.at_box.set(temp)
            self._at_box = temp
            self._change = False
            self.__at_txt__()

    def __at_txt__(self):
        """
        get infos for at_txt
        :return:
        """
        if not self.data:
            message.showerror("DataManager" + random.sample(adj, 1)[0] + "告诉你：", "*DataManager 没有匹配到.data文件")
            raise (Exception("没有匹配到.data文件"))
        self.attrs_txt.config(state=tk.NORMAL)
        txt = ""
        for i in self.data:
            if i not in exclude_attr:
                txt += str(self.data[i]) + "\n"
        txt = txt[:len(txt) - 1]
        self.attrs_txt.delete(1.0, "end")
        self.attrs_txt.insert("insert", txt)

    def __dt_box_bind__(self, eve):

        if eve.keycode == 13:
            # Create new .data here

            if not self.dt_box.get() or "__new__" not in tidy_tuple(self.dt_box.get()):
                getattr(self.md, self.model)("__new__").save()
                self.__init_at_box_txt__()
                self.datum_box.insert("end", "__new__")
        elif eve.keycode == 46 and self.datum_box.curselection():
            os.remove(os.path.join(self.path, self.model,
                                   tidy_tuple(self.dt_box.get())[self.datum_box.curselection()[0]] + ".data"))
            self.__init_datum_box__()
            self.__init_at_box_txt__()
            self.model_box.focus_set()

    def __at_txt_bind__(self, eve):

        """
        keycode:
        8 退格
        13 回车
        48~57 ，96~105 : 0~9
        65~90: A~z
        :param eve:
        :return:
        """
        line, column = eve.widget.index("insert").split(".")
        if 48 <= eve.keycode <= 57 or 65 <= eve.keycode <= 90 or 96 <= eve.keycode <= 105:
            self.attrs_box.select_clear(0, "end")
            self.attrs_box.select_set(int(line) - 1)
            self._change = True
        elif eve.keycode == 13:
            self.__on_closing__()

    def __on_closing__(self):
        print("正在储存数据，此时请勿强制关闭窗口...")
        if self._change and self.data:
            self._save_data()
        print("储存完毕.")
        self.win.destroy()

    def _save_data(self):
        self._change = False
        txt = self.attrs_txt.get(1.0, "end")
        txt = self.__tidy__(txt.split("\n"))
        attrs = tidy_tuple(self.at_box.get())
        temp = []
        trig = None
        if len(txt) != len(attrs):
            message.showerror("格式错误:","attributes没有和values一一对应")
            self.__init_datum_box__()
            return
        for i in range(len(txt)):
            if attrs[i] == self.data["main_key"] and txt[i] != self.data[attrs[i]]:
                if os.path.exists(os.path.join(self.path, self.model, txt[i] + ".data")):
                    message.showerror("部分设置失败:",
                                      self.data["main_key"] + " is the main key, it can not be repeated..\nBut " +
                                      self.data["main_key"] + ":" + txt[i] + " is already existed.")
                    continue
                trig = self.data[attrs[i]]
            if isinstance(self.data[attrs[i]], str):
                self.data[attrs[i]] = txt[i]
            else:
                self.data[attrs[i]] = eval(txt[i])
        pick.dump(self.data,
                  open(os.path.join(self.path, self.model, self.data[self.data["main_key"]] + ".data"), "wb"))
        if trig is not None:
            os.remove(os.path.join(self.path, self.model, trig + ".data"))
            self.__init_datum_box__()

    def __tidy__(self, lis):
        temp = []
        for i in lis:
            if i:
                temp.append(i)
        return temp

    def __create_window__(self):
        """
        由从用户模型中获取的数据类型编辑attrs
        模型，数据只看不能删不能改，只能操作数据中的内容，
        model: listbox
        datum: listbox
        attrs: listbox + text
        :return:
        """

        self.model_scr = tk.Scrollbar(self.win)
        self.datum_scr = tk.Scrollbar(self.win)
        self.attrs_scr = tk.Scrollbar(self.win)
        self.at_txt_scr = tk.Scrollbar(self.win)
        self.at_txt_hscr = tk.Scrollbar(self.win, orient=tk.HORIZONTAL)
        self.model_box = tk.Listbox(self.win, height=35, font=("simhei", 12), yscrollcommand=self.model_scr.set,
                                    listvariable=self.md_box)
        self.datum_box = tk.Listbox(self.win, height=35, font=("simhei", 12), yscrollcommand=self.datum_scr.set,
                                    listvariable=self.dt_box)
        self.attrs_box = tk.Listbox(self.win, height=35, font=("simhei", 12), yscrollcommand=self.attrs_scr.set,
                                    listvariable=self.at_box)
        self.attrs_txt = tk.Text(self.win, height=35, font=("simhei", 13), yscrollcommand=self.at_txt_scr.set,
                                 xscrollcommand=self.at_txt_hscr.set, undo=True, wrap="none")
        self.model_box.bind("<FocusIn>", lambda eve: (self.__init_datum_box__(), self.__init_at_box_txt__()))
        self.model_box.bind("<Button>", lambda eve: (self.__init_datum_box__(), self.__init_at_box_txt__()))
        self.model_box.bind("<Double-Button-1>", lambda eve: self.__dt_box__(eve.widget))
        self.datum_box.bind("<FocusIn>", lambda eve: self.__init_at_box_txt__())
        self.datum_box.bind("<Button>", lambda eve: self.__init_at_box_txt__())
        self.datum_box.bind("<Double-Button-1>", lambda eve: self.__at_box__(eve.widget))
        self.datum_box.bind("<Key>", lambda eve: self.__dt_box_bind__(eve))
        self.attrs_txt.bind("<Key>", lambda eve: self.__at_txt_bind__(eve))
        self.model_scr.config(command=self.model_box.yview)
        self.datum_scr.config(command=self.datum_box.yview)
        self.attrs_scr.config(command=self.attrs_box.yview)
        self.at_txt_scr.config(command=self.attrs_txt.yview)
        self.at_txt_hscr.config(command=self.attrs_txt.xview)

        self.md_Label = tk.Label(self.win, text="Models:")
        self.dt_Label = tk.Label(self.win, text="MainKeys:")
        self.at_Label = tk.Label(self.win, text="Attributes:")
        self.txt_Label = tk.Label(self.win, text="Values:")

        self.md_Label.grid(row=0, column=0)
        self.dt_Label.grid(row=0, column=2)
        self.at_Label.grid(row=0, column=4)
        self.txt_Label.grid(row=0, column=6)
        self.model_box.grid(row=1, column=0)
        self.model_scr.grid(row=1, column=1, sticky=tk.N + tk.S)
        self.datum_box.grid(row=1, column=2)
        self.datum_scr.grid(row=1, column=3, sticky=tk.N + tk.S)
        self.attrs_box.grid(row=1, column=4)
        self.attrs_scr.grid(row=1, column=5, sticky=tk.N + tk.S)
        self.attrs_txt.grid(row=1, column=6)
        self.at_txt_scr.grid(row=1, column=7, sticky=tk.N + tk.S)
        self.at_txt_hscr.grid(row=2, column=6, sticky=tk.W + tk.E)


if __name__ == "__main__":
    # test
    import user_models as model
    import user_settings as st

    a = DataManager(model, st)
    a.Start()
