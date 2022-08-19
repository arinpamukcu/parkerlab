# Created by Arin Pamukcu, PhD on August 2022

# y-axis: Ca event rate (event/min)
# x-axis: Locomotor speed bin (cm/s)
# bin: <0.5, 0.5-1, 1-2, 2-4, 4-8, 8-14

from data import *
from info import *
from mars import *
import numpy as np
import matplotlib.pyplot as plt

def event_per_left_turn():
    D1_event_per_speed_ctrl = []
    D1_event_per_speed_amph = []
    D2_event_per_speed_ctrl = []
    D2_event_per_speed_amph = []

    drugs = ['Clozapine']
    # drugs = get_drug()
    dose = 'Vehicle'

    for drug in drugs:

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)

        for experiment in experiments:
            print(experiment)

            _, _, _, _, eventmean_ctrl, eventmean_amph, neuron, time_ctrl, time_amph = get_data(drug, dose, experiment)

            _, _, mars_left_angle_ctrl, mars_left_angle_amph, _, _ = mars_feature(drug, dose, experiment)

            bin1_events_ctrl, bin2_events_ctrl, bin3_events_ctrl, bin4_events_ctrl, bin5_events_ctrl, bin6_events_ctrl = (
                [] for i in range(6))
            bin1_events_amph, bin2_events_amph, bin3_events_amph, bin4_events_amph, bin5_events_amph, bin6_events_amph = (
                [] for i in range(6))
            bin1_duration_ctrl, bin2_duration_ctrl, bin3_duration_ctrl, bin4_duration_ctrl, bin5_duration_ctrl, bin6_duration_ctrl = (
                0 for i in range(6))
            bin1_duration_amph, bin2_duration_amph, bin3_duration_amph, bin4_duration_amph, bin5_duration_amph, bin6_duration_amph = (
                0 for i in range(6))

            for t in range(0, len(mars_left_angle_ctrl)):
                if mars_left_angle_ctrl[t] <= 30:
                    bin1_events_ctrl.append(eventmean_ctrl[t])
                    bin1_duration_ctrl += 1
                if 30 < mars_left_angle_ctrl[t] <= 60:
                    bin2_events_ctrl.append(eventmean_ctrl[t])
                    bin2_duration_ctrl += 1
                if 60 < mars_left_angle_ctrl[t] <= 90:
                    bin3_events_ctrl.append(eventmean_ctrl[t])
                    bin3_duration_ctrl += 1
                if 90 < mars_left_angle_ctrl[t] <= 120:
                    bin4_events_ctrl.append(eventmean_ctrl[t])
                    bin4_duration_ctrl += 1
                if 120 < mars_left_angle_ctrl[t] <= 150:
                    bin5_events_ctrl.append(eventmean_ctrl[t])
                    bin5_duration_ctrl += 1
                if 150 < mars_left_angle_ctrl[t] <= 180:
                    bin6_events_ctrl.append(eventmean_ctrl[t])
                    bin6_duration_ctrl += 1

            event_per_turn_ctrl = [(np.sum(bin1_events_ctrl)/bin1_duration_ctrl)*300,
                                    (np.sum(bin2_events_ctrl)/bin2_duration_ctrl)*300,
                                    (np.sum(bin3_events_ctrl)/bin3_duration_ctrl)*300,
                                    (np.sum(bin4_events_ctrl)/bin4_duration_ctrl)*300,
                                    (np.sum(bin5_events_ctrl)/bin5_duration_ctrl)*300,
                                    (np.sum(bin6_events_ctrl)/bin6_duration_ctrl)*300]

            for t in range(0, len(mars_left_angle_amph)):
                if mars_left_angle_amph[t] <= 30:
                    bin1_events_amph.append(eventmean_amph[t])
                    bin1_duration_amph += 1
                if 30 < mars_left_angle_amph[t] <= 60:
                    bin2_events_amph.append(eventmean_amph[t])
                    bin2_duration_amph += 1
                if 60 < mars_left_angle_amph[t] <= 90:
                    bin3_events_amph.append(eventmean_amph[t])
                    bin3_duration_amph += 1
                if 90 < mars_left_angle_amph[t] <= 120:
                    bin4_events_amph.append(eventmean_amph[t])
                    bin4_duration_amph += 1
                if 120 < mars_left_angle_amph[t] <= 150:
                    bin5_events_amph.append(eventmean_amph[t])
                    bin5_duration_amph += 1
                if 150 < mars_left_angle_amph[t] <= 180:
                    bin6_events_amph.append(eventmean_amph[t])
                    bin6_duration_amph += 1

            event_per_turn_amph = [(np.sum(bin1_events_amph)/bin1_duration_amph)*300,
                                    (np.sum(bin2_events_amph)/bin2_duration_amph)*300,
                                    (np.sum(bin3_events_amph)/bin3_duration_amph)*300,
                                    (np.sum(bin4_events_amph)/bin4_duration_amph)*300,
                                    (np.sum(bin5_events_amph)/bin5_duration_amph)*300,
                                    (np.sum(bin6_events_amph)/bin6_duration_amph)*300]

            if experiment in D1_folders:
                D1_event_per_speed_ctrl.append(event_per_turn_ctrl)
                D1_event_per_speed_amph.append(event_per_turn_amph)

            elif experiment in D2_folders:
                D2_event_per_speed_ctrl.append(event_per_turn_ctrl)
                D2_event_per_speed_amph.append(event_per_turn_amph)

    plt.figure(figsize=(4, 8))
    ax = plt.subplot(2, 1, 1)
    plt.plot(np.mean(D1_event_per_speed_ctrl, axis=0), label='D1 ctrl', color='k')
    plt.plot(np.mean(D1_event_per_speed_amph, axis=0), label='D1 amph', color='b')
    x_default = [0, 1, 2, 3, 4, 5];
    x_new = ['30', '60', '90', '120', '150', '180'];
    plt.xticks(x_default, x_new);
    plt.ylim((0, 2.5))
    plt.xlabel('Left turn bin (degrees°)')
    plt.ylabel('Ca event rate (event/min)')
    plt.title("D1 SPNs")
    plt.legend()

    ax = plt.subplot(2, 1, 2)
    plt.plot(np.mean(D2_event_per_speed_ctrl, axis=0), label='D2 ctrl', color='k')
    plt.plot(np.mean(D2_event_per_speed_amph, axis=0), label='D2 amph', color='r')
    x_default = [0, 1, 2, 3, 4, 5];
    x_new = ['30', '60', '90', '120', '150', '180'];
    plt.xticks(x_default, x_new);
    plt.ylim((0, 2.5))
    plt.xlabel('Left turn bin (degrees°)')
    plt.ylabel('Ca event rate (event/min)')
    plt.title("D2 SPNs")
    plt.legend()
    plt.show()

    return


