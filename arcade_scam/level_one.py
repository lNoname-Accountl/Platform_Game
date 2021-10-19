import arcade
import pathlib
from window_game import *



def setup(self) -> None:
    """For setting up Level"""
    n_map = f"platform_level_{self.level:01}.tmx"
    path_map = ASSET_PATH / n_map
    
    layer_wall = "ground"
    layer_coin = "coins"
    layer_goal = "goal"
    layer_background = "background"

#Load the current map
    game_map = arcade.tilemap.read_tmx(str(path_map))

#Load the layers
    self.background = arcade.tilemap.process_layer(
        game_map, layer_name = layer_background, scaling = MAP_SCALING
    )
    self.goals = arcade.tilemap.process_layer(
        game_map, layer_name = layer_goal, scaling = MAP_SCALING
    )
    self.walls = arcade.tilemap.process_layer(
        game_map, layer_name = layer_wall, scaling = MAP_SCALING
    )
    self.coins = arcade.tilemap.process_layer(
        game_map, layer_name = layer_coin, scaling = MAP_SCALING
    )

#Set the Background color
    background_color = arcade.color.FRESH_AIR
    if game_map.background_color:
        background_color = game_map.background_color
    arcade.set_background_color(background_color)


    self.map_width = (
        game_map.map_size.width-1
    )* game_map.tile_size.width

#Create the player sprite if they're not already set up
    if not self.player:
        self.player = self.create_player_sprite()

#Move the player sprite back to the beginning
    self.player.center_x = PLAYER_START_X
    self.player.center_y = PLAYER_START_Y
    self.player.change_x = 0
    self.player.change_y = 0

#Reset window
    self.view_left = 0
    self.view_right = 0

#Load the physics engine for this map
    self.physics_engine = arcade.PhysicsEnginePlatformer(
        player_sprite = self.player,
        platforms = self.walls,
        gravity_constant= GRAVITY,
        ladders = self.ladders
    )