import tkinter as tk
import multiprocessing

def insert_text(text_widget, text):
    text_widget.insert('1.0', text)

def text_editor_window(shared_queue):
    window = tk.Tk()
    window.title('Text Editor')
    # window.geometry('1920x1080')
    text_widget = tk.Text(window)
    text_widget.pack(expand=True, fill='both')
    print(shared_queue.get())
    
    text_widget.configure(state='disabled')

    window.mainloop()

def read_keyboard_input(shared_queue):
    inp = input('Enter:')
    shared_queue.put(input)

def main():
    
    shared_queue = multiprocessing.Queue()
    
    p1 = multiprocessing.Process(target=text_editor_window, args=(shared_queue,))
    p2 = multiprocessing.Process(target=read_keyboard_input, args=(shared_queue,))

    # Start the processes
    p1.start()
    p2.start()

    # Wait for both processes to finish
    p1.join()
    p2.join()
    
if __name__ == '__main__':
    main()