# def event_per_right_turn():
#     D1_event_per_speed_ctrl = []
#     D1_event_per_speed_amph = []
#     D2_event_per_speed_ctrl = []
#     D2_event_per_speed_amph = []
#
#     drugs = ['Clozapine']
#     # drugs = get_drug()
#     dose = 'Vehicle'
#
#     for drug in drugs:
#
#         experiments, D1_folders, D2_folders = get_animal_id(drug, dose)
#
#         for experiment in experiments:
#             print(experiment)
#
#             _, _, _, _, eventmean_ctrl, eventmean_amph, neuron, time_ctrl, time_amph = get_data(drug, dose, experiment)
#
#             _, _, _, _, mars_right_angle_ctrl, mars_right_angle_amph = mars_feature(drug, dose, experiment)
#
#             bin1_events_ctrl, bin2_events_ctrl, bin3_events_ctrl, bin4_events_ctrl, bin5_events_ctrl, bin6_events_ctrl = (
#                 [] for i in range(6))
#             bin1_events_amph, bin2_events_amph, bin3_events_amph, bin4_events_amph, bin5_events_amph, bin6_events_amph = (
#                 [] for i in range(6))
#             bin1_duration_ctrl, bin2_duration_ctrl, bin3_duration_ctrl, bin4_duration_ctrl, bin5_duration_ctrl, bin6_duration_ctrl = (
#                 0 for i in range(6))
#             bin1_duration_amph, bin2_duration_amph, bin3_duration_amph, bin4_duration_amph, bin5_duration_amph, bin6_duration_amph = (
#                 0 for i in range(6))
#
#             for t in range(0, len(mars_left_angle_ctrl)):
#                 if mars_left_angle_ctrl[t] <= 30:
#                     bin1_events_ctrl.append(eventmean_ctrl[t])
#                     bin1_duration_ctrl += 1
#                 if 30 < mars_left_angle_ctrl[t] <= 60:
#                     bin2_events_ctrl.append(eventmean_ctrl[t])
#                     bin2_duration_ctrl += 1
#                 if 60 < mars_left_angle_ctrl[t] <= 90:
#                     bin3_events_ctrl.append(eventmean_ctrl[t])
#                     bin3_duration_ctrl += 1
#                 if 90 < mars_left_angle_ctrl[t] <= 120:
#                     bin4_events_ctrl.append(eventmean_ctrl[t])
#                     bin4_duration_ctrl += 1
#                 if 120 < mars_left_angle_ctrl[t] <= 150:
#                     bin5_events_ctrl.append(eventmean_ctrl[t])
#                     bin5_duration_ctrl += 1
#                 if 150 < mars_left_angle_ctrl[t] <= 180:
#                     bin6_events_ctrl.append(eventmean_ctrl[t])
#                     bin6_duration_ctrl += 1
#
#             event_per_turn_ctrl = [(np.sum(bin1_events_ctrl)/bin1_duration_ctrl)*300,
#                                     (np.sum(bin2_events_ctrl)/bin2_duration_ctrl)*300,
#                                     (np.sum(bin3_events_ctrl)/bin3_duration_ctrl)*300,
#                                     (np.sum(bin4_events_ctrl)/bin4_duration_ctrl)*300,
#                                     (np.sum(bin5_events_ctrl)/bin5_duration_ctrl)*300,
#                                     (np.sum(bin6_events_ctrl)/bin6_duration_ctrl)*300]
#
#             for t in range(0, len(mars_left_angle_amph)):
#                 if mars_left_angle_amph[t] <= 30:
#                     bin1_events_amph.append(eventmean_amph[t])
#                     bin1_duration_amph += 1
#                 if 30 < mars_left_angle_amph[t] <= 60:
#                     bin2_events_amph.append(eventmean_amph[t])
#                     bin2_duration_amph += 1
#                 if 60 < mars_left_angle_amph[t] <= 90:
#                     bin3_events_amph.append(eventmean_amph[t])
#                     bin3_duration_amph += 1
#                 if 90 < mars_left_angle_amph[t] <= 120:
#                     bin4_events_amph.append(eventmean_amph[t])
#                     bin4_duration_amph += 1
#                 if 120 < mars_left_angle_amph[t] <= 150:
#                     bin5_events_amph.append(eventmean_amph[t])
#                     bin5_duration_amph += 1
#                 if 150 < mars_left_angle_amph[t] <= 180:
#                     bin6_events_amph.append(eventmean_amph[t])
#                     bin6_duration_amph += 1
#
#             event_per_turn_amph = [(np.sum(bin1_events_amph)/bin1_duration_amph)*300,
#                                     (np.sum(bin2_events_amph)/bin2_duration_amph)*300,
#                                     (np.sum(bin3_events_amph)/bin3_duration_amph)*300,
#                                     (np.sum(bin4_events_amph)/bin4_duration_amph)*300,
#                                     (np.sum(bin5_events_amph)/bin5_duration_amph)*300,
#                                     (np.sum(bin6_events_amph)/bin6_duration_amph)*300]
#
#             if experiment in D1_folders:
#                 D1_event_per_speed_ctrl.append(event_per_turn_ctrl)
#                 D1_event_per_speed_amph.append(event_per_turn_amph)
#
#             elif experiment in D2_folders:
#                 D2_event_per_speed_ctrl.append(event_per_turn_ctrl)
#                 D2_event_per_speed_amph.append(event_per_turn_amph)
#
#     plt.figure(figsize=(4, 8))
#     ax = plt.subplot(2, 1, 1)
#     plt.plot(np.mean(D1_event_per_speed_ctrl, axis=0), label='D1 ctrl', color='k')
#     plt.plot(np.mean(D1_event_per_speed_amph, axis=0), label='D1 amph', color='b')
#     x_default = [0, 1, 2, 3, 4, 5];
#     x_new = ['30', '60', '90', '120', '150', '180'];
#     plt.xticks(x_default, x_new);
#     plt.ylim((0, 2.5))
#     plt.xlabel('Left turn bin (degrees°)')
#     plt.ylabel('Ca event rate (event/min)')
#     plt.title("D1 SPNs")
#     plt.legend()
#
#     ax = plt.subplot(2, 1, 2)
#     plt.plot(np.mean(D2_event_per_speed_ctrl, axis=0), label='D2 ctrl', color='k')
#     plt.plot(np.mean(D2_event_per_speed_amph, axis=0), label='D2 amph', color='r')
#     x_default = [0, 1, 2, 3, 4, 5];
#     x_new = ['30', '60', '90', '120', '150', '180'];
#     plt.xticks(x_default, x_new);
#     plt.ylim((0, 2.5))
#     plt.xlabel('Left turn bin (degrees°)')
#     plt.ylabel('Ca event rate (event/min)')
#     plt.title("D2 SPNs")
#     plt.legend()
#     plt.show()
#
#     return
