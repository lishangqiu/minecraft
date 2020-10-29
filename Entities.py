import math
from config import *

class Entities:
    def __init__(self, initial_momentum=[0,0,0], initial_position=[0,0,4],
                 initial_direction=[0,0,0], initial_speed=[0,0,0]):
        self.momentum = initial_momentum
        self.position = initial_position
        self.direction = initial_direction
        self.speed = initial_speed

    def __find_position(self, direction_vector, speed_vector):
        position = [
            ((globalClock.get_dt()*speed_vector[0])*math.sin(math.radians(direction_vector[0]))),
            ((globalClock.get_dt() * speed_vector[0]) * math.sin(math.radians(direction_vector[0]))),
            ((globalClock.get_dt() * speed_vector[0]) * math.sin(math.radians(direction_vector[0])))
        ]
        return position

    #def __find

