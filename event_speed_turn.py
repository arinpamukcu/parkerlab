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
    nospeed_events, lospeed_events, midspeed_events, hispeed_events, acc_events = ([] for i in range(5))
    nospeed_duration, lospeed_duration, midspeed_duration, hispeed_duration, acc_duration = (0 for i in range(5))

    for fr in range(0, len(turn_data)):
        if turn_angle-5 < turn_data[fr] < turn_angle+5 and speed_data[fr] < 1:
            nospeed_events.append(eventmean_data[fr])
            nospeed_duration += 1
        if turn_angle-5 < turn_data[fr] < turn_angle+5 and 1 < speed_data[fr] <= 5:
            lospeed_events.append(eventmean_data[fr])
            lospeed_duration += 1
        if turn_angle-5 < turn_data[fr] < turn_angle+5 and 5 < speed_data[fr] <= 10:
            midspeed_events.append(eventmean_data[fr])
            midspeed_duration += 1
        if turn_angle-5 < turn_data[fr] < turn_angle+5 and 10 < speed_data[fr]:
            hispeed_events.append(eventmean_data[fr])
            hispeed_duration += 1

    event_speed_turn = [(np.sum(nospeed_events) / nospeed_duration) * 300,
                       (np.sum(lospeed_events) / lospeed_duration) * 300,
                       (np.sum(midspeed_events) / midspeed_duration) * 300,
                       (np.sum(hispeed_events) / hispeed_duration) * 300]

    return event_speed_turn

def data_ctrl():
    drugs = ['Clozapine', 'Haloperidol', 'MP-10', 'Olanzapine']
    dose = 'Vehicle'

    for drug in drugs:

        experiments, _, D1_folders, D2_folders = get_animal_id(drug, dose)

        D1_est_ctrl = {}
        D2_est_ctrl = {}

        for experiment in experiments:
            print(experiment)

            speed_ctrl, speed_amph, _, _, eventmean_ctrl, eventmean_amph, _, _, _ = get_data(drug, dose, experiment)
            turn_ctrl, turn_amph, _, _ = mars_feature(drug, dose, experiment)

            est_ctrl_0 = speed_bins(speed_ctrl, turn_ctrl, 0, eventmean_ctrl)
            est_ctrl_30 = speed_bins(speed_ctrl, turn_ctrl, 30, eventmean_ctrl)
            est_ctrl_60 = speed_bins(speed_ctrl, turn_ctrl, 60, eventmean_ctrl)

            if experiment in D1_folders:
                D1_est_ctrl['0'] = est_ctrl_0
                D1_est_ctrl['30'] = est_ctrl_30
                D1_est_ctrl['60'] = est_ctrl_60

            elif experiment in D2_folders:
                D2_est_ctrl['0'] = est_ctrl_0
                D2_est_ctrl['30'] = est_ctrl_30
                D2_est_ctrl['60'] = est_ctrl_60

    pickle.dump(D1_est_ctrl, open("D1_est_ctrl.pkl", "wb"))
    pickle.dump(D2_est_ctrl, open("D2_est_ctrl.pkl", "wb"))

    return D1_est_ctrl, D2_est_ctrl


def data_amph():
    drugs = ['Clozapine']
    dose = 'Vehicle'

    for drug in drugs:

        experiments, _, D1_folders, D2_folders = get_animal_id(drug, dose)

        D1_est_amph = {}
        D2_est_amph = {}

        for experiment in experiments:
            print(experiment + '_amph')

            speed_ctrl, speed_amph, _, _, eventmean_ctrl, eventmean_amph, _, _, _ = get_data(drug, dose, experiment)
            turn_ctrl, turn_amph, _, _ = mars_feature(drug, dose, experiment)

            est_amph_0 = speed_bins(speed_amph, turn_amph, 0, eventmean_amph)
            est_amph_30 = speed_bins(speed_amph, turn_amph, 30, eventmean_amph)
            est_amph_60 = speed_bins(speed_amph, turn_amph, 60, eventmean_amph)

            if experiment in D1_folders:
                D1_est_amph['0'] = est_amph_0
                D1_est_amph['30'] = est_amph_30
                D1_est_amph['60'] = est_amph_60

            elif experiment in D2_folders:
                D2_est_amph['0'] = est_amph_0
                D2_est_amph['30'] = est_amph_30
                D2_est_amph['60'] = est_amph_60

    pickle.dump(D1_est_amph, open("D1_est_amph.pkl", "wb"))
    pickle.dump(D2_est_amph, open("D2_est_amph.pkl", "wb"))

    return D1_est_amph, D2_est_amph


def plot():

    # D1_est_ctrl, D2_est_ctrl = data_ctrl()
    D1_est_ctrl = pickle.load(open("D1_est_ctrl.pkl", "rb"))
    D2_est_ctrl = pickle.load(open("D2_est_ctrl.pkl", "rb"))
    # D1_est_amph, D2_est_amph = data_amph()
    D1_est_amph = pickle.load(open("D1_est_amph.pkl", "rb"))
    D2_est_amph = pickle.load(open("D2_est_amph.pkl", "rb"))

    plt.figure(figsize=(5, 9))
    plt.subplot(211)
    plt.plot(D1_est_ctrl['0'], label='D1 ctrl 0', color='k')
    plt.plot(D1_est_ctrl['30'], label='D1 ctrl 30', color='k', linestyle='--')
    plt.plot(D1_est_ctrl['60'], label='D1 ctrl 60', color='k', linestyle=':')
    plt.plot(D1_est_amph['0'], label='D1 amph 0', color='b')
    plt.plot(D1_est_amph['30'], label='D1 amph 30', color='b', linestyle='--')
    plt.plot(D1_est_amph['60'], label='D1 amph 60', color='b', linestyle=':')
    x_default = [0, 1, 2, 3];
    x_new = ['<1', '1-5', '5-10', '>10'];
    plt.xticks(x_default, x_new);
    plt.ylim((0, 2.5))
    plt.xlabel('Locomotor speed bin (cm/s)')
    plt.ylabel('Ca event rate (event/min)')
    plt.title('D1 SPNs')
    plt.suptitle('Ca spike per speed bout')
    plt.legend()

    plt.subplot(212)
    plt.plot(D2_est_ctrl['0'], label='D2 ctrl 0', color='k')
    plt.plot(D2_est_ctrl['30'], label='D2 ctrl 30', color='k', linestyle='--')
    plt.plot(D2_est_ctrl['60'], label='D2 ctrl 60', color='k', linestyle=':')
    plt.plot(D2_est_amph['0'], label='D2 amph 0', color='r')
    plt.plot(D2_est_amph['30'], label='D2 amph 30', color='r', linestyle='--')
    plt.plot(D2_est_amph['60'], label='D2 amph 60', color='r', linestyle=':')
    x_default = [0, 1, 2, 3];
    x_new = ['<1', '1-5', '5-10', '>10'];
    plt.xticks(x_default, x_new);
    plt.ylim((0, 2.5))
    plt.xlabel('Locomotor speed bin (cm/s)')
    plt.ylabel('Ca event rate (event/min)')
    plt.title('D2 SPNs')
    plt.legend()
    plt.show()

    return