# Created by Arin Pamukcu, PhD on August 2022
# histogras for time spent doing particular action

from data import *
from info import *
from mars import *
import numpy as np
import matplotlib.pyplot as plt

def speed_bouts(speed_data, time):
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
    lospeed_time = np.sum(lospeed_frames)

    midspeed_frames = np.zeros(time)
    for fr in range(len(midspeed_bouts)):
        midspeed_frames[midspeed_bouts[fr]] = 1
    midspeed_time = np.sum(midspeed_frames)

    hispeed_frames = np.zeros(time)
    for fr in range(len(hispeed_bouts)):
        hispeed_frames[hispeed_bouts[fr]] = 1
    hispeed_time = np.sum(hispeed_frames)

    acc_frames = np.zeros(time)
    for fr in range(len(acc_bouts)):
        acc_frames[acc_bouts[fr]] = 1
    acc_time = np.sum(acc_frames)

    return nospeed_time, lospeed_time, midspeed_time, hispeed_time, acc_time


def turn_bouts(turn_data, time):
    right_turn_bouts = []
    left_turn_bouts = []

    for fr in range(0, len(turn_data) - 5):
        if turn_data[fr] > turn_data[fr + 1] > turn_data[fr + 2] > turn_data[fr + 3] > turn_data[fr + 4]:
            right_turn_bouts.append(fr)
        elif turn_data[fr] < turn_data[fr + 1] < turn_data[fr + 2] < turn_data[fr + 3] < turn_data[fr + 4]:
            left_turn_bouts.append(fr)

    right_turn_bout_frames = np.zeros(time)
    for fr in range(len(right_turn_bouts)):
        right_turn_bout_frames[right_turn_bouts[fr]] = 1
    right_turn_bout_time = np.sum(right_turn_bout_frames)

    left_turn_bout_frames = np.zeros(time)
    for fr in range(len(left_turn_bouts)):
        left_turn_bout_frames[left_turn_bouts[fr]] = 1
    left_turn_bout_time = np.sum(left_turn_bout_frames)/5

    return right_turn_bout_time, left_turn_bout_time


