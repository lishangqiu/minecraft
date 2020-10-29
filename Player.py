from Entities import Entities
from config import *
from direct.task import Task
from math import pi, sin, cos


class Player(Entities):
    def __init__(self):
        Entities.__init__(self)
        taskMgr.add(self.follow_player_task,  "FollowPlayerTask")
        taskMgr.add(self.mouse_movement_task, "mouse_movement_task")

    def follow_player_task(self, task):
        positions = self.position
        positions[2] = positions[2] + 1.5
        return Task.cont

    def mouse_movement_task(self, task):
        if base.mouseWatcherNode.hasMouse():
            camera.setHpr(showbase.mouseWatcherNode.getMouseX()*Y_degree_per_mouse_moved,
                          showbase.mouseWatcherNode.getMouseY()*Z_degree_per_mouse_moved,0)
            self.direction[1] = showbase.mouseWatcherNode.getMouseX()*Y_degree_per_mouse_moved
        return Task.cont
    #def jump(self):
    #    self.

