import Algo
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from matplotlib.backend_bases import key_press_handler
from matplotlib.widgets import Slider, Button, RadioButtons



class Table:

    def __init__(self, root):
        Table = tk.Frame(GUI_window)
        Table.place(x=265, y=390, width=700, height=160)
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                if j == 0:
                    self.e = tk.Entry(Table, width=20, fg='black', font=('Arial', 15, 'bold'))
                else:
                    self.e = tk.Entry(Table, width=3, fg='black', font=('Arial', 15, 'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(tk.END, lst[i][j])




def execute():
    if ECG==[]:
        return
    else:
        res = (Algo.processing(ECG))
        for x in range(1, 5):
            for y in range(0, 12):
                lst[x][y+1] = res[x-1][y]
        Table(GUI_window)



def import_data():
    ECG.clear()
    file_path = tk.filedialog.askopenfilename()
    new = np.loadtxt(file_path, delimiter=",", dtype="int")
    new = np.transpose(new)
    for lead in range(0, 13):
        ECG.append(new[lead])
    plot()


def plot_lead(val):
    if not len(ECG)==0:
        fig.clear()
        plot1 = fig.add_subplot(111)
        plot1.plot(ECG[0] * 0.002, ECG[lead_selection.get()])
        canvas.draw_idle()


def plot():
    fig.clear()
    plot1 = fig.add_subplot(111)
    plot1.plot(ECG[0]*0.002, ECG[lead_selection.get()])
    canvas.draw_idle()


GUI_window = tk.Tk()
GUI_window.title("ECG Lead Signal Quality Assessment")
GUI_window.geometry("960x540")

fig = plt.Figure(figsize=(9.6, 3.3), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=GUI_window)
canvas.get_tk_widget().place(x=0, y=50)
toolbar = NavigationToolbar2Tk(canvas, GUI_window)

file_path = 0
ECG = []

lead_selection = tk.Scale(GUI_window, from_=1, to_=12, command=plot_lead, bd=5, orient="horizontal")
lead_selection.place(x=200, y=0, width=600, height=50)
lead_selection.set(1)
lead_label = tk.Label(GUI_window, text="Lead: ", font="30")
lead_label.place(x=0, y=0, width=200, height=50)

import_data_button = tk.Button(GUI_window, text="1 - Import Data", command=import_data)
import_data_button.place(x=0, y=380, width=240, height=80)

# take the data
lst = [["Lead", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
       ["Stationary", "", "", "", "", "", "", "", "", "", "", "", ""],
       ["Peak detection", "", "", "", "", "", "", "", "", "", "", "", ""],
       ["SNR", "", "", "", "", "", "", "", "", "", "", "", ""],
       ["Conclusion", "", "", "", "", "", "", "", "", "", "", "", ""]]

# find total number of rows and
# columns in list
total_rows = len(lst)
total_columns = len(lst[0])
t = Table(GUI_window)


process_button = tk.Button(GUI_window, text="2 - Process", command=execute)
process_button.place(x=0, y=460, width=240, height=80)

GUI_window.mainloop()
