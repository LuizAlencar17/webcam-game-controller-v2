from pynput.keyboard import Controller


class KeyboardController:
    """
    A controller for simulating keyboard key presses and releases using pynput.
    """

    def __init__(self):
        """
        Initializes the KeyboardController with a pynput keyboard Controller instance.
        """
        self.keyboard = Controller()

    def press(self, key):
        """
        Presses the specified key.

        Args:
            key (str): The key to press.
        """
        self.keyboard.press(key)

    def release(self, key):
        """
        Releases the specified key.

        Args:
            key (str): The key to release.
        """
        self.keyboard.release(key)
