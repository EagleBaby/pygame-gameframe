import os
from tkinter import *
from tkinter import filedialog as fd

import PIL.Image as Img
import PIL.ImageTk as ImgTk
from pgframe.base import IsInArea

cnv_images = []  # 用于cnv加载专用的变量


class AnimManager(object):
    class Anim(object):
        def __init__(self, inst, width, height):
            self.inst = inst
            self.width = width
            self.height = height
            self.images = inst.used_images
            self.points_rec = []

            self.ResetChoose()

            self.animations = {"default": {
                "1": []}}  # [](spirits) 与self.images一一对应，每一项是一个列表[img_path,position(中心位置)](有关scale,rotate,hflip,vflip的操作均由pillow操作完成,这里只保留原始数据)
            self.now = "default"  # 当前动画归属
            self._last = None

        def ResetChoose(self):
            self.choose_id = {"default": {"1": None}}
            self.choose_frame = {"default": {"1": None}}

        def get_last_point(self, point=None):
            if not point:
                point = self.inst.p.get()
            else:
                point = int(point)

        def set_choose_frame(self, value, index=None):
            if not index:
                index = str(self.inst.p.get())
            else:
                index = str(index)

            if not self.choose_frame.get(self.now):
                self.choose_frame[self.now] = {"1": None}
            self.choose_frame[self.now][index] = value

        def get_choose_frame(self, index=None):
            if not index:
                index = str(self.inst.p.get())
            else:
                index = str(index)
            if not self.choose_frame.get(self.now):
                self.choose_frame[self.now] = {"1": None}
            if self.choose_frame[self.now].get(index, "None") == "None":
                self.choose_frame[self.now][index] = None
            return self.choose_frame[self.now][index]

        def set_choose_id(self, value, index=None):
            if not index:
                index = str(self.inst.p.get())
            else:
                index = str(index)

            if not self.choose_id.get(self.now):
                self.choose_id[self.now] = {"1": None}
            self.choose_id[self.now][index] = value

        def get_choose_id(self, index=None):
            if not index:
                index = str(self.inst.p.get())
            else:
                index = str(index)
            if not self.choose_id.get(self.now):
                self.choose_id[self.now] = {"1": None}
            if self.choose_id[self.now].get(index, "None") == "None":
                self.choose_id[self.now][index] = None
            return self.choose_id[self.now][index]

        def get_spirits(self, index=None):
            if not index:
                index = str(self.inst.p.get())
            else:
                index = str(index)
            if not self.animations.get(self.now):
                self.animations[self.now] = {"1": []}
            if not self.animations[self.now].get(index):
                self.animations[self.now][index] = []

            return self.animations[self.now][index]

    def __init__(self):
        self.img_path = []  # 由文件添加所得到所有路径
        self.images = []  # 由文件添加所得到的所有image对象
        self.img_f = []  # 图片映射函数, import_image -> 原始id,[(import_img,id)]
        self.used_images = {"1": []}  # 添加到画布中的所有image对象, 与每一帧对应
        self.ids = []  # 元素在画布上的所有id, 每一帧都会被刷新
        self.scales = {"1": []}
        self.rotates = {"1": []}
        # self.used_photoimages = cnv_images  # 供画布使用的所有photoimage对象

        self._win = Tk()
        self._win.title("AnimManager")
        self._win.minsize(1520, 990)
        self._win.maxsize(1520, 990)
        self._win.attributes("-alpha", .9)
        self.__create__()
        self._win.mainloop()

    def _get_ori_img_(self, changed_img):
        for i in self.img_f:
            if i[0] == changed_img:
                return self.images[i[1]]


    def __part_ctrl__(self, state):  # 禁止/可用 的控制
        state = ACTIVE if state else DISABLED
        f_mb = [3, 5, 7, 8]
        edit_mb = [0, 1, 3, 4, 5, 7]
        for i in f_mb:
            self.f_mb.entryconfig(i, state=state)
        for i in edit_mb:
            self.edit_mb.entryconfig(i, state=state)

        # 属性条隐藏
        if state == DISABLED:
            self.attrs.pack_forget()
        else:
            self.attrs.pack()
            self.attr_scale_entry.config(state=DISABLED)
            self.attr_rotate_entry.config(state=DISABLED)

    def __add_source__(self):  # 添加文件到左边框框
        paths = fd.askopenfilenames(title="选择动画元素文件:", defaultextension=".png",
                                    filetypes=[("png", ".png"), ("所有文件", "*")])
        for i in paths:
            if i not in self.img_path:
                self.img_path += [i]
                temp = str(len(self.img_path))
                if len(temp) == 1:
                    temp = "00" + temp
                elif len(temp) == 2:
                    temp = "0" + temp
                elif len(temp) == 3:
                    pass
                else:
                    del self.img_path[-1]
                    print("达到上限.")
                self.images += [Img.open(i)]
                self.box_cps.insert("end", temp + os.path.basename(i))

    def __cp_box__(self, widget):
        if not widget.curselection():
            return
        else:
            which = widget.get(widget.curselection()[0])

        self.__add_spirit__(which)

    def __act_box__(self, widget):
        if not widget.curselection():
            return
        else:
            which = widget.get(widget.curselection()[0])

        self.anim.now = which

    def get_ori_index(self,changed_img):
        for i in self.img_f:
            if i[0] == changed_img:
                return i[1]

    def set_img

    def __add_spirit__(self, select_name):
        index = int(select_name[:3]) - 1
        self.used_images[str(self.p.get())] += [self.images[index].copy()]
        self.img_f[self.used_images[str(self.p.get())]] = index
        self.scales[str(self.p.get())] += [100]  # 0~400
        self.rotates[str(self.p.get())] += [0]  # 0~360
        x, y = int(.5 * self._p_width), int(.5 * self._p_height)
        temp = self.anim.get_spirits()
        temp += [[self.img_path[index], (x, y)]]
        size = int(self._p_width * self.cnv_zoom / 100), int(self._p_height * self.cnv_zoom / 100)
        if self.cnv:
            self.cnv.destroy()
            self.cnv = None
        self.ReFreshCanvas(*size)

    def _set_important_(self):
        pass

    def _get_point_(self):
        return self.p.get()

    def _get_scale_(self):
        return self.attr_scale.get()

    def _get_rotate_(self):
        return self.attr_rotate.get()

    def __create__(self):
        self.mb = Menu(self._win)
        self.f_mb = Menu(self.mb, tearoff=False)
        self.edit_mb = Menu(self.mb, tearoff=False)
        self.help_mb = Menu(self.mb, tearoff=False)

        self.f_mb.add_command(label="new", command=self._NewAnimProject)
        self.f_mb.add_command(label="open", command=self._OpenAnimProject)
        self.f_mb.add_separator()
        self.f_mb.add_command(label="add source", command=self.__add_source__)
        self.f_mb.add_separator()
        self.f_mb.add_command(label="close", command=self._CloseAnimProject)
        self.f_mb.add_separator()
        self.f_mb.add_command(label="save", command=self._SaveAnimProject)
        self.f_mb.add_command(label="save As", command=self._SaveAsAnimProject)
        self.f_mb.add_separator()
        self.f_mb.add_command(label="quit", command=self._win.quit)
        # ----
        self.edit_mb.add_command(label="undo", command=self._Undo)
        self.edit_mb.add_command(label="redo", command=self._Redo)
        self.edit_mb.add_separator()
        self.edit_mb.add_command(label="copy", command=self._Copy)
        self.edit_mb.add_command(label="cut", command=self._Cut)
        self.edit_mb.add_command(label="paste", command=self._Paste)
        self.edit_mb.add_separator()
        self.edit_mb.add_command(label="set as important", command=self._set_important_)
        # ----
        self.help_mb.add_command(label="info", command=self._info)
        self.mb.add_cascade(label="file", menu=self.f_mb)
        self.mb.add_cascade(label="edit", menu=self.edit_mb)
        self.mb.add_cascade(label="help", menu=self.help_mb)

        self._win.config(menu=self.mb)
        # Create Menus ------- Status: Finish ----------

        self.fr_cps = Frame(self._win, height=870, width=120)
        self.fr_cps.pack_propagate(0)
        self.fr_cnv = Frame(self._win, height=870, width=1200)
        self.fr_cnv.pack_propagate(0)
        self.fr_attr = Frame(self._win, height=870, width=200, bg="#FFF8DC")  # 右边框框
        self.fr_attr.pack_propagate(0)
        self.fr_ele = Frame(self._win, height=120, width=1200, bg="#F0FFFF")  # 底下框框
        self.fr_ele.pack_propagate(0)
        self.fr_inf = Frame(self._win, height=120, width=200, bg="#FFE4E1")  # 右下边框框  # Frame:<--
        self.fr_inf.pack_propagate(0)

        self.cnv_src = Scrollbar(self.fr_cnv), Scrollbar(self.fr_cnv, orient=HORIZONTAL)
        self.attr_src = Scrollbar(self.fr_attr), Scrollbar(self.fr_attr, orient=HORIZONTAL)
        self.ele_src = Scrollbar(self.fr_ele), Scrollbar(self.fr_ele, orient=HORIZONTAL)
        # {
        self.zoom_inf = StringVar(self.fr_inf, "")
        self.zoom_lab = Label(self.fr_inf, textvariable=self.zoom_inf, bg="#FFE4E1")

        self.box_act = Listbox(self.fr_attr, bg="#FFFFF0", bd=0, relief="flat")
        self.box_cps = Listbox(self.fr_cps, height=50, bg="#FFF8DC", bd=0, relief="flat")

        self.box_cps.bind("<Double-Button-1>", lambda eve: self.__cp_box__(eve.widget))
        self.box_act.bind("<Double-Button-1>", lambda eve: self.__act_box__(eve.widget))

        self.attrs = Frame(self.fr_attr, bg="#FFF8DC")
        # {
        self.attr_scale_label = Label(self.attrs, text="缩放(Scale):", bg="#FFF8DC")
        self.attr_scale = StringVar()
        self.attr_scale_entry = Entry(self.attrs, textvariable=self.attr_scale)
        self.attr_scale_entry.bind("<FocusOut>", self._ChangeSpiritScale)

        self.attr_rotate_label = Label(self.attrs, text="旋转(Rotate):", bg="#FFF8DC")
        self.attr_rotate = StringVar()
        self.attr_rotate_entry = Entry(self.attrs, textvariable=self.attr_rotate)
        self.attr_rotate_entry.bind("<FocusOut>", self._ChangeSpiritRotate)
        # }

        # }
        self.fr_cps.grid(row=0, column=0)
        self.fr_cnv.grid(row=0, column=1)
        self.fr_attr.grid(row=0, column=2)
        self.fr_ele.grid(row=1, column=1)
        self.fr_inf.grid(row=1, column=2)

        self.zoom_lab.pack()
        self.box_act.pack(fill=X)
        self.attrs.pack()
        self.attr_scale_label.pack(fill=X)
        self.attr_scale_entry.pack(fill=X)
        self.attr_rotate_label.pack(fill=X)
        self.attr_rotate_entry.pack(fill=X)
        self.box_cps.pack(fill=BOTH)
        # Create Widgets ------- Status: Finish ----------
        self.cnv = None
        # Create Special ------- Status: Finish ----------
        self.__part_ctrl__(False)

    def _ChangeSpiritScale(self, eve):
        _id = self.anim.get_choose_id()
        self.scales[self._get_point_()][_id] = self._get_scale_()
        index = self.img_f.pop(self.used_images[_id])
        self.used_images[_id] = self.images[index].resize(
            self._trans_position(self.images[index].size, self._get_scale_()))
        self.img_f[self.used_images[_id]] = index
        self._UpdateCnv()

    def _ChangeSpiritRotate(self, eve):
        self.rotates[self._get_point_()][self.anim.get_choose_id()] = self._get_rotate_()
        self._UpdateCnv()

    def _trans_position(self, pos, per):
        return int(pos[0] * per), int(pos[1] * per)

    def _justify_pos(self, pos, justify):
        return pos[0] + justify[0], pos[1] + justify[1]

    def _GetPhotoImage(self, _from):
        return ImgTk.PhotoImage(Image.open(_from) if isinstance(_from, str) else _from)

    def __cnv_choose_spirit(self, eve):
        top = None
        percent = self.cnv_zoom / 100
        for i in range(len(self.used_images[str(self.p.get())])):
            if IsInArea((eve.x, eve.y), self._trans_position(
                    self._justify_pos(self.anim.get_spirits()[i][1],
                                      self._trans_position(self.used_images[str(self.p.get())][i].size, -0.5)),
                    percent), self._trans_position(self.used_images[str(self.p.get())][i].size, percent)):
                top = i
        if top is not None:
            self.anim.set_choose_id(top)
            self.attr_scale_entry.config(state=NORMAL)
            self.attr_rotate_entry.config(state=NORMAL)
        else:
            self.anim.set_choose_id(None)
            self.attr_scale_entry.config(state=DISABLED)
            self.attr_rotate_entry.config(state=DISABLED)
        self._Update_Choose_Frame()

    def _Update_Choose_Frame(self):
        if self.anim.get_choose_id() is not None:
            if self.anim.get_choose_frame():
                self.cnv.delete(self.anim.get_choose_frame())
            temp = self.anim.get_spirits()[self.anim.get_choose_id()][1]
            w, h = self.used_images[str(self.p.get())][self.anim.get_choose_id()].size
            x, y = int(temp[0] - .5 * w), int(temp[1] - .5 * h)
            x, y, w, h = int(x * self.cnv_zoom / 100), int(y * self.cnv_zoom / 100), int(w * self.cnv_zoom / 100), int(
                h * self.cnv_zoom / 100)
            self.anim.set_choose_frame(self.cnv.create_rectangle(x, y, x + w, y + h, fill="", dash=(2, 3)))
        else:
            if self.anim.get_choose_frame():
                self.cnv.delete(self.anim.get_choose_frame())
            self.anim.set_choose_frame(None)

    def __cnv_move_spirit(self, eve):
        global cnv_images
        if self.anim.get_choose_id() is not None:
            self.cnv.delete(self.ids[self.anim.get_choose_id()])
            self.ids[self.anim.get_choose_id()] = self.cnv.create_image(eve.x, eve.y,
                                                                        image=cnv_images[self.anim.get_choose_id()])
            self.anim.get_spirits()[self.anim.get_choose_id()][1] = (
                int(eve.x / self.cnv_zoom * 100), int(eve.y / self.cnv_zoom * 100))
            self._Update_Choose_Frame()

    def __cnv_processWheel(self, eve):
        direct = eve.delta
        if direct > 0 and self.cnv_zoom < 400 and (
                self.cnv.winfo_height() <= 750 and self.cnv.winfo_width() <= 1050):
            self.cnv_zoom += 25
        elif direct < 0 and self.cnv_zoom > 50:
            self.cnv_zoom -= 25

        self.zoom_inf.set("缩放比例:" + str(self.cnv_zoom) + "%")
        size = int(self._p_width * self.cnv_zoom / 100), int(self._p_height * self.cnv_zoom / 100)
        if self.cnv:
            self.cnv.destroy()
            self.cnv = None
        self.ReFreshCanvas(*size)

    def _UpdateCnv(self):
        global cnv_images
        cnv_images = []
        self.ids = []
        if self.cnv:
            self._Update_Choose_Frame()
            for img in self.used_images[str(self.p.get())]:
                w, h = img.size
                cnv_images += [
                    self._GetPhotoImage(img.resize((int(w * self.cnv_zoom / 100), int(h * self.cnv_zoom / 100))))]
            for i in range(len(cnv_images)):
                x, y = self.anim.get_spirits()[i][1]
                self.ids += [self.cnv.create_image(int(x * self.cnv_zoom / 100), int(y * self.cnv_zoom / 100),
                                                   image=cnv_images[i])]

    def ReFreshCanvas(self, width, height):
        self.cnv = Canvas(self.fr_cnv, height=height, width=width, bg="white", yscrollcommand=self.cnv_src[0].set,
                          xscrollcommand=self.cnv_src[1].set)
        self.cnv_src[0].config(command=self.cnv.yview), self.cnv_src[1].config(command=self.cnv.xview)
        self.cnv.bind("<MouseWheel>", self.__cnv_processWheel)
        self.cnv.bind("<Button-1>", self.__cnv_choose_spirit)
        self.cnv.bind("<B1-Motion>", self.__cnv_move_spirit)
        self._UpdateCnv()
        self.cnv.grid(row=0, column=0)

    def __scale2_change_(self, scale):
        self.scl1.config(from_=0 + int(scale), to=200 + int(scale))
        # print(self.p.get())  #debug

    def __point_change_(self, point):
        if point == 0:
            self.p.set(1)
            point = 1
        size = int(self._p_width * self.cnv_zoom / 100), int(self._p_height * self.cnv_zoom / 100)
        if not self.used_images.get(str(point)):
            self.used_images[str(point)] = []
            self.scales[str(point)] = []
            self.rotates[str(point)] = []
        self.ReFreshCanvas(*size)
        # print("l'm changed, now is " + str(self.p.get()) + ',point is ' + point)  #debug

    def _PrepareWorkEnvironment(self):
        self.cnv_zoom = 100
        self.zoom_inf.set("缩放比例:" + str(self.cnv_zoom) + "%")
        for k in self.anim.animations:
            self.box_act.insert("end", k)
        self.p = IntVar(value=1)
        self.scl1 = Scale(self.fr_ele, orient=HORIZONTAL, bg="#F0FFFF", from_=0, to=200, variable=self.p,
                          command=self.__point_change_)
        self.scl2 = Scale(self.fr_ele, orient=HORIZONTAL, bg="#F0FFFF", from_=0, to=10000, resolution=50,
                          label="调整条(50位)", command=self.__scale2_change_)
        self.scl1.pack(fill=X)
        self.scl2.pack(fill=X)

    def _NewAnimProject(self):
        global cnv_images
        size = SizeInputWin()
        self._CleanUp()
        self.anim = self.Anim(self, *size)
        self._p_width, self._p_height = size
        self._PrepareWorkEnvironment()
        if self.cnv:
            self.cnv.destroy()
            self.cnv = None
        self.ReFreshCanvas(*size)

        self.__part_ctrl__(True)

    def _OpenAnimProject(self):
        print("打开工程")

    def _SaveAnimProject(self):
        print("保存工程")

    def _SaveAsAnimProject(self):
        print("另存为工程")

    def _CleanUp(self):
        global cnv_images
        self.images, self.img_path, self.used_images, self.ids, cnv_images = [], [], {"1": []}, [], []
        if hasattr(self, "anim") and self.anim is not None:
            self.anim.ResetChoose()
        self.anim = None
        self.animations = {"default": None}
        self.box_cps.delete(0, "end")
        self.box_act.delete(0, "end")

    def _CloseAnimProject(self):
        self._CleanUp()
        self.zoom_inf.set("")
        self.cnv.destroy()
        self.cnv = None

        self.__part_ctrl__(True)

    def _Redo(self):
        print("重做")

    def _Undo(self):
        print("撤销")

    def _Copy(self):
        print("拷贝")

    def _Cut(self):
        print("剪贴")

    def _Paste(self):
        print("粘贴")

    def _info(self):
        print("帮助信息")


