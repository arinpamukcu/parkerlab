# Created by Arin Pamukcu, PhD on August 2022

# y-axis: Ca event rate (event/min)
# x-axis: Locomotor speed bin (cm/s)
# bin: <0.5, 0.5-1, 1-2, 2-4, 4-8, 8-14

from data import *
from info import *
import numpy as np
import matplotlib.pyplot as plt

def event_per_speed():
    # event_per_speed_dict = {}
    D1_event_per_speed_ctrl = []
    D1_event_per_speed_amph = []
    D2_event_per_speed_ctrl = []
    D2_event_per_speed_amph = []

    # drugs = ['Clozapine']
    drugs = get_drug()
    dose = 'Vehicle'

    for drug in drugs:

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)

        for experiment in experiments:
            print(experiment)

            _, _, calcium_ctrl_events, calcium_amph_events, \
            eventmean_ctrl, eventmean_amph, neuron, time_ctrl, time_amph = get_data(drug, dose, experiment)

            bin1_events_ctrl, bin2_events_ctrl, bin3_events_ctrl = ([] for i in range(3))
            bin1_events_amph, bin2_events_amph, bin3_events_amph = ([] for i in range(3))
            bin1_duration_ctrl, bin2_duration_ctrl, bin3_duration_ctrl = (0 for i in range(3))
            bin1_duration_amph, bin2_duration_amph, bin3_duration_amph = (0 for i in range(3))

            for t in range(0, len(turn_ctrl)):
                if turn_ctrl[t] < 0.5:
                    bin1_events_ctrl.append(eventmean_ctrl[t])
                    bin1_duration_ctrl += 1
                if 0.5 <= turn_ctrl[t] < 1:
                    bin2_events_ctrl.append(eventmean_ctrl[t])
                    bin2_duration_ctrl += 1
                if 1 <= turn_ctrl[t] < 2:
                    bin3_events_ctrl.append(eventmean_ctrl[t])
                    bin3_duration_ctrl += 1

            event_per_speed_ctrl = [(np.sum(bin1_events_ctrl)/bin1_duration_ctrl)*300,
                                    (np.sum(bin2_events_ctrl)/bin2_duration_ctrl)*300,
                                    (np.sum(bin3_events_ctrl)/bin3_duration_ctrl)*300]

            for t in range(0, len(turn_ctrl)):
                if turn_ctrl[t] < 0.5:
                    bin1_events_amph.append(eventmean_amph[t])
                    bin1_duration_amph += 1
                if 0.5 <= turn_ctrl[t] < 1:
                    bin2_events_amph.append(eventmean_amph[t])
                    bin2_duration_amph += 1
                if 1 <= turn_ctrl[t] < 2:
                    bin3_events_amph.append(eventmean_amph[t])
                    bin3_duration_amph += 1

            event_per_speed_amph = [(np.sum(bin1_events_amph)/bin1_duration_amph)*300,
                                    (np.sum(bin2_events_amph)/bin2_duration_amph)*300,
                                    (np.sum(bin3_events_amph)/bin3_duration_amph)*300]

            # event_per_speed_dict[experiment] = [event_per_speed_ctrl, event_per_speed_amph]

            if experiment in D1_folders:
                D1_event_per_speed_ctrl.append(event_per_speed_ctrl)
                D1_event_per_speed_amph.append(event_per_speed_amph)

            elif experiment in D2_folders:
                D2_event_per_speed_ctrl.append(event_per_speed_ctrl)
                D2_event_per_speed_amph.append(event_per_speed_amph)

    plt.figure(figsize=(4, 8))
    ax = plt.subplot(2, 1, 1)
    plt.plot(np.mean(D1_event_per_speed_ctrl, axis=0), label='D1 ctrl', color='k')
    plt.plot(np.mean(D1_event_per_speed_amph, axis=0), label='D1 amph', color='b')
    x_default = [0, 1, 2, 3, 4, 5];
    x_new = ['<0.5', '0.5-1', '1-2', '2-4', '4-8', '8-14'];
    plt.xticks(x_default, x_new);
    plt.ylim((0, 2.5))
    plt.xlabel('Locomotor speed bin (cm/s)')
    plt.ylabel('Ca event rate (event/min)')
    plt.title("D1 SPNs")
    plt.legend()

    ax = plt.subplot(2, 1, 2)
    plt.plot(np.mean(D2_event_per_speed_ctrl, axis=0), label='D2 ctrl', color='k')
    plt.plot(np.mean(D2_event_per_speed_amph, axis=0), label='D2 amph', color='r')
    x_default = [0, 1, 2, 3, 4, 5];
    x_new = ['<0.5', '0.5-1', '1-2', '2-4', '4-8', '8-14'];
    plt.xticks(x_default, x_new);
    plt.ylim((0, 2.5))
    plt.xlabel('Locomotor speed bin (cm/s)')
    plt.ylabel('Ca event rate (event/min)')
    plt.title("D2 SPNs")
    plt.legend()
    plt.show()

    return

