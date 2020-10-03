from pynput import keyboard

# Keys currently pressed
current = set()

hotkeys = [
    {keyboard.Key.ctrl, keyboard.KeyCode(char='`')}
]

def on_press(key):
    if any([key in hotkey for hotkey in hotkeys]):
        current.add(key)
        if any(all(k in current for k in hotkey) for hotkey in hotkeys):
            execute()

def on_release(key):
    if any([key in hotkey for hotkey in hotkeys]):
        current.remove(key)

def execute():
    print("Taking screenshot")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


