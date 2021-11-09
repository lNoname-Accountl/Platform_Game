import pathlib
import os

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
LAYER_NAME_GOAL = "Goal"

ASSETS_PATH = pathlib.Path(__file__).resolve().parent / "assets"
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)