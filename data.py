# Created by Arin Pamukcu, PhD on August 2022

import os
import numpy as np
from scipy.io import loadmat

#  path
# calcium_dir = 'R:\Basic_Sciences\Phys\Kennedylab\Parkerlab\Calcium_JP' #pc
calcium_dir = '/Volumes/fsmresfiles/Basic_Sciences/Phys/Kennedylab/Parkerlab/Calcium_JP' #mac

def get_dir(drug, dose, experiment):
    calcium_ctrl_path = os.path.join(calcium_dir, drug, dose, experiment, 'veh_drug.mat')
    calcium_amph_path = os.path.join(calcium_dir, drug, dose, experiment + '_amph', 'amph_drug.mat')

    return calcium_ctrl_path, calcium_amph_path


def get_data(drug, dose, experiment):
    # reshape
    # ctrl: 15 min * 60 sec * 5 Hz sampling rate = 4500
    # amph: 45 min * 60 sec * 5 Hz sampling rate = 13500
    calcium_ctrl_path, calcium_amph_path = get_dir(drug, dose, experiment)

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

    return speed_ctrl, speed_amph, \
           calcium_ctrl_events, calcium_amph_events, \
           eventmean_ctrl, eventmean_amph, \
           neuron_count, time_ctrl, time_amph
