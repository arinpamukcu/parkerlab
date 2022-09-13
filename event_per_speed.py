# Created by Arin Pamukcu, PhD on August 2022

# y-axis: Ca event rate (event/min)
# x-axis: Locomotor speed bin (cm/s)
# bin: <0.5, 0.5-1, 1-2, 2-4, 4-8, 8-14

from data import *
from info import *
import numpy as np
import matplotlib.pyplot as plt

def speed_bins(speed_data, eventmean_data):
    bin1_events, bin2_events, bin3_events, bin4_events, bin5_events, bin6_events = ([] for i in range(6))
    bin1_duration, bin2_duration, bin3_duration, bin4_duration, bin5_duration, bin6_duration = (0 for i in range(6))

    for t in range(0, len(speed_data)):
        if speed_data[t] < 0.5:
            bin1_events.append(eventmean_data[t])
            bin1_duration += 1
        if 0.5 <= speed_data[t] < 1:
            bin2_events.append(eventmean_data[t])
            bin2_duration += 1
        if 1 <= speed_data[t] < 2:
            bin3_events.append(eventmean_data[t])
            bin3_duration += 1
        if 2 <= speed_data[t] < 4:
            bin4_events.append(eventmean_data[t])
            bin4_duration += 1
        if 4 <= speed_data[t] < 8:
            bin5_events.append(eventmean_data[t])
            bin5_duration += 1
        if 8 <= speed_data[t] < 14:
            bin6_events.append(eventmean_data[t])
            bin6_duration += 1

    event_per_speed = [(np.sum(bin1_events) / bin1_duration) * 300, (np.sum(bin2_events) / bin2_duration) * 300,
                       (np.sum(bin3_events) / bin3_duration) * 300, (np.sum(bin4_events) / bin4_duration) * 300,
                       (np.sum(bin5_events) / bin5_duration) * 300, (np.sum(bin6_events) / bin6_duration) * 300]

    return event_per_speed

def data():
    drugs = ['Clozapine']
    # drugs = get_drug()
    dose = 'Vehicle'

    for drug in drugs:

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)

        D1_event_per_speed_ctrl = []
        D1_event_per_speed_amph = []
        D2_event_per_speed_ctrl = []
        D2_event_per_speed_amph = []

        for experiment in experiments:
            print(experiment)

            speed_ctrl, speed_amph, _, _, eventmean_ctrl, eventmean_amph, _, _, _ = get_data(drug, dose, experiment)

            event_per_speed_ctrl = speed_bins(speed_ctrl, eventmean_ctrl)
            event_per_speed_amph = speed_bins(speed_amph, eventmean_amph)

            # event_per_speed_dict[experiment] = [event_per_speed_ctrl, event_per_speed_amph]

            if experiment in D1_folders:
                D1_event_per_speed_ctrl.append(event_per_speed_ctrl)
                D1_event_per_speed_amph.append(event_per_speed_amph)

            elif experiment in D2_folders:
                D2_event_per_speed_ctrl.append(event_per_speed_ctrl)
                D2_event_per_speed_amph.append(event_per_speed_amph)

    return D1_event_per_speed_ctrl, D1_event_per_speed_amph, D2_event_per_speed_ctrl, D2_event_per_speed_amph


def plot():

    D1_event_per_speed_ctrl, D1_event_per_speed_amph, D2_event_per_speed_ctrl, D2_event_per_speed_amph = data()

    plt.figure(figsize=(5, 9))
    plt.subplot(211)
    plt.plot(np.mean(D1_event_per_speed_ctrl, axis=0), label='D1 ctrl', color='k')
    plt.plot(np.mean(D1_event_per_speed_amph, axis=0), label='D1 amph', color='b')
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
    plt.plot(np.mean(D2_event_per_speed_ctrl, axis=0), label='D2 ctrl', color='k')
    plt.plot(np.mean(D2_event_per_speed_amph, axis=0), label='D2 amph', color='r')
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