import arcade
import pathlib


#Window dimension
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLES = "Platformer"

# Scaling constants
MAP_SCALING = 1.0

#Player constants
GRAVITY = 1.0
PLAYER_START_X = 65
PLAYER_START_Y = 256
PLAYER_SPEED = 10
PLAYER_JUMP = 20


#Window margin
LEFT_MARGIN = 50
RIGHT_MARGIN = 300
TOP_MARGIN = 150
BOT_MARGIN = 150

# Assets path
ASSET_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"

class Platformer(arcade.Window):
    def __init__(self) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLES)
    
        # These lists will hold different sets of sprites
        self.coins = None
        self.background = None
        self.walls = None
        self.ladders = None
        self.goals = None
        self.enemies = None

        # One sprite for the player, no more is needed
        self.player = None

        # We need a physics engine as well
        self.physics_engine = None

        # Someplace to keep score
        self.score = 0

        # Which level are we on?
        self.level = 1

        # Load up our sounds here
        # self.coin_sound = arcade.load_sound(
        #    str(ASSETS_PATH / "sounds" / "coin.wav")
        # )
        # self.jump_sound = arcade.load_sound(
        #    str(ASSETS_PATH / "sounds" / "jump.wav")
        # )
        # self.victory_sound = arcade.load_sound(
        #    str(ASSETS_PATH / "sounds" / "victory.wav")
        # )
    
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

    def create_player_sprite(self) -> arcade.AnimatedWalkingSprite:
    
        path_texture = ASSET_PATH / "images" / "player"

        path_walking = [
        path_texture / f"Run({x}).png" for x in (1, 7)
        ]


        path_climbing = [
            path_texture / f"Climb_00{x}.png" for x in (0, 9)
        ]

        path_standing = path_texture / f"Idle(5).png"

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
    
    def onControl(self, key: int, modifiers: int):
    
        if key in [arcade.key.LEFT, arcade.key.A]:
            self.player.change_x = -PLAYER_SPEED
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.player.change_x = PLAYER_SPEED

        elif key in [arcade.key.UP, arcade.key.W]:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = PLAYER_SPEED
        elif key in [arcade.key.DOWN, arcade.key.S]:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = -PLAYER_SPEED
        elif key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP
                #arcade.play_sound(self.jump_sound) #wait for jump sound effect

    

    def onRelease(self, key: int, modifiers: int) -> None:
        if key in [
            arcade.key.LEFT, 
            arcade.key.A, 
            arcade.key.RIGHT, 
            arcade.key.D,
        ]:
            self.player.change_x = 0

        elif key in [
            arcade.key.UP,
            arcade.key.W,
            arcade.key.DOWN,
            arcade.key.S,
        ]:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = 0

    def onUpdate(self, delta_time: float) -> None:
    
        self.player.update_animation(delta_time)
        self.physics_engine.update()

        if self.player.left < 0:
            self.player.left = 0

        coins_pick = arcade.check_for_collision_with_lists(
            sprite = self.player, sprite_lists= self.coins
        )


        for coin in coins_pick:

            self.score += int(coin.properties["coin_value"])

            #arcade.play_sound(self.coin_sound)

            coin.remove_from_sprite_lists()
        
        in_goal = arcade.check_for_collision_with_lists(
            sprite = self.player, sprite_list = self.goals
        )

        if in_goal:

            #self.victory_sound.play()

            self.level += 1
            self.setup()
        
        self.scroll_view()

    def scroll_view(self) -> None:
    
        left_bound = self.veiw_left + LEFT_MARGIN

        if self.player.left < left_bound:
            self.view_left -= left_bound - self.player.left

            if self.view_left <0:
                self.view_left 

                if self.view_left < 0:
                    self.view_left = 0

        right_bound = self.veiw_right + SCREEN_WIDTH -  RIGHT_MARGIN

        if self.player.right > right_bound:
            self.view_left += self.player.right - right_bound

            if self.view_left > self.map_width - SCREEN_WIDTH:
                self.view_left = self.map_width - SCREEN_WIDTH

        top_bound = self.view_bottom + SCREEN_HEIGHT - TOP_MARGIN
        if self.player.top_bound > top_bound:
            self.view_bottom += self.player.top - top_bound

        bottom_bound = self.view_bottom + BOT_MARGIN
        if self.player.bottom < bottom_bound:
            self.view_bottom -= bottom_bound - self.player.bottom

        self.view_bottom = int(self.view_bottom)
        self.view_left = int(self.view_left)

        arcade.set_viewport(
            left = self.view_left,
            right = SCREEN_WIDTH + self.view_left,
            bottom = self.view_bottom,
            top = SCREEN_HEIGHT + self.view_bottom,
        )

    def onDraw(self) -> None:
        arcade.start_render()

        self.background.draw()  
        self.coins.draw()
        self.walls.draw()
        self.goals.draw()
        self.ladders.draw()
        self.player.draw()
        
        
if __name__ == "__main__":
    window = arcade.Window(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLES)
    platform_view = Platformer()
    platform_view.setup()
    window.show_view(platform_view)
    arcade.run()

        