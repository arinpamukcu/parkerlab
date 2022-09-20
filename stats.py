# Created by Arin Pamukcu, PhD on August 2022
# histogras for time spent doing particular action

from data import *
from info import *
from mars import *
import numpy as np
import matplotlib.pyplot as plt
import pdb

def get_speed(speed_data, time):

    nospeed_bout = []
    lospeed_bouts = []
    midspeed_bouts = []
    hispeed_bouts = []
    acc_bouts = []

    for fr in range(0, len(speed_data) - 5):
        if speed_data[fr] < 1:
            nospeed_bout.append(fr)
        if 1 < speed_data[fr] <= 5:
            lospeed_bouts.append(fr)
        if 5 < speed_data[fr] <= 10:
            midspeed_bouts.append(fr)
        if 10 < speed_data[fr]:
            hispeed_bouts.append(fr)
        if speed_data[fr] < 2 and (np.mean(speed_data[fr + 1:fr + 5]) - np.mean(speed_data[fr - 5:fr - 1])) > 1:
            acc_bouts.append(fr)

    nospeed_frames = np.zeros(time)
    for fr in range(len(nospeed_bout)):
        nospeed_frames[nospeed_bout[fr]] = 1
    nospeed_time = np.sum(nospeed_frames)/5

    lospeed_frames = np.zeros(time)
    for fr in range(len(lospeed_bouts)):
        lospeed_frames[lospeed_bouts[fr]] = 1
    lospeed_time = np.sum(lospeed_frames)/5

    midspeed_frames = np.zeros(time)
    for fr in range(len(midspeed_bouts)):
        midspeed_frames[midspeed_bouts[fr]] = 1
    midspeed_time = np.sum(midspeed_frames)/5

    hispeed_frames = np.zeros(time)
    for fr in range(len(hispeed_bouts)):
        hispeed_frames[hispeed_bouts[fr]] = 1
    hispeed_time = np.sum(hispeed_frames)/5

    acc_frames = np.zeros(time)
    for fr in range(len(acc_bouts)):
        acc_frames[acc_bouts[fr]] = 1
    acc_time = np.sum(acc_frames)/5

    return nospeed_time, lospeed_time, midspeed_time, hispeed_time, acc_time


def get_turns(turn_data, time):
    right_turn = []
    left_turn = []
    straight = []

    for fr in range(0, len(turn_data) - 5):
        if turn_data[fr] > 30 and turn_data[fr] > turn_data[fr + 1] > turn_data[fr + 2] > turn_data[fr + 3] > turn_data[fr + 4]:
            right_turn.append(fr)
        elif turn_data[fr] < -30 and turn_data[fr] < turn_data[fr + 1] < turn_data[fr + 2] < turn_data[fr + 3] < turn_data[fr + 4]:
            left_turn.append(fr)
        elif -30 < turn_data[fr] < 30:
            straight.append(fr)

    right_turn_frames = np.zeros(time)
    for fr in range(len(right_turn)):
        right_turn_frames[right_turn[fr]] = 1
    right_turn_time = np.sum(right_turn_frames)

    left_turn_frames = np.zeros(time)
    for fr in range(len(left_turn)):
        left_turn_frames[left_turn[fr]] = 1
    left_turn_time = np.sum(left_turn_frames)/5

    straight_frames = np.zeros(time)
    for fr in range(len(left_turn)):
        straight_frames[left_turn[fr]] = 1
    straight_time = np.sum(straight_frames) / 5

    return right_turn_time, left_turn_time, straight_time


