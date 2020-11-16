class WorldGen:  # TODO: add more options for world gen
    def __init__(self, world_size):
        self.world_size = world_size

    def create_super_flat(self, *args):  # TODO: add more customizable options for super flat
        map_ = {}
        for x in range(-self.world_size // 2, (self.world_size // 2) + 1):
            for y in range(-self.world_size // 2, (self.world_size // 2) + 1):
                map_[(x + 0.5, y + 0.5, 0.5)] = 1
                map_[(x + 0.5, y + 0.5, 1.5)], map_[(x + 0.5, y + 0.5, 2.5)], map_[(x + 0.5, y + 0.5, 3.5)] = 2, 2, 2
                map_[(x + 0.5, y + 0.5, 4.5)] = 3
        return map_
