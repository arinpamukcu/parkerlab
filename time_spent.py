# Created by Arin Pamukcu, PhD on August 2022
# histogras for time spent doing particular action

from data import *
from info import *
from mars import *
import numpy as np
import matplotlib.pyplot as plt

def speed_bouts(speed_data, time):
    speed_bouts = []

    for fr in range(0, len(speed_data) - 5):
        if speed_data[fr] > 1:
            speed_bouts.append(fr)

    speed_bout_frames = np.zeros(time)
    for fr in range(len(speed_bouts)):
        speed_bout_frames[speed_bouts[fr]] = 1
    speed_bout_duration = np.sum(speed_bout_frames)

    return speed_bout_duration


def acceleration_bouts(speed_data, time):
    acc_bouts = []

    for fr in range(0, len(speed_data) - 5):
        if speed_data[fr] > 1 and \
                np.mean(speed_data[fr - 5:fr - 1]) < np.mean(speed_data[fr + 1:fr + 5]):
            acc_bouts.append(fr)

    acc_bout_frames = np.zeros(time)
    for fr in range(len(acc_bouts)):
        acc_bout_frames[acc_bouts[fr]] = 1
    acc_bout_duration = np.sum(acc_bout_frames)

    return acc_bout_duration

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
    right_turn_bout_duration = np.sum(right_turn_bout_frames)

    left_turn_bout_frames = np.zeros(time)
    for fr in range(len(left_turn_bouts)):
        left_turn_bout_frames[left_turn_bouts[fr]] = 1
    left_turn_bout_duration = np.sum(left_turn_bout_frames)

    return right_turn_bout_duration, left_turn_bout_duration

def speed_data():
    drugs = ['Clozapine']
    # drugs = get_drug()
    dose = 'Vehicle'

    speed_duration_ctrl_all = []
    speed_duration_amph_all = []
    acc_duration_ctrl_all = []
    acc_duration_amph_all = []

    for drug in drugs:

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)

        for experiment in experiments:
            print(experiment + '_speed')

            speed_ctrl, speed_amph, _, _, _, _, neuron, time_ctrl, time_amph = get_data(drug, dose, experiment)

            # mars_turn_angle_ctrl, mars_turn_angle_amph, _, _ = mars_feature(drug, dose, experiment)

            speed_duration_ctrl_peranimal = speed_bouts(speed_ctrl, time_ctrl)
            speed_duration_amph_peranimal = speed_bouts(speed_amph, time_amph)
            acc_duration_ctrl_peranimal = acceleration_bouts(speed_ctrl, time_ctrl)
            acc_duration_amph_peranimal = acceleration_bouts(speed_amph, time_amph)

        speed_duration_ctrl_perdrug = np.nanmean(speed_duration_ctrl_peranimal, axis=0)
        speed_duration_amph_perdrug = np.nanmean(speed_duration_amph_peranimal, axis=0)
        acc_duration_ctrl_perdrug = np.nanmean(acc_duration_ctrl_peranimal, axis=0)
        acc_duration_amph_perdrug = np.nanmean(acc_duration_amph_peranimal, axis=0)

        speed_duration_ctrl_all.append(speed_duration_ctrl_perdrug)
        speed_duration_amph_all.append(speed_duration_amph_perdrug)
        acc_duration_ctrl_all.append(acc_duration_ctrl_perdrug)
        acc_duration_amph_all.append(acc_duration_amph_perdrug)

    speed_duration_ctrl = np.nanmean(speed_duration_ctrl_all, axis=0)
    speed_duration_amph = np.nanmean(speed_duration_amph_all, axis=0)
    acc_duration_ctrl = np.nanmean(acc_duration_ctrl_all, axis=0)
    acc_duration_amph = np.nanmean(acc_duration_amph_all, axis=0)

    speed_duration_ctrl_sem = np.std(speed_duration_ctrl_all, axis=0) / np.sqrt(len(speed_duration_ctrl_all))
    speed_duration_amph_sem = np.std(speed_duration_amph_all, axis=0) / np.sqrt(len(speed_duration_amph_all))
    acc_duration_ctrl_sem = np.std(acc_duration_ctrl_all, axis=0) / np.sqrt(len(acc_duration_ctrl_all))
    acc_duration_amph_sem = np.std(acc_duration_amph_all, axis=0) / np.sqrt(len(acc_duration_amph_all))

    return speed_duration_ctrl, speed_duration_ctrl_sem, \
           speed_duration_amph, speed_duration_amph_sem, \
           acc_duration_ctrl, acc_duration_ctrl_sem, \
           acc_duration_amph, acc_duration_amph_sem, \

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

    speed_duration_ctrl, speed_duration_ctrl_sem, \
    speed_duration_amph, speed_duration_amph_sem, \
    acc_duration_ctrl_, acc_duration_ctrl_sem, \
    acc_duration_amph, acc_duration_amph_sem = speed_data()

    right_turn_duration_ctrl_all, right_turn_duration_ctrl_sem, \
    right_turn_duration_amph_all, right_turn_duration_amph_sem, \
    left_turn_duration_ctrl_all, left_turn_duration_ctrl_sem, \
    left_turn_duration_amph_all, left_turn_duration_amph_sem = turn_data()

    plt.figure(figsize=(5, 9))
    plt.subplot(211)
    plt.bar('speed_ctrl', speed_duration_ctrl, yerr=speed_duration_ctrl_sem)
    plt.bar('acc_ctrl', acc_duration_ctrl_, yerr=acc_duration_ctrl_sem)
    plt.bar('speed_amph', speed_duration_amph, yerr=speed_duration_amph_sem)
    plt.bar('acc_amph', acc_duration_amph, yerr=acc_duration_amph_sem)
    plt.ylabel('Time (frames in 5Hz)')
    plt.title('Time spent for speed')
    plt.legend()

    plt.subplot(212)
    plt.bar('right_ctrl', right_turn_duration_ctrl_all, yerr=right_turn_duration_ctrl_sem)
    plt.bar('left_ctrl', left_turn_duration_ctrl_all, yerr=left_turn_duration_ctrl_sem)
    plt.bar('right_amph', right_turn_duration_amph_all, yerr=right_turn_duration_amph_sem)
    plt.bar('left_amph', left_turn_duration_amph_all, yerr=left_turn_duration_amph_sem)
    plt.ylabel('Time (frames in 5Hz)')
    plt.title('Time spent for turn')
    plt.legend()

    plt.show()

    return

def plot_turn():

    right_turn_duration_ctrl_all, right_turn_duration_ctrl_sem, \
    right_turn_duration_amph_all, right_turn_duration_amph_sem, \
    left_turn_duration_ctrl_all, left_turn_duration_ctrl_sem, \
    left_turn_duration_amph_all, left_turn_duration_amph_sem = turn_data()

    plt.bar('right_ctrl', right_turn_duration_ctrl_all, yerr = right_turn_duration_ctrl_sem)
    plt.bar('left_ctrl', left_turn_duration_ctrl_all, yerr = left_turn_duration_ctrl_sem)

    plt.bar('right_amph', right_turn_duration_amph_all, yerr = right_turn_duration_amph_sem)
    plt.bar('right_amph', left_turn_duration_amph_all, yerr = left_turn_duration_amph_sem)

    plt.xlabel('Frames from left turn time at 0')
    plt.ylabel('Turn (degree)')
    plt.title("Left turn triggered average")
    plt.legend()
    plt.show()

    return