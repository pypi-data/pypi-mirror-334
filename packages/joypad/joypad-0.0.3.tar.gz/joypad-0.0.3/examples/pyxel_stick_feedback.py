import pyxel
import joypad


class Controls(joypad.BaseControls):
    
    def on_a_button_push(self):
        pyxel.cls(0)

    def on_b_button_push(self):
        pyxel.rect(10, 10, 20, 20, 11)


manager = joypad.Manager()
for controller in manager.controllers:
    print(controller.name)
    controller.nintendo_mode = True
    controller.register_callbacks(Controls())


pyxel.init(160, 120)

def update():
    manager.dispatch_events()
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    ...
    # pyxel.cls(0)
    pyxel.rect(40, 50, 20, 20, 11)


pyxel.run(update, draw)