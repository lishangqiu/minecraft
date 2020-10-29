from Entities import Entities
from config import *
from direct.task import Task

forward_button = KeyboardButton.ascii_key('w')
backward_button = KeyboardButton.ascii_key('s')
left_button = KeyboardButton.ascii_key('a')
right_button = KeyboardButton.ascii_key('d')


class Player(Entities):
    def __init__(self):
        self.movement_state = 0 # 0: still, 1: walk, 2: jump, 3: sprint
        Entities.__init__(self)
        taskMgr.add(self.movement_task, "MovementTask")
        taskMgr.add(self.follow_player_task,  "FollowPlayerTask")
        taskMgr.add(self.mouse_movement_task, "mouse_movement_task")

    def follow_player_task(self, task):
        position = [self.position[0], self.position[1], self.position[2]+1.5]
        camera.setPos(*position)
        return Task.cont

    def mouse_movement_task(self, task):
        if base.mouseWatcherNode.hasMouse():
            camera.setHpr(-showbase.mouseWatcherNode.getMouseX()*X_degree_per_mouse_moved,  # negative sign is nessasary
                          showbase.mouseWatcherNode.getMouseY()*Y_degree_per_mouse_moved, 0)
            self.direction[0] = showbase.mouseWatcherNode.getMouseX()*X_degree_per_mouse_moved
        return Task.cont

    def movement_task(self, task):

        is_down = showbase.mouseWatcherNode.is_button_down

        new_pos = self.position

        if is_down(left_button):
            direction = self.direction
            direction[0] += 90
            added_pos = self.find_position(self.direction, PLAYER_WALK_SPEED)
            new_pos = [new_pos[0] + added_pos[0], new_pos[1] + added_pos[1],
                       new_pos[2] + added_pos[2]]

        if is_down(right_button):
            direction = self.direction
            direction[0] -= 90
            added_pos = self.find_position(self.direction, PLAYER_WALK_SPEED)
            new_pos = [new_pos[0] + added_pos[0], new_pos[1] + added_pos[1],
                       new_pos[2] + added_pos[2]]

        if is_down(backward_button):
            direction = self.direction
            direction[0] += 180
            added_pos = self.find_position(self.direction, PLAYER_WALK_SPEED)
            new_pos = [new_pos[0] + added_pos[0], new_pos[1] + added_pos[1],
                       new_pos[2] + added_pos[2]]

        if is_down(forward_button):
            added_pos = self.find_position(self.direction, PLAYER_WALK_SPEED)
            new_pos = [new_pos[0] + added_pos[0], new_pos[1] + added_pos[1],
                       new_pos[2] + added_pos[2]]
            print(new_pos)


        self.position = new_pos

        return Task.cont


    #def jump(self):
    #    self.

