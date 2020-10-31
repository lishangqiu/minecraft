from config import *

class HotBar:
    def __init__(self):
        self.current_selected = 1 # 1-9
        self.keybinds = []
        for x in range(1,10):
            self.keybinds.append(KeyboardButton.ascii_key(str(x)))
        self.items = []
        taskMgr.add(self.selection_task, "SelectionTask")

    def selection_task(self, task):
        is_down = showbase.mouseWatcherNode.is_button_down

        for x in range(1,10):
            if is_down(self.keybinds[x-1]):
                if self.current_selected!=x:
                    taskMgr.add(self.update_task, "UpdateTask", x)
                return Task.cont
        return Task.cont


