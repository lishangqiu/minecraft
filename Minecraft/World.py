class World:  # TODO: create MyApp which includes 2d UIs
    def __init__(self):
        self.world_block_map = {}  # key: coordinate, value: chunk map
        self.entity_map = []
        self.name_map = {0: 'bedrock', 1: 'stone', 2: 'grass'}
        self.texture_atlas_path = './testing/test_texture2.png'  # TODO: texture_atlas
        self.texture_atlas = loader.loadTexture(self.texture_atlas_path)

    def __assure_world_size(self, world_size):  # TODO: add in more chunks if world size not multiple of 16

        return world_size

    # TODO: add in boarder

    def __get_chunk_pos(self, x, y):
        return x // 16, y // 16

    def __split_chunks(self, map_):
        new_map = {}
        for (x, y, z), id_ in map_.items():
            chunk_pos = x // 16, y // 16
            if chunk_pos not in new_map:
                new_map[chunk_pos] = {(x, y, z): id_}
            else:
                new_map[chunk_pos][(x, y, z)] = id_
        return new_map

    def create_world(self, world_size=128, option=0, *args):
        import chunk_block
        from WorldGen import WorldGen
        generation = WorldGen(self.__assure_world_size(world_size))
        if option == 0:
            created_map = self.__split_chunks(generation.create_super_flat())
            for pos, map_ in created_map.items():
                self.world_block_map[pos] = chunk_block.Chunk(pos, map_)
        return
