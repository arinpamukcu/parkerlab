# TO-DO: add preprocessing: take the derivative of the normalized Ca traces and remove any negative values

import os
import pandas as pd
import numpy as np
from scipy.signal import find_peaks

def get_calcium_dir(drug, dose, experiment):
    calcium_dir = 'R:\Basic_Sciences\Phys\Kennedylab\Parkerlab\Calcium'
    calcium_file = experiment + '_neurons_dv.csv'
    calcium_path = os.path.join(calcium_dir, drug, dose, experiment, calcium_file)

    return calcium_path


def get_calcium_data(drug, dose, experiment):
    # reshape
    # ctrl: 15 min * 60 sec * 5 Hz sampling rate = 4500
    # amph: 45 min * 60 sec * 5 Hz sampling rate = 13500
    calcium = pd.read_csv(get_calcium_dir(drug, dose, experiment), header=None)
    calcium_ctrl = np.array(calcium.iloc[:, :4500])
    calcium_amph = np.array(calcium.iloc[:, 4500:18000])

    # define
    neuron = np.size(calcium_amph, 0)
    time_ctrl = np.size(calcium_ctrl, 1)
    time_amph = np.size(calcium_amph, 1)
    # print("neuron count: " + str(neuron))
    # print("time during ctrl: " + str(time_ctrl))
    # print("time during amph: " + str(time_amph))

    # # smooth
    # calcium_ctrl_smooth = gaussian_filter1d(calcium_ctrl, sigma=10)
    # calcium_amph_smooth = gaussian_filter1d(calcium_amph, sigma=10)

    return calcium_ctrl, calcium_amph, neuron, time_ctrl, time_amph


def binarize_calcium(drug, dose, experiment):
    calcium_ctrl, calcium_amph, neuron, time_ctrl, time_amph = get_calcium_data(drug, dose, experiment)

    # binarize
    events_ctrl = np.zeros((neuron, time_ctrl))
    for n in range(0, neuron):
        peakt_ctrl = calcium_ctrl[n, :]
        peaks_ctrl, _ = find_peaks(calcium_ctrl[n, :], prominence=(np.std(peakt_ctrl) * 5))
        for t in range(0, len(peaks_ctrl)):
            events_ctrl[n, peaks_ctrl[t]] = 1

    events_amph = np.zeros((neuron, time_amph))
    for n in range(0, neuron):
        peakt_amph = calcium_amph[n, :]
        peaks_amph, _ = find_peaks(calcium_amph[n, :], prominence=np.std(peakt_amph) * 5)
        for t in range(0, len(peaks_amph)):
            events_amph[n, peaks_amph[t]] = 1

    # spikecount
    # after you binarize per neuron, change the sum to mean
    eventcount_ctrl = np.sum(np.array(events_ctrl), axis=0)
    eventcount_amph = np.sum(np.array(events_amph), axis=0)

    # eventcount_ctrl_total = np.sum(np.array(events_ctrl))
    # eventcount_amph_total = np.sum(np.array(events_amph))

    return events_ctrl, events_amph
