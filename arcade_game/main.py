import arcade
from platformer import Platformer

def main():
    platformer = Platformer()
    
    platformer.setup()
    arcade.run()

if __name__ == '__main__':
    main()