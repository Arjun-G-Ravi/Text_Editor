import tkinter as tk
import keyboard

class ListDisplayApp:
    def __init__(self, initial_list):
        self.list_content = initial_list

        self.window = tk.Tk()
        self.window.title("List Content Display")

        self.label = tk.Label(self.window, text="\n".join(self.list_content), padx=20, pady=20)
        self.label.pack()

        self.update_button = tk.Button(self.window, text="Update List", command=self.update_list_content)
        self.update_button.pack()

        self.window.mainloop()

    def update_list_content(self):
        # Update the content of the list
        new_list_content = ["New Item 1", "New Item 2", "New Item 3"]
        self.list_content = new_list_content

        # Update the label with the new content
        self.label.config(text="\n".join(self.list_content))

# Create an instance of the ListDisplayApp with the initial list
initial_list = ["Item 1", "Item 2", "Item 3", "Item 4"]
app = ListDisplayApp(initial_list)




import keyboard

def on_key_event(e):
    print(f'Key {e.name} {e.event_type}')

keyboard.hook(on_key_event)

# Keep the program running
keyboard.wait('esc')
