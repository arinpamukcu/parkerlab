# Created by Arin Pamukcu, PhD on August 2022
# histogras for time spent doing particular action

from data import *
from info import *
from mars import *
import numpy as np
import matplotlib.pyplot as plt
import pdb

def get_speed(speed_data, eventmean_data):

    # nospeed_bouts, lospeed_bouts, midspeed_bouts, hispeed_bouts, acc_bouts = ([] for i in range(5))
    nospeed_events, lospeed_events, midspeed_events, hispeed_events, acc_events = ([] for i in range(5))
    nospeed_duration, lospeed_duration, midspeed_duration, hispeed_duration, acc_duration = ([] for i in range(5))

    for fr in range(0, len(speed_data) - 5):
        if speed_data[fr] < 1:
            # nospeed_bouts.append(fr)
            nospeed_events.append(eventmean_data[fr])
            nospeed_duration += 1
        if 1 < speed_data[fr] <= 5:
            # lospeed_bouts.append(fr)
            lospeed_events.append(eventmean_data[fr])
            lospeed_duration += 1
        if 5 < speed_data[fr] <= 10:
            # midspeed_bouts.append(fr)
            midspeed_events.append(eventmean_data[fr])
            midspeed_duration += 1
        if 10 < speed_data[fr]:
            # hispeed_bouts.append(fr)
            hispeed_events.append(eventmean_data[fr])
            hispeed_duration += 1
        if speed_data[fr] < 2 and (np.mean(speed_data[fr + 1:fr + 5]) - np.mean(speed_data[fr - 5:fr - 1])) > 1:
            # acc_bouts.append(fr)
            acc_events.append(eventmean_data[fr])
            acc_duration += 1

    nospeed = [nospeed_duration/5, nospeed_events/5]
    lospeed = [lospeed_duration / 5, lospeed_events / 5]
    midspeed = [midspeed_duration / 5, midspeed_events / 5]
    hispeed = [hispeed_duration / 5, hispeed_events / 5]
    acc = [acc_duration / 5, acc_events / 5]

    # nospeed_frames = np.zeros(time)
    # for fr in range(len(nospeed_bouts)):
    #     nospeed_frames[nospeed_bouts[fr]] = 1
    # nospeed_time = np.sum(nospeed_frames)/5
    #
    # lospeed_frames = np.zeros(time)
    # for fr in range(len(lospeed_bouts)):
    #     lospeed_frames[lospeed_bouts[fr]] = 1
    # lospeed_time = np.sum(lospeed_frames)/5
    #
    # midspeed_frames = np.zeros(time)
    # for fr in range(len(midspeed_bouts)):
    #     midspeed_frames[midspeed_bouts[fr]] = 1
    # midspeed_time = np.sum(midspeed_frames)/5
    #
    # hispeed_frames = np.zeros(time)
    # for fr in range(len(hispeed_bouts)):
    #     hispeed_frames[hispeed_bouts[fr]] = 1
    # hispeed_time = np.sum(hispeed_frames)/5
    #
    # acc_frames = np.zeros(time)
    # for fr in range(len(acc_bouts)):
    #     acc_frames[acc_bouts[fr]] = 1
    # acc_time = np.sum(acc_frames)/5

    return nospeed, lospeed, midspeed, hispeed, acc


def get_turns(turn_data, time):
    right_turn, left_turn, straight = ([] for i in range(3))
    right_turn_events, left_turn_events, straight_events = ([] for i in range(3))

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

    for experiment, animal in zip(experiments, animals):
        data_ctrl[animal] = {}
        data_amph[animal] = {}

        print(experiment)

        # get values for speed or turn
        speed_ctrl, speed_amph, _, _, eventmean_ctrl, eventmean_amph, \
        neuron, time_ctrl, time_amph = get_data(drug, dose, experiment)
        # turn_angle_ctrl, turn_angle_amph, _, _ = mars_feature(drug, dose, experiment)

        # get values for each animal for that drug & dose
        nospeed_ctrl, lospeed_ctrl, midspeed_ctrl, hispeed_ctrl, acc_ctrl = get_speed(speed_ctrl, eventmean_ctrl)
        nospeed_amph, lospeed_amph, midspeed_amph, hispeed_amph, acc_amph = get_speed(speed_amph, eventmean_amph)
        # right_turn_ctrl, left_turn_ctrl, straight_ctrl = get_turns(turn_angle_ctrl, eventmean_ctrl)
        # right_turn_amph, left_turn_amph, straight_amph = get_turns(turn_angle_amph, eventmean_amph)

        # append values for each animal to a list
        data_ctrl[animal]['nospeed'] = nospeed_ctrl
        data_ctrl[animal]['lospeed'] = lospeed_ctrl
        data_ctrl[animal]['midspeed'] = midspeed_ctrl
        data_ctrl[animal]['hispeed'] = hispeed_ctrl
        data_ctrl[animal]['acc'] = acc_ctrl
        # data_ctrl[animal]['right_turn'] = right_turn_ctrl
        # data_ctrl[animal]['left_turn'] = left_turn_ctrl
        # data_ctrl[animal]['straight'] = straight_ctrl

        data_amph[animal]['nospeed'] = nospeed_amph
        data_amph[animal]['lospeed'] = lospeed_amph
        data_amph[animal]['midspeed'] = midspeed_amph
        data_amph[animal]['hispeed'] = hispeed_amph
        data_amph[animal]['acc'] = acc_amph
        # data_amph[animal]['right_turn'] = right_turn_amph
        # data_amph[animal]['left_turn'] = left_turn_amph
        # data_amph[animal]['straight'] = straight_amph

    return data_ctrl, data_amph


def get_alldata():

    # drugs = ['Clozapine', 'Haloperidol', 'MP-10', 'Olanzapine']
    # doses = ['Vehicle', 'LowDose', 'HighDose']
    drugs = ['Clozapine', 'Haloperidol']
    doses = ['Vehicle', 'HighDose']

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
            alldata[drug][dose]['ctrl'] = data_ctrl
            alldata[drug][dose]['amph'] = data_amph

    # pdb.set_trace()
    # print(alldata['Clozapine']['Vehicle']['ctrl']['m085'])

    return alldata['Clozapine']['Vehicle']['ctrl']['m085']


def plot(drug, dose, bases=['ctrl', 'amph'],
         metrics=['nospeed', 'lospeed', 'midspeed', 'hispeed', 'acc']):

    alldata = get_alldata()

    plt.figure(figsize=(18, 6))
    for base in bases:
        for metric in metrics:
            x = [alldata[drug][dose][base][a][metric] for a in alldata[drug][dose][base].keys()]
            mean = np.mean(x)
            sem = np.std(x, axis=0) / np.sqrt(len(x))
            plt.bar(metric, mean, yerr=sem, color='k')
    plt.ylabel('Time (s)')
    plt.title(drug, dose)
    plt.legend()
    plt.show()

    return
