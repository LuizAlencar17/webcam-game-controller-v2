from pynput.keyboard import Controller

class KeyboardController:
    def __init__(self):
        self.keyboard = Controller()
    def press(self, key):
        self.keyboard.press(key)
    def release(self, key):
        self.keyboard.release(key)
