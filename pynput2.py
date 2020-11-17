from pynput.keyboard import Key, Listener, Controller
import time
from threading import Lock, Thread
import random

lock = Lock()
abilities = set()
hot_keys = {
    Key.f1: 'q',
    Key.f2: 'w',
    Key.f3: 'e',
    Key.f4: 'r'
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


def toggle_ability_status(key):
    if key in hot_keys:
        ability = hot_keys[key]
        with lock:
            if ability in abilities:
                abilities.remove(ability)
            else:
                abilities.add(ability)


threads = [Thread(target=cast_ability), Listener(on_press=toggle_ability_status)]
for listener in threads:
    listener.start()
for listener in threads:
    listener.join()
