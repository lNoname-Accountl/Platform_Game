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