def get_metrics(drug, dose):
    experiments, animals, _, _ = get_animal_id(drug, dose)

    data_ctrl = {}
    data_amph = {}

    nospeed_ctrl_peranimal, lospeed_ctrl_peranimal, midspeed_ctrl_peranimal, hispeed_ctrl_peranimal, \
    acc_ctrl_peranimal = ([] for i in range(5))
    nospeed_amph_peranimal, lospeed_amph_peranimal, midspeed_amph_peranimal, hispeed_amph_peranimal, \
    acc_amph_peranimal = ([] for i in range(5))

    for experiment in experiments:
        print(experiment)

        # get values for speed or turn
        speed_ctrl, speed_amph, _, _, _, _, neuron, time_ctrl, time_amph = get_data(drug, dose, experiment)
        turn_angle_ctrl, turn_angle_amph, _, _ = mars_feature(drug, dose, experiment)

        # get values for each animal for that drug & dose
        nospeed_ctrl, lospeed_ctrl, midspeed_ctrl, hispeed_ctrl, acc_ctrl = get_speed(speed_ctrl, time_ctrl)
        nospeed_amph, lospeed_amph, midspeed_amph, hispeed_amph, acc_amph = get_speed(speed_amph, time_amph)
        right_turn_ctrl, left_turn_ctrl, straight_ctrl = get_turns(turn_angle_ctrl, time_ctrl)
        right_turn_amph, left_turn_amph, straight_amph = get_turns(turn_angle_amph, time_amph)

        # append values for each animal to a list
        nospeed_ctrl_peranimal.append(nospeed_ctrl)
        lospeed_ctrl_peranimal.append(lospeed_ctrl)
        midspeed_ctrl_peranimal.append(midspeed_ctrl)
        hispeed_ctrl_peranimal.append(hispeed_ctrl)
        acc_ctrl_peranimal.append(acc_ctrl)
        nospeed_amph_peranimal.append(nospeed_amph)
        lospeed_amph_peranimal.append(lospeed_amph)
        midspeed_amph_peranimal.append(midspeed_amph)
        hispeed_amph_peranimal.append(hispeed_amph)
        acc_amph_peranimal.append(acc_amph)

    # make a dictionary of values for each animal for that drug & dose
    data_ctrl['nospeed'] = nospeed_ctrl_peranimal
    data_ctrl['lospeed'] = lospeed_ctrl_peranimal
    data_ctrl['midspeed'] = midspeed_ctrl_peranimal
    data_ctrl['hispeed'] = hispeed_ctrl_peranimal
    data_ctrl['acc'] = acc_ctrl_peranimal
    data_amph['nospeed'] = nospeed_amph_peranimal
    data_amph['lospeed'] = lospeed_amph_peranimal
    data_amph['midspeed'] = midspeed_amph_peranimal
    data_amph['hispeed'] = hispeed_amph_peranimal
    data_amph['acc'] = acc_amph_peranimal

    return data_ctrl, data_amph


def get_alldata():

    drugs = ['Clozapine', 'Haloperidol', 'MP-10', 'Olanzapine']
    doses = ['Vehicle', 'LowDose', 'HighDose']

    alldata = {}
    for drug in drugs:
        alldata[drug] = {}
        for dose in doses:
            print(drug, dose)
            alldata[drug][dose] = {}
            alldata[drug][dose]['ctrl'] = {}
            alldata[drug][dose]['amph'] = {}
            data_ctrl, data_amph = get_metrics(drug, dose)
            _, animals, _, _ = get_animal_id(drug, dose)
            for animal in animals:
                alldata[drug][dose]['ctrl'][animal] = {}
                alldata[drug][dose]['amph'][animal] = {}
                # alldata[drug][dose]['ctrl'][animal] = data_ctrl
                # alldata[drug][dose]['amph'][animal] = data_amph

                # todo: fix this so Vehicle has data from all drugs
                if dose == 'Vehicle':
                    for metric in data_ctrl.keys():
                        alldata[dose]['ctrl'][animal][metric] = data_ctrl[metric]
                    for metric in data_amph.keys():
                        alldata[dose]['amph'][animal][metric] = data_amph[metric]
                else:
                    alldata[drug][dose]['ctrl'][animal] = data_ctrl
                    alldata[drug][dose]['amph'][animal] = data_amph

    pdb.set_trace()

    return alldata


def plot():

    # todo: fix this so it computes mean and sem and plots only selected data from alldata

    data_ctrl_mean, data_ctrl_sem, data_amph_mean, data_amph_sem = get_metrics()

    plt.figure(figsize=(18, 6))
    plt.bar('nospeed_ctrl', data_ctrl_mean['nospeed'], yerr=data_ctrl_sem['nospeed'], color='k')
    plt.bar('lospeed_ctrl', data_ctrl_mean['lospeed'], yerr=data_ctrl_sem['lospeed'], color='k')
    plt.bar('midspeed_ctrl', data_ctrl_mean['midspeed'], yerr=data_ctrl_sem['midspeed'], color='k')
    plt.bar('hispeed_ctrl', data_ctrl_mean['hispeed'], yerr=data_ctrl_sem['hispeed'], color='k')
    plt.bar('acc_ctrl', data_ctrl_mean['acc'], yerr=data_ctrl_sem['acc'], color='k')
    plt.bar('nospeed_amph', data_amph_mean['nospeed'], yerr=data_amph_sem['nospeed'], color='m')
    plt.bar('lospeed_amph', data_amph_mean['lospeed'], yerr=data_amph_sem['lospeed'], color='m')
    plt.bar('midspeed_amph', data_amph_mean['midspeed'], yerr=data_amph_sem['midspeed'], color='m')
    plt.bar('hispeed_amph', data_amph_mean['hispeed'], yerr=data_amph_sem['hispeed'], color='m')
    plt.bar('acc_amph', data_amph_mean['acc'], yerr=data_amph_sem['acc'], color='m')
    plt.ylabel('Time (s)')
    plt.title('MP-10, LowDose')
    plt.legend()
    plt.show()

    return
