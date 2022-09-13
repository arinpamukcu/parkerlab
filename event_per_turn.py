# Created by Arin Pamukcu, PhD on August 2022

# y-axis: Ca event rate (event/min)
# x-axis: Locomotor speed bin (cm/s)
# bin: <0.5, 0.5-1, 1-2, 2-4, 4-8, 8-14

from data import *
from info import *
from mars import *
import numpy as np
import matplotlib.pyplot as plt
import pdb

def turn_bins(mars_turn_data, eventmean_data):
    bin1r_events, bin2r_events, bin3r_events, bin4r_events, bin5r_events, bin6r_events, \
        bin1l_events, bin2l_events, bin3l_events, bin4l_events, bin5l_events, bin6l_events = ([] for i in range(12))
    bin1r_duration, bin2r_duration, bin3r_duration, bin4r_duration, bin5r_duration, bin6r_duration, \
        bin1l_duration, bin2l_duration, bin3l_duration, bin4l_duration, bin5l_duration, bin6l_duration = (0 for i in range(12))

    for t in range(0, len(mars_turn_data)):
        if -180 < mars_turn_data[t] <= -150:
            bin1l_events.append(eventmean_data[t])
            bin1l_duration += 1
        elif -150 < mars_turn_data[t] <= -120:
            bin2l_events.append(eventmean_data[t])
            bin2l_duration += 1
        elif -120 < mars_turn_data[t] <= -90:
            bin3l_events.append(eventmean_data[t])
            bin3l_duration += 1
        elif -90 < mars_turn_data[t] <= -60:
            bin4l_events.append(eventmean_data[t])
            bin4l_duration += 1
        elif -60 < mars_turn_data[t] <= -30:
            bin5l_events.append(eventmean_data[t])
            bin6l_duration += 1
        elif -30 < mars_turn_data[t] <= 0:
            bin6l_events.append(eventmean_data[t])
            bin6l_duration += 1
        elif 0 < mars_turn_data[t] <= 30:
            bin1r_events.append(eventmean_data[t])
            bin1r_duration += 1
        elif 30 < mars_turn_data[t] <= 60:
            bin2r_events.append(eventmean_data[t])
            bin2r_duration += 1
        elif 60 < mars_turn_data[t] <= 90:
            bin3r_events.append(eventmean_data[t])
            bin3r_duration += 1
        elif 90 < mars_turn_data[t] <= 120:
            bin4r_events.append(eventmean_data[t])
            bin4r_duration += 1
        elif 120 < mars_turn_data[t] <= 150:
            bin5r_events.append(eventmean_data[t])
            bin5r_duration += 1
        elif 150 < mars_turn_data[t] <= 180:
            bin6r_events.append(eventmean_data[t])
            bin6r_duration += 1

    event_per_right_turn = [(np.sum(bin1r_events)/bin1r_duration)*300, (np.sum(bin2r_events)/bin2r_duration)*300,
                            (np.sum(bin3r_events)/bin3r_duration)*300, (np.sum(bin3r_events)/bin3r_duration)*300,
                            (np.sum(bin4r_events)/bin5r_duration)*300, (np.sum(bin6r_events)/bin6r_duration)*300]

    event_per_left_turn = [(np.sum(bin1l_events)/bin1l_duration)*300, (np.sum(bin2l_events)/bin2l_duration)*300,
                            (np.sum(bin3l_events)/bin3l_duration)*300, (np.sum(bin3l_events)/bin3l_duration)*300,
                            (np.sum(bin4l_events)/bin5l_duration)*300, (np.sum(bin6l_events)/bin6l_duration)*300]

    return event_per_right_turn, event_per_left_turn


