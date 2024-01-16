import tkinter as tk


def text_editor():
    window = tk.Tk()
    window.title('Text Editor')
    txt_edit = tk.Text(window)
    txt_edit.grid(row=0, column=2)

    window.mainloop()


if __name__ == '__main__':
    text_editor()


# This is doing everything for me. We have to go deeper!