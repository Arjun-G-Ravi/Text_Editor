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
        # self.add_data(self.my_list,['cow2'])

        # self.update_button = tk.Button(root, text="Add Item", command=self.add_item)
        # self.update_button.pack()

        # self.update_listbox()

    # def add_item(self):
    #     new_item = f"Item {len(self.my_list) + 1}"
    #     self.my_list.append(new_item)
    #     self.update_listbox()

    # def update_listbox(self):
    #     self.listbox.delete(0, tk.END)
    #     for item in self.my_list:
    #         self.listbox.insert(tk.END, item)

    #     self.root.after(1000, self.update_listbox)
    def add_data(self, data):
        # self.listbox.delete(0, tk.END)
        self.my_list = data
        self.update_listbox()
        self.listbox.delete(0, tk.END)
        for item in self.my_list:
            self.listbox.insert(tk.END, item)
        self.root.after(1000, self.add_data)


'''---------------------'''


def update_data(data, index, char):
    print(data, index)
    return data, index


def read_keyboard(shared_queue):
    def on_key_event(e, shared_queue):
        if e.event_type == 'up' or e.name == 'esc':
            shared_queue.append(e.name)
            # print("Shared q 1:", shared_queue)
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
            # update_windows(data)
            # win.update_list_content('cow')


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

        pRunEditor.join()
        pKeyRead.join()
