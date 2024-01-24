# Run the code with sudo in linux
# Press esc to stop the bg processes

import keyboard
import time
from multiprocessing import Process, Manager
import tkinter as tk


class TextEditor:
    def __init__(self, root, shared_data):
        self.root = root
        self.root.title("COW - Text Editor")
        self.root.geometry("600x800")
        self.shared_data = shared_data
        self.listbox = tk.Listbox(root)
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)
        self.update_data()

    def update_data(self):  # to the GUI
        data = self.shared_data
        self.listbox.delete(0, tk.END)
        for item in data:
            self.listbox.insert(tk.END, item)

        self.root.after(100, self.update_data)


def read_keyboard(shared_queue, shared_data):
    def on_key_event(e, shared_queue):
        if e.event_type == 'up' or e.name == 'esc':
            shared_queue.append(e.name)
        return e

    keyboard.hook(lambda e: on_key_event(e, shared_queue))
    keyboard.wait('esc')


def editor(shared_queue, shared_data):
    out = ''
    r, c = 0, 0
    if not shared_data:
        shared_data.append([])
        print('initiated')
        print(shared_data)
    print(type(shared_data))
    while out != 'esc':
        time.sleep(0.1)

        if shared_queue:
            character = shared_queue.pop(0)
            # Make changes to out here
            # hmap = {'enter': '\n', 'space': ' '}
            print("Char: ",character, r, c)
            if character == 'enter':
                print('new line')
                shared_data.append([])
                r += 1
                c = 0
            else:
                shared_data[0].append(character)
                print('here')
                print(shared_data[r])
                
                c += 1
            print(shared_data)

            # if out in hmap:
            #     out = hmap[out]

            # shared_data.append([out])

            # print("Shared data: ", shared_data)


def run_window(shared_data, shared_queue):
    root = tk.Tk()
    app = TextEditor(root, shared_data)
    root.mainloop()
    print("Press esc to close")


if __name__ == '__main__':
    with Manager() as manager:
        shared_queue = manager.list()  # To share the keyboard inputs
        shared_data = manager.list()  # To share the data structre that stores the whole text

        # Three processes run in parallel
        pKeyRead = Process(target=read_keyboard,
                           args=(shared_queue, shared_data))
        pRunEditor = Process(target=editor, args=(shared_queue, shared_data))
        pRunWindow = Process(
            target=run_window, args=(shared_data, shared_queue))

        pRunEditor.start()
        pKeyRead.start()
        pRunWindow.start()

        pRunWindow.join()
        pKeyRead.join()
        pRunEditor.join()