def SizeInputWin(title="Create New Anim:"):
    def Click(lis):
        if etr[0].get().isdigit() and etr[1].get().isdigit():
            w, h = int(etr[0].get()), int(etr[1].get())
            if 0 < w <= 1200 and 0 < h <= 800:
                lis[0] = int(etr[0].get())
                lis[1] = int(etr[1].get())
                _win.quit()
                _win.destroy()
            else:
                print("输入范围:\nWidth:\n0~1200\nHeight:\n0~800")
        else:
            print("请输入正确数据:")

    def Enter(eve):
        if eve.keycode == 13:
            Click(rtn)

    rtn = [200, 200]
    _win = Tk()
    _win.title(title)
    _win.attributes("-alpha", .9)
    _win.bind("<KeyPress>", Enter)
    lab = Label(_win, text="Width:"), Label(_win, text="Height:")
    etr = Entry(_win), Entry(_win)
    btn = Button(_win, text="Cancel", command=_win.quit), Button(_win, text="Create", command=lambda: Click(rtn))
    lab[0].grid(column=0, row=0, sticky=W), lab[1].grid(column=1, row=0, sticky=W)
    etr[0].grid(column=0, row=1, sticky=W + E), etr[1].grid(column=1, row=1, sticky=W + E)
    btn[0].grid(column=0, row=2, sticky=W + E), btn[1].grid(column=1, row=2, sticky=W + E)
    etr[0].insert("end", str(rtn[0])), etr[1].insert("end", str(rtn[1]))
    size = (288, 74)
    _win.minsize(*size)
    _win.maxsize(*size)
    _win.mainloop()
    return rtn


if __name__ == "__main__":
    _anim = AnimManager()
