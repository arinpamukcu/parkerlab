# Created by Arin Pamukcu, PhD on August 2022

from data import *
from info import *
from mars import *
from speed_neurons import *
import matplotlib.pyplot as plt
import pdb

def turn_trig_ctrl():
    D1_turn_trig_avg_ctrl_all = []
    D2_turn_trig_avg_ctrl_all = []

    # drugs = get_drug()
    drugs = ['Clozapine']
    dose = 'Vehicle'
    for drug in drugs:
        print(drug)

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)
        D1_turn_trig_avg_ctrl_perdrug = []
        D2_turn_trig_avg_ctrl_perdrug = []

        for experiment in experiments:
            print(experiment)

            _, _, calcium_ctrl_dff, _, _, _, _, _, \
            neuron_count, time_ctrl, time_amph = get_data(drug, dose, experiment)

            _, _, mars_left_angle_ctrl, mars_left_angle_amph, _, _ = mars_feature(drug, dose, experiment)

            # remove events in first 25 and last 25 frames (is this okay to do?)
            window = 25
            mars_left_angle_ctrl_modified = mars_left_angle_ctrl[window:-window]

            # find left turn triggered Ca event dff average per neuron and per animal
            # find frames where angle gets smaller for five consecutive frames (i.e. 1 second)
            turn_ctrl_frames = []
            for frame in range(0, len(mars_left_angle_ctrl_modified) - 4):
                if mars_left_angle_ctrl_modified[frame] > mars_left_angle_ctrl_modified[frame + 1] > \
                        mars_left_angle_ctrl_modified[frame + 2] > mars_left_angle_ctrl_modified[frame + 3] > \
                        mars_left_angle_ctrl_modified[frame + 4]:
                    frame = frame + window
                    turn_ctrl_frames.append(frame)

            # find average Ca event of neurons
            calcium_ctrl_mean = np.mean(calcium_ctrl_dff, axis=0)

            # find average Ca event of neurons at those frames
            turn_trig_avg_ctrl = []
            for frame in turn_ctrl_frames:
                turn_trig_avg_ctrl.append((calcium_ctrl_mean[frame - 25:frame + 26]))

            turn_trig_avg_ctrl_peranimal = np.mean(turn_trig_avg_ctrl, axis=0)

            if experiment in D1_folders:
                D1_turn_trig_avg_ctrl_perdrug.append(turn_trig_avg_ctrl_peranimal)

            elif experiment in D2_folders:
                D2_turn_trig_avg_ctrl_perdrug.append(turn_trig_avg_ctrl_peranimal)

        D1_turn_trig_avg_ctrl_perdrug = np.nanmean(D1_turn_trig_avg_ctrl_perdrug, axis=0)
        D2_turn_trig_avg_ctrl_perdrug = np.nanmean(D2_turn_trig_avg_ctrl_perdrug, axis=0)

        D1_turn_trig_avg_ctrl_all.append(D1_turn_trig_avg_ctrl_perdrug)
        D2_turn_trig_avg_ctrl_all.append(D2_turn_trig_avg_ctrl_perdrug)

    D1_turn_trig_avg_ctrl_all = np.nanmean(D1_turn_trig_avg_ctrl_all, axis=0)
    D2_turn_trig_avg_ctrl_all = np.nanmean(D2_turn_trig_avg_ctrl_all, axis=0)

    return D1_turn_trig_avg_ctrl_all, D2_turn_trig_avg_ctrl_all


