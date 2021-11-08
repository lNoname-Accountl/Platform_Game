import arcade
from constant import *

class PhysicsEngine:
    def __init__(self):
        self.pengine = None

    def startEngine(self, player, scene):
        self.pengine = arcade.PhysicsEnginePlatformer(
            player,
            [
                scene.get_sprite_list(LAYER_NAME_PLATFORMS),
                scene.get_sprite_list(LAYER_NAME_MOVING)
            ],
            gravity_constant = GRAVITY,
            ladders = scene.get_sprite_list(LAYER_NAME_LADDERS)
        )
