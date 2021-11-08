import arcade
from constant import *


class Camera:

    def __init__(self):
        self.camera = None

        self.gui_camera = None

    
    def set_camera(self):
        return arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    
    