def data():
    D1_event_per_right_turn_ctrl = []
    D1_event_per_left_turn_ctrl = []
    D1_event_per_right_turn_amph = []
    D1_event_per_left_turn_amph = []

    D2_event_per_right_turn_ctrl = []
    D2_event_per_left_turn_ctrl = []
    D2_event_per_right_turn_amph = []
    D2_event_per_left_turn_amph = []

    drugs = ['Clozapine']
    # drugs = get_drug()
    dose = 'Vehicle'

    for drug in drugs:

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)

        for experiment in experiments:
            print(experiment)

            _, _, _, _, eventmean_ctrl, eventmean_amph, neuron, time_ctrl, time_amph = get_data(drug, dose, experiment)

            mars_turn_angle_ctrl, mars_turn_angle_amph, _, _ = mars_feature(drug, dose, experiment)

            event_per_right_turn_ctrl, event_per_left_turn_ctrl = turn_bins(mars_turn_angle_ctrl, eventmean_ctrl)
            event_per_right_turn_amph, event_per_left_turn_amph = turn_bins(mars_turn_angle_amph, eventmean_amph)

            if experiment in D1_folders:
                D1_event_per_right_turn_ctrl.append(event_per_right_turn_ctrl)
                D1_event_per_left_turn_ctrl.append(event_per_left_turn_ctrl)
                D1_event_per_right_turn_amph.append(event_per_right_turn_amph)
                D1_event_per_left_turn_amph.append(event_per_left_turn_amph)

            elif experiment in D2_folders:
                D2_event_per_right_turn_ctrl.append(event_per_right_turn_ctrl)
                D2_event_per_left_turn_ctrl.append(event_per_left_turn_ctrl)
                D2_event_per_right_turn_amph.append(event_per_right_turn_amph)
                D2_event_per_left_turn_amph.append(event_per_left_turn_amph)

    return D1_event_per_right_turn_ctrl, D1_event_per_right_turn_amph, \
           D1_event_per_left_turn_ctrl, D1_event_per_left_turn_amph, \
           D2_event_per_right_turn_ctrl, D2_event_per_right_turn_amph, \
           D2_event_per_left_turn_ctrl, D2_event_per_left_turn_amph


def plot():

    D1_event_per_right_turn_ctrl, D1_event_per_right_turn_amph, \
    D1_event_per_left_turn_ctrl, D1_event_per_left_turn_amph, \
    D2_event_per_right_turn_ctrl, D2_event_per_right_turn_amph, \
    D2_event_per_left_turn_ctrl, D2_event_per_left_turn_amph = data()

    plt.figure(figsize=(5, 9))
    plt.subplot(211)
    plt.plot(np.mean(D1_event_per_left_turn_ctrl, axis=0), label='D1 ctrl', color='k')
    plt.plot(np.mean(D1_event_per_left_turn_amph, axis=0), label='D1 amph', color='b')
    x_default = [0, 1, 2, 3, 4, 5];
    x_new = ['30', '60', '90', '120', '150', '180'];
    plt.xticks(x_default, x_new);
    plt.ylim((0, 2.5))
    plt.xlabel('Turn bin (degrees)')
    plt.ylabel('Ca event rate (event/min)')
    plt.title('D1 SPNs')
    plt.suptitle('Ca activity per left turn bout')
    plt.legend()

    plt.subplot(212)
    plt.plot(np.mean(D2_event_per_left_turn_ctrl, axis=0), label='D2 ctrl', color='k')
    plt.plot(np.mean(D2_event_per_left_turn_amph, axis=0), label='D2 amph', color='r')
    x_default = [0, 1, 2, 3, 4, 5];
    x_new = ['30', '60', '90', '120', '150', '180'];
    plt.xticks(x_default, x_new);
    plt.ylim((0, 2.5))
    plt.xlabel('Turn bin (degrees)')
    plt.ylabel('Ca event rate (event/min)')
    plt.title('D2 SPNs')
    plt.legend()
    plt.show()

    plt.figure(figsize=(5, 9))
    plt.subplot(211)
    plt.plot(np.mean(D1_event_per_right_turn_ctrl, axis=0), label='D1 ctrl', color='k')
    plt.plot(np.mean(D1_event_per_right_turn_amph, axis=0), label='D1 amph', color='b')
    x_default = [0, 1, 2, 3, 4, 5];
    x_new = ['30', '60', '90', '120', '150', '180'];
    plt.xticks(x_default, x_new);
    plt.ylim((0, 2.5))
    plt.xlabel('Turn bin (degrees)')
    plt.ylabel('Ca event rate (event/min)')
    plt.title('D1 SPNs')
    plt.suptitle('Ca activity per right turn bout')
    plt.legend()

    plt.subplot(212)
    plt.plot(np.mean(D2_event_per_right_turn_ctrl, axis=0), label='D2 ctrl', color='k')
    plt.plot(np.mean(D2_event_per_right_turn_amph, axis=0), label='D2 amph', color='r')
    x_default = [0, 1, 2, 3, 4, 5];
    x_new = ['30', '60', '90', '120', '150', '180'];
    plt.xticks(x_default, x_new);
    plt.ylim((0, 2.5))
    plt.xlabel('Turn bin (degrees)')
    plt.ylabel('Ca event rate (event/min)')
    plt.title('D2 SPNs')
    plt.legend()
    plt.show()

