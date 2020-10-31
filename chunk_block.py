from panda3d.core import *
import time
import array
import World
from config import *

BREAKING_ANIMATION_PATH = []  # TODO: TODO(make and load breaking animation)'''
TEXTURE_ID = []  # TODO: a dictionary of ID to NAME, ID is the index

cube_vert_count = 24  # 6 sides, 8 vertices per side
cube_prim_vert_count = 36  # 6 sides, 6 index rows per side
data_stride = 8  # 3 coordinates + 3 normal components + 2 UVs


class Chunk(World.World):  # TODO: Should be a children of World
    def __init__(self, coordinates, initial_map={}):
        World.World.__init__(self)
        self.coordinates = coordinates
        self.map = initial_map  # key: pos, value: id
        # self.num_ids = len(self.name_map)  # number of textures

        # create chunk model
        model_node = self.__create_model()
        self.model = render.attach_new_node(model_node)
        self.model.set_texture(texture_atlas)
        #self.model.set_scale(0.25,0.25,0.25)
        self.__create_map()

    def __create_model(self):
        vertex_format = GeomVertexFormat.get_v3n3t2()
        vertex_data = GeomVertexData("model_data", vertex_format, Geom.UH_dynamic)
        tris_prim = GeomTriangles(Geom.UH_dynamic)
        tris_prim.set_index_type(Geom.NT_uint32)
        model_geom = Geom(vertex_data)
        model_geom.add_primitive(tris_prim)
        model_node = GeomNode("model")
        model_node.add_geom(model_geom)

        return model_node

    def __create_map(self):
        print('creating_map')
        for (x, y, z), id_ in self.map.items():
            self.add_cube((x * 2, y * 2, z * 2), id_)

    def __modify_model(self):
        model_geom = self.model.node().modify_geom(0)
        model_array = model_geom.modify_vertex_data().modify_array(0)
        model_vert_count = model_array.get_num_rows()

        return model_geom, model_array, model_vert_count

    def add_cube(self, pos, id_):
        model_geom, model_array, model_vert_count = self.__modify_model()

        model_array.set_num_rows(model_vert_count + cube_vert_count)
        model_view = memoryview(model_array).cast("B").cast("f")
        prim_array = model_geom.modify_primitive(0).modify_vertices()
        model_prim_vert_count = prim_array.get_num_rows()
        prim_array.set_num_rows(model_prim_vert_count + cube_prim_vert_count)
        model_prim_view = memoryview(prim_array).cast("B").cast("I")

        cube_node = self.__create_cube(id_)
        cube_geom = cube_node.modify_geom(0)
        vertex_data = cube_geom.modify_vertex_data()
        mat = Mat4.translate_mat(*pos)
        vertex_data.transform_vertices(mat)
        vert_array_data = vertex_data.get_array(0)
        vert_array_view = memoryview(vert_array_data).cast("B").cast("f")
        model_view[model_vert_count * data_stride:] = vert_array_view
        prim = cube_geom.modify_primitive(0)
        offset = cube_vert_count * model_prim_vert_count // cube_prim_vert_count
        prim.offset_vertices(offset, 0, cube_prim_vert_count)
        cube_prim_array = prim.get_vertices()
        cube_prim_view = memoryview(cube_prim_array).cast("B").cast("I")
        model_prim_view[model_prim_vert_count:] = cube_prim_view

    def seperate_remove_cube(self, pos, separate=False):
        index = pos.index(self.map.keys())

        model_geom, model_array, model_vert_count = self.__modify_model()

        model_view = memoryview(model_array).cast("B").cast("f")
        cube_data_size = cube_vert_count * data_stride
        start = index * cube_data_size
        end = start + cube_data_size

        if separate:
            assert pos in self.map, "cannot remove, there's no block at " + str(pos)
            new_block = Block(self.map[pos])
            separated_cube, cube_view, cube_prim_view = new_block.prepare_block()
            cube_view[:] = model_view[start:end]

        model_view[start:-cube_data_size] = model_view[end:]
        model_array.set_num_rows(model_vert_count - cube_vert_count)

        prim = model_geom.modify_primitive(0)
        prim_array = prim.modify_vertices()
        start = index * cube_prim_vert_count
        end = start + cube_prim_vert_count
        model_prim_vert_count = prim_array.get_num_rows()
        prim.offset_vertices(-cube_vert_count, end, model_prim_vert_count)
        model_prim_view = memoryview(prim_array).cast("B").cast("I")

        if separate:
            cube_prim_view[:] = model_prim_view[:cube_prim_vert_count]

        model_prim_view[start:-cube_prim_vert_count] = model_prim_view[end:]
        prim_array.set_num_rows(model_prim_vert_count - cube_prim_vert_count)

    def __create_cube(self, texture_row):
        vertex_count = 0
        values = array.array("f", [])
        indices = array.array("I", [])
        # use an offset along the U-axis to give each side of the cube different
        # texture coordinates, such that each side shows a different part of a
        # texture applied to the cube
        u_offset = 0.

        for direction in (-1, 1):
            for i in range(3):
                normal = VBase3()
                normal[i] = direction
                for a, b in ((-1., -1.), (-1., 1.), (1., 1.), (1., -1.)):
                    pos = Point3()
                    pos[i] = direction
                    pos[(i + direction) % 3] = a
                    pos[(i + direction * 2) % 3] = b
                    u, v = [pos[j] for j in range(3) if j != i]
                    u *= (-1. if i == 1 else 1.) * direction
                    uv = (max(0., u) / 6. + u_offset,
                          max((texture_row - 1) / len(name_map), (v / len(name_map) * texture_row)))

                    values.extend(pos)
                    values.extend(normal)
                    values.extend(uv)

                u_offset += 1. / 6.
                vertex_count += 4

                indices.extend((vertex_count - 2, vertex_count - 3, vertex_count - 4))
                indices.extend((vertex_count - 4, vertex_count - 1, vertex_count - 2))

        vertex_format = GeomVertexFormat.get_v3n3t2()

        vertex_data = GeomVertexData("cube_data", vertex_format, Geom.UH_static)
        vertex_data.unclean_set_num_rows(vertex_count)
        data_array = vertex_data.modify_array(0)
        memview = memoryview(data_array).cast("B").cast("f")
        memview[:] = values

        tris_prim = GeomTriangles(Geom.UH_static)
        tris_prim.set_index_type(Geom.NT_uint32)
        tris_array = tris_prim.modify_vertices()
        tris_array.unclean_set_num_rows(len(indices))
        memview = memoryview(tris_array).cast("B").cast("I")
        memview[:] = indices

        geom = Geom(vertex_data)
        geom.add_primitive(tris_prim)
        node = GeomNode("cube")
        node.add_geom(geom)

        return node


