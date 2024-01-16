import tkinter as tk


def text_editor():
    window = tk.Tk()
    window.title('Text Editor')
    window.geometry("400x300")

    txt_edit = tk.Text(window)
    txt_edit.grid(row=0, column=1, sticky='nsew')

    window.mainloop()


if __name__ == '__main__':
    text_editor()
