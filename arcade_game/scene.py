import math
import arcade
from constant import *
from enemy import *


class Scene():
        def __init__(self):
            self.scene = None

        def addPlayer(self, player):
            self.scene.add_sprite(LAYER_NAME_PLAYER, player)

        def addEnemy(self, gmap):
            enemies_layer = gmap.object_lists[LAYER_NAME_ENEMIES]
            for my_object in enemies_layer:
                cartesian = gmap.get_cartesian(
                    my_object.shape[0], my_object.shape[1]
                )
                print(cartesian)
                enemy_type = my_object.properties["type"]
                if enemy_type == "robot":
                    enemy = RobotEnemy()
                elif  enemy_type == "zombie":
                    enemy = ZombieEnemy()
                else:
                    raise Exception(f"Unknow enemy type {enemy_type}.")
                
                enemy.center_x = math.floor(
                    cartesian[0] * TILE_SCALING * gmap.tile_width
                )
                enemy.center_y = math.floor(
                (cartesian[1] + 1.2 )*(gmap.tile_height*TILE_SCALING)
                )
                if "boundary_left" in my_object.properties:
                    enemy.boundary_left = my_object.properties["boundary_left"]
                if "boundary_right" in my_object.properties:
                    enemy.boundary_right = my_object.properties["boundary_right"]
                if "change_x" in my_object.properties:
                    enemy.change_x  = my_object.properties["change_x"]
                self.scene.add_sprite(LAYER_NAME_ENEMIES,enemy)

        def getScene(self, map):
            return arcade.Scene.from_tilemap(map)
