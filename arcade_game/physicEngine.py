import arcade
from constant import *

#Physics Engine of the game
class PhysicsEngine:
    def __init__(self):
        self.pengine = None

    #Function for initiating the physic engine by accepting the player layer, platform layer, gravity, and ladder layer
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
