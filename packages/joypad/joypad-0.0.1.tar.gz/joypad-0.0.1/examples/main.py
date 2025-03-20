import time
from joypad import BaseControllerCallbacks, PygletControllerManager

# Create Custom Controls by inheriting from BaseControllerCallbacks
class Controls(BaseControllerCallbacks):

    def __init__(self, name = ""):
        self.name = name
    
    def on_a_button_push(self):
        print(f'{self.name} Pressed A.')

    def on_left_stick_move(self, x, y):
        print(f'{self.name} Moved Left Stick:', x, y)

    def on_right_trigger_move(self, value):
        print(f'{self.name} Pulled Right Trigger to Level {value}')



# Register Controllers and Custom Controls
controller_manager = PygletControllerManager()
controller_manager.listen()  # start controller event detection loop on a seperate thread.

controllers = controller_manager.get_controllers()
print(f'Detected {len(controllers)} controller{'s' if len(controllers) > 1 else ''}.')
for idx, controller in enumerate(controllers, start=1):
    controller.register_callbacks(Controls(f'Player {idx}'))


# Start Application Loop
while True:
    time.sleep(1)
