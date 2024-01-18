import keyboard
import time
from multiprocessing import Process, Manager
import tkinter as tk


class ListUpdaterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("List Updater")

        self.my_list = ['cow']

        self.listbox = tk.Listbox(root)
        self.listbox.pack(pady=10)
        self.add_data(self.my_list)

    def add_data(self, data):
        self.my_list = data
        self.listbox.delete(0, tk.END)
        for item in self.my_list:
            self.listbox.insert(tk.END, item)
        self.root.after(1000, lambda: self.add_data(data))



def read_keyboard(shared_queue):
    def on_key_event(e, shared_queue):
        if e.event_type == 'up' or e.name == 'esc':
            shared_queue.append(e.name)
        return e

    keyboard.hook(lambda e: on_key_event(e, shared_queue))
    keyboard.wait('esc')


def editor(shared_queue):
    out = ''
    data = [[]]
    index = 0, 0

    while out != 'esc':
        time.sleep(0.1)

        if shared_queue:
            out = shared_queue.pop(0)
            print(f'Popped "{out}" from shared_queue')
            data, index = update_data(data, index, out)


def update_data(data, index, char):
    print(data, index)
    return data, index

if __name__ == '__main__':
    with Manager() as manager:
        shared_queue = manager.list()

        pKeyRead = Process(target=read_keyboard, args=(shared_queue,))
        pRunEditor = Process(target=editor, args=(shared_queue,))

        pRunEditor.start()
        pKeyRead.start()

        root = tk.Tk()
        app = ListUpdaterApp(root)
        root.mainloop()

        pKeyRead.join()
        pRunEditor.join()
