import arcade
from window_game import ASSET_PATH
from level_one import *

def create_player_sprite(self) -> arcade.AnimatedWalkingSprite:

    path_texture = ASSET_PATH / "images" / "player"

    path_walking = [
        path_texture /
    ]

    path_walking = [
        path_texture /
    ]

    path_climbing = [
        path_texture /
    ]

    path_standing = path_texture /

    texture_walking_right = [
        arcade.load_texture(texture) for texture in path_walking
    ]

    texture_walking_left = [
        arcade.load_texture(texture, mirrored= True) for texture in path_walking
    ]

    texture_climb_up = [
        arcade.load_texture(texture) for texture in path_climbing
    ]

    texture_climb_down = [
        arcade.load_texture(texture) for texture in path_climbing
    ]

    texture_standing_right = [arcade.load_texture(path_standing)]

    texture_standing_left = [arcade.load_texture(path_standing, mirrored= True)]

    player = arcade.AnimatedWalkingSprite()

    player.texture_standing_left = texture_standing_left

    player.texture_standing_right = texture_standing_right

    player.texture_walking_left = texture_walking_left

    player.texture_walking_right = texture_walking_right

    player.texture_climb_up = texture_climb_up

    player.texture_climb_down = texture_climb_down

    player.center_x = PLAYER_START_X
    player.center_y = PLAYER_START_Y
    player.state = arcade.FACE_RIGHT

    player.texture = player.stand_right_textures[0]

    return player

