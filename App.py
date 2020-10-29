from config import *
from World import World
from Player import Player
from pandac.PandaModules import WindowProperties
import sys

loadPrcFileData("editor-startup", "show-frame-rate-meter #t")
loadPrcFileData("editor-startup", "sync-video #f")

props = WindowProperties()
base.disableMouse()
class MyApp:
    def __init__(self):
        self.world = self.create_world()
        showbase.accept('q', self.quit_game)

    def create_world(self):
        world = World()
        world.create_world(8)
        camera.setPos(0, 0, 10)
        player = Player()
        return world

    def mouse_relative_mode(self, on=True):
        props.setCursorHidden(on)
        props.setMouseMode(WindowProperties.M_relative)
        showbase.win.requestProperties(props)
        return

    def quit_game(self):
        #showbase.destroy()
        #fagsagbhhf
        base.enableMouse()


app = MyApp()
app.mouse_relative_mode()
showbase.run()


