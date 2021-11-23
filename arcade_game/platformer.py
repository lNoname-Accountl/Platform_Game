import arcade
import math
from constant import *
from enemy import *
from player import *
from imap import *
from scene import *
from physicEngine import *
from camera import *
from gameover import *
from victory import *

class Platformer(arcade.View):  
    def __init__(self):
        
        #Call the parent class and set up the window
        super().__init__()

        #Set the path to start the progoram
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        songpath = ASSETS_PATH / "Summer_Smile.mp3"

        # Track current state to see that what key is pressed
        self.dmap = Map()
        self.dscene = Scene()
        self.dengine = PhysicsEngine()
        self.dcamera = Camera()

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        self.player = None
        
        self.score = 0
        self.timer = 0
        self.show = "00"
        
        # Initial level
        self.level = 1

        #Load Sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav") #Coin sound
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav") #Jump Sound
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.win = arcade.load_sound(":resources:sounds/upgrade5.wav")
        self.song = arcade.load_sound(songpath)

        #Set background color
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        arcade.play_sound(self.song, volume = 0.01, looping = True)  #Playing background music
    
    def setup(self):
        self.score = self.score
        self.timer = 60
        self.player = Player()
        self.dmap.map = self.dmap.get_map()
        self.dcamera.gui_camera = self.dcamera.set_camera()
        self.dcamera.camera = self.dcamera.set_camera()
        self.dscene.scene = self.dscene.getScene(self.dmap.map)
        self.dscene.addPlayer(self.player)
        self.dscene.addEnemy(self.dmap.map)
        self.dmap.set_background()
        self.dengine.startEngine(self.player, self.dscene.scene)
      
    def on_draw(self):
        
        #Clear the screen to the background color
        arcade.start_render()

        #Activate game camera
        self.dcamera.camera.use()

        #Draw our scene
        self.dscene.scene.draw()

        #Activate the GUI camera 
        self.dcamera.gui_camera.use()

        #Draw the score on the screen
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

        arcade.draw_text(
            self.show,
            1100,
            10,
            arcade.csscolor.WHITE,
            18,
        )

    def process_keychange(self):
        
        #Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.dengine.pengine.is_on_ladder():
                self.player.change_y = PLAYER_MOVEMENT_SPEED
            elif (
                self.dengine.pengine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                self.player.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.dengine.pengine.is_on_ladder():
                self.player.change_y = -PLAYER_MOVEMENT_SPEED
        
        # Process up/down when on a Ladder and no movement
        if self.dengine.pengine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player.change_y = 0

        #Process Left and Right
        if self.right_pressed and not self.left_pressed:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player.change_x = 0

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
        screen_center_x = self.player.center_x - (self.dcamera.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (self.dcamera.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.dcamera.camera.move_to(player_centered, 0.2)

    def on_update(self, delta_time):
        #Movement and game logic 

        #Move player with physic engine
        self.dengine.pengine.update()

        self.timer -= delta_time
        second = int(self.timer) % 60
        self.show = f"Time : {second:02d}"
        
            

        #Update animation
        if self.dengine.pengine.can_jump():
            self.player.can_jump = False
        else:                                                                                                             
            self.player.can_jump = True

        if self.dengine.pengine.is_on_ladder() and not self.dengine.pengine.can_jump():
            self.player.is_on_ladder = True
            self.process_keychange()
        else:
            self.player.is_on_ladder = False
            self.process_keychange()

        self.dscene.scene.update_animation(
            delta_time, 
            [
                LAYER_NAME_COINS,
                LAYER_NAME_BACKGROUND, 
                LAYER_NAME_PLAYER, 
                LAYER_NAME_ENEMIES,
                ],
        )

        #Update walls, used with moving platforms
        self.dscene.scene.update([LAYER_NAME_MOVING, LAYER_NAME_ENEMIES])
        
        #See if the enemy hit a boundary then it reverse
        for enemy in self.dscene.scene.get_sprite_list(LAYER_NAME_ENEMIES):
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
        for wall in self.dscene.scene.get_sprite_list(LAYER_NAME_MOVING):
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
            self.player, 
            [
                self.dscene.scene.get_sprite_list(LAYER_NAME_COINS),
                self.dscene.scene.get_sprite_list(LAYER_NAME_ENEMIES),
                self.dscene.scene.get_sprite_list(LAYER_NAME_GOAL),
            ],
        )



        if self.timer < 0:
            self.timer = 0
        if self.player.center_y < -100 or second == 0:
            self.score = 0
            arcade.play_sound(self.game_over)
            gameover = GameOver(self)
            self.window.show_view(gameover)

        #Loop through each coin character hit and remove coins
        for collision in player_collision_list:

            #Check how many points this is worth
            if self.dscene.scene.get_sprite_list(LAYER_NAME_ENEMIES) in collision.sprite_lists:
                self.score = 0
                arcade.play_sound(self.game_over)
                gameover = GameOver(self)
                self.window.show_view(gameover)

            elif self.dscene.scene.get_sprite_list(LAYER_NAME_GOAL) in collision.sprite_lists:
                if self.dmap.level == 5:
                    arcade.play_sound(self.win)
                    victory = Victory(self.score, self)
                    self.window.show_view(victory)
                else:
                    arcade.play_sound(self.win)
                    self.dmap.level+= 1
                    self.setup()
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