class Block(Chunk):
    def __init__(self, id_):
        Chunk.__init__(self)

        self.name = name_map[id_]
        self.texture_path = texture_path
        self.texture = loader.loadTexture(self.texture_path)
        self.id_ = id_
        self.breaking_animation = []
        for x in BREAKING_ANIMATION_PATH:
            self.breaking_animation.append(loader.loadTexture(x))

        self.breaking_time_table = [-1, 4, 3, 2, 1]  # hand, wood, stone, gold, diamond[time in seconds]

    def prepare_block(self):
        vertex_format = GeomVertexFormat.get_v3n3t2()
        vertex_data = GeomVertexData("cube_data", vertex_format, Geom.UH_static)
        cube_array = vertex_data.modify_array(0)
        cube_array.unclean_set_num_rows(self.cube_vert_count)
        cube_view = memoryview(cube_array).cast("B").cast("f")
        tris_prim = GeomTriangles(Geom.UH_static)
        tris_prim.set_index_type(Geom.NT_uint32)
        cube_geom = Geom(vertex_data)
        cube_geom.add_primitive(tris_prim)
        cube_node = GeomNode("cube")
        cube_node.add_geom(cube_geom)
        separated_cube = self.render.attach_new_node(cube_node)

        separated_cube.set_texture(self.texture)  # not sure if I should add the texture there

        cube_prim_array = tris_prim.modify_vertices()
        cube_prim_array.unclean_set_num_rows(self.cube_prim_vert_count)
        cube_prim_view = memoryview(cube_prim_array).cast("B").cast("I")

        return separated_cube, cube_view, cube_prim_view

    def StartBlockBreaking(self, tool):
        breaking_time = self.breaking_time_table[tool]
        start_time = time.time()
        i = 1
        while '''TODO(add check if still pointing the same block)''':
            if (time.time() - start_time) >= i * breaking_time / 4:
                ts = TextureStage(str(i))
                self
