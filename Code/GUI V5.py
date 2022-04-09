import wfdb.io
import AlgorithmsV5
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ecg_plot
from matplotlib.ticker import AutoMinorLocator
import pathlib
import pandas as pd



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
    global sampling_freq
    if not ECG:
        return
    else:
        res = (AlgorithmsV5.processing(ECG, num_leads, sampling_freq))
        sampling_freq = 500
        for x in range(1, 5):
            for y in range(0, num_leads):
                lst[x][y + 1] = res[x - 1][y]
            for y in range(num_leads, 12):
                lst[x][y + 1] = ""
        Table(GUI_window)


def import_data():
    ECG.clear()
    global sampling_freq
    sampling_freq = int(freq_import.get())
    global num_leads
    num_leads = int(lead_import.get())
    lead_selection.config(to_=num_leads)

    global total_columns
    total_columns = num_leads + 1

    file_path = tk.filedialog.askopenfilename()
    file_extension = pathlib.Path(file_path).suffix
    if file_extension == '.txt':
        new = np.loadtxt(file_path, delimiter=",", dtype="int")
        new = np.transpose(new)
    elif file_extension == '.csv':
        new = np.genfromtxt(file_path, delimiter=",", dtype="int")
        new = np.transpose(new)
    elif file_extension == '.hea' or file_extension == '.xws' or file_extension == '.dat' or file_extension == '.atr':
        print(file_path.replace(file_extension, ''))
        new, temp = wfdb.io.rdsamp(file_path.replace(file_extension, ''))
        new = np.transpose(new)
        new = new * 1000
        new = new.astype(int)
    elif file_extension == '.xls':
        new = pd.read_excel(file_path, dtype="int").to_numpy()
        new = np.transpose(new)
    elif file_extension == '.xlsx':
        new = pd.read_excel(file_path, dtype="int").to_numpy()
        new = np.transpose(new)
    else:
        return
    for lead in range(0, num_leads + 1):
        ECG.append(new[lead])
    plot()


def plot_lead(val):
    if not len(ECG) == 0:
        fig.clear()
        plot1 = fig.add_subplot(111)
        #ecg_plot.plot_1(ECG[0] * 0.002, ECG[lead_selection.get()])
        plot1.plot(ECG[0] * 1 / int(freq_import.get()), ECG[lead_selection.get()])
        secs = len(ECG[0])/int(freq_import.get())
        plot1.minorticks_on()
        plot1.xaxis.set_minor_locator(AutoMinorLocator(5))
        #plot1.set_ylim(-amplitude_ecg, amplitude_ecg)
        plot1.set_xlim(0, secs)
        plot1.grid(which='major', linestyle='-', linewidth='0.4', color='red')
        plot1.grid(which='minor', linestyle='-', linewidth='0.4', color=(1, 0.7, 0.7))
        canvas.draw_idle()


def plot():
    fig.clear()
    plot1 = fig.add_subplot(111)
    plot1.plot(ECG[0] * 1 / int(freq_import.get()), ECG[lead_selection.get()])
    secs = len(ECG[1])/int(freq_import.get())
    plot1.minorticks_on()
    plot1.xaxis.set_minor_locator(AutoMinorLocator(5))
    plot1.set_xlim(0, secs)
    plot1.grid(which='major', linestyle='-', linewidth='0.4', color='red')
    plot1.grid(which='minor', linestyle='-', linewidth='0.4', color=(1, 0.7, 0.7))
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
sampling_freq = 500
ECG = []


lead_selection = tk.Scale(GUI_window, from_=1, to_=12, command=plot_lead, bd=5, orient="horizontal")
lead_selection.place(x=200, y=0, width=600, height=50)
lead_selection.set(1)
lead_label = tk.Label(GUI_window, text="Lead: ", font="30")
lead_label.place(x=0, y=0, width=200, height=50)

import_label = tk.Label(GUI_window, text="1 - leads:")
import_label.place(x=0, y=380, width=60, height=50)
var = tk.StringVar(GUI_window)
var.set("12")
lead_import = tk.Spinbox(GUI_window, from_=1, to=12, textvariable=var)
lead_import.place(x=60, y=390, width=30, height=30)
import_label2 = tk.Label(GUI_window, text=" sampling freq.(Hz): ")
import_label2.place(x=95, y=380, width=100, height=50)
var = tk.StringVar(GUI_window)
var.set("500")
freq_import = tk.Spinbox(GUI_window, from_=1, to=5000, textvariable=var)
freq_import.place(x=200, y=390, width=40, height=30)
#import_label3 = tk.Label(GUI_window, text=" Hz ")
#import_label3.place(x=200, y=380, width=20, height=50)

import_data_button = tk.Button(GUI_window, text="2 - Import Data", command=import_data)
import_data_button.place(x=0, y=430, width=240, height=55)

lst = [["Lead", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
       ["Stationary Signal Check", "", "", "", "", "", "", "", "", "", "", "", ""],
       ["Heart Rate Check", "", "", "", "", "", "", "", "", "", "", "", ""],
       ["SNR Check", "", "", "", "", "", "", "", "", "", "", "", ""],
       ["Overall Result", "", "", "", "", "", "", "", "", "", "", "", ""]]

total_rows = len(lst)
total_columns = len(lst[0])
t = Table(GUI_window)

process_button = tk.Button(GUI_window, text="3 - Process", command=execute)
process_button.place(x=0, y=485, width=240, height=55)


GUI_window.mainloop()
