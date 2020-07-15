import tkinter as tk
import warnings

import win32con
import win32gui
from pgframe.support import *  # pg, display, draw, transform,Data

warnings.filterwarnings("ignore")

data = Data()


class Game(object):
    def __init__(self, data, models=None, controlors=None, views=None, components=None, events=None, settings=None):
        if models is None:
            models = md
        if controlors is None:
            controlors = ct
        if views is None:
            views = vw
        if components is None:
            components = cp
        if settings is None:
            settings = st
        if events is None:
            events = ev
        self.data = data
        self.data.inst = self
        self.data.md = models
        self.data.st = settings
        self.data.ct = controlors
        self.data.vw = views
        self.data.cp = components
        self.data.ev = events
        self.data.clock = pg.time.Clock()
        if not hasattr(models, "System_Model_Part_Init"):
            raise (Exception("In your models.py,you need \"from pgframe.models import *\"."))

    def SetWindowCenter(self):
        old_vision_adjust = self.data.st.Window_Center_Adjust if hasattr(self.data.st, '') else (0, 38)
        temp = tk.Tk()
        s_w = temp.winfo_screenwidth()
        s_h = temp.winfo_screenheight()
        temp.destroy()
        t = self.data.st.DEFAULT_WINDOW_SIZE
        x, y, a, b = int((s_w - t[0]) / 2), int((s_h - t[1]) / 2), *t
        hwnd = win32gui.FindWindow(None, self.data.st.TITLE_CAPTION)
        win32gui.SetWindowPos(hwnd, None, x, y, a + old_vision_adjust[0], b + old_vision_adjust[1],
                              win32con.SWP_SHOWWINDOW)

    def run(self, window_name):
        pg.init()
        self.data.screen = display.set_mode(self.data.st.DEFAULT_WINDOW_SIZE)
        self.data.System_Support_Part_GetThingsReady(srt_window=window_name)
        win = self.data.Support_Part_GetWindow()
        display.set_caption(self.data.st.TITLE_CAPTION)
        display.set_icon(image.load(self.data.st.TITLE_ICON))
        self.SetWindowCenter()
        while True:
            self.data.System_Support_Part_TickSetProcess()
            for eve in pg.event.get():
                if eve.type == pg.QUIT:
                    quit()
                self.data.Support_Part_GetCtrlManage().AddQueue("CtrlHandler", data=self.data, eve=eve)
                self.data.Support_Part_GetEveManage().AddQueue("EventHandler", data=self.data, eve=eve)
            self.data.Support_Part_GetEveManage().AddQueue("PeriodTaskHandler", data=self.data)
            self.data.Support_Part_GetWinManage().AddQueue("UpdateGameWindow")
            self.data.clock.tick(self.data.st.FREQUENCY)
            self.data.Support_Part_GetSoundManage().AddQueue("MusicQueueHandler")
            self.data.Support_Part_GetCamera().CameraUpdate()

    def TidyPngImage(self):
        from PyQt5.QtGui import QImage
        img = QImage()
        path = self.data.st.PATH_SET["img"]
        for root, dirs, files in os.walk(path):
            for name in files:
                print(name)
                if name.endswith(".png"):
                    img.load(path + name)
                    img.save(path + name)

    def TidySoundFiles(self, to_format="ogg"):
        from pydub import AudioSegment
        temp = []
        path = self.data.st.PATH_SET["sound"]
        for root, dirs, files in os.walk(path):
            for file in files:
                temp.append(os.path.join(root, file))
        path = temp
        for i in path:
            base, format = os.path.splitext(i)
            format = format[1:]
            if not hasattr(AudioSegment, "from_" + format):
                print("\"", format, "\" format doesn' t be supported.")
            sound = getattr(AudioSegment, "from_" + format)(i)
            sound.export(base + "." + to_format, format=to_format)


def main_init(models, controlors, views, components, events, settings):
    if not data.game___init__:
        data.game___init__ = True
        return Game(data, models, controlors, views, components, events, settings)
    else:
        print("pgframe has already __init__ed.")


if __name__ == "__main__":
    a = main_init(None, None, None, None, None, None)
    a.run("Root")
