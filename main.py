# Run the code with sudo in linux
# Press esc to stop the bg processes

import keyboard
import time
from multiprocessing import Process, Manager
import tkinter as tk


# class TextEditor:
#     def __init__(self, root, shared_data):
#         self.root = root
#         self.root.title("COW - Text Editor")
#         self.root.geometry("600x800")
#         self.shared_data = shared_data
#         self.listbox = tk.Listbox(root)
#         self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)
#         self.update_data()


class TextEditor:
    def __init__(self, root, shared_data):
        self.root = root
        self.root.title("COW - Text Editor")
        self.root.geometry("600x800")
        self.shared_data = shared_data

        vertical_scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
        horizontal_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
        self.listbox = tk.Listbox(
            root, yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        vertical_scrollbar.config(command=self.listbox.yview)
        horizontal_scrollbar.config(command=self.listbox.xview)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.update_data()

    def update_data(self):  # to the GUI
        data = self.shared_data
        self.listbox.delete(0, tk.END)
        for line in data:
            item = ''.join(line)
            self.listbox.insert(tk.END, item)

        self.root.after(10, self.update_data)


def read_keyboard(shared_queue, shared_data):
    def on_key_event(e, shared_queue):
        global shift
        if e.event_type == 'down' or e.name == 'esc':
            shared_queue.append(e.name)
        return e

    keyboard.hook(lambda e: on_key_event(e, shared_queue))
    keyboard.wait('esc')


def editor(shared_queue, shared_data):
    out = ''
    r, c = 0, 0
    if not shared_data:
        shared_data.append(manager.list())
    while out != 'esc':
        time.sleep(0.01)

        if shared_queue:
            character = shared_queue.pop(0)
            # Make changes to out here
            hmap = {'space': ' '}
            if character == 'enter':
                shared_data.append(manager.list())
                r += 1
                c = 0
            elif character == 'backspace':
                if r == 0 and c == 0:
                    # Beginning
                    pass
                elif c == 0:
                    # one row up
                    r -= 1
                    c = len(shared_data[r])
                else:
                    # Remove character to left
                    shared_data[r].pop(c-1)
                    c -= 1

            elif character == 'left':
                if r == 0 and c == 0:
                    pass
                elif c == 0:
                    print('Row up')
                    # one row up
                    r -= 1
                    c = len(shared_data[r])
                else:
                    # print("Delete char")
                    c -= 1

            elif character == 'right':
                if c < len(shared_data[r]):
                    c += 1
            
            elif character == 'up':
                if r>0:
                    r-=1
                    c = min(c, len(shared_data[r]))
            elif character == 'down':
                if r<len(shared_data)-1:
                    r+=1
                    c = min(c, len(shared_data[r]))
            elif character == 'shift' or character == 'ctrl' or character == 'del' or character == 'tab':
                raise 'Not Defined.'
            else:
                if character in hmap:
                    character = hmap[character]
                shared_data[r].insert(c, character)
                c += 1
            print("Char:", character, ' CursorIndex:', r, c)


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
