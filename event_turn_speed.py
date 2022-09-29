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
    farleft_events, left_events, straight_events, right_events, farright_events = ([] for i in range(5))
    farleft_duration, left_duration, straight_duration, right_duration,farright_duration = (0 for i in range(5))

    for fr in range(0, len(turn_data)):
        if speed_data[fr] < speed and -65 < turn_data[fr] < -55:
            farleft_events.append(eventmean_data[fr])
            farleft_duration += 1
        if speed_data[fr] < speed and -35 < turn_data[fr] < -25:
            left_events.append(eventmean_data[fr])
            left_duration += 1
        if speed_data[fr] < speed and -5 < turn_data[fr] < 5:
            straight_events.append(eventmean_data[fr])
            straight_duration += 1
        if speed_data[fr] < speed and 25 < turn_data[fr] < 35:
            right_events.append(eventmean_data[fr])
            right_duration += 1
        if speed_data[fr] < speed and 25 < turn_data[fr] < 35:
            farright_events.append(eventmean_data[fr])
            farright_duration += 1

    event_turn_speed = [(np.sum(farleft_events) / farleft_duration) * 300,
                       (np.sum(left_events) / left_duration) * 300,
                       (np.sum(straight_events) / straight_duration) * 300,
                       (np.sum(right_events) / right_duration) * 300,
                       (np.sum(farright_events) / farright_duration) * 300]

    return event_turn_speed

def data_ctrl():
    drugs = ['Clozapine', 'Haloperidol', 'MP-10', 'Olanzapine']
    dose = 'Vehicle'

    for drug in drugs:

        experiments, _, D1_folders, D2_folders = get_animal_id(drug, dose)

        D1_ets_ctrl = {}
        D2_ets_ctrl = {}

        for experiment in experiments:
            print(experiment)

            speed_ctrl, speed_amph, _, _, eventmean_ctrl, eventmean_amph, _, _, _ = get_data(drug, dose, experiment)
            turn_ctrl, turn_amph, _, _ = mars_feature(drug, dose, experiment)

            ets_ctrl_0 = speed_bins(speed_ctrl, turn_ctrl, 1, eventmean_ctrl)
            ets_ctrl_30 = speed_bins(speed_ctrl, turn_ctrl, 1, eventmean_ctrl)
            ets_ctrl_60 = speed_bins(speed_ctrl, turn_ctrl, 1, eventmean_ctrl)

            if experiment in D1_folders:
                D1_ets_ctrl['0'] = ets_ctrl_0
                D1_ets_ctrl['30'] = ets_ctrl_30
                D1_ets_ctrl['60'] = ets_ctrl_60

            elif experiment in D2_folders:
                D2_ets_ctrl['0'] = ets_ctrl_0
                D2_ets_ctrl['30'] = ets_ctrl_30
                D2_ets_ctrl['60'] = ets_ctrl_60

    pickle.dump(D1_ets_ctrl, open("D1_ets_ctrl.pkl", "wb"))
    pickle.dump(D2_ets_ctrl, open("D2_ets_ctrl.pkl", "wb"))

    return D1_ets_ctrl, D2_ets_ctrl


def data_amph():
    drugs = ['Clozapine']
    dose = 'Vehicle'

    for drug in drugs:

        experiments, _, D1_folders, D2_folders = get_animal_id(drug, dose)

        D1_ets_amph = {}
        D2_ets_amph = {}

        for experiment in experiments:
            print(experiment + '_amph')

            speed_ctrl, speed_amph, _, _, eventmean_ctrl, eventmean_amph, _, _, _ = get_data(drug, dose, experiment)
            turn_ctrl, turn_amph, _, _ = mars_feature(drug, dose, experiment)

            ets_amph_0 = speed_bins(speed_amph, turn_amph, 1, eventmean_amph)
            ets_amph_30 = speed_bins(speed_amph, turn_amph, 1, eventmean_amph)
            ets_amph_60 = speed_bins(speed_amph, turn_amph, 1, eventmean_amph)

            if experiment in D1_folders:
                D1_ets_amph['0'] = ets_amph_0
                D1_ets_amph['30'] = ets_amph_30
                D1_ets_amph['60'] = ets_amph_60

            elif experiment in D2_folders:
                D2_ets_amph['0'] = ets_amph_0
                D2_ets_amph['30'] = ets_amph_30
                D2_ets_amph['60'] = ets_amph_60

    pickle.dump(D1_ets_amph, open("D1_ets_amph.pkl", "wb"))
    pickle.dump(D2_ets_amph, open("D2_ets_amph.pkl", "wb"))

    return D1_ets_amph, D2_ets_amph


def plot():

    # D1_ets_ctrl, D2_ets_ctrl = data_ctrl()
    D1_ets_ctrl = pickle.load(open("D1_ets_ctrl.pkl", "rb"))
    D2_ets_ctrl = pickle.load(open("D2_ets_ctrl.pkl", "rb"))
    # D1_ets_amph, D2_ets_amph = data_amph()
    D1_ets_amph = pickle.load(open("D1_ets_amph.pkl", "rb"))
    D2_ets_amph = pickle.load(open("D2_ets_amph.pkl", "rb"))

    plt.figure(figsize=(5, 9))
    plt.subplot(211)
    plt.plot(D1_ets_ctrl['0'], label='D1 ctrl 0', color='k')
    plt.plot(D1_ets_ctrl['30'], label='D1 ctrl 30', color='k', linestyle='--')
    plt.plot(D1_ets_ctrl['60'], label='D1 ctrl 60', color='k', linestyle=':')
    plt.plot(D1_ets_amph['0'], label='D1 amph 0', color='b')
    plt.plot(D1_ets_amph['30'], label='D1 amph 30', color='b', linestyle='--')
    plt.plot(D1_ets_amph['60'], label='D1 amph 60', color='b', linestyle=':')
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
    plt.plot(D2_ets_ctrl['0'], label='D2 ctrl 0', color='k')
    plt.plot(D2_ets_ctrl['30'], label='D2 ctrl 30', color='k', linestyle='--')
    plt.plot(D2_ets_ctrl['60'], label='D2 ctrl 60', color='k', linestyle=':')
    plt.plot(D2_ets_amph['0'], label='D2 amph 0', color='r')
    plt.plot(D2_ets_amph['30'], label='D2 amph 30', color='r', linestyle='--')
    plt.plot(D2_ets_amph['60'], label='D2 amph 60', color='r', linestyle=':')
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