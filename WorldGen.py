class WorldGen: #TODO: add more options for world gen
    def __init__(self, world_size):
        self.world_size = world_size

    def create_super_flat(self, *args): # TODO: add more customizable options for super flat
        map_ = {}
        for x in range(-self.world_size//2,(self.world_size//2)+1):
            for y in range(-self.world_size // 2, (self.world_size // 2) + 1):
                map_[(x, y, 0)] = 1
                map_[(x, y, 1)], map_[(x, y, 2)], map_[(x, y, 3)] = 2, 2, 2
                map_[(x, y, 4)] = 3
        return map_
