import tkinter as tk
import os

radio_a = 'KX3'
radio_b = 'IC7300'


def execute_setab():
    os.system(f'python flrigs-coordinator.py set {radio_a} {radio_b}')


def execute_setba():
    os.system(f'python flrigs-coordinator.py set {radio_b} {radio_a}')


def execute_swap():
    os.system(f'python flrigs-coordinator.py swap {radio_a} {radio_b}')


def execute_showa():
    os.system(f'python flrigs-coordinator.py show {radio_a}')


def execute_showb():
    os.system(f'python flrigs-coordinator.py show {radio_b}')


window = tk.Tk()
window.wm_title("FLRIGs")
window.geometry("200x100")

button1 = tk.Button(window, text=f'{radio_a} x {radio_b}', command=execute_swap)
button1.pack()

button2 = tk.Button(window, text=f'{radio_a} > {radio_b}', command=execute_setab)
button2.pack()

button3 = tk.Button(window, text=f'{radio_b} > {radio_a}', command=execute_setba)
button3.pack()

button4 = tk.Button(window, text=f'Show {radio_a}', command=execute_showa)
button4.pack()

button5 = tk.Button(window, text=f'Show {radio_b}', command=execute_showb)
button5.pack()

window.mainloop()