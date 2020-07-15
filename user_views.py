# 这是一个用户文件
import random

from pgframe.views import View, Anim


class Root(View):
    auto = True

    def Loading(self, **kwargs):
        self.layer = -1
        # self.SetPercent((0.2, 0.2))
        # self.PlaySound("test")
        # self.PlaySound("g")
        # self.PlaySound("spider dance")
        # self.PlaySound("heartache")
        # self.MapInit((6, 10), Box)
        # self.AddView(Player)
        # self.AddView(Box)
        for n in range(4):
            for i in range(0, 7):
                self.AddView(TestAnim, _pos=(n*30 +i*10+30, 30 * i +n), stars=i)
            for i in range(6, -1, -1):
                self.AddView(TestAnim, _pos=(n*30+i*10+30, 420 - 30 * i+n), stars=i)
        # a = self.AddView(Box)
        # self.AddView(Time)
        # self.GetView(a).SetPercent((0.6, 0.2))
        # for i in ["MoveUp", "MoveDown", "MoveLeft", "MoveRight"]:
        #     self.LogController(i)


class TestAnim(Anim):
    def Loading(self, **kwargs):
        self.SetSize((12, 24))
        self.fill_num = kwargs["stars"]
        for i in range(6):
            self.AddSpirit("empty", "p" + str(i + 1), False, justify=(i * 30, 0), tim=18)
        for i in range(6):
            self.AddSpirit("wave", "w" + str(i + 1), False, 20, tim=6, keep_tim=18, justify=(i * 30, 0))
        self.ShowStars()
        # self.data.Support_Part_GetCamera().LiftCamera(200, 90)
        # self.data.Support_Part_GetCamera().MoveCamera((-200, -200), 90)

    def SetStarsNum(self, num):
        self.fill_num = num if 0 <= num <= 6 else random.randint(0, 6)

    def ShowStars(self):
        codes = []
        # self.tick = Tick(40)
        for i in range(1, 7):
            codes += ["self.p" + str(i) + ".Show()"]
            for rotate, scale in zip(range(40, 361, 40), range(39, 11, -3)):
                codes += ["self.p" + str(i) + ".Rotate(" + str(rotate) + ")," +
                          "self.p" + str(i) + ".Scale(" + str(scale) + ")"
                          ]
            if self.fill_num >= i:
                codes += ["self.w" + str(i) + ".Show()"]

        if self.fill_num >= 1:
            self.p1.SetPic("fill")
        if self.fill_num >= 2:
            self.p2.SetPic("fill")
        if self.fill_num >= 3:
            self.p3.SetPic("fill")
        if self.fill_num >= 4:
            self.p4.SetPic("fill")
        if self.fill_num >= 5:
            self.p5.SetPic("fill")
        if self.fill_num >= 6:
            self.p6.SetPic("fill")
        self.DoThingsInTick(codes, 36)


class Time(View):
    def Loading(self, **kwargs):
        self.SetPercent((.1, .1))
        self.AddComponent("Text", text="hello\nworld!", equality=True, auto=True, sign="txt")
        # self.AddComponent("Text", text="hello,world!",equality=True, sign="txt1")
        self.txt.Show()


class Box(View):
    def Loading(self, **kwargs):
        self.SetSize((60, 60))
        # self.SetPercent((0.8, 0.2))
        self.AddComponent("Collide", group_name="Box")
        self.AddComponent("Pic", ArtDef="box")
        self.data.Support_Part_GetCamera().LiftCamera(200, 90)
        self.data.Support_Part_GetCamera().MoveCamera((-200, -200), 90)


class Player(View):
    def func(self, inst, data):
        print("玩家被点击")

    def Loading(self, **kwargs):
        self.data.player = self
        self.SetSize((60, 60))
        self.SetPercent((0.5, 0.5))
        self.AddComponent("Collide", group_name="player", aim_name="Box", push=True)
        self.AddComponent("Pic", ArtDef="player", tim=4, sign="pic")
        self.AddComponent("Locomotor", sign="motor", frequency=50, collide_act="keep")
        self.LogController("Hello")
        self.ListenForEvent("test", lambda eve, data: print("event", "我被点击了"))
