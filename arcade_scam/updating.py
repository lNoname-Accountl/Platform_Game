import arcade
import pathlib
from window_game import *


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

        arcade.play_sound(self.coin_sound)

        coin.remove_from_sprite_lists()
    
    in_goal = arcade.check_for_collision_with_lists(
        sprite = self.player, sprite_list = self.goals
    )

    if in_goal:

        self.victory_sound.play()

        self.level += 1
        self.setup()

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
    if key in [arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D,]:
        self.player.change_x = 0

    elif key in [
        arcade.key.UP,
        arcade.key.W,
        arcade.key.DOWN,
        arcade.key.S,
    ]:
        if self.physics_engine.is_on_ladder():
            self.player.change_y = 0