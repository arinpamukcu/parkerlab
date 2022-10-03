# Created by Arin Pamukcu, PhD on August 2022

# y-axis: Ca event rate (event/min)
# x-axis: Locomotor speed bin (cm/s)

from data import *
from info import *
from mars import *
import pickle
import numpy as np
import matplotlib.pyplot as plt
import pdb

def speed_bins(speed_data, turn_data, speed, eventmean_data):
    left60_events, left30_events, straight_events, right30_events, right60_events = ([] for i in range(5))
    left60_duration, left30_duration, straight_duration, right30_duration, right60_duration = (0 for i in range(5))

    for fr in range(0, len(turn_data)):
        if speed_data[fr] < speed and -70 < turn_data[fr] < -50:
            left60_events.append(eventmean_data[fr])
            left60_duration += 1
        if speed_data[fr] < speed and -40 < turn_data[fr] < -20:
            left30_events.append(eventmean_data[fr])
            left30_duration += 1
        if speed_data[fr] < speed and -10 < turn_data[fr] < 10:
            straight_events.append(eventmean_data[fr])
            straight_duration += 1
        if speed_data[fr] < speed and 20 < turn_data[fr] < 40:
            right30_events.append(eventmean_data[fr])
            right30_duration += 1
        if speed_data[fr] < speed and 50 < turn_data[fr] < 70:
            right60_events.append(eventmean_data[fr])
            right60_duration += 1

    event_turn_speed = [(np.sum(left60_events) / left60_duration) * 300,
                        (np.sum(left30_events) / left30_duration) * 300,
                        (np.sum(straight_events) / straight_duration) * 300,
                        (np.sum(right30_events) / right30_duration) * 300,
                        (np.sum(right60_events) / right60_duration) * 300]

    return event_turn_speed

def data_ctrl():
    drugs = ['Clozapine', 'Haloperidol', 'MP-10', 'Olanzapine']
    # drugs = ['Clozapine']
    dose = 'Vehicle'

    D1_ets_ctrl = []
    D2_ets_ctrl = []

    for drug in drugs:

        experiments, _, D1_folders, D2_folders = get_animal_id(drug, dose)

        for experiment in experiments:
            print(experiment)

            speed_ctrl, speed_amph, _, _, eventmean_ctrl, eventmean_amph, _, _, _ = get_data(drug, dose, experiment)
            turn_ctrl, turn_amph, _, _ = mars_feature(drug, dose, experiment)

            ets_ctrl = speed_bins(speed_ctrl, turn_ctrl, 1, eventmean_ctrl)

            if experiment in D1_folders:
                D1_ets_ctrl.append(ets_ctrl)

            elif experiment in D2_folders:
                D2_ets_ctrl.append(ets_ctrl)

    D1_ets_ctrl_mean = np.nanmean(D1_ets_ctrl, axis=0)
    D2_ets_ctrl_mean = np.nanmean(D2_ets_ctrl, axis=0)

    D1_ets_ctrl_sem = np.nanstd(D1_ets_ctrl, axis=0) / np.sqrt(len(D1_ets_ctrl))
    D2_ets_ctrl_sem = np.nanstd(D2_ets_ctrl, axis=0) / np.sqrt(len(D2_ets_ctrl))

    # pickle.dump(D1_ets_ctrl_mean, open("D1_ets_ctrl_mean.pkl", "wb"))
    # pickle.dump(D1_ets_ctrl_sem, open("D1_ets_ctrl_sem.pkl", "wb"))
    # pickle.dump(D2_ets_ctrl_mean, open("D2_ets_ctrl_mean.pkl", "wb"))
    # pickle.dump(D2_ets_ctrl_sem, open("D2_ets_ctrl_sem.pkl", "wb"))

    return D1_ets_ctrl_mean, D2_ets_ctrl_mean, D1_ets_ctrl_sem, D2_ets_ctrl_sem


