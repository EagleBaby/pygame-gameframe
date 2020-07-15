# 这是一个用户文件
from pgframe import GetGame
import user_events
import user_models
import user_settings
import user_views
import user_components
import user_controllers

Game = GetGame(user_models, user_controllers, user_views, user_components, user_events, user_settings)

Game.run()
