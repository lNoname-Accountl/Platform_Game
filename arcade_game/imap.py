import arcade
from constant import *

class Map:

    def __init__(self):

        
        map_path = "level1.json"
        map_name = ASSETS_PATH / map_path
        
        self.layer_options ={
            LAYER_NAME_PLATFORMS : {
                "use_spatial_hash" : True,
            },
            LAYER_NAME_COINS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_LADDERS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_MOVING: {
                "use_spatial_hash": True,
            },
        }

        self.map = arcade.load_tilemap(map_name, TILE_SCALING, self.layer_options)

        self.end_map = self.map.tiled_map.map_size.width * GRID_PIXEL_SIZE
    
    def set_background(self):
        if self.map.tiled_map.background_color:
            arcade.set_background_color(self.map.tiled_map.background_color)

    def get_map(self):
        return self.map