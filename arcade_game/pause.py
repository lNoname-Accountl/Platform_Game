from constant import *
import arcade

class Pause(arcade.View):
        def __init__(self, game_view: arcade.View):
            super().__init__()
            self.game_view = game_view

            pause_path = ASSETS_PATH / "title.png"

            self.title = arcade.load_texture(pause_path)

            arcade.draw_texture_rectangle(
              center_x= SCREEN_WIDTH/2,
              center_y = SCREEN_HEIGHT/2,
              width = SCREEN_WIDTH,
              height = SCREEN_HEIGHT,
              texture = self.title,
            )

            arcade.draw_text(
               "Press ESC to continue",
                start_x= 115,
                start_y = 320,
                color = arcade.color.INDIGO,
                font_size = 40,
            )

        def on_key_press(self, key, modifiers):
            if key == arcade.key.ESCAPE:
                self.window.show_view(self.game_view)



            
            