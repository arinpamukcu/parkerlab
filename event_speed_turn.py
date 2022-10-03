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

def speed_bins(speed_data, turn_data, turn_angle, eventmean_data):
    speed01_events, speed02_events, speed03_events, speed04_events, speed05_events, speed06_events = ([] for i in range(6))
    speed01_duration, speed02_duration, speed03_duration, speed04_duration, speed05_duration, speed06_duration = (0 for i in range(6))

    for fr in range(0, len(turn_data)):
        if turn_angle-10 < turn_data[fr] < turn_angle+10 and speed_data[fr] <= 0.5:
            speed01_events.append(eventmean_data[fr])
            speed01_duration += 1
        if turn_angle-10 < turn_data[fr] < turn_angle+10 and 0.5 < speed_data[fr] <= 1:
            speed02_events.append(eventmean_data[fr])
            speed02_duration += 1
        if turn_angle-10 < turn_data[fr] < turn_angle+10 and 1 < speed_data[fr] <= 2:
            speed03_events.append(eventmean_data[fr])
            speed03_duration += 1
        if turn_angle-10 < turn_data[fr] < turn_angle+10 and 2 < speed_data[fr] <= 4:
            speed04_events.append(eventmean_data[fr])
            speed04_duration += 1
        if turn_angle-10 < turn_data[fr] < turn_angle+10 and 4 < speed_data[fr] <= 8:
            speed05_events.append(eventmean_data[fr])
            speed05_duration += 1
        if turn_angle-10 < turn_data[fr] < turn_angle+10 and 8 < speed_data[fr] <= 14:
            speed06_events.append(eventmean_data[fr])
            speed06_duration += 1

    event_speed_turn = [(np.sum(speed01_events) / speed01_duration) * 300,
                        (np.sum(speed02_events) / speed02_duration) * 300,
                        (np.sum(speed03_events) / speed03_duration) * 300,
                        (np.sum(speed04_events) / speed04_duration) * 300,
                        (np.sum(speed05_events) / speed05_duration) * 300,
                        (np.sum(speed06_events) / speed06_duration) * 300]

    return event_speed_turn

def data_ctrl():
    drugs = ['Clozapine', 'Haloperidol', 'MP-10', 'Olanzapine']
    dose = 'Vehicle'

    D1_est_ctrl_0, D1_est_ctrl_30, D1_est_ctrl_60, D2_est_ctrl_0, D2_est_ctrl_30, D2_est_ctrl_60 = ([] for i in
                                                                                                    range(6))

    for drug in drugs:

        experiments, _, D1_folders, D2_folders = get_animal_id(drug, dose)

        for experiment in experiments:
            print(experiment)

            speed_ctrl, speed_amph, _, _, eventmean_ctrl, eventmean_amph, _, _, _ = get_data(drug, dose, experiment)
            turn_ctrl, turn_amph, _, _ = mars_feature(drug, dose, experiment)

            est_ctrl_0 = speed_bins(speed_ctrl, turn_ctrl, 0, eventmean_ctrl)
            est_ctrl_30 = speed_bins(speed_ctrl, turn_ctrl, 30, eventmean_ctrl)
            est_ctrl_60 = speed_bins(speed_ctrl, turn_ctrl, 60, eventmean_ctrl)

            if experiment in D1_folders:
                D1_est_ctrl_0.append(est_ctrl_0)
                D1_est_ctrl_30.append(est_ctrl_30)
                D1_est_ctrl_60.append(est_ctrl_60)

            elif experiment in D2_folders:
                D2_est_ctrl_0.append(est_ctrl_0)
                D2_est_ctrl_30.append(est_ctrl_30)
                D2_est_ctrl_60.append(est_ctrl_60)

    D1_est_ctrl_0_mean = np.nanmean(np.array(D1_est_ctrl_0), axis=0)
    D1_est_ctrl_30_mean = np.nanmean(np.array(D1_est_ctrl_30), axis=0)
    D1_est_ctrl_60_mean = np.nanmean(np.array(D1_est_ctrl_60), axis=0)
    D2_est_ctrl_0_mean = np.nanmean(np.array(D2_est_ctrl_0), axis=0)
    D2_est_ctrl_30_mean = np.nanmean(np.array(D2_est_ctrl_30), axis=0)
    D2_est_ctrl_60_mean = np.nanmean(np.array(D2_est_ctrl_60), axis=0)

    D1_est_ctrl_0_sem = np.nanstd(np.array(D1_est_ctrl_0), axis=0) / np.sqrt(len(D1_est_ctrl_0))
    D1_est_ctrl_30_sem = np.nanstd(np.array(D1_est_ctrl_30), axis=0) / np.sqrt(len(D1_est_ctrl_30))
    D1_est_ctrl_60_sem = np.nanstd(np.array(D1_est_ctrl_60), axis=0) / np.sqrt(len(D1_est_ctrl_60))
    D2_est_ctrl_0_sem = np.nanstd(np.array(D2_est_ctrl_0), axis=0) / np.sqrt(len(D2_est_ctrl_0))
    D2_est_ctrl_30_sem = np.nanstd(np.array(D2_est_ctrl_30), axis=0) / np.sqrt(len(D2_est_ctrl_30))
    D2_est_ctrl_60_sem = np.nanstd(np.array(D2_est_ctrl_60), axis=0) / np.sqrt(len(D2_est_ctrl_60))


    return D1_est_ctrl_0_mean, D1_est_ctrl_30_mean, D1_est_ctrl_60_mean, \
           D2_est_ctrl_0_mean, D2_est_ctrl_30_mean, D2_est_ctrl_60_mean, \
           D1_est_ctrl_0_sem, D1_est_ctrl_30_sem, D1_est_ctrl_60_sem, \
           D2_est_ctrl_0_sem, D2_est_ctrl_30_sem, D2_est_ctrl_60_sem


