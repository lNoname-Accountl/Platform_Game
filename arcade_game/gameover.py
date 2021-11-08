import arcade
from constant import *

class GameOver(arcade.View):
    def __init__(self, game_view: arcade.View):
        super().__init__()

        over_path = ASSETS_PATH / "gameover.png"

        self.over = arcade.load_texture(over_path)
        self.timer = 0
        self.show = False
        self.game_view = game_view

        
    
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
              texture = self.over,
        )

        if self.show:
            arcade.draw_text(
               "Press Enter to Play again",
                start_x= 340,
                start_y = 220,
                color = arcade.color.WHITE,
                font_size = 40,
            )
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.RETURN:
            self.game_view.setup()
            self.window.show_view(self.game_view)





        