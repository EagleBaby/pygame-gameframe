import os

PATH = os.getcwd()
DATAPATH = os.path.join(PATH, "data")
PATH_SET = dict(img=os.path.join(DATAPATH, "img"), sound=os.path.join(DATAPATH, "sound"),
                datum=os.path.join(DATAPATH, "datum"))

TITLE_CAPTION = "PGFRAME_EXAMPLE"
TITLE_ICON = "game.png"
DEFAULT_WINDOW_SIZE = (600, 800)
FREQUENCY = 60

AUTO_UPDATE_MODEL = False  # 请在需要的时候激活一次，激活时启动会显著消耗更多资源

AUTO_TIDY = dict(sound=True)
AUDIO_BIT = 44100
AUDIO_BUFFER = 512
