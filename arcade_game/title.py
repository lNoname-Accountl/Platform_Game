import arcade
from platformer import *
from constant import *
#Class that is used for title view when player first start the game
class Title(arcade.View):
    def __init__(self):
        super().__init__()

        #Load Title picture
        title_path = ASSETS_PATH / "title.png"

        self.title = arcade.load_texture(title_path)
        self.timer = 0
        self.show = False

    #To update the text on the screen to keep blinking
    def on_update(self, delta_time: float):
        self.timer -= delta_time
        
        if self.timer < 0:
            self.show = not self.show
            self.timer = 1
    
    #To draw a text with imported background image
    def on_draw(self):

        arcade.start_render()

        #For importing title image
        arcade.draw_texture_rectangle(
              center_x= SCREEN_WIDTH/2,
              center_y = SCREEN_HEIGHT/2,
              width = SCREEN_WIDTH,
              height = SCREEN_HEIGHT,
              texture = self.title,
        )
        #To ensure that the message keep blinking
        if self.show:
            arcade.draw_text(
               "Press Enter to Start | ESC to Exit",
                start_x= 115,
                start_y = 320,
                color = arcade.color.INDIGO,
                font_size = 40,
            )
    #When press ENTER it will start the first stage by initiating Platformer class but if press ESC it will exit the game
    def on_key_press(self, key, modifiers):
        if key == arcade.key.RETURN:
            game_view = Platformer()
            game_view.setup()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()     





