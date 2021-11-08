import arcade
from constant import *
from platformer import Platformer
from title import *

def main():
    window = arcade.Window(
        width = SCREEN_WIDTH,
        height = SCREEN_HEIGHT,
        title = SCREEN_TITLES,
    )
    title_view = Title()
    window.show_view(title_view)
    arcade.run()
    

if __name__ == '__main__':
    main()