def data_amph():
    drugs = ['Clozapine', 'Haloperidol', 'MP-10', 'Olanzapine']
    # drugs = ['Clozapine']
    dose = 'Vehicle'

    D1_ets_amph = []
    D2_ets_amph = []

    for drug in drugs:

        experiments, _, D1_folders, D2_folders = get_animal_id(drug, dose)

        for experiment in experiments:
            print(experiment + '_amph')

            speed_ctrl, speed_amph, _, _, eventmean_ctrl, eventmean_amph, _, _, _ = get_data(drug, dose, experiment)
            turn_ctrl, turn_amph, _, _ = mars_feature(drug, dose, experiment)

            ets_amph = speed_bins(speed_amph, turn_amph, 1, eventmean_amph)

            if experiment in D1_folders:
                D1_ets_amph.append(ets_amph)

            elif experiment in D2_folders:
                D2_ets_amph.append(ets_amph)

    D1_ets_amph_mean = np.nanmean(D1_ets_amph, axis=0)
    D2_ets_amph_mean = np.nanmean(D2_ets_amph, axis=0)

    D1_ets_amph_sem = np.nanstd(D1_ets_amph, axis=0) / np.sqrt(len(D1_ets_amph))
    D2_ets_amph_sem = np.nanstd(D2_ets_amph, axis=0) / np.sqrt(len(D2_ets_amph))

    # pickle.dump(D1_ets_amph_mean, open("D1_ets_amph_mean.pkl", "wb"))
    # pickle.dump(D1_ets_amph_sem, open("D1_ets_amph_sem.pkl", "wb"))
    # pickle.dump(D2_ets_amph_mean, open("D2_ets_amph_mean.pkl", "wb"))
    # pickle.dump(D2_ets_amph_sem, open("D2_ets_amph_sem.pkl", "wb"))

    return D1_ets_amph_mean, D2_ets_amph_mean, D1_ets_amph_sem, D2_ets_amph_sem


def plot():

    D1_ets_ctrl_mean, D2_ets_ctrl_mean, D1_ets_ctrl_sem, D2_ets_ctrl_sem = data_ctrl()
    D1_ets_amph_mean, D2_ets_amph_mean, D1_ets_amph_sem, D2_ets_amph_sem = data_amph()

    x = range(5)

    plt.figure(figsize=(5, 9))
    plt.subplot(211)
    plt.plot(D1_ets_ctrl_mean, label='D1 ctrl', color='k')
    plt.fill_between(x, D1_ets_ctrl_mean + D1_ets_ctrl_sem, D1_ets_ctrl_mean - D1_ets_ctrl_sem, color='k', alpha=0.2)
    plt.plot(D1_ets_amph_mean, label='D1 amph', color='b')
    plt.fill_between(x, D1_ets_amph_mean + D1_ets_amph_sem, D1_ets_amph_mean - D1_ets_amph_sem, color='b', alpha=0.2)
    x_default = [0, 1, 2, 3, 4];
    x_new = ['right 60°', 'right 30°', 'straight 0°', 'left 30°', 'left 60°'];
    plt.xticks(x_default, x_new);
    plt.ylim((0, 2))
    # plt.xlabel('Locomotor speed bin (cm/s)')
    plt.ylabel('Ca event rate (event/min)')
    plt.title('D1 SPNs')
    plt.suptitle('Ca events for speed: 0-1 cm/s')
    plt.legend()

    plt.subplot(212)
    plt.plot(D2_ets_ctrl_mean, label='D2 ctrl', color='k')
    plt.fill_between(x, D2_ets_ctrl_mean + D2_ets_ctrl_sem, D2_ets_ctrl_mean - D2_ets_ctrl_sem, color='k', alpha=0.2)
    plt.plot(D2_ets_amph_mean, label='D2 amph', color='r')
    plt.fill_between(x, D2_ets_amph_mean + D2_ets_amph_sem, D2_ets_amph_mean - D2_ets_amph_sem, color='r', alpha=0.2)
    x_default = [0, 1, 2, 3, 4];
    x_new = ['right 60°', 'right 30°', 'straight 0°', 'left 30°', 'left 60°'];
    plt.xticks(x_default, x_new);
    plt.ylim((0, 2))
    # plt.xlabel('Locomotor speed bin (cm/s)')
    plt.ylabel('Ca event rate (event/min)')
    plt.title('D2 SPNs')
    plt.legend()
    plt.show()

    return