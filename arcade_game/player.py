from entity import *
 

class Player(Entity):

    def __init__(self):
        
        super().__init__("male_adventurer","maleAdventurer")

        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.center_x = PLAYER_X
        self.center_y = PLAYER_Y


    def update_animation(self, delta_time: float = 1/60):
        
        #Flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Climbing animation
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return
            
        #Jumping animation    
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        #Idle animation            
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        #Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
        