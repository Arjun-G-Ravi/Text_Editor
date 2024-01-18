import keyboard
import time
from multiprocessing import Process, Manager
import tkinter as tk


class ListUpdaterApp:
    def __init__(self, root, shared_data):
        self.root = root
        self.root.title("COW - Text Editor")
        self.root.geometry("600x800")

        self.shared_data = shared_data

        self.listbox = tk.Listbox(root)
        self.listbox.pack(pady=10)

        self.update_data()

    def update_data(self):
        
        data = ''.join(self.shared_data).split('enter')
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
    data = []
    index = 0, 0

    while out != 'esc':
        time.sleep(0.1)

        if shared_queue:
            out = shared_queue.pop(0)
            
            shared_data.append(out)
            # print("Shared data: ", shared_data)

def run_window(shared_data):
    root = tk.Tk()
    app = ListUpdaterApp(root, shared_data)
    root.mainloop()
    print("Close me now...")


if __name__ == '__main__':
    with Manager() as manager:
        shared_queue = manager.list()
        shared_data = manager.list()

        pKeyRead = Process(target=read_keyboard,
                           args=(shared_queue, shared_data))
        pRunEditor = Process(target=editor, args=(shared_queue, shared_data))
        pRunWindow = Process(target=run_window, args=(shared_data,))

        pRunEditor.start()
        pKeyRead.start()
        pRunWindow.start()

        pRunWindow.join()
        pKeyRead.join()
        pRunEditor.join()
