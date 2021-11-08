import arcade
import os
import math
import pathlib
from arcade.scene import Scene


#Set The Screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLES = "Platformer"

#Set size of the Character
TILE_SCALING = 0.5
CHARACTER_SCALING = TILE_SCALING * 1.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

#Set movement character speed
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

PLAYER_X = SPRITE_PIXEL_SIZE * TILE_SCALING * 2
PLAYER_Y = SPRITE_PIXEL_SIZE * TILE_SCALING * 1

#Camera tracking player
RIGHT_FACING = 0
LEFT_FACING = 1

LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_MOVING = "Moving Platforms"
LAYER_NAME_LADDERS = "Ladders"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_ENEMIES = "Enemies"

ASSETS_PATH = pathlib.Path(__file__).resolve().parent / "assets"

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
            
class Enemy(Entity):
    def __init__(self, name_folder, name_file):
        
        super().__init__(name_folder, name_file)

        self.should_update_walk = 0
    
    def update_animation(self, delta_time: float = 1 / 60):
        
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        #idle     
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return
            
        #walking animation
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1
    
class RobotEnemy(Enemy):
    def __init__(self):
        super().__init__("robot", "robot")
        
class ZombieEnemy(Enemy):
    def __init__(self):
        super().__init__("zombie", "zombie")
        
class Player(Entity):

    def __init__(self):
        
        super().__init__("male_adventurer","maleAdventurer")

        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False


    def update_animation(self, delta_time: float = 1/60):
        
        #Flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Climbing animation
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
            
        #Jumping animation    
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        #Idle animation            
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        #Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
        
class Platformer(arcade.Window):  
    def __init__(self):
        
        #Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLES)

        #Set the path to start the progoram
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Track current state to see that what key is pressed
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
        
        # Initial level
        self.level = 1

        #Load Sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav") #Coin sound
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav") #Jump Sound
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

        #Set background color
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        
    
    def setup(self):

        #Set up the camera
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        #Set the map 
        map_path = "level1.json"
        map_name = ASSETS_PATH / map_path
        
        #Layer Specific Options for the map
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

        #Load the TileMap
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        #Initiate New Scene
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        #Track Scores
        self.score = 0
        
        #Set up the player
        self.player_sprite = Player()
        self.player_sprite.center_x = PLAYER_X
        self.player_sprite.center_y = PLAYER_Y
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)
        
        #Calculate the right edge of map in pixel
        self.end_of_map = self.tile_map.tiled_map.map_size.width * GRID_PIXEL_SIZE
        
        enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]

        for my_object in enemies_layer:
            cartesian = self.tile_map.get_cartesian(
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
                cartesian[0] * TILE_SCALING * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
            (cartesian[1] + 1.2 )*(self.tile_map.tile_height*TILE_SCALING)
            )
            if "boundary_left" in my_object.properties:
                enemy.boundary_left = my_object.properties["boundary_left"]
            if "boundary_right" in my_object.properties:
                enemy.boundary_right = my_object.properties["boundary_right"]
            if "change_x" in my_object.properties:
                enemy.change_x  = my_object.properties["change_x"]
            self.scene.add_sprite(LAYER_NAME_ENEMIES,enemy)
       
            

        #Set Background Color
        if self.tile_map.tiled_map.background_color:
            arcade.set_background_color(self.tile_map.tiled_map.background_color)

        #Create the 'physics engine'
        
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
        
        #Clear the screen to the background color
        arcade.start_render()

        #Activate game camera
        self.camera.use()

        #Draw our scene
        self.scene.draw()

        #Activate the GUI camera 
        self.gui_camera.use()

        #Draw the score on the screen
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

    def process_keychange(self):
        
        #Process up/down
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
        
        # Process up/down when on a Ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite_y = 0

        #Process Left and Right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        #Called when a key is pressed.
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        self.process_keychange()

    def on_key_release(self, key, modifiers):
        #Called when a key is release
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        self.process_keychange()
            
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
        #Movement and game logic

        #Move player with physic engine
        self.physics_engine.update()

        #Update animation
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
            delta_time, 
            [
                LAYER_NAME_COINS,
                LAYER_NAME_BACKGROUND, 
                LAYER_NAME_PLAYER, 
                LAYER_NAME_ENEMIES,
                ],
        )

        #Update walls, used with moving platforms
        self.scene.update([LAYER_NAME_MOVING, LAYER_NAME_ENEMIES])
        
        #See if the enemy hit a boundary then it reverse
        for enemy in self.scene.get_sprite_list(LAYER_NAME_ENEMIES):
            if(
                enemy.boundary_right
                and enemy.right > enemy.boundary_right
                and enemy.change_x > 0
            ):
                enemy.change_x *= -1
                
            if(
                enemy.boundary_left
                and enemy.left < enemy.boundary_left
                and enemy.change_x < 0
            ):
                enemy.change_x *= -1
                    
        #See if the moving wall hit a boundary and reverse
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
        
        player_collision_list = arcade.check_for_collision_with_lists(
            self.player_sprite, 
            [
                self.scene.get_sprite_list(LAYER_NAME_COINS),
                self.scene.get_sprite_list(LAYER_NAME_ENEMIES),
            ],
        )

        #Loop through each coin character hit and remove coins
        for collision in player_collision_list:

            #Check how many points this is worth
            if self.scene.get_sprite_list(LAYER_NAME_ENEMIES) in collision.sprite_lists:
                arcade.play_sound(self.game_over)
                self.setup()
                return
            else:

                if "Points" not in collision.properties: 
                   print("Warning, collected a coin without a Points property.")
                else:
                    points = int(collision.properties["Points"])
                    self.score += points

                #Remove the coin
                collision.remove_from_sprite_lists()
                arcade.play_sound(self.collect_coin_sound)

        #Position the camera
        self.center_camera_to_player()

def main():
    #Main Function
    
    window = Platformer()
    window.setup()
    arcade.run()
        
if __name__ == "__main__":
    main()     