def speed_data():
    drugs = ['Clozapine']
    # drugs = get_drug()
    dose = 'HighDose'

    nospeed_duration_ctrl_all, lospeed_duration_ctrl_all, midspeed_duration_ctrl_all, hispeed_duration_ctrl_all, \
        acc_duration_ctrl_all = ([] for i in range(5))
    nospeed_duration_amph_all, lospeed_duration_amph_all, midspeed_duration_amph_all, hispeed_duration_amph_all, \
        acc_duration_amph_all = ([] for i in range(5))

    for drug in drugs:

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)

        nospeed_duration_ctrl_perdrug, lospeed_duration_ctrl_perdrug, midspeed_duration_ctrl_perdrug, \
            hispeed_duration_ctrl_perdrug, acc_duration_ctrl_perdrug = ([] for i in range(5))
        nospeed_duration_amph_perdrug, lospeed_duration_amph_perdrug, midspeed_duration_amph_perdrug, \
            hispeed_duration_amph_perdrug, acc_duration_amph_perdrug = ([] for i in range(5))

        for experiment in experiments:
            print(experiment + '_speed')

            speed_ctrl, speed_amph, _, _, _, _, neuron, time_ctrl, time_amph = get_data(drug, dose, experiment)

            # mars_turn_angle_ctrl, mars_turn_angle_amph, _, _ = mars_feature(drug, dose, experiment)

            nospeed_duration_ctrl_peranimal, lospeed_duration_ctrl_peranimal, midspeed_duration_ctrl_peranimal, \
            hispeed_duration_ctrl_peranimal, acc_duration_ctrl_peranimal = speed_bouts(speed_ctrl, time_ctrl)
            nospeed_duration_amph_peranimal, lospeed_duration_amph_peranimal, midspeed_duration_amph_peranimal, \
            hispeed_duration_amph_peranimal, acc_duration_amph_peranimal = speed_bouts(speed_amph, time_amph)

            nospeed_duration_ctrl_perdrug.append(nospeed_duration_ctrl_peranimal)
            lospeed_duration_ctrl_perdrug.append(lospeed_duration_ctrl_peranimal)
            midspeed_duration_ctrl_perdrug.append(midspeed_duration_ctrl_peranimal)
            hispeed_duration_ctrl_perdrug.append(hispeed_duration_ctrl_peranimal)
            acc_duration_ctrl_perdrug.append(acc_duration_ctrl_peranimal)
            nospeed_duration_amph_perdrug.append(nospeed_duration_amph_peranimal)
            lospeed_duration_amph_perdrug.append(lospeed_duration_amph_peranimal)
            midspeed_duration_amph_perdrug.append(midspeed_duration_amph_peranimal)
            hispeed_duration_amph_perdrug.append(hispeed_duration_amph_peranimal)
            acc_duration_amph_perdrug.append(acc_duration_amph_peranimal)

        nospeed_duration_ctrl_all = nospeed_duration_ctrl_all + nospeed_duration_ctrl_perdrug
        lospeed_duration_ctrl_all = lospeed_duration_ctrl_all + lospeed_duration_ctrl_perdrug
        midspeed_duration_ctrl_all = midspeed_duration_ctrl_all + midspeed_duration_ctrl_perdrug
        hispeed_duration_ctrl_all = hispeed_duration_ctrl_all + hispeed_duration_ctrl_perdrug
        acc_duration_ctrl_all = acc_duration_ctrl_all + acc_duration_ctrl_perdrug
        nospeed_duration_amph_all = nospeed_duration_amph_all + nospeed_duration_amph_perdrug
        lospeed_duration_amph_all = lospeed_duration_amph_all + lospeed_duration_amph_perdrug
        midspeed_duration_amph_all = midspeed_duration_amph_all + midspeed_duration_amph_perdrug
        hispeed_duration_amph_all = hispeed_duration_amph_all + hispeed_duration_amph_perdrug
        acc_duration_amph_all = acc_duration_amph_all + acc_duration_amph_perdrug

    nospeed_duration_ctrl = np.nanmean(nospeed_duration_ctrl_all, axis=0)
    lospeed_duration_ctrl = np.nanmean(lospeed_duration_ctrl_all, axis=0)
    midspeed_duration_ctrl = np.nanmean(midspeed_duration_ctrl_all, axis=0)
    hispeed_duration_ctrl = np.nanmean(hispeed_duration_ctrl_all, axis=0)
    acc_duration_ctrl = np.nanmean(acc_duration_ctrl_all, axis=0)
    nospeed_duration_amph = np.nanmean(nospeed_duration_amph_all, axis=0)
    lospeed_duration_amph = np.nanmean(lospeed_duration_amph_all, axis=0)
    midspeed_duration_amph = np.nanmean(midspeed_duration_amph_all, axis=0)
    hispeed_duration_amph = np.nanmean(hispeed_duration_amph_all, axis=0)
    acc_duration_amph = np.nanmean(acc_duration_amph_all, axis=0)

    nospeed_duration_ctrl_sem = np.std(nospeed_duration_ctrl_all, axis=0) / np.sqrt(len(nospeed_duration_ctrl_all))
    lospeed_duration_ctrl_sem = np.std(lospeed_duration_ctrl_all, axis=0) / np.sqrt(len(lospeed_duration_ctrl_all))
    midspeed_duration_ctrl_sem = np.std(midspeed_duration_ctrl_all, axis=0) / np.sqrt(len(midspeed_duration_ctrl_all))
    hispeed_duration_ctrl_sem = np.std(hispeed_duration_ctrl_all, axis=0) / np.sqrt(len(hispeed_duration_ctrl_all))
    acc_duration_ctrl_sem = np.std(acc_duration_ctrl_all, axis=0) / np.sqrt(len(acc_duration_ctrl_all))
    nospeed_duration_amph_sem = np.std(nospeed_duration_amph_all, axis=0) / np.sqrt(len(nospeed_duration_amph_all))
    lospeed_duration_amph_sem = np.std(lospeed_duration_amph_all, axis=0) / np.sqrt(len(lospeed_duration_amph_all))
    midspeed_duration_amph_sem = np.std(midspeed_duration_amph_all, axis=0) / np.sqrt(len(midspeed_duration_amph_all))
    hispeed_duration_amph_sem = np.std(hispeed_duration_amph_all, axis=0) / np.sqrt(len(hispeed_duration_amph_all))
    acc_duration_amph_sem = np.std(acc_duration_amph_all, axis=0) / np.sqrt(len(acc_duration_amph_all))

    return nospeed_duration_ctrl, nospeed_duration_ctrl_sem, lospeed_duration_ctrl, lospeed_duration_ctrl_sem, \
           midspeed_duration_ctrl, midspeed_duration_ctrl_sem, hispeed_duration_ctrl, hispeed_duration_ctrl_sem, \
           acc_duration_ctrl, acc_duration_ctrl_sem, \
           nospeed_duration_amph, nospeed_duration_amph_sem, lospeed_duration_amph, lospeed_duration_amph_sem, \
           midspeed_duration_amph, midspeed_duration_amph_sem, hispeed_duration_amph, hispeed_duration_amph_sem, \
           acc_duration_amph, acc_duration_amph_sem


