# Created by Arin Pamukcu, PhD on August 2022

from data import *
from info import *
from mars import *
from speed_neurons import *
import matplotlib.pyplot as plt

def ctrl():
    D1_turn_trig_dff_ctrl_all = []
    D2_turn_trig_dff_ctrl_all = []

    drugs = get_drug()
    # drugs = ['Clozapine']
    dose = 'Vehicle'
    for drug in drugs:
        print(drug)

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)
        D1_turn_trig_dff_ctrl_perdrug = []
        D2_turn_trig_dff_ctrl_perdrug = []

        for experiment in experiments:
            print(experiment)

            _, _, _, _, _, _, eventmean_ctrl, eventmean_amph, \
            neuron_count, time_ctrl, time_amph = get_data(drug, dose, experiment)

            _, _, mars_left_angle_ctrl, mars_left_angle_amph, \
            mars_right_angle_ctrl, mars_right_angle_amph = mars_feature(drug, dose, experiment)

            # remove events in first 25 and last 25 frames (is this okay to do?)
            window = 25
            # mars_turn_ctrl_modified = mars_left_angle_ctrl[window:-window]
            mars_turn_ctrl_modified = mars_right_angle_ctrl[window:-window]

            # find left turn triggered Ca event dff average per neuron and per animal
            # find frames where angle gets smaller for five consecutive frames (i.e. 1 second)
            turn_ctrl_frames = []
            for frame in range(0, len(mars_turn_ctrl_modified) - 4):
                if mars_turn_ctrl_modified[frame] > mars_turn_ctrl_modified[frame + 1] > \
                        mars_turn_ctrl_modified[frame + 2] > mars_turn_ctrl_modified[frame + 3] > \
                        mars_turn_ctrl_modified[frame + 4]:
                    frame = frame + window
                    turn_ctrl_frames.append(frame)

            # find average Ca event of neurons at those frames
            turn_trig_dff_ctrl = []
            for frame in turn_ctrl_frames:
                turn_trig_dff_ctrl.append((eventmean_ctrl[frame - 25:frame + 26]))

            turn_trig_dff_ctrl_peranimal = np.mean(turn_trig_dff_ctrl, axis=0)

            if experiment in D1_folders:
                D1_turn_trig_dff_ctrl_perdrug.append(turn_trig_dff_ctrl_peranimal)

            elif experiment in D2_folders:
                D2_turn_trig_dff_ctrl_perdrug.append(turn_trig_dff_ctrl_peranimal)

        D1_turn_trig_dff_ctrl_perdrug = np.nanmean(D1_turn_trig_dff_ctrl_perdrug, axis=0)
        D2_turn_trig_dff_ctrl_perdrug = np.nanmean(D2_turn_trig_dff_ctrl_perdrug, axis=0)

        D1_turn_trig_dff_ctrl_all.append(D1_turn_trig_dff_ctrl_perdrug)
        D2_turn_trig_dff_ctrl_all.append(D2_turn_trig_dff_ctrl_perdrug)

    D1_turn_trig_dff_ctrl_all = np.nanmean(D1_turn_trig_dff_ctrl_all, axis=0)
    D2_turn_trig_dff_ctrl_all = np.nanmean(D2_turn_trig_dff_ctrl_all, axis=0)

    D1_turn_trig_dff_ctrl_sem = np.std(D1_turn_trig_dff_ctrl_all, axis=0) / np.sqrt(len(D1_turn_trig_dff_ctrl_all))
    D2_turn_trig_dff_ctrl_sem = np.std(D2_turn_trig_dff_ctrl_all, axis=0) / np.sqrt(len(D2_turn_trig_dff_ctrl_all))

    return D1_turn_trig_dff_ctrl_all, D2_turn_trig_dff_ctrl_all, \
           D1_turn_trig_dff_ctrl_sem, D2_turn_trig_dff_ctrl_sem


