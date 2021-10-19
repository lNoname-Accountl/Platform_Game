import arcade
import pathlib
from window_game import *
from player import *

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
