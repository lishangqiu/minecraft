
class Player:
    def __init__(self, starting_pos = (0, 0, 0)):
        self.position = starting_pos
        self.state = 0
        self.mo

    def follow_player_task(self, task):
        positions = self.position
        positions[2] = positions[2] + 1.5
        self.camera.setPos(positions)

