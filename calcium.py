# Created by Arin Pamukcu, PhD on August 2022 in Chicago, IL

import os
import numpy as np
import pandas as pd
from scipy.io import loadmat
from scipy.signal import find_peaks

#  path
calcium_dir = 'R:\Basic_Sciences\Phys\Kennedylab\Parkerlab\Calcium_v2' #pc
# calcium_dir = '/Volumes/fsmresfiles/Basic_Sciences/Phys/Kennedylab/Parkerlab/Calcium_v2' #mac


def get_calcium_data(drug, dose, experiment):

    calcium_ctrl_path = os.path.join(calcium_dir, drug, dose, experiment, 'veh_drug.mat')
    calcium_amph_path = os.path.join(calcium_dir, drug, dose, experiment + '_amph', 'amph_drug.mat')

    # ctrl: 15 min * 60 sec * 5 Hz sampling rate = 4500
    # amph: 45 min * 60 sec * 5 Hz sampling rate = 13500

    # reshape (to account for different durations of ca recordings in different files)
    mat_ctrl = loadmat(calcium_ctrl_path)
    speed_ctrl = mat_ctrl['veh_drug']['speed_traces_5hz'][0][0][0, :4500]
    calcium_ctrl_dff = mat_ctrl['veh_drug']['dff_traces_5hz'][0][0][:, :4500]
    calcium_ctrl_events = mat_ctrl['veh_drug']['events_5hz'][0][0][:, :4500]
    eventmean_ctrl = np.mean(np.array(calcium_ctrl_events), axis=0)

    mat_amph = loadmat(calcium_amph_path)
    speed_amph = mat_amph['amph_drug']['speed_traces_5hz'][0][0][0, :13500]
    calcium_amph_dff = mat_amph['amph_drug']['dff_traces_5hz'][0][0][:, :13500]
    calcium_amph_events = mat_amph['amph_drug']['events_5hz'][0][0][:, :13500]
    eventmean_amph = np.mean(np.array(calcium_amph_events), axis=0)

    # define
    neuron_count = np.size(calcium_ctrl_dff, 0)
    time_ctrl = np.size(calcium_ctrl_dff, 1)
    time_amph = np.size(calcium_amph_dff, 1)

    # # smooth
    # calcium_ctrl_smooth = gaussian_filter1d(calcium_ctrl_dff, sigma=10)
    # calcium_amph_smooth = gaussian_filter1d(calcium_amph_dff, sigma=10)

    return speed_ctrl, speed_amph, \
           calcium_ctrl_events, calcium_amph_events, \
           eventmean_ctrl, eventmean_amph, \
           neuron_count, time_ctrl, time_amph


### for older version (Calcium_v1) files ###
# def get_calcium_data(drug, dose, experiment):
#
#     calcium_file = experiment + '_neurons_dv.csv'
#     calcium_path = os.path.join(calcium_dir, drug, dose, experiment, calcium_file)
#
#     # reshape (old version)
#     calcium = pd.read_csv(calcium_path, header=None)
#     calcium_ctrl = np.array(calcium.iloc[:, :4500])
#     calcium_amph = np.array(calcium.iloc[:, 4500:18000])
#
#     # define (old version)
#     neuron = np.size(calcium_amph, 0)
#     time_ctrl = np.size(calcium_ctrl, 1)
#     time_amph = np.size(calcium_amph, 1)
#
#     return calcium_ctrl, calcium_amph, neuron, time_ctrl, time_amph
#
#
# def binarize_calcium(drug, dose, experiment):
#     calcium_ctrl, calcium_amph, neuron, time_ctrl, time_amph = get_calcium_data(drug, dose, experiment)
#
#     # binarize
#     events_ctrl = np.zeros((neuron, time_ctrl))
#     for n in range(0, neuron):
#         peakt_ctrl = calcium_ctrl[n, :]
#         peaks_ctrl, _ = find_peaks(calcium_ctrl[n, :], prominence=(np.std(peakt_ctrl) * 5))
#         for t in range(0, len(peaks_ctrl)):
#             events_ctrl[n, peaks_ctrl[t]] = 1
#
#     events_amph = np.zeros((neuron, time_amph))
#     for n in range(0, neuron):
#         peakt_amph = calcium_amph[n, :]
#         peaks_amph, _ = find_peaks(calcium_amph[n, :], prominence=np.std(peakt_amph) * 5)
#         for t in range(0, len(peaks_amph)):
#             events_amph[n, peaks_amph[t]] = 1
#
#     # # spikecount
#     # # after you binarize per neuron, change the sum to mean
#     # eventcount_ctrl = np.sum(np.array(events_ctrl), axis=0)
#     # eventcount_amph = np.sum(np.array(events_amph), axis=0)
#     #
#     # # eventcount_ctrl_total = np.sum(np.array(events_ctrl))
#     # # eventcount_amph_total = np.sum(np.array(events_amph))
#
#     return events_ctrl, events_amph


