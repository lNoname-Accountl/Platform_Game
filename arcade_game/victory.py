import arcade
from constant import *

class Victory(arcade.View):
    def __init__(self, score, game_view: arcade.View):
        super().__init__()

        victory_path = ASSETS_PATH / "victory.png"

        self.victory = arcade.load_texture(victory_path)
        self.timer = 0
        self.show = False
        self.game_view = game_view
        self.score = score

        
    
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
              texture = self.victory,
        )

        score_text = f"Your score: {self.score}"
        arcade.draw_text(
            score_text,
            start_x= 450,
            start_y = 100,
            color = arcade.color.BLACK,
            font_size = 40,
        )
            
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()