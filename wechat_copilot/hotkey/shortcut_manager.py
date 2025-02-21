from pynput import keyboard
import asyncio


class ShortcutManager:
    def __init__(self, callback):
        self.callback = callback
        self.shortcut = None
        self.is_running = False
        self.listener = None
        self.pressed_keys = set()

    def register_shortcut(self, key_combination):
        """Register global shortcut"""
        # Parse shortcut string like "cmd+shift+space"
        keys = key_combination.split("+")
        self.shortcut = {
            "cmd": keyboard.Key.cmd,
            "shift": keyboard.Key.shift,
            "key": keys[-1].upper(),
        }

        # Create keyboard listener
        self.listener = keyboard.Listener(
            on_press=self._on_press, on_release=self._on_release
        )

    def _on_press(self, key):
        """Handle key press"""
        try:
            if not self.is_running:
                return

            # Add key to pressed keys
            self.pressed_keys.add(key)

            # Convert key to string representation
            key_str = (
                key.char.upper() if hasattr(key, "char") else str(key.name).upper()
            )

            # Check if shortcut combination is pressed
            if (
                key_str == self.shortcut["key"]
                and self.shortcut["cmd"] in self.pressed_keys
                and self.shortcut["shift"] in self.pressed_keys
            ):
                print("handle shortcut")
                self.callback()
        except Exception as e:
            print(f"Error handling keypress: {e}")

    def _on_release(self, key):
        """Handle key release"""
        try:
            self.pressed_keys.discard(key)
        except:
            pass

    def start(self):
        """Start listening for shortcuts"""
        self.is_running = True
        if self.listener:
            self.listener.start()

    def stop(self):
        """Stop listening for shortcuts"""
        self.is_running = False
        if self.listener:
            self.listener.stop()
