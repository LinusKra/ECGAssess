import numpy as np
import scipy.signal
from ecgdetectors import Detectors
import scipy.stats

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


def processing(ECG):
    filt_ECG = [ECG[0]]
    for lead in range(1, total_leads + 1):
        x = high_frequency_noise_filter(ECG[lead]) - baseline_filter(ECG[lead])
        filt_ECG.append(x)

    SQM = []  # Signal Quality Matrix
    SQM.append(stationary_signal(ECG))
    SQM.append(peak_detection(filt_ECG))
    SQM.append(signal_to_noise(ECG))

    temp = list((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    for lead in range(1, total_leads + 1):
        temp[lead - 1] = SQM[0][lead - 1] + SQM[1][lead - 1] + SQM[2][lead - 1]

    res = []
    for x in range(0, total_leads):
        if temp[x] >= 1:
            temp[x] = u"\u2716"
        else:
            temp[x] = u"\u2714"

    for y in range(0, 3):
        t = []
        for x in range (0, total_leads):
            if SQM[y][x] == 1:
                t.append(u"\u2716")
            else:
                t.append(u"\u2714")
        res.append(t)



    # print(tabulate(SQM, headers=lead_name, showindex=SQM_rows))
    # print(LQI)
    res.append(temp)
    return res
