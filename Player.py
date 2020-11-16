from Entities import Entities
from config import *
from direct.task import Task
import math
import copy

forward_button = KeyboardButton.ascii_key('w')
backward_button = KeyboardButton.ascii_key('s')
left_button = KeyboardButton.ascii_key('a')
right_button = KeyboardButton.ascii_key('d')


def get_possible_cubes(directions, pos):
    offsets = list(map(lambda i: i - int(i), pos))

    possible_pos = []
    for x in range(1, 6):
        for y in range(1, 6):
            for z in range(1, 6):
                possible_pos.append([x + 0.5, y + 0.5, z + 0.5])

    if 0 < directions[0] < 90:
        pass
    elif 90 < directions[0] < 180:
        for x in range(len(possible_pos)):
            possible_pos[x][1] *= -1
    elif 180 < directions[0] < 270:
        for x in range(len(possible_pos)):
            possible_pos[x][0] *= -1
            possible_pos[x][1] *= -1
    elif 270 < directions[0]:
        for x in range(len(possible_pos)):
            possible_pos[x][0] *= -1
    else:
        print(directions)

    if directions[1] <= 0:
        for x in range(len(possible_pos)):
            possible_pos[x][2] *= -1

    for x in range(len(possible_pos)):
        possible_pos = map(lambda i, j: i - j, possible_pos[x], offsets)

    return possible_pos


def get_left_right(directions, possible_pos):
    possible_y = sorted(list(set(list(map(lambda i: i[1], possible_pos)))))  # all y offsets to the player(select all
    # the unique y offsets from possible_pos variable

    possible_pos2 = []
    distances = []
    for adjacent in possible_y:
        # finding the x/y coordinate of the selected block
        # a right triangle with y offset as adjacent, x offset as opposite and distance to player as hypotenuse
        opposite = adjacent * math.tan(math.radians(directions[0]))  # x offset
        hypotenuse = opposite / math.sin(math.radians(directions[0]))  # distance to player on 2d x/y plane
        # finding the z coordinate of the selected block
        # using previous hypotenuse(parameter "hypotenuse" in this section) as the adjacent
        # z offset as opposite, hypotenuse as the distance to the block
        opposite2 = hypotenuse * math.tan(math.radians(directions[1]))  # z offset to the player
        hypotenuse2 = hypotenuse / math.cos(math.radians(directions[1]))  # distance to player on 3d

        pos = [opposite, possible_y, opposite2]  # x, y, z

        if pos in possible_pos:
            possible_pos2.append(pos)
            distances.append(hypotenuse2)

    smallest_index = distances.index(min(distances))

    return possible_pos2[smallest_index] + [distances[smallest_index]]


class Player(Entities):
    def __init__(self, initial_momentum=[0, 0, 0], initial_position=[0, 0, 11],
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
                          max(min(showbase.mouseWatcherNode.getMouseY() * Y_degree_per_mouse_moved, 90), -90), 0)

            self.direction = [showbase.mouseWatcherNode.getMouseX() * X_degree_per_mouse_moved,
                              max(min(showbase.mouseWatcherNode.getMouseY() * Y_degree_per_mouse_moved, 90), -90), 0]
        return Task.cont

    def movement_task(self, task):
        is_down = showbase.mouseWatcherNode.is_button_down
        direction_dict = {'w': 0, 'a': 270, 'd': 90, 's': 180,
                          'aw': -45, 'dw': 45, 'as': 225, 'ds': 135}
        buttons_pressed = ''
        if is_down(left_button):
            buttons_pressed += 'a'
        if is_down(right_button):
            buttons_pressed += 'd'
        if is_down(backward_button):
            buttons_pressed += 's'
        if is_down(forward_button):
            buttons_pressed += 'w'
        buttons_pressed = ''.join(sorted(buttons_pressed))

        if buttons_pressed not in direction_dict:
            return Task.cont
        directions = copy.copy(self.direction)
        new_pos = copy.copy(self.position)
        directions[0] = (directions[0] + direction_dict[buttons_pressed])
        added_pos = self.find_position(directions, PLAYER_WALK_SPEED)
        new_pos = [new_pos[0] + added_pos[0], new_pos[1] + added_pos[1],
                   new_pos[2] + added_pos[2]]

        self.position = new_pos

        return Task.cont

    # def jump(self):
    #    self.
