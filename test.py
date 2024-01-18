import keyboard
import time
from multiprocessing import Process, Manager
import tkinter as tk


# class ListDisplayApp:
#     def __init__(self, initial_list):
#         self.list_content = initial_list

#         self.window = tk.Tk()
#         self.window.title("TEXT EDITOR")
#         self.window.geometry('400x400')

#         self.label = tk.Label(self.window, text="", padx=20, pady=20)
#         self.label.pack()

#         self.window.mainloop()

#     def update_list_content(self,new_list_content):
#         self.list_content = new_list_content
#         self.label.config(text="\n".join(self.list_content))


# # initial_list = ["Item 1", "Item 2", "Item 3", "Item 4"]
# app = ListDisplayApp(initial_list)

class ListUpdaterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("List Updater")

        self.my_list = ["Item 1", "Item 2", "Item 3"]

        self.listbox = tk.Listbox(root)
        self.listbox.pack(pady=10)

        self.update_button = tk.Button(root, text="Add Item", command=self.add_item)
        self.update_button.pack()

        self.update_listbox()

    def add_item(self):
        new_item = f"Item {len(self.my_list) + 1}"
        self.my_list.append(new_item)
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in self.my_list:
            self.listbox.insert(tk.END, item)

        # Schedule the update_listbox method to be called after 1000 milliseconds (1 second)
        self.root.after(1000, self.update_listbox)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ListUpdaterApp(root)
#     root.mainloop()

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