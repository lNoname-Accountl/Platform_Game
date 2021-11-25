from entity import *
from constant import *

#This method for every enemy in game

#This class for initialize an enemy
class Enemy(Entity):
    def __init__(self, name_folder, name_file):
        #accept filename as an argument to create animation
        super().__init__(name_folder, name_file)

        self.should_update_walk = 0
    
    #The function to update the animation of enemy
    def update_animation(self, delta_time: float = 1 / 60):
        
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        #For loading texture when enemy idle   which their change_x is zero  
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return
            
        #Walking animation of enemy in game that will reset once it reach maximum sprite
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1

#Class for robot enemy to initialize with Enemy Class
class RobotEnemy(Enemy):
    def __init__(self):
        super().__init__("robot", "robot")


#Class for zombie enemy to initialize with Enemy Class        
class ZombieEnemy(Enemy):
    def __init__(self):
        super().__init__("zombie", "zombie")
  
    