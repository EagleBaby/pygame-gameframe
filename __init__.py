import os
import shutil
import sys

"""
采用mcv模式
m：
一个继承model的class一个数据类型
一个class实例化，一条数据
被其他模块调用
c：
一个继承ctrl的class一种控制
在view里调用LogController激活控制器
v:
一个继承view的class一种视图
被其他视图通过AddView加载或以主界面形式被pgframe调用(run中填写view的名称并且将此view的auto设为True)

其他：
c(Components):
一个继承components的class一种组件
调用AddComponents为你的view添加组件

以上模式简称mcv-c
除m外，cv-c中任一class实例对象中含有.data和.inst属性，通过他们可以访问到全局数据和上级对象

全局数据中以System_Support_Part_开头的全为系统方法；以system_support_part_开头的全为系统属性，用户不应随意调用它们,随意调用这些方法可能会导致程序崩溃
而全局数据中以Support_Part_开头的为用户可调用方法；以support_part_开头的为用户可调用属性，虽然这些方法和属性用户可以使用，但仍然不建议使用他们，因为这些方法仍然位于较底层并且用于底层的debug
建议用户在.data中保存数据时不要以support_part_或system_support_part_作为数据名称的开头，避免重名覆盖
总之，程序项目编写几乎不需要用户使用全局数据中(.data)的方法和属性，对用户而言.data的作用就只是存放全局数据。例如model实例化对象建议放在.data中，便于全局调用

components中内置了Pic，Collide组件
controllers中内置了Click，Focus控制器
"""
pgframe_dir = os.path.split(__file__)[0]
os.environ['PATH'] = os.environ['PATH'] + ';' + pgframe_dir

import pgframe.main as main
import pgframe.ModuleSettings as MST


def GetGame(models, controllers, views, components, events, settings):
    return main.main_init(models, controllers, views, components, events, settings)


def CreateProject(path, version=MST.PGFRAME_VERSION):
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
        open(os.path.join(path, "views.py"), "w", encoding="utf-8").write(MST.USER_VIEW[version])
        open(os.path.join(path, "controllers.py"), "w", encoding="utf-8").write(MST.USER_CTRL[version])
        open(os.path.join(path, "components.py"), "w", encoding="utf-8").write(MST.USER_COMPONENT[version])
        open(os.path.join(path, "events.py"), "w", encoding="utf-8").write(MST.USER_EVENT[version])
        open(os.path.join(path, "settings.py"), "w", encoding="utf-8").write(MST.USER_SETTING[version])
        open(os.path.join(path, "models.py"), "w", encoding="utf-8").write(MST.USER_MODEL[version])
        open(os.path.join(path, "main.py"), "w", encoding="utf-8").write(MST.USER_MAIN[version])
        open(os.path.join(path, "DataManager.py"), "w", encoding="utf-8").write(MST.USER_DataManager[version])
        shutil.copy(os.path.join(pgframe_dir, "game.png"), os.path.join(path, "game.png"))
        # shutil.copytree(os.path.join(pgframe_dir, "data"), os.path.join(path, "data")) # 刚刚创建好时data里应该没有文件
        os.mkdir(os.path.join(path, "data"))
        os.mkdir(os.path.join(path, "data", "datum"))
        os.mkdir(os.path.join(path, "data", "img"))
        os.mkdir(os.path.join(path, "data", "sound"))
        os.mkdir(os.path.join(path, "data", "sound", "sound"))
        os.mkdir(os.path.join(path, "data", "sound", "music"))
    except KeyError:
        print("-->Error:Can not find a suit version for " + str(version) + ".<--")


def shell():
    help_doc = "\nhelp    查看帮助信息\nquit,exit,shutdown  退出shell\nnew    新建项目\n"
    while True:
        temp = input("输入命令:\n")
        temp = temp.lower()
        if temp == "help":
            print(help_doc)
        elif temp in ["quit", "exit", "shutdown"]:
            break
        elif temp == "new":
            path = input("请输入目标路径:\n(若路径存在,则该路径下所有文件将被清理,请确保路径不是根目录或有文件的目录)\n")
            version = input("请输入您想创建的pgframe工程版本(可选，默认为最新" + str(MST.PGFRAME_VERSION) + "):")
            if version != "":
                try:
                    float(version)
                except:
                    print("-->Error:Version can not be a non-int<--")
                    continue
                CreateProject(path, float(version))
            else:
                CreateProject(path)
                print("-->Successful:Project at " + path + " be successfully created.<--")
        else:
            print("\n无效的命令(输入help命令可以查看帮助).\n")
