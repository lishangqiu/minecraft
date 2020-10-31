from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

# Important Stuff
showbase = ShowBase()
render = showbase.render
globalClock = globalClock

# Blocks
name_map = {1: 'bedrock', 2: 'stone', 3: 'grass'}
texture_atlas_path = './testing/test_texture3.png'  # TODO: texture_atlas
texture_atlas = loader.loadTexture(texture_atlas_path)

# Player/Controls
PLAYER_WALK_SPEED = 4
X_degree_per_mouse_moved = 40
Y_degree_per_mouse_moved = 40