def turn_trig_amph():
    D1_turn_trig_avg_amph_all = []
    D2_turn_trig_avg_amph_all = []

    # drugs = get_drug()
    drugs = ['Clozapine']
    dose = 'Vehicle'
    for drug in drugs:
        print(drug + '_amph')

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)
        D1_turn_trig_avg_amph_perdrug = []
        D2_turn_trig_avg_amph_perdrug = []

        for experiment in experiments:
            print(experiment + '_amph')

            _, _, _, calcium_amph_dff, _, _, _, _, \
            neuron_count, time_ctrl, time_amph = get_data(drug, dose, experiment)

            _, _, mars_left_angle_ctrl, mars_left_angle_amph, _, _ = mars_feature(drug, dose, experiment)

            # remove events in first 25 and last 25 frames (is this okay to do?)
            window = 25
            mars_left_angle_amph_modified = mars_left_angle_amph[window:-window]

            # find left turn triggered Ca event dff average per neuron and per animal
            # find frames where angle gets smaller for five consecutive frames (i.e. 1 second)
            turn_amph_frames = []
            for frame in range(0, len(mars_left_angle_amph_modified) - 4):
                if mars_left_angle_amph_modified[frame] > mars_left_angle_amph_modified[frame + 1] > \
                        mars_left_angle_amph_modified[frame + 2] > mars_left_angle_amph_modified[frame + 3] > \
                        mars_left_angle_amph_modified[frame + 4]:
                    frame = frame + window
                    turn_amph_frames.append(frame)

            # find average Ca event of neurons
            calcium_amph_mean = np.mean(calcium_amph_dff, axis=0)

            # find average Ca event of neurons at those frames
            turn_trig_avg_amph = []
            for frame in turn_amph_frames:
                turn_trig_avg_amph.append((calcium_amph_mean[frame - 25:frame + 26]))

            turn_trig_avg_ctrl_peranimal = np.mean(turn_trig_avg_amph, axis=0)

            if experiment in D1_folders:
                D1_turn_trig_avg_amph_perdrug.append(turn_trig_avg_ctrl_peranimal)

            elif experiment in D2_folders:
                D2_turn_trig_avg_amph_perdrug.append(turn_trig_avg_ctrl_peranimal)

        D1_turn_trig_avg_amph_perdrug = np.nanmean(D1_turn_trig_avg_amph_perdrug, axis=0)
        D2_turn_trig_avg_amph_perdrug = np.nanmean(D2_turn_trig_avg_amph_perdrug, axis=0)

        D1_turn_trig_avg_amph_all.append(D1_turn_trig_avg_amph_perdrug)
        D2_turn_trig_avg_amph_all.append(D2_turn_trig_avg_amph_perdrug)

    D1_turn_trig_avg_amph_all = np.nanmean(D1_turn_trig_avg_amph_all, axis=0)
    D2_turn_trig_avg_amph_all = np.nanmean(D2_turn_trig_avg_amph_all, axis=0)

    return D1_turn_trig_avg_amph_all, D2_turn_trig_avg_amph_all


def turn_trig_plot():

    D1_turn_trig_avg_ctrl_all, D2_turn_trig_avg_ctrl_all = turn_trig_ctrl()
    D1_turn_trig_avg_amph_all, D2_turn_trig_avg_amph_all = turn_trig_amph()

    plt.figure(figsize=(6, 8))
    ax = plt.subplot(2, 1, 1)
    # plt.plot(D1_turn_trig_avg_ctrl_all, color='k', label='D1 ctrl')
    plt.plot(D2_turn_trig_avg_ctrl_all, color='k', label='D2 ctrl')
    x_default = [0, 25, 50]
    x_new = ['-25', '0', '+25']
    plt.xticks(x_default, x_new)
    plt.xlabel('Time (5hz) from left turn bout at time at 0')
    plt.ylabel('Speed (cm/s)')
    plt.title('Left turn trig avg CTRL')
    plt.legend()

    ax = plt.subplot(2, 1, 2)
    # plt.plot(D1_turn_trig_avg_amph_all, color='b', label='D1 amph')
    plt.plot(D2_turn_trig_avg_amph_all, color='r', label='D2 amph')
    x_default = [0, 25, 50]
    x_new = ['-25', '0', '+25']
    plt.xticks(x_default, x_new)
    plt.xlabel('Time (5hz) from left turn bout at time at 0')
    plt.ylabel('Speed (cm/s)')
    plt.title('Left turn trig avg AMPH')
    plt.legend()
    plt.show()

    return