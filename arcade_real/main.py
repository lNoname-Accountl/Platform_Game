import arcade
import os
import json
from arcade.scene import Scene

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLES = "Platformer"

TILE_SCALING = 0.5
CHARACTER_SCALING = TILE_SCALING * 1.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

PLAYER_X = SPRITE_PIXEL_SIZE * TILE_SCALING * 2
PLAYER_Y = SPRITE_PIXEL_SIZE * TILE_SCALING * 1

RIGHT_FACING = 0
LEFT_FACING = 1

LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_MOVING = "Moving Platforms"
LAYER_NAME_LADDERS = "Ladders"
LAYER_NAME_PLAYER = "Player"

def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally = True),
    ]

class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()
        
        self.character_face_direction = RIGHT_FACING

        self.cur_texture = 0
        self.scale =  CHARACTER_SCALING
        
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        main_path = ":resources:images/animated_characters/male_adventurer/maleAdventurer"

        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")

        self.walk_textures = []
        for i in range(8):
            texture  = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)
        
        
        
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)

        self.texture = self.idle_texture_pair[0]

        self.hit_box = self.texture.hit_box_points


    def update_animation(self, delta_time: float = 1/60):
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING


        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0

        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return
            
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][
            self.character_face_direction
        ]
class Platformer(arcade.Window):  
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLES)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        self.tile_map = None

        self.scene = None

        self.player_sprite = None

        self.physics_engine = None

        self.camera = None

        self.gui_camera = None
        
        self.score = 0
        
        self.end_of_map = 0
        
        self.level = 1

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav") #Coin sound
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav") #Jump Sound
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        
    
    def setup(self):

        self.camera = arcade.Camera(self.width, self.height)

        self.gui_camera = arcade.Camera(self.width, self.height)

        map_name = f":resources:tiled_maps/map_with_ladders.json"
        
        layer_options ={
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

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.score = 0
        
        self.player_sprite = Player()
        self.player_sprite.center_x = PLAYER_X
        self.player_sprite.center_y = PLAYER_Y
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)
        
        self.end_of_map = self.tile_map.tiled_map.map_size.width * GRID_PIXEL_SIZE

        if self.tile_map.tiled_map.background_color:
            arcade.set_background_color(self.tile_map.tiled_map.background_color)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            [
                self.scene.get_sprite_list(LAYER_NAME_PLATFORMS),
                self.scene.get_sprite_list(LAYER_NAME_MOVING)
            ],
            gravity_constant = GRAVITY,
            ladders = self.scene.get_sprite_list(LAYER_NAME_LADDERS)
        )

    def on_draw(self):
        
        arcade.start_render()

        self.camera.use()

        self.scene.draw()

        self.gui_camera.use()

        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

    def process_keychange(self):
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite_y = 0

        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True


    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
            
    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered, 0.2)

    def on_update(self, delta_time):
        
        self.physics_engine.update()

        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        self.scene.update_animation(
            delta_time, [LAYER_NAME_COINS, LAYER_NAME_BACKGROUND, LAYER_NAME_PLAYER]
        )

        self.scene.update([LAYER_NAME_MOVING])
        
        for wall in self.scene.get_sprite_list(LAYER_NAME_MOVING):
            if (
                wall.boundary_right
                and wall.right > wall.boundary_right
                and wall.change_x > 0
            ):
                wall.change_x *= -1
            if (
                wall.boundary_left
                and wall.left < wall.boundary_left
                and wall.change_x < 0
            ):
                wall.change_x *= -1
            if wall.boundary_top and wall.top > wall.boundary_top and wall.change_y > 0:
                wall.change_y *= -1
            if (
                wall.boundary_bottom
                and wall.bottom < wall.boundary_bottom
                and wall.change_y < 0
            ):
                wall.change_y *= -1    
        
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene.get_sprite_list(LAYER_NAME_COINS)
        )
        
        for coin in coin_hit_list:

            if "Points" not in coin.properties:
                print("Warning, collected a coin without a Points property.")
            else:
                point = int(coin.properties["Points"])
                self.score += point

            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)

        self.center_camera_to_player()

def main():
    window = Platformer()
    window.setup()
    arcade.run()
        
if __name__ == "__main__":
    main()        

