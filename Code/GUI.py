import Algorithms
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Table:
    def __init__(self, root):
        Table = tk.Frame(GUI_window)
        Table.place(x=260, y=390, width=700, height=160)
        for i in range(total_rows):
            for j in range(total_columns):
                if j == 0:
                    self.e = tk.Entry(Table, width=21, fg='black', font=('Arial', 15, 'bold'))
                else:
                    self.e = tk.Entry(Table, width=3, fg='black', font=('Arial', 15, 'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(tk.END, lst[i][j])


def execute():
    if not ECG:
        return
    else:
        res = (Algorithms.processing(ECG, num_leads))
        for x in range(1, 5):
            for y in range(0, num_leads):
                lst[x][y + 1] = res[x - 1][y]
            for y in range(num_leads, 12):
                lst[x][y + 1] = ""
        Table(GUI_window)


def import_data():
    ECG.clear()

    global num_leads
    num_leads = int(lead_import.get())
    lead_selection.config(to_=num_leads)

    global total_columns
    total_columns = num_leads + 1

    file_path = tk.filedialog.askopenfilename()
    new = np.loadtxt(file_path, delimiter=",", dtype="int")
    new = np.transpose(new)
    for lead in range(0, num_leads + 1):
        ECG.append(new[lead])
    plot()


def plot_lead(val):
    if not len(ECG) == 0:
        fig.clear()
        plot1 = fig.add_subplot(111)
        plot1.plot(ECG[0] * 0.002, ECG[lead_selection.get()])
        canvas.draw_idle()


def plot():
    fig.clear()
    plot1 = fig.add_subplot(111)
    plot1.plot(ECG[0] * 0.002, ECG[lead_selection.get()])
    canvas.draw_idle()


GUI_window = tk.Tk()
GUI_window.title("ECGAssess")
GUI_window.geometry("960x540")

fig = plt.Figure(figsize=(9.6, 3.3), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=GUI_window)
canvas.get_tk_widget().place(x=0, y=50)

# set defaults
file_path = 0
num_leads = 12
ECG = []

lead_selection = tk.Scale(GUI_window, from_=1, to_=12, command=plot_lead, bd=5, orient="horizontal")
lead_selection.place(x=200, y=0, width=600, height=50)
lead_selection.set(1)
lead_label = tk.Label(GUI_window, text="Lead: ", font="30")
lead_label.place(x=0, y=0, width=200, height=50)

import_label = tk.Label(GUI_window, text="1 - Number of Leads: ")
import_label.place(x=0, y=380, width=230, height=50)
var = tk.StringVar(GUI_window)
var.set("12")
lead_import = tk.Spinbox(GUI_window, from_=1, to=12, textvariable=var)
lead_import.place(x=180, y=390, width=30, height=30)

import_data_button = tk.Button(GUI_window, text="2 - Import Data", command=import_data)
import_data_button.place(x=0, y=430, width=240, height=55)

lst = [["Lead", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
       ["Stationary Signal Check", "", "", "", "", "", "", "", "", "", "", "", ""],
       ["Heart Rate Check", "", "", "", "", "", "", "", "", "", "", "", ""],
       ["SNR Check", "", "", "", "", "", "", "", "", "", "", "", ""],
       ["Combination", "", "", "", "", "", "", "", "", "", "", "", ""]]

total_rows = len(lst)
total_columns = len(lst[0])
t = Table(GUI_window)

process_button = tk.Button(GUI_window, text="3 - Process", command=execute)
process_button.place(x=0, y=485, width=240, height=55)

GUI_window.mainloop()