def amph():
    D1_turn_trig_dff_amph_all = []
    D2_turn_trig_dff_amph_all = []

    drugs = get_drug()
    # drugs = ['Clozapine']
    dose = 'Vehicle'
    for drug in drugs:
        print(drug + '_amph')

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)
        D1_turn_trig_dff_amph_perdrug = []
        D2_turn_trig_dff_amph_perdrug = []

        for experiment in experiments:
            print(experiment + '_amph')

            _, _, _, _, _, _, eventmean_ctrl, eventmean_amph, \
            neuron_count, time_ctrl, time_amph = get_data(drug, dose, experiment)

            _, _, mars_left_angle_ctrl, mars_left_angle_amph, \
            mars_right_angle_ctrl, mars_right_angle_amph, = mars_feature(drug, dose, experiment)

            # remove events in first 25 and last 25 frames (is this okay to do?)
            window = 25
            # mars_turn_amph_modified = mars_left_angle_amph[window:-window]
            mars_turn_amph_modified = mars_right_angle_amph[window:-window]

            # find left turn triggered Ca event dff average per neuron and per animal
            # find frames where angle gets smaller for five consecutive frames (i.e. 1 second)
            turn_amph_frames = []
            for frame in range(0, len(mars_turn_amph_modified) - 4):
                if mars_turn_amph_modified[frame] > mars_turn_amph_modified[frame + 1] > \
                        mars_turn_amph_modified[frame + 2] > mars_turn_amph_modified[frame + 3] > \
                        mars_turn_amph_modified[frame + 4]:
                    frame = frame + window
                    turn_amph_frames.append(frame)

            # find average Ca event of neurons at those frames
            turn_trig_dff_amph = []
            for frame in turn_amph_frames:
                turn_trig_dff_amph.append((eventmean_amph[frame - 25:frame + 26]))

            turn_trig_dff_ctrl_peranimal = np.mean(turn_trig_dff_amph, axis=0)

            if experiment in D1_folders:
                D1_turn_trig_dff_amph_perdrug.append(turn_trig_dff_ctrl_peranimal)

            elif experiment in D2_folders:
                D2_turn_trig_dff_amph_perdrug.append(turn_trig_dff_ctrl_peranimal)

        D1_turn_trig_dff_amph_perdrug = np.nanmean(D1_turn_trig_dff_amph_perdrug, axis=0)
        D2_turn_trig_dff_amph_perdrug = np.nanmean(D2_turn_trig_dff_amph_perdrug, axis=0)

        D1_turn_trig_dff_amph_all.append(D1_turn_trig_dff_amph_perdrug)
        D2_turn_trig_dff_amph_all.append(D2_turn_trig_dff_amph_perdrug)

    D1_turn_trig_dff_amph_all = np.nanmean(D1_turn_trig_dff_amph_all, axis=0)
    D2_turn_trig_dff_amph_all = np.nanmean(D2_turn_trig_dff_amph_all, axis=0)

    D1_turn_trig_dff_amph_sem = np.std(D1_turn_trig_dff_amph_all, axis=0) / np.sqrt(len(D1_turn_trig_dff_amph_all))
    D2_turn_trig_dff_amph_sem = np.std(D2_turn_trig_dff_amph_all, axis=0) / np.sqrt(len(D2_turn_trig_dff_amph_all))

    return D1_turn_trig_dff_amph_all, D2_turn_trig_dff_amph_all, \
           D1_turn_trig_dff_amph_sem, D2_turn_trig_dff_amph_sem


def plot():

    D1_turn_trig_dff_ctrl_all, D2_turn_trig_dff_ctrl_all, \
    D1_turn_trig_dff_ctrl_sem, D2_turn_trig_dff_ctrl_sem = ctrl()

    D1_turn_trig_dff_amph_all, D2_turn_trig_dff_amph_all, \
    D1_turn_trig_dff_amph_sem, D2_turn_trig_dff_amph_sem = amph()

    D1_ctrl_yerr_hi = D1_turn_trig_dff_ctrl_all + D1_turn_trig_dff_ctrl_sem
    D1_ctrl_yerr_lo = D1_turn_trig_dff_ctrl_all - D1_turn_trig_dff_ctrl_sem

    D2_ctrl_yerr_hi = D2_turn_trig_dff_ctrl_all + D2_turn_trig_dff_ctrl_sem
    D2_ctrl_yerr_lo = D2_turn_trig_dff_ctrl_all - D2_turn_trig_dff_ctrl_sem

    D1_amph_yerr_hi = D1_turn_trig_dff_amph_all + D1_turn_trig_dff_amph_sem
    D1_amph_yerr_lo = D1_turn_trig_dff_amph_all - D1_turn_trig_dff_amph_sem

    D2_amph_yerr_hi = D2_turn_trig_dff_amph_all + D2_turn_trig_dff_amph_sem
    D2_amph_yerr_lo = D2_turn_trig_dff_amph_all - D2_turn_trig_dff_amph_sem

    x = range(51)

    plt.figure(figsize=(6, 9.5))
    plt.subplot(211)
    plt.plot(D1_turn_trig_dff_ctrl_all, color='k', label='D1 ctrl')
    plt.fill_between(x, D1_ctrl_yerr_hi, D1_ctrl_yerr_lo, color='k', alpha=0.2)
    # plt.plot(D2_turn_trig_dff_ctrl_all, color='k', label='D2 ctrl')
    # plt.fill_between(x, D2_ctrl_yerr_hi, D2_ctrl_yerr_lo, color='k', alpha=0.2)
    x_default = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    x_new = ['-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5']
    plt.xticks(x_default, x_new)
    plt.xlabel('Time (s) from left turn bout')
    plt.ylabel('Ca activity (dff)')
    plt.title('CTRL')
    plt.suptitle('Left turn triggered Ca activity')
    plt.legend()

    plt.subplot(212)
    plt.plot(D1_turn_trig_dff_amph_all, color='b', label='D1 amph')
    plt.fill_between(x, D1_amph_yerr_hi, D1_amph_yerr_lo, color='b', alpha=0.2)
    # plt.plot(D2_turn_trig_dff_amph_all, color='r', label='D2 amph')
    # plt.fill_between(x, D2_amph_yerr_hi, D2_amph_yerr_lo, color='r', alpha=0.2)
    x_default = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    x_new = ['-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5']
    plt.xticks(x_default, x_new)
    plt.xlabel('Time (s) from left turn bout')
    plt.ylabel('Ca activity (dff)')
    plt.title('AMPH')
    plt.legend()
    plt.show()

    return