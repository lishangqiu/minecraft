from Entities import Entities
from config import *
from direct.task import Task
import numpy as np
import copy

forward_button = KeyboardButton.ascii_key('w')
backward_button = KeyboardButton.ascii_key('s')
left_button = KeyboardButton.ascii_key('a')
right_button = KeyboardButton.ascii_key('d')


class Player(Entities):
    def __init__(self, initial_momentum=[0, 0, 0], initial_position=[0, 0, 10.5],
                 initial_direction=[0, 0, 0], initial_speed=[0, 0, 0]):

        Entities.__init__(self, initial_momentum, initial_position, initial_direction, initial_speed)
        self.movement_state = 0  # 0: still, 1: walk, 2: jump, 3: sprint
        taskMgr.add(self.movement_task, "MovementTask")
        taskMgr.add(self.follow_player_task, "FollowPlayerTask")
        taskMgr.add(self.mouse_movement_task, "mouse_movement_task")

    def follow_player_task(self, task):
        position = [self.position[0], self.position[1], self.position[2] + 1.5]
        camera.setPos(*position)
        return Task.cont

    def mouse_movement_task(self, task):
        if base.mouseWatcherNode.hasMouse():
            camera.setHpr(-showbase.mouseWatcherNode.getMouseX() * X_degree_per_mouse_moved,
                          # negative sign is nessasary
                          showbase.mouseWatcherNode.getMouseY() * Y_degree_per_mouse_moved, 0)
            self.direction[0] = showbase.mouseWatcherNode.getMouseX() * X_degree_per_mouse_moved
        return Task.cont

    def movement_task(self, task):
        is_down = showbase.mouseWatcherNode.is_button_down
        direction_dict = {'w': 0, 'a': -90, 'd': 90, 's': 180,
                          'aw': -45, 'dw': 45, 'as': 225, 'ds': 135}
        buttons_pressed = ''
        if is_down(left_button):
            buttons_pressed += 'a'
        if is_down(right_button):
            buttons_pressed += 'd'
        if is_down(backward_button):
            buttons_pressed += 'a'
        if is_down(forward_button):
            buttons_pressed += 'w'
        buttons_pressed = ''.join(sorted(buttons_pressed))

        if buttons_pressed not in direction_dict:
            return Task.cont

        directions = copy.copy(self.direction)
        new_pos = copy.copy(self.position)

        directions[0] += direction_dict[buttons_pressed]
        added_pos = self.find_position(directions, PLAYER_WALK_SPEED)
        new_pos = [new_pos[0] + added_pos[0], new_pos[1] + added_pos[1],
                   new_pos[2] + added_pos[2]]

        self.position = new_pos

        return Task.cont

    # def jump(self):
    #    self.
