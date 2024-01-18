import keyboard
import time
from multiprocessing import Process, Manager
import tkinter as tk


class ListUpdaterApp:
    def __init__(self, root, shared_data):
        self.root = root
        self.root.title("COW - Text Editor")

        self.shared_data = shared_data

        self.listbox = tk.Listbox(root)
        self.listbox.pack(pady=10)

        self.update_data()

    def update_data(self):
        data = list(self.shared_data)
        data = list(''.join(data))
        self.listbox.delete(0, tk.END)
        for item in data:
            self.listbox.insert(tk.END, item)
        print(self.shared_data)
        self.root.after(1000, self.update_data)


def read_keyboard(shared_queue, shared_data):
    def on_key_event(e, shared_queue):
        if e.event_type == 'up' or e.name == 'esc':
            shared_queue.append(e.name)
        return e

    keyboard.hook(lambda e: on_key_event(e, shared_queue))
    keyboard.wait('esc')


def editor(shared_queue, shared_data):
    out = ''
    data = []
    index = 0, 0

    while out != 'esc':
        time.sleep(0.1)

        if shared_queue:
            out = shared_queue.pop(0)
            print(f'Popped "{out}" from shared_queue')
            # data, index = update_data(data, index, out)
            print(out)

            # Update shared data
            shared_data.append(out)
            print(shared_data)


def update_data(data, index, char):
    print(data, index)
    return data, index


def run_window(shared_data):
    root = tk.Tk()
    app = ListUpdaterApp(root, shared_data)
    root.mainloop()


if __name__ == '__main__':
    with Manager() as manager:
        shared_queue = manager.list()
        shared_data = manager.list()

        pKeyRead = Process(target=read_keyboard, args=(shared_queue, shared_data))
        pRunEditor = Process(target=editor, args=(shared_queue, shared_data))
        pRunWindow = Process(target=run_window, args=(shared_data,))

        pRunEditor.start()
        pKeyRead.start()
        pRunWindow.start()

        pRunWindow.join()
        pKeyRead.join()
        pRunEditor.join()
