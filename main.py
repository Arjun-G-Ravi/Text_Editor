from multiprocessing import Process
import os
import time
import keyboard

global shared_queue
shared_queue = []

def read_keyboard():
    def on_key_event(e):
        shared_queue.append(e)
        return e

    keyboard.hook(on_key_event)
    keyboard.wait('esc')
        
def editor():
    l = []
    if shared_queue:
        l.append(shared_queue.pop(0))        

print(shared_queue)
pKeyRead = Process(target=read_keyboard)
pRunEditor = Process(target=editor)
pRunEditor.start()
pKeyRead.start()
pRunEditor.join()
pKeyRead.join()



