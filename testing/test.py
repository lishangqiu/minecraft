from panda3d.core import *
from random import randint
from direct.task.Task import Task

loadPrcFileData("editor-startup", "show-frame-rate-meter #t")
loadPrcFileData("editor-startup", "sync-video #f")

from direct.showbase.ShowBase import ShowBase

class MyApp(ShowBase):


    def __init__(self):
        ShowBase.__init__(self)
        
        self.trackball.node().set_pos(0, 30, 0)
        self.trackball.node().set_p(-45)

        # Create
        node = GeomNode('gnode')
        geoms = []
        textures_count = 3

        for i in range(textures_count):
            gvd = GeomVertexData('name', GeomVertexFormat.getV3t2(), Geom.UHStatic)
            geom = Geom(gvd)
            prim = GeomTriangles(Geom.UHStatic)
            vertex = GeomVertexWriter(gvd, 'vertex')
            texcoord = GeomVertexWriter(gvd, 'texcoord')
            tex = loader.loadTexture('%i.png' % (i+1))
            tex.setMagfilter(Texture.FTLinearMipmapLinear)
            tex.setMinfilter(Texture.FTLinearMipmapLinear)
            geoms.append({'geom':geom,
                          'prim':prim,
                          'vertex':vertex,
                          'texcoord':texcoord,
                          'index':0,
                          'gvd':gvd,
                          'texture':tex})

        for x in range(0,100):
            for z in range(0,100):
                t_img = randint(0,textures_count - 1)
                i = geoms[t_img]['index']
                geoms[t_img]['vertex'].addData3f(x, 0, z)
                geoms[t_img]['texcoord'].addData2f(0, 0)
                geoms[t_img]['vertex'].addData3f(x, 0, z+1)
                geoms[t_img]['texcoord'].addData2f(0, 1)
                geoms[t_img]['vertex'].addData3f(x+1, 0, z+1)
                geoms[t_img]['texcoord'].addData2f(1, 1)
                geoms[t_img]['vertex'].addData3f(x+1, 0, z)
                geoms[t_img]['texcoord'].addData2f(1, 0)
                d = i*4
                geoms[t_img]['prim'].addVertices(d, d + 2, d + 1)
                geoms[t_img]['prim'].addVertices(d, d + 3, d + 2)
                geoms[t_img]['index'] += 1

        for i in range(textures_count):
            geoms[i]['prim'].closePrimitive()
            geoms[i]['geom'].addPrimitive(geoms[i]['prim'])
            node.addGeom(geoms[i]['geom'])
            node.setGeomState(i, node.getGeomState(i).addAttrib(TextureAttrib.make(geoms[i]['texture'])))

        terrain = render.attachNewNode(node)
        #terrain.analyze()
        
        del geoms
        
        # Modify
        taskMgr.add(self.animation,'animation')
        
        geom_blue = node.modifyGeom(2)
        self.vdata = geom_blue.modifyVertexData()

    def animation(self, task):

        vertex_blue = GeomVertexRewriter(self.vdata, 'vertex')
        
        vertex_blue.setRow(0)
        v = vertex_blue.getData3f()
        vertex_blue.setData3f(v[0], v[1]-0.1*globalClock.get_dt(), v[2])
        
        vertex_blue.setRow(1)
        v = vertex_blue.getData3f()
        vertex_blue.setData3f(v[0], v[1]-0.1*globalClock.get_dt(), v[2])
        
        vertex_blue.setRow(2)
        v = vertex_blue.getData3f()
        vertex_blue.setData3f(v[0], v[1]-0.1*globalClock.get_dt(), v[2])
        
        vertex_blue.setRow(3)
        v = vertex_blue.getData3f()
        vertex_blue.setData3f(v[0], v[1]-0.1*globalClock.get_dt(), v[2])
        
        return Task.cont

app = MyApp()
app.run()
