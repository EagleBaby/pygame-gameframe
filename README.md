# pygame-gameframe  
* 仅供个人学习使用，不得用于商业目的；For personal study only, not for commercial purposes  
* 这是一个基于pygame的封装框架，效率也不是很高，主要的目的是让写小游戏变得更容易；This is a pyGame based packaging framework, and its efficiency is not very high. The main purpose is to make it easier to write small games  
* 目前文档资料部分只写了函数文档，以后可能会慢慢补充；At present, only function documents are written in the documentation section, which may be supplemented gradually in the future  
* 将pgframe文件夹放到site-packages下就可以如同其他库一样使用了；Put the pgframe folder under site-packages and you can use it just like other libraries  
使用方法:；usage method:  
# 1.创建项目；Create project  
* 打开idle，输入:；Open idle and enter:  
* from pgframe import *  
* shell()  
* 然后依次输入:；Then enter:  
* new  
* 'project path'
  
* 然后pgframe会自动生成一个框架在你的'project path'下；Then pgframe will automatically generate a framework under your < project Path >  
# 2.游戏框架说明；Game framework description  
* 游戏框架主要包括:；The game framework mainly includes:  
* main.py 游戏启动文件，运行它就可以启动游戏；Game startup file, run it to start the game  
* views.py 最重要的文件之一，控制游戏的界面；One of the most important files to control the game's interface  
* events.py 定义事件，每个事件被push后只能被接受一次，可以无限push；Define events. Each event can only be accepted once after being pushed, and can be pushed infinitely  
* models.py 定义存储数据的结构与一些用户定义的运算方法；Define the structure of stored data and some user-defined operation methods  
* settings.py 程序设置；Program settings  
* components.py 编写用户自定义的组件；Write user-defined components  
* controllers.py 编写用户自定义的控制器；Write user-defined controllers  
* DataManager.py 工具，对models.py中定义好的数据结构添加实例；this is a tool, right models.py Add instance of defined data structure in  
* *AnimManager.py 工具，制作pgframe原生支持的动画文件(还没有写完这个部分，目前还不可用)；this is a tool, create animation files supported by pgframe(This part has not been finished and is not available at present)  
  
* 程序编写主要需要编写view.py controller.py和models.py；Programming mainly needs to be written view.py controller.py and models.py  
  
* 每一个框架中的class都含有inst属性(上一级对象，可以为None)和Loading(self, **kwargs)方法(代替__init__的空方法)；The class in each framework contains the Inst attribute (the upper level object, which can be none) and the loading (self, * * kwargs) method (instead of__ init__ Empty method of)  
# 3.创建第一个视图；Create the first view  
* 在view.py下创建一个新的视图:  
* class xxxx(View):  
    * pass  
  * 载入刚才创建的视图:  
    * 在view.py下默认有一个Root(View)类，这个是游戏的view入口，即程序会第一个载入该视图  
    * 在Root类下添加如下方法，即可完成对刚刚创建的视图的载入  
    * def Loading(self, **kwargs):  # view的载入方法  
      * self.AddView(xxxx)  
    * 常用的基本载入方法有:  
    * .AddView(class, ...)  
    * .AddComponent(string, **kwargs)  
    * .LogController(string)  
    * .SetPos(positon)  
    * .SetSize(size)  
    * 现在运行游戏，窗口内依然什么也没有，因为所有能显示在屏幕上的内容都由components决定  
# 4.Pic组件  
  * 游戏使用png格式的图片，将其放在.../data/img/下的任意文件夹内(比如/data/img/example/background.png)，文件名background则是游戏中使用的名称。因此，pgframe不允许图片重名，那怕它们不在同一个文件夹内；The game uses PNG format pictures and places them in any folder under... / data / img / (for example, / data / img / example/ background.png ）The file name background is the name used in the game. Therefore, pgframe does not allow images to have duplicate names, even if they are not in the same folder  
  * 还有一种情况，将多张图片放在同一文件夹下，并在该文件目录下添加一个空的__init__.py文件，那么这个目录会被视为一个图片，该目录名即为游戏中使用的名称，不能与其他图片同名，该目录下的单个图片不与其他图片名称冲突In another case, put multiple pictures in the same folder and add an empty one to the file directory __init__.py file, then this directory will be treated as an image. The directory name is the name used in the game and cannot have the same name with other pictures. The single picture in this directory does not conflict with other picture names  
  * 在程序编写时只需通过Pic组件和图片名即可使用图片，例如在重写某个class view的Loading方法是时为该view对象添加图片:；When writing a program, you only need to use the picture through the pic component and the picture name. For example, when the loading method of a class view is rewritten, add a picture to the view object:  
  * class xxxx(View):  
    * def Loading(self, **kwargs):  
      * self.SetPos((100,100))  
      * self.AddComponent('Pic', ArtDef='background')  
  * Pic对象创建时的可选参数:;Optional parameters for PIC object creation:  
  * """  
    * Pic组件，用于显示图片或图片组  
    * :param ArtDef: 艺术数据名String  
    * :param scale: 缩放倍率Int 0-无限 (100->100%, 10->10%)(传入String类型能减少程序资源占用)  
    * :param rotate: 旋转角度Int 0-360 (向上为0, 顺时针旋转)(传入String类型能减少程序资源占用)  
    * :param hflip: 水平翻转Int 0/1(1表示水平翻转)(传入String类型能减少程序资源占用)  
    * :param vflip: 竖直翻转Int 0/1(1表示竖直翻转)(传入String类型能减少程序资源占用)  
    * :param center: 是否以中心为基准点Bool(传入False能减少程序资源占用)  
    * :param tim: 图片间隔帧Int(只适用于多图片,控制图片播放时间隔的帧数)  
    * :param keep_tim: 持续帧数Int(显示多少帧，大于此数时，该组件会被隐藏)  
    * :param justify: Tuple(int, int) 图片位置微调  
    * :param end_func: function(pic= Pic Components) 允许Pic即将Hide时激活函数  
    * :param sign: String 设置组件在inst中的变量名称,None表示不添加  
  * English vision：  
    * Pic component for displaying pictures or picture groups  
    * : param artdef: art data name string  
    * : param scale: zoom ratio int 0 ~ infinite (100 - > 100%, 10 - > 10%) (passing in string type can reduce program resource consumption)  
    * : param rotate: rotation angle int 0 ~ 360 (up = 0, clockwise rotation) (passing in string type can reduce program resource consumption)  
    * : param hflip: horizontal flip int 0 / 1 (1 means horizon flip) (passing in string type can reduce program resource consumption)  
    * : param vflip: vertical flip int 0 / 1 (1 means vertical flip) (passing in string type can reduce program resource consumption)  
    * : param Center: whether to use the center as the reference point  
    * : param Tim: picture interval frame int(It is only applicable to multiple pictures and controls the number of frames in the picture playback interval)  
    * : param keep_Tim: number of consecutive frames int (how many frames are displayed, and when the number is greater, the component will be hidden)  
    * : param justify: tuple (int, int) image position adjustment  
    * : param end_Func: function (PIC = pic components) allows pic to activate the function when it is about to hide  
    * : param sign: String sets the variable name of the component in inst, and none means not to add  
  * """  
  * 此外，框架提供了Area、Progress、Text、Collide、Locomotor组件，详细帮助请查看pgframe/view.py  
# 5.Controller控制器  
  * pass  
  
  
# --------------------------------------------------------------------------------  
我会附带上传一些例子，便于理解和模仿用法  
translation by: Baidu Translation  
    
  
    
