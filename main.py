from multiprocessing import Process
import os
import time
import keyboard

global shared_queue
shared_queue = []

def read_keyboard():
    global shared_queue
    def on_key_event(e):
        global shared_queue
        if e.event_type == 'up':
            shared_queue.append(e.name)
            print("Shared q 1:", shared_queue)
        return e

    keyboard.hook(on_key_event)
    keyboard.wait('esc')
        
def editor():
    global shared_queue
    out = ''
    print(shared_queue)
    while out != 'esc':
        time.sleep(0.1)
        print("Shared q 2:", shared_queue)
        if shared_queue:
            print("BOAT ------------------------")
            out = shared_queue.pop(0)
            print("Popped from shared_queue")      


pKeyRead = Process(target=read_keyboard)
pRunEditor = Process(target=editor)

pRunEditor.start()
pKeyRead.start()

pRunEditor.join()
pKeyRead.join()
