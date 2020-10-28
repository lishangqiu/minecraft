from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
import array
import random

loadPrcFileData("editor-startup", "show-frame-rate-meter #t")
loadPrcFileData("editor-startup", "sync-video #f")


def create_cube():

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
                print(v)
                uv = (max(0., u) / 6. + u_offset, max(0.5, v))

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


class MyApp(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        # set up a light source
        p_light = PointLight("point_light")
        p_light.set_color((1., 1., 1., 1.))
        self.light = self.camera.attach_new_node(p_light)
        self.light.set_pos(5., -100., 7.)
        self.render.set_light(self.light)

        # create an initially empty model parented to the scene root
        vertex_format = GeomVertexFormat.get_v3n3t2()
        vertex_data = GeomVertexData("model_data", vertex_format, Geom.UH_dynamic)
        tris_prim = GeomTriangles(Geom.UH_dynamic)
        # allow adding more than 65536 vertices
        tris_prim.set_index_type(Geom.NT_uint32)
        model_geom = Geom(vertex_data)
        model_geom.add_primitive(tris_prim)
        model_node = GeomNode("model")
        model_node.add_geom(model_geom)
        self.model = self.render.attach_new_node(model_node)
        self.model.set_texture(loader.loadTexture('./test_texture2.png'))
        
        # the number of vertices in each cube
        self.cube_vert_count = 24  # 6 sides, 8 vertices per side

        # the number of vertex indices in the GeomTriangles primitive of each cube
        self.cube_prim_vert_count = 36  # 6 sides, 6 index rows per side

        # the number of float values used for the data of a single vertex
        self.data_stride = 8  # 3 coordinates + 3 normal components + 2 UVs

        # define the possible positions for the cubes
        # (they form a pyramid shape in this example)
        self.positions = positions = []
        for i in range(-2, 3):
            pos = (i * 2, -4, 0)
            positions.append(pos)
        for i in range(-2, 3):
            pos = (i * 2, 4, 0)
            positions.append(pos)
        for i in range(-1, 2):
            pos = (-4, i * 2, 0)
            positions.append(pos)
        for i in range(-1, 2):
            pos = (4, i * 2, 0)
            positions.append(pos)
        for i in range(-1, 2):
            pos = (i * 2, -2, 2)
            positions.append(pos)
        for i in range(-1, 2):
            pos = (i * 2, 2, 2)
            positions.append(pos)
        positions.append((-2, 0, 2))
        positions.append((2, 0, 2))
        positions.append((0, 0, 4))
        # keep track of which positions are currently occupied
        self.free_positions = list(range(len(positions)))
        self.used_positions = []

        # the cubes that have been separated and are falling down
        self.falling_cubes = []

        # start a task that makes separated cubes fall down
        self.task_mgr.add(self.__drop_cubes, "drop_cubes")

        # enable randomly adding and removing cubes at runtime
        self.add_cube((0, 0, 1))
        self.add_cube((0, 2, 1))
        #self.add_cube((1, 0, 1))
        #self.add_cube((1, 1, 1))

        #self.add_cube((0, 0, 2))
        #self.add_cube((0, 1, 2))
        #self.add_cube((1, 0, 2))
        #self.add_cube((1, 1, 2))

        self.accept("a", self.__add_random_cube)
        self.accept("b", self.__remove_random_cube)
        create_cube()

    def add_cube(self, pos):

        model_geom = self.model.node().modify_geom(0)
        model_array = model_geom.modify_vertex_data().modify_array(0)
        model_vert_count = model_array.get_num_rows()
        model_array.set_num_rows(model_vert_count + self.cube_vert_count)
        model_view = memoryview(model_array).cast("B").cast("f")
        prim_array = model_geom.modify_primitive(0).modify_vertices()
        model_prim_vert_count = prim_array.get_num_rows()
        prim_array.set_num_rows(model_prim_vert_count + self.cube_prim_vert_count)
        model_prim_view = memoryview(prim_array).cast("B").cast("I")

        cube_node = create_cube()
        cube_geom = cube_node.modify_geom(0)
        vertex_data = cube_geom.modify_vertex_data()
        mat = Mat4.translate_mat(*pos)
        vertex_data.transform_vertices(mat)
        vert_array_data = vertex_data.get_array(0)
        vert_array_view = memoryview(vert_array_data).cast("B").cast("f")
        model_view[model_vert_count * self.data_stride:] = vert_array_view
        prim = cube_geom.modify_primitive(0)
        offset = self.cube_vert_count * model_prim_vert_count // self.cube_prim_vert_count
        prim.offset_vertices(offset, 0, self.cube_prim_vert_count)
        cube_prim_array = prim.get_vertices()
        cube_prim_view = memoryview(cube_prim_array).cast("B").cast("I")
        model_prim_view[model_prim_vert_count:] = cube_prim_view

    def prepare_separated_cube(self):

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

        # give the separated cube a red color to easily identify it as a
        # falling cube
        separated_cube.set_color(1., 0., 0.)

        cube_prim_array = tris_prim.modify_vertices()
        # the call to `GeomPrimitive.unclean_set_num_rows` fills the primitive
        # with random integers, which will cause an AssertionError when an
        # integer bigger than the number of vertex data rows is encountered
        # while adding the primitive to the geometry, so only call this method
        # after the primitive, its geom and its node have been added to the
        # scenegraph
        cube_prim_array.unclean_set_num_rows(self.cube_prim_vert_count)
        cube_prim_view = memoryview(cube_prim_array).cast("B").cast("I")

        # the separated cube will start to fall
        self.falling_cubes.append(separated_cube)

        # return the created memoryviews for further manipulation
        return cube_view, cube_prim_view

    def remove_cube(self, index, separate=True):

        model_geom = self.model.node().modify_geom(0)
        model_array = model_geom.modify_vertex_data().modify_array(0)
        model_vert_count = model_array.get_num_rows()
        model_view = memoryview(model_array).cast("B").cast("f")
        cube_data_size = self.cube_vert_count * self.data_stride
        start = index * cube_data_size
        end = start + cube_data_size

        if separate:
            cube_view, cube_prim_view = self.prepare_separated_cube()
            cube_view[:] = model_view[start:end]

        model_view[start:-cube_data_size] = model_view[end:]
        model_array.set_num_rows(model_vert_count - self.cube_vert_count)

        prim = model_geom.modify_primitive(0)
        prim_array = prim.modify_vertices()
        start = index * self.cube_prim_vert_count
        end = start + self.cube_prim_vert_count
        model_prim_vert_count = prim_array.get_num_rows()
        prim.offset_vertices(-self.cube_vert_count, end, model_prim_vert_count)
        model_prim_view = memoryview(prim_array).cast("B").cast("I")

        if separate:
            cube_prim_view[:] = model_prim_view[:self.cube_prim_vert_count]

        model_prim_view[start:-self.cube_prim_vert_count] = model_prim_view[end:]
        prim_array.set_num_rows(model_prim_vert_count - self.cube_prim_vert_count)

    def __add_random_cube(self):
        print('adding')

        if not self.free_positions:
            return

        index = random.choice(self.free_positions)
        pos = self.positions[index]
        self.free_positions.remove(index)
        self.used_positions.append(index)
        self.add_cube(pos)

    def __remove_random_cube(self):

        if not self.used_positions:
            return

        index = random.randint(0, len(self.used_positions) - 1)
        self.remove_cube(index)
        pos_index = self.used_positions[index]
        self.used_positions.remove(pos_index)
        self.free_positions.append(pos_index)

    def __drop_cubes(self, task):

        for cube in self.falling_cubes[:]:
                
            z = cube.get_z()

            if z < -10.:
                self.falling_cubes.remove(cube)
                cube.detach_node()
            else:
                cube.set_z(z - .1)

        return task.cont


app = MyApp()
app.run()
