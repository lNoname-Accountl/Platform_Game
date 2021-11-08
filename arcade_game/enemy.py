from entity import *
from constant import *

class Enemy(Entity):
    def __init__(self, name_folder, name_file):
        
        super().__init__(name_folder, name_file)

        self.should_update_walk = 0
    
    def update_animation(self, delta_time: float = 1 / 60):
        
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        #idle     
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return
            
        #walking animation
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1
    
class RobotEnemy(Enemy):
    def __init__(self):
        super().__init__("robot", "robot")
        
class ZombieEnemy(Enemy):
    def __init__(self):
        super().__init__("zombie", "zombie")
  
    