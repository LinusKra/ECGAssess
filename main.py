import numpy as np
import scipy.signal
from ecgdetectors import Detectors
from tabulate import tabulate
import scipy.stats
from tkinter import filedialog

detectors = Detectors(500)

# region set parameters
total_leads = 12        # leads
sampling_frequency = 500        # Hz
nyquist_frequency = sampling_frequency * 0.5        # Hz
max_loss_passband = 0.1     # dB
min_loss_stopband = 20      # dB
SNR_threshold = 0.5
signal_freq_band = [2, 40]      # from .. to .. in Hz
heart_rate_limits = [24, 300]       # from ... to ... in beats per minute
time = 10       # seconds
window_length = 100      # measurements
# endregion


def high_frequency_noise_filter(data):
    order, normal_cutoff = scipy.signal.buttord(20, 30, max_loss_passband, min_loss_stopband, fs=sampling_frequency)
    iir_b, iir_a = scipy.signal.butter(order, normal_cutoff, fs=sampling_frequency)
    filtered_data = scipy.signal.filtfilt(iir_b, iir_a, data)
    return filtered_data


def baseline_filter(data):
    order, normal_cutoff = scipy.signal.buttord(0.5, 8, max_loss_passband, min_loss_stopband, fs=sampling_frequency)
    iir_b, iir_a = scipy.signal.butter(order, normal_cutoff, fs=sampling_frequency)
    filtered_data = scipy.signal.filtfilt(iir_b, iir_a, data)
    return filtered_data


def stationary_signal(data):
    res = []
    for lead in range(1, total_leads + 1):
        window_matrix = np.lib.stride_tricks.sliding_window_view(data[lead], window_length)[::10]
        for window in window_matrix:
            if np.amax(window) == np.amin(window):
                res.append(1)
                break
        if len(res) != lead:
            res.append(0)
    return res


def peak_detection(data):
    res = []
    for lead in range(1, total_leads + 1):
        peaks = detectors.pan_tompkins_detector(data[lead])
        if len(peaks) > ((heart_rate_limits[1]*time)/60) or len(peaks) < ((heart_rate_limits[0]*time)/60):
            res.append(1)
        else:
            res.append(0)
    return res


def signal_to_noise(data):
    res = []
    for lead in range(1, total_leads + 1):
        f, Pxx_den = scipy.signal.periodogram(data[lead], fs=sampling_frequency, scaling="spectrum")
        if sum(Pxx_den):
            Signal_Power = sum(Pxx_den[(signal_freq_band[0]*10):(signal_freq_band[1]*10)])
            SNR = Signal_Power / (sum(Pxx_den) - Signal_Power)
        else:
            res.append(0)
            continue
        if SNR < SNR_threshold:
            res.append(1)
        else:
            res.append(0)
    return res


# region loading the data
def callback():
    name = filedialog.askopenfilename()
    return name

ECG_list = np.loadtxt(callback(), dtype="int")
ECG_list = np.transpose(ECG_list)
# endregion


classification_res = []
for name_txt in ECG_list:
    SQM = []  # Signal Quality Matrix
    # TODO: type in the file path of the set-a folder in your computer where ________ (next line)
    ECG = np.loadtxt("C:/Users/_________________________/set-a/" + str(name_txt) + ".txt", delimiter=",", dtype="int")
    ECG = np.transpose(ECG)
    filt_ECG = [ECG[0]]
    for lead in range(1, 13):
        x = high_frequency_noise_filter(ECG[lead])-baseline_filter(ECG[lead])
        filt_ECG.append(x)

    SQM.append(stationary_signal(ECG))
    SQM.append(peak_detection(filt_ECG))
    SQM.append(signal_to_noise(ECG))

    temp = list((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    for lead in range(1, 13):
        temp[lead - 1] = SQM[0][lead - 1] + SQM[1][lead - 1] + SQM[2][lead - 1]
    classification_res.append(temp)

    # lead_name = ["I", "II", "III", "aVF", "aVR", "aVL", "V1", "V2", "V3", "V4", "V5", "V6"]
    # SQM_rows = ["Stationary", "Peak Detection", "Signal to Noise Ratio"]
    # print(tabulate(SQM, headers=lead_name, showindex=SQM_rows))


lead_name = ["I", "II", "III", "aVF", "aVR", "aVL", "V1", "V2", "V3", "V4", "V5", "V6"]
TP = []
FP = []
TN = []
FN = []

# TODO: type in the file path of the correct annotation list in your computer where ________ (next line)
annotation = np.loadtxt("C:/Users/________________________.txt", dtype="int")
for x in range(0, len(classification_res)):
    for y in range(0, total_leads):
        if classification_res[x][y] >= 1:
            classification_res[x][y] = 1
        else:
            classification_res[x][y] = 0

        if classification_res[x][y] == annotation[x][y] and annotation[x][y] == 0:
            TP.append("signal " + str(x+1) + " lead " + lead_name[y])
        elif classification_res[x][y] == annotation[x][y] and annotation[x][y] == 1:
            TN.append("signal " + str(x+1) + " lead " + lead_name[y])
        elif classification_res[x][y] > annotation[x][y]:
            FN.append("signal " + str(x + 1) + " lead " + lead_name[y] + " FN")
        else:
            FP.append("signal " + str(x + 1) + " lead " + lead_name[y] + " FP")


# print(tabulate(classification_res, headers=lead_name))

print("TP: " + str(len(TP)))
print("FP: " + str(len(FP)))
print("TN: " + str(len(TN)))
print("FN: " + str(len(FN)))
print("Correctly categorized: " + str((len(TP) + len(TN))/(len(TP) + len(TN) + len(FP) + len(FN))))