def data_amph():
    drugs = ['Clozapine', 'Haloperidol', 'MP-10', 'Olanzapine']
    dose = 'Vehicle'

    D1_est_amph_0, D1_est_amph_30, D1_est_amph_60, D2_est_amph_0, D2_est_amph_30, D2_est_amph_60 = ([] for i in
                                                                                                    range(6))

    for drug in drugs:

        experiments, _, D1_folders, D2_folders = get_animal_id(drug, dose)

        for experiment in experiments:
            print(experiment + '_amph')

            speed_ctrl, speed_amph, _, _, eventmean_ctrl, eventmean_amph, _, _, _ = get_data(drug, dose, experiment)
            turn_ctrl, turn_amph, _, _ = mars_feature(drug, dose, experiment)

            est_amph_0 = speed_bins(speed_amph, turn_amph, 0, eventmean_amph)
            est_amph_30 = speed_bins(speed_amph, turn_amph, 30, eventmean_amph)
            est_amph_60 = speed_bins(speed_amph, turn_amph, 60, eventmean_amph)

            if experiment in D1_folders:
                D1_est_amph_0.append(est_amph_0)
                D1_est_amph_30.append(est_amph_30)
                D1_est_amph_60.append(est_amph_60)

            elif experiment in D2_folders:
                D2_est_amph_0.append(est_amph_0)
                D2_est_amph_30.append(est_amph_30)
                D2_est_amph_60.append(est_amph_60)

    D1_est_amph_0_mean = np.nanmean(np.array(D1_est_amph_0), axis=0)
    D1_est_amph_30_mean = np.nanmean(np.array(D1_est_amph_30), axis=0)
    D1_est_amph_60_mean = np.nanmean(np.array(D1_est_amph_60), axis=0)
    D2_est_amph_0_mean = np.nanmean(np.array(D2_est_amph_0), axis=0)
    D2_est_amph_30_mean = np.nanmean(np.array(D2_est_amph_30), axis=0)
    D2_est_amph_60_mean = np.nanmean(np.array(D2_est_amph_60), axis=0)

    D1_est_amph_0_sem = np.nanstd(np.array(D1_est_amph_0), axis=0) / np.sqrt(len(D1_est_amph_0))
    D1_est_amph_30_sem = np.nanstd(np.array(D1_est_amph_30), axis=0) / np.sqrt(len(D1_est_amph_30))
    D1_est_amph_60_sem = np.nanstd(np.array(D1_est_amph_60), axis=0) / np.sqrt(len(D1_est_amph_60))
    D2_est_amph_0_sem = np.nanstd(np.array(D2_est_amph_0), axis=0) / np.sqrt(len(D2_est_amph_0))
    D2_est_amph_30_sem = np.nanstd(np.array(D2_est_amph_30), axis=0) / np.sqrt(len(D2_est_amph_30))
    D2_est_amph_60_sem = np.nanstd(np.array(D2_est_amph_60), axis=0) / np.sqrt(len(D2_est_amph_60))

    return D1_est_amph_0_mean, D1_est_amph_30_mean, D1_est_amph_60_mean, \
           D2_est_amph_0_mean, D2_est_amph_30_mean, D2_est_amph_60_mean, \
           D1_est_amph_0_sem, D1_est_amph_30_sem, D1_est_amph_60_sem, \
           D2_est_amph_0_sem, D2_est_amph_30_sem, D2_est_amph_60_sem


