from multiprocessing import Process, Manager
import time
import keyboard

def read_keyboard(shared_queue):
    def on_key_event(e, shared_queue):
        if e.event_type == 'up' or e.name =='esc':
            shared_queue.append(e.name)
            # print("Shared q 1:", shared_queue)
        return e

    keyboard.hook(lambda e: on_key_event(e, shared_queue))
    keyboard.wait('esc')
        
def editor(shared_queue):
    out = ''
    while out != 'esc':
        time.sleep(0.1)
        if shared_queue:
            out = shared_queue.pop(0)
            print(f'Popped "{out}" from shared_queue')      





if __name__ == '__main__':
    with Manager() as manager:
        shared_queue = manager.list()

        pKeyRead = Process(target=read_keyboard, args=(shared_queue,))
        pRunEditor = Process(target=editor, args=(shared_queue,))

        pRunEditor.start()
        pKeyRead.start()

        pRunEditor.join()
        pKeyRead.join()