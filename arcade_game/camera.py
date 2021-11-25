import arcade
from constant import *

# This class is for start and set width and height of screen camera
class Camera:

    def __init__(self):
        self.camera = None

        self.gui_camera = None

    #Return the camera to the place that call it with the camera attribute
    def set_camera(self):
        return arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    
    