def turn_data():
    drugs = ['Clozapine']
    # drugs = get_drug()
    dose = 'Vehicle'

    right_turn_duration_ctrl_all = []
    right_turn_duration_amph_all = []
    left_turn_duration_ctrl_all = []
    left_turn_duration_amph_all = []

    for drug in drugs:

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)

        for experiment in experiments:
            print(experiment + '_turn')

            _, _, _, _, _, _, neuron, time_ctrl, time_amph = get_data(drug, dose, experiment)

            turn_angle_ctrl, turn_angle_amph, _, _ = mars_feature(drug, dose, experiment)

            right_turn_duration_ctrl_peranimal, left_turn_duration_ctrl_peranimal = turn_bouts(turn_angle_ctrl, time_ctrl)
            right_turn_duration_amph_peranimal, left_turn_duration_amph_peranimal = turn_bouts(turn_angle_amph, time_amph)

        right_turn_duration_ctrl_perdrug = np.nanmean(right_turn_duration_ctrl_peranimal, axis=0)
        right_turn_duration_amph_perdrug = np.nanmean(right_turn_duration_amph_peranimal, axis=0)
        left_turn_duration_ctrl_perdrug = np.nanmean(left_turn_duration_ctrl_peranimal, axis=0)
        left_turn_duration_amph_perdrug = np.nanmean(left_turn_duration_amph_peranimal, axis=0)

        right_turn_duration_ctrl_all.append(right_turn_duration_ctrl_perdrug)
        right_turn_duration_amph_all.append(right_turn_duration_amph_perdrug)
        left_turn_duration_ctrl_all.append(left_turn_duration_ctrl_perdrug)
        left_turn_duration_amph_all.append(left_turn_duration_amph_perdrug)

    right_turn_duration_ctrl = np.nanmean(right_turn_duration_ctrl_all, axis=0)
    right_turn_duration_amph = np.nanmean(right_turn_duration_amph_all, axis=0)
    left_turn_duration_ctrl = np.nanmean(left_turn_duration_ctrl_all, axis=0)
    left_turn_duration_amph = np.nanmean(left_turn_duration_amph_all, axis=0)

    right_turn_duration_ctrl_sem = np.std(right_turn_duration_ctrl_all, axis=0) / np.sqrt(len(right_turn_duration_ctrl_all))
    right_turn_duration_amph_sem = np.std(right_turn_duration_amph_all, axis=0) / np.sqrt(len(right_turn_duration_amph_all))
    left_turn_duration_ctrl_sem = np.std(left_turn_duration_ctrl_all, axis=0) / np.sqrt(len(left_turn_duration_ctrl_all))
    left_turn_duration_amph_sem = np.std(left_turn_duration_amph_all, axis=0) / np.sqrt(len(left_turn_duration_amph_all))

    return right_turn_duration_ctrl, right_turn_duration_ctrl_sem,\
           right_turn_duration_amph, right_turn_duration_amph_sem, \
           left_turn_duration_ctrl, left_turn_duration_ctrl_sem, \
           left_turn_duration_amph, left_turn_duration_amph_sem


