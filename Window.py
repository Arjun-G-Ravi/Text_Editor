

import tkinter as tk

def display_list_content(l):

    window = tk.Tk()
    window.title("Text Editor")
    window.geometry('600x400')
    # Create a label to display the list content
    label = tk.Label(window, text="\n".join(l), padx=20, pady=20)
    label.pack()

    # Run the Tkinter event loop
    window.mainloop()

# Call the function to display the list content
display_list_content()
