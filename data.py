# TO-DO: add preprocessing: take the derivative of the normalized Ca traces and remove any negative values
import os
import pandas as pd
import numpy as np
from scipy.io import loadmat


def get_dir(drug, dose, animal_id):
    calcium_dir = 'R:\Basic_Sciences\Phys\Kennedylab\Parkerlab\Calcium_JP'
    calcium_ctrl_path = os.path.join(calcium_dir, drug, dose, animal_id, 'veh_drug.mat')
    calcium_amph_path = os.path.join(calcium_dir, drug, dose, animal_id + '_amph', 'amph_drug.mat')

    return calcium_ctrl_path, calcium_amph_path


def get_data(drug, dose, animal_id):
    # reshape
    # ctrl: 15 min * 60 sec * 5 Hz sampling rate = 4500
    # amph: 45 min * 60 sec * 5 Hz sampling rate = 13500
    calcium_ctrl_path, calcium_amph_path = get_dir(drug, dose, animal_id)

    mat_ctrl = loadmat(calcium_ctrl_path)
    speed_ctrl = mat_ctrl['veh_drug']['speed_traces_5hz'][0][0][0, :4500]
    calcium_ctrl_dff = mat_ctrl['veh_drug']['dff_traces_5hz'][0][0][:, :4500]
    calcium_ctrl_events = mat_ctrl['veh_drug']['events_5hz'][0][0][:, :4500]
    eventsum_ctrl = np.mean(np.array(calcium_ctrl_events), axis=0)
    eventmean_ctrl = np.mean(np.array(calcium_ctrl_events), axis=0)

    mat_amph = loadmat(calcium_amph_path)
    speed_amph = mat_amph['amph_drug']['speed_traces_5hz'][0][0][0, :13500]
    calcium_amph_dff = mat_amph['amph_drug']['dff_traces_5hz'][0][0][:, :13500]
    calcium_amph_events = mat_amph['amph_drug']['events_5hz'][0][0][:, :13500]
    eventsum_amph = np.mean(np.array(calcium_amph_events), axis=0)
    eventmean_amph = np.mean(np.array(calcium_amph_events), axis=0)

    # define
    neuron = np.size(calcium_ctrl_dff, 0)
    time_ctrl = np.size(calcium_ctrl_dff, 1)
    time_amph = np.size(calcium_amph_dff, 1)
    # print("neuron count: " + str(neuron))
    # print("time during ctrl: " + str(time_ctrl))
    # print("time during amph: " + str(time_amph))

    return speed_ctrl, speed_amph, eventmean_ctrl, eventmean_amph, neuron