def plot():

    nospeed_duration_ctrl, nospeed_duration_ctrl_sem, lospeed_duration_ctrl, lospeed_duration_ctrl_sem, \
    midspeed_duration_ctrl, midspeed_duration_ctrl_sem, hispeed_duration_ctrl, hispeed_duration_ctrl_sem, \
    acc_duration_ctrl, acc_duration_ctrl_sem, \
    nospeed_duration_amph, nospeed_duration_amph_sem, lospeed_duration_amph, lospeed_duration_amph_sem, \
    midspeed_duration_amph, midspeed_duration_amph_sem, hispeed_duration_amph, hispeed_duration_amph_sem, \
    acc_duration_amph, acc_duration_amph_sem = speed_data()

    # right_turn_duration_ctrl_all, right_turn_duration_ctrl_sem, \
    # right_turn_duration_amph_all, right_turn_duration_amph_sem, \
    # left_turn_duration_ctrl_all, left_turn_duration_ctrl_sem, \
    # left_turn_duration_amph_all, left_turn_duration_amph_sem = turn_data()

    plt.figure(figsize=(8, 4))
    # plt.subplot(211)
    # plt.bar('nospeed_ctrl', nospeed_duration_ctrl, yerr=nospeed_duration_ctrl_sem)
    # plt.bar('lospeed_ctrl', lospeed_duration_ctrl, yerr=lospeed_duration_ctrl_sem)
    # plt.bar('midspeed_ctrl', midspeed_duration_ctrl, yerr=midspeed_duration_ctrl_sem)
    # plt.bar('hispeed_ctrl', hispeed_duration_ctrl, yerr=hispeed_duration_ctrl_sem)
    plt.bar('acc_ctrl', acc_duration_ctrl, yerr=acc_duration_ctrl_sem)
    # plt.bar('nospeed_amph', nospeed_duration_amph, yerr=nospeed_duration_amph_sem)
    # plt.bar('lospeed_amph', lospeed_duration_amph, yerr=lospeed_duration_amph_sem)
    # plt.bar('midspeed_amph', midspeed_duration_amph, yerr=midspeed_duration_amph_sem)
    # plt.bar('hispeed_amph', hispeed_duration_amph, yerr=hispeed_duration_amph_sem)
    plt.bar('acc_amph', acc_duration_amph, yerr=acc_duration_amph_sem)
    plt.ylabel('Time (s)')
    plt.title('Time spent for speed')
    plt.legend()
    plt.show()

    # plt.subplot(212)
    # plt.bar('right_ctrl', right_turn_duration_ctrl_all, yerr=right_turn_duration_ctrl_sem)
    # plt.bar('left_ctrl', left_turn_duration_ctrl_all, yerr=left_turn_duration_ctrl_sem)
    # plt.bar('right_amph', right_turn_duration_amph_all, yerr=right_turn_duration_amph_sem)
    # plt.bar('left_amph', left_turn_duration_amph_all, yerr=left_turn_duration_amph_sem)
    # plt.ylabel('Time (s)')
    # plt.title('Time spent for turn')
    # plt.legend()
    # plt.show()

    return
