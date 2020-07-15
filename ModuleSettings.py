from pgframe.base import *

# 设定

# 常量
PGFRAME_VERSION = 1.0

USER_VIEW = {
    1.0: "# 这是一个用户文件\nfrom pgframe.views import View\nfrom models import *\n\n\nclass Root(View):\n    auto = True\n    layer = -1\n",
}
USER_EVENT = {
    1.0: "# 这是一个用户文件\nfrom pgframe.events import *\n",
}
USER_CTRL = {
    1.0: "# 这是一个用户文件\nfrom pgframe.controllers import *\nfrom models import *\n",
}

USER_MODEL = {
    1.0: "# 这是一个用户文件\nfrom pgframe.models import *\n",
}
USER_COMPONENT = {
    1.0: "# 这是一个用户文件\nfrom pgframe.components import *\nfrom models import *\n",
}
USER_SETTING = {
    1.0: "# 这是一个用户文件\nimport os\nPATH = os.getcwd()\nDATAPATH = os.path.join(PATH,\"data\")\nPATH_SET = dict("
         "img=os.path.join(DATAPATH,\"img\"),sound=os.path.join(DATAPATH,\"sound\"),datum=os.path.join(DATAPATH,"
         "\"datum\"))\n\nTITLE_CAPTION = \"PGFRAME_EXAMPLE\"\nTITLE_ICON = \"game.png\"\nDEFAULT_WINDOW_SIZE = (600, 800)"
         "\nFREQUENCY = 60\n\nAUTO_UPDATE_MODEL = False  # 请在需要的时候激活一次，激活时启动会显著消耗更多资源\n"
         "\nAUTO_TIDY = dict(sound=True)\nAUDIO_BIT = 44100\nAUDIO_BUFFER = 512\n\nWindow_Center_Adjust = (0, 38)",
}
USER_MAIN = {
    1.0: "# 这是一个用户文件\nfrom pgframe import GetGame\nimport events\nimport models\nimport "
         "settings\nimport views\nimport components\nimport controllers\n\nGame = GetGame("
         "models, controllers, views, components, events, settings)\n\nGame.run(\"Root\")\n "
}

USER_DataManager = {
    1.0: "# 这是一个用户文件\n\"\"\"\n打开时会自动更新model\n\"\"\"\nfrom pgframe.DataManager import DataManager\nimport models\nimport settings\n\nDataManager(models,settings).Start()"
}

