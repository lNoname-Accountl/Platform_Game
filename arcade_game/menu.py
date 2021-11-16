import arcade
from constant import *
from platformer import *

background = ASSETS_PATH / "Menu.png"
arrow = ASSETS_PATH / "Arrow2.png"
move_x = [375, 390, 240]
move_y = [330, 250, 178]
i = 0

class MenuStart(arcade.View):    
    def on_draw(self):
        arcade.start_render()
        self.background = arcade.load_texture(background)
        self.arrow = arcade.load_texture(arrow)
        arcade.draw_texture_rectangle(
            center_x= SCREEN_WIDTH/2,
            center_y = SCREEN_HEIGHT/2,
            width = SCREEN_WIDTH,
            height = SCREEN_HEIGHT,
            texture = self.background,
        )
        arcade.draw_texture_rectangle(
            center_x = move_x[i],
            center_y = move_y[i],
            width = 40,
            height = 50,
            texture = self.arrow,
        )
        
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            if move_x[0] == 375 and move_y[0] == 330:
                game_view = Platformer()
                game_view.setup()
                self.window.show_view(game_view)
            elif move_x[1] == 390 and move_y[1] == 250: 
                pass  #select skins
            elif move_x[2] == 240 and move_y[2] == 178:
                raise SystemExit(0)
        '''elif key == arcade.key.W or key == arcade.key.UP:
            i += 1
        elif key == arcade.key.S or key == arcade.key.DOWN:
            i -= 1'''



    
    