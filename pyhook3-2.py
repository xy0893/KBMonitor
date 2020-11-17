import pythoncom
import PyHook3
from pynput.keyboard import Controller
import time
from threading import Lock, Thread
import random

lock = Lock()
abilities = set()
hot_keys = {
    'F1': 'q',
    'F2': 'w',
    'F3': 'e',
    'F4': 'r'
}
keyboard = Controller()


def cast_ability():
    while True:
        time.sleep(0.001)
        bak = list(abilities)
        random.shuffle(bak)
        for ability in bak:
            time.sleep(random.uniform(0.05, 0.1))
            keyboard.press(ability)
            keyboard.release(ability)


def toggle_ability_status(event):
    key = event.Key
    if key in hot_keys:
        print(key)
        ability = hot_keys[key]
        with lock:
            if ability in abilities:
                abilities.remove(ability)
            else:
                abilities.add(ability)
    return True


hm = PyHook3.HookManager()
hm.KeyDown = toggle_ability_status
hm.HookKeyboard()
Thread(target=cast_ability).start()
pythoncom.PumpMessages()