def plot():
    D1_est_ctrl_0_mean, D1_est_ctrl_30_mean, D1_est_ctrl_60_mean, \
    D2_est_ctrl_0_mean, D2_est_ctrl_30_mean, D2_est_ctrl_60_mean, \
    D1_est_ctrl_0_sem, D1_est_ctrl_30_sem, D1_est_ctrl_60_sem, \
    D2_est_ctrl_0_sem, D2_est_ctrl_30_sem, D2_est_ctrl_60_sem = data_ctrl()

    D1_est_amph_0_mean, D1_est_amph_30_mean, D1_est_amph_60_mean, \
    D2_est_amph_0_mean, D2_est_amph_30_mean, D2_est_amph_60_mean, \
    D1_est_amph_0_sem, D1_est_amph_30_sem, D1_est_amph_60_sem, \
    D2_est_amph_0_sem, D2_est_amph_30_sem, D2_est_amph_60_sem = data_amph()
    # D1_est_amph = pickle.load(open("D1_est_amph.pkl", "rb"))
    # D2_est_amph = pickle.load(open("D2_est_amph.pkl", "rb"))

    x = range(6)

    plt.figure(figsize=(5, 9))
    plt.subplot(211)
    plt.plot(D1_est_ctrl_0_mean, label='D1 ctrl 0°', color='k')
    plt.fill_between(x, D1_est_ctrl_0_mean + D1_est_ctrl_0_sem, D1_est_ctrl_0_mean - D1_est_ctrl_0_sem, color='k', alpha=0.2)
    plt.plot(D1_est_ctrl_30_mean, label='D1 ctrl 30°', color='k', linestyle='--')
    plt.fill_between(x, D1_est_ctrl_30_mean + D1_est_ctrl_30_sem, D1_est_ctrl_30_mean - D1_est_ctrl_30_sem, color='k', alpha=0.2)
    plt.plot(D1_est_ctrl_60_mean, label='D1 ctrl 60°', color='k', linestyle=':')
    plt.fill_between(x, D1_est_ctrl_60_mean + D1_est_ctrl_60_sem, D1_est_ctrl_60_mean - D1_est_ctrl_60_sem, color='k', alpha=0.2)
    plt.plot(D1_est_amph_0_mean, label='D1 amph 0°', color='b')
    plt.fill_between(x, D1_est_amph_0_mean + D1_est_amph_0_sem, D1_est_amph_0_mean - D1_est_amph_0_sem, color='b', alpha=0.2)
    plt.plot(D1_est_amph_30_mean, label='D1 amph 30°', color='b', linestyle='--')
    plt.fill_between(x, D1_est_amph_30_mean + D1_est_amph_30_sem, D1_est_amph_30_mean - D1_est_amph_30_sem, color='b', alpha=0.2)
    plt.plot(D1_est_amph_60_mean, label='D1 amph 60°', color='b', linestyle=':')
    plt.fill_between(x, D1_est_amph_60_mean + D1_est_amph_60_sem, D1_est_amph_60_mean - D1_est_amph_60_sem, color='b', alpha=0.2)
    x_default = [0, 1, 2, 3, 4, 5];
    x_new = ['<0.5', '0.5-1', '1-2', '2-4', '4-8', '8-14'];
    plt.xticks(x_default, x_new);
    plt.ylim((0, 2.5))
    plt.xlabel('Locomotor speed bin (cm/s)')
    plt.ylabel('Ca event rate (event/min)')
    plt.title('D1 SPNs')
    plt.suptitle('Ca spike per speed bout')
    plt.legend()

    plt.subplot(212)
    plt.plot(D2_est_ctrl_0_mean, label='D2 ctrl 0°', color='k')
    plt.fill_between(x, D2_est_ctrl_0_mean + D2_est_ctrl_0_sem, D2_est_ctrl_0_mean - D2_est_ctrl_0_sem, color='k', alpha=0.2)
    plt.plot(D2_est_ctrl_30_mean, label='D2 ctrl 30°', color='k', linestyle='--')
    plt.fill_between(x, D2_est_ctrl_30_mean + D2_est_ctrl_30_sem, D2_est_ctrl_30_mean - D2_est_ctrl_30_sem, color='k', alpha=0.2)
    plt.plot(D2_est_ctrl_60_mean, label='D2 ctrl 60°', color='k', linestyle=':')
    plt.fill_between(x, D2_est_ctrl_60_mean + D2_est_ctrl_60_sem, D2_est_ctrl_60_mean - D2_est_ctrl_60_sem, color='k', alpha=0.2)
    plt.plot(D2_est_amph_0_mean, label='D2 amph 0°', color='r')
    plt.fill_between(x, D2_est_amph_0_mean + D2_est_amph_0_sem, D2_est_amph_0_mean - D2_est_amph_0_sem, color='r', alpha=0.2)
    plt.plot(D2_est_amph_30_mean, label='D2 amph 30°', color='r', linestyle='--')
    plt.fill_between(x, D2_est_amph_30_mean + D2_est_amph_30_sem, D2_est_amph_30_mean - D2_est_amph_30_sem, color='r', alpha=0.2)
    plt.plot(D2_est_amph_60_mean, label='D2 amph 60°', color='r', linestyle=':')
    plt.fill_between(x, D2_est_amph_60_mean + D2_est_amph_60_sem, D2_est_amph_60_mean - D2_est_amph_60_sem, color='r', alpha=0.2)
    x_default = [0, 1, 2, 3, 4, 5];
    x_new = ['<0.5', '0.5-1', '1-2', '2-4', '4-8', '8-14'];
    plt.xticks(x_default, x_new);
    plt.ylim((0, 2.5))
    plt.xlabel('Locomotor speed bin (cm/s)')
    plt.ylabel('Ca event rate (event/min)')
    plt.title('D2 SPNs')
    plt.legend()
    plt.show()

    return