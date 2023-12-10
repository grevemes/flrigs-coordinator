import tkinter as tk
from flrigs_coordinator import set_radio, swap_radio, show_radio, flrigs_init

radio_a = 'KX3'
radio_b = 'IC7300'
config_file = 'flrigs_coordinator.ini'


def execute_setab():
    config = flrigs_init(config_file)
    set_radio(radio_a, radio_b, config)


def execute_setba():
    config = flrigs_init(config_file)
    set_radio(radio_b, radio_a, config)


def execute_swap():
    config = flrigs_init(config_file)
    swap_radio(radio_a, radio_b, config)


window = tk.Tk()
window.wm_title("FLRIGs")
window.geometry("200x100")

button1 = tk.Button(window, text=f'{radio_a} x {radio_b}', command=execute_swap)
button1.pack()

button2 = tk.Button(window, text=f'{radio_a} > {radio_b}', command=execute_setab)
button2.pack()

button3 = tk.Button(window, text=f'{radio_b} > {radio_a}', command=execute_setba)
button3.pack()

window.mainloop()
