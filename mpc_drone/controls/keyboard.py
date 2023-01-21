from pynput import keyboard

class droneControl:
    def __init__(self) -> None:
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def on_press(self,key):
        global control_input
        try:
            if key.char == '+':
                control_input[3] += 0.1
            elif key.char == '-':
                control_input[3] -= 0.1
        except AttributeError:
            pass
        
