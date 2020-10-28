from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
loadPrcFileData("editor-startup", "show-frame-rate-meter #t")
loadPrcFileData("editor-startup", "sync-video #f")


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        #global render
        render = self.render

        self.world = self.create_world()

    def create_world(self):
        from World import World

        world = World()
        world.create_world(32)
        return world
app = MyApp()
app.run()


