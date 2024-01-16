import tkinter as tk
import multiprocessing

def insert_text(text_widget, text):
    text_widget.insert('1.0', text)

def text_editor_window():
    window = tk.Tk()
    window.title('Text Editor')
    # window.geometry('1920x1080')

    text_widget = tk.Text(window)
    text_widget.pack(expand=True, fill='both')

    insert_text(text_widget, 'he;ll')
    text_widget.configure(state='disabled')

    window.mainloop()

def read_keyboard_input():
    inp = input()
    print(input)
    return inp

def main():
    # Run process in parallel
    p1 = multiprocessing.Process(target=text_editor_window)
    p2 = multiprocessing.Process(target=read_keyboard_input)

    # Start the processes
    p1.start()
    p2.start()

    # Wait for both processes to finish
    p1.join()
    p2.join()
    
if __name__ == '__main__':
    main()
