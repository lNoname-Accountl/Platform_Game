import arcade
from platformer import *
from constant import *

class Title(arcade.View):
    def __init__(self):
        super().__init__()

        title_path = ASSETS_PATH / "title.png"

        self.title = arcade.load_texture(title_path)
        self.timer = 0
        self.show = False

    def on_update(self, delta_time: float):
        self.timer -= delta_time
        
        if self.timer < 0:
            self.show = not self.show
            self.timer = 1
    
    def on_draw(self):

        arcade.start_render()

        arcade.draw_texture_rectangle(
              center_x= SCREEN_WIDTH/2,
              center_y = SCREEN_HEIGHT/2,
              width = SCREEN_WIDTH,
              height = SCREEN_HEIGHT,
              texture = self.title,
        )

        if self.show:
            arcade.draw_text(
               "Press Enter to Start",
                start_x= 115,
                start_y = 320,
                color = arcade.color.INDIGO,
                font_size = 40,
            )
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.RETURN:
            game_view = Platformer()
            game_view.setup()
            self.window.show_view(game_view)
    




