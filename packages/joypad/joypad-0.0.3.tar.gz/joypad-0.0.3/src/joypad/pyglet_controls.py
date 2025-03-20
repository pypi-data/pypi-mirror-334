from threading import Thread
import time
import pyglet

from .controller import BaseControls, IController


def register_callbacks(controller: pyglet.input.Control, callbacks: BaseControls, nintendo_mode: bool = False):

        @controller.event
        def on_dpad_motion(controller, vector):
            funs = {
                 (0, 0): callbacks.on_dpad_center,
                 (0, 1): callbacks.on_dpad_up,
                 (-1, 1): callbacks.on_dpad_up_left,
                 (-1, 0): callbacks.on_dpad_left,
                 (-1, -1): callbacks.on_dpad_down_left,
                 (0, -1): callbacks.on_dpad_down,
                 (1, 1): callbacks.on_dpad_down_right,
                 (1, 0): callbacks.on_dpad_right,
                 (1, 1): callbacks.on_dpad_up_right,
            }

        @controller.event
        def on_button_press(controller, button_name):
            funs = {
                 'x' if not nintendo_mode else 'y': callbacks.on_x_button_push,
                 'y' if not nintendo_mode else 'x': callbacks.on_y_button_push,
                 'a' if not nintendo_mode else 'b': callbacks.on_a_button_push,
                 'b' if not nintendo_mode else 'a': callbacks.on_b_button_push,
                 'leftshoulder': callbacks.on_left_shoulder_button_push,
                 'rightshoulder': callbacks.on_right_shoulder_button_push,
                 'leftstick': callbacks.on_left_stick_button_push,
                 'rightstick': callbacks.on_right_stick_button_push,
                 'start': callbacks.on_start_button_push,
                 'back': callbacks.on_back_button_push,
                 'guide': callbacks.on_guide_button_push,
            }
            fun = funs[button_name]
            fun()

        @controller.event
        def on_button_release(controller, button_name):
            funs = {
                 'x' if not nintendo_mode else 'y': callbacks.on_x_button_release,
                 'y' if not nintendo_mode else 'x': callbacks.on_y_button_release,
                 'a' if not nintendo_mode else 'b': callbacks.on_a_button_release,
                 'b' if not nintendo_mode else 'a': callbacks.on_b_button_release,
                 'leftshoulder': callbacks.on_left_shoulder_button_release,
                 'rightshoulder': callbacks.on_right_shoulder_button_release,
                 'leftstick': callbacks.on_left_stick_button_release,
                 'rightstick': callbacks.on_right_stick_button_release,
                 'start': callbacks.on_start_button_release,
                 'back': callbacks.on_back_button_release,
                 'guide': callbacks.on_guide_button_release,
            }
            fun = funs[button_name]
            fun()

        @controller.event
        def on_stick_motion(controller, name, vector):
            funs = {
                 'leftstick': callbacks.on_left_stick_move,
                 'rightstick': callbacks.on_right_stick_move,
            }
            fun = funs[name]
            x, y = round(vector.x, 4), round(vector.y, 4)
            fun(x=x, y=y)

        @controller.event
        def on_trigger_motion(controller, name, value):
            funs = {
                 'lefttrigger': callbacks.on_left_trigger_move,
                 'righttrigger': callbacks.on_right_trigger_move,
            }
            fun = funs[name]
            fun(value=round(value, 4))


    


class PygletController(IController):
    nintendo_mode: bool

    def __init__(self, controller: pyglet.input.Controller):
        self.nintendo_mode = False
        self._controller = controller
        self._controller.open()

    @property
    def name(self) -> str:
        return self._controller.name
    
    def register_callbacks(self, callbacks: BaseControls) -> None:
        register_callbacks(controller=self._controller, callbacks=callbacks, nintendo_mode=self.nintendo_mode)


        
    
class Manager:

    def __init__(self):
        self._thread: Thread = None

    @property
    def controllers(self) -> list[PygletController]:
        controllers = []
        for pyglet_controller in pyglet.input.ControllerManager().get_controllers():
            controllers.append(PygletController(controller=pyglet_controller))
        return controllers

    def listen(self) -> None:
        self._thread = Thread(target=self._collect_controller_events, daemon=True)
        self._thread.start()

    def dispatch_events(self) -> None:
        pyglet.app.platform_event_loop.dispatch_posted_events()  

    def _collect_controller_events(self):
        while True:
            pyglet.clock.tick()           # Allows scheduled events to run
            self.dispatch_events()
            time.sleep(0.002)  # sleep to avoid busy-wait

