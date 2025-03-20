from dataclasses import dataclass
import time
import pyxel

@dataclass
class App:
    x: float = 0
    y: float = 0
    a: bool = False

app = App()

pyxel.init(160, 120, fps=60, quit_key=pyxel.KEY_Q)

norm = 2**15
def update():
    t0 = time.perf_counter()
    app.x = pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX) / norm
    app.y = pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY) / norm
    app.a = pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)
    t1 = time.perf_counter()
    # print(round(t1 - t0, 6))

def draw():
    pyxel.cls(0)
    # print(app)
    pyxel.rect(round(80 + 80*app.x) - 10, round(60 + 60*app.y) - 10, 20, 20, 11)


pyxel.run(update, draw)