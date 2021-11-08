import arcade
from constant import *

def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally = True),
    ]

class Entity(arcade.Sprite):
        def __init__(self, name_folder, name_file):
            super().__init__()
            
            #Default: Make character face to right
            self.character_face_direction = RIGHT_FACING

            #flipping between image sequences
            self.cur_texture = 0
            self.scale =  CHARACTER_SCALING
            
            # Track our state
            self.jumping = False
            self.climbing = False
            self.is_on_ladder = False

            #Load Character textures
            main_path = f":resources:images/animated_characters/{name_folder}/{name_file}"

            #Character standing textures
            self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
            self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
            self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")
  
            #Character walking textures
            self.walk_textures = []
            for i in range(8):
                texture  = load_texture_pair(f"{main_path}_walk{i}.png")
                self.walk_textures.append(texture)
            
            #Character climbing textures
            self.climbing_textures = []
            texture = arcade.load_texture(f"{main_path}_climb0.png")
            self.climbing_textures.append(texture)
            texture = arcade.load_texture(f"{main_path}_climb1.png")
            self.climbing_textures.append(texture)

            #Set the initial texture
            self.texture = self.idle_texture_pair[0]

            self.hit_box = self.texture.hit_box_points