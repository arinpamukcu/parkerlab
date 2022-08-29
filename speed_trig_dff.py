# Created by Arin Pamukcu, PhD on August 2022

from data import *
from info import *
from speed_neurons import *
import matplotlib.pyplot as plt

def ctrl():
    D1_speed_trig_dff_ctrl_all = []
    D2_speed_trig_dff_ctrl_all = []

    drugs = get_drug()
    # drugs = ['Clozapine']
    dose = 'Vehicle'
    for drug in drugs:
        print(drug)

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)
        D1_speed_trig_dff_ctrl_perdrug = []
        D2_speed_trig_dff_ctrl_perdrug = []

        for experiment in experiments:
            print(experiment)

            speed_ctrl, speed_amph, calcium_ctrl_dff, calcium_amph_dff, _, _, _, _, \
            neuron_count, time_ctrl, time_amph = get_data(drug, dose, experiment)

            # if you just want to use speed neurons for your analysis
            _, _, _, speed_neuron_ctrl_events, speed_neuron_amph_events = get_speed_neurons(drug, dose, experiment)

            # remove events in first 25 and last 25 frames
            window = 25
            speed_ctrl_modified = speed_ctrl[window:-window]  # 4450

            # find left turn triggered Ca event dff average per neuron and per animal
            # find frames where angle gets smaller for five consecutive frames (i.e. 1 second)
            speed_ctrl_frames = []
            for frame in range(0, len(speed_ctrl_modified) - 4):
                if 1 < speed_ctrl_modified[frame] < speed_ctrl_modified[frame + 1] < speed_ctrl_modified[frame + 2] < \
                        speed_ctrl_modified[frame + 3] < speed_ctrl_modified[frame + 4]:
                    frame = frame + window
                    speed_ctrl_frames.append(frame)

            # find average Ca event of neurons
            calcium_ctrl_mean = np.mean(calcium_ctrl_dff, axis=0)

            # find average Ca event of neurons at those frames
            speed_trig_dff_ctrl = []
            for frame in speed_ctrl_frames:
                speed_trig_dff_ctrl.append((calcium_ctrl_mean[frame - 25:frame + 26]))

            speed_trig_dff_ctrl_peranimal = np.mean(speed_trig_dff_ctrl, axis=0)

            if experiment in D1_folders:
                D1_speed_trig_dff_ctrl_perdrug.append(speed_trig_dff_ctrl_peranimal)

            elif experiment in D2_folders:
                D2_speed_trig_dff_ctrl_perdrug.append(speed_trig_dff_ctrl_peranimal)

        D1_speed_trig_dff_ctrl_perdrug = np.nanmean(D1_speed_trig_dff_ctrl_perdrug, axis=0)
        D2_speed_trig_dff_ctrl_perdrug = np.nanmean(D2_speed_trig_dff_ctrl_perdrug, axis=0)

        D1_speed_trig_dff_ctrl_all.append(D1_speed_trig_dff_ctrl_perdrug)
        D2_speed_trig_dff_ctrl_all.append(D2_speed_trig_dff_ctrl_perdrug)

    D1_speed_trig_dff_ctrl_all = np.nanmean(D1_speed_trig_dff_ctrl_all, axis=0)
    D2_speed_trig_dff_ctrl_all = np.nanmean(D2_speed_trig_dff_ctrl_all, axis=0)

    D1_speed_trig_dff_ctrl_sem = np.std(D1_speed_trig_dff_ctrl_all, axis=0) / np.sqrt(len(D1_speed_trig_dff_ctrl_all))
    D2_speed_trig_dff_ctrl_sem = np.std(D2_speed_trig_dff_ctrl_all, axis=0) / np.sqrt(len(D2_speed_trig_dff_ctrl_all))

    return D1_speed_trig_dff_ctrl_all, D2_speed_trig_dff_ctrl_all, \
           D1_speed_trig_dff_ctrl_sem, D2_speed_trig_dff_ctrl_sem


def amph():
    D1_speed_trig_dff_amph_all = []
    D2_speed_trig_dff_amph_all = []

    drugs = get_drug()
    # drugs = ['Clozapine']
    dose = 'Vehicle'
    for drug in drugs:
        print(drug + '_amph')

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)
        D1_speed_trig_dff_amph_perdrug = []
        D2_speed_trig_dff_amph_perdrug = []

        for experiment in experiments:
            print(experiment + '_amph')

            speed_ctrl, speed_amph, calcium_ctrl_dff, calcium_amph_dff, _, _, _, _, \
            neuron_count, time_ctrl, time_amph = get_data(drug, dose, experiment)

            # remove events in first 25 and last 25 frames (is this okay to do?)
            window = 25
            speed_amph_modified = speed_amph[window:-window]  # 4450

            # find left turn triggered Ca event dff average per neuron and per animal
            # find frames where angle gets smaller for five consecutive frames (i.e. 1 second)
            speed_amph_frames = []
            for frame in range(0, len(speed_amph_modified) - 4):
                if 1 < speed_amph_modified[frame] < speed_amph_modified[frame + 1] < speed_amph_modified[frame + 2] < \
                        speed_amph_modified[frame + 3] < speed_amph_modified[frame + 4]:
                    frame = frame + window
                    speed_amph_frames.append(frame)

            # find average Ca event of neurons
            calcium_amph_mean = np.mean(calcium_amph_dff, axis=0)

            # find average Ca event of neurons at those frames
            speed_trig_dff_amph = []
            for frame in speed_amph_frames:
                speed_trig_dff_amph.append((calcium_amph_mean[frame - 25:frame + 26]))

            speed_trig_dff_ctrl_peranimal = np.mean(speed_trig_dff_amph, axis=0)

            if experiment in D1_folders:
                D1_speed_trig_dff_amph_perdrug.append(speed_trig_dff_ctrl_peranimal)

            elif experiment in D2_folders:
                D2_speed_trig_dff_amph_perdrug.append(speed_trig_dff_ctrl_peranimal)

        D1_speed_trig_dff_amph_perdrug = np.nanmean(D1_speed_trig_dff_amph_perdrug, axis=0)
        D2_speed_trig_dff_amph_perdrug = np.nanmean(D2_speed_trig_dff_amph_perdrug, axis=0)

        D1_speed_trig_dff_amph_all.append(D1_speed_trig_dff_amph_perdrug)
        D2_speed_trig_dff_amph_all.append(D2_speed_trig_dff_amph_perdrug)

    D1_speed_trig_dff_amph_all = np.nanmean(D1_speed_trig_dff_amph_all, axis=0)
    D2_speed_trig_dff_amph_all = np.nanmean(D2_speed_trig_dff_amph_all, axis=0)

    D1_speed_trig_dff_amph_sem = np.std(D1_speed_trig_dff_amph_all, axis=0) / np.sqrt(len(D1_speed_trig_dff_amph_all))
    D2_speed_trig_dff_amph_sem = np.std(D2_speed_trig_dff_amph_all, axis=0) / np.sqrt(len(D2_speed_trig_dff_amph_all))

    return D1_speed_trig_dff_amph_all, D2_speed_trig_dff_amph_all, \
           D1_speed_trig_dff_amph_sem, D2_speed_trig_dff_amph_sem


def plot():
    D1_speed_trig_dff_ctrl_all, D2_speed_trig_dff_ctrl_all, \
    D1_speed_trig_dff_ctrl_sem, D2_speed_trig_dff_ctrl_sem = ctrl()

    D1_speed_trig_dff_amph_all, D2_speed_trig_dff_amph_all, \
    D1_speed_trig_dff_amph_sem, D2_speed_trig_dff_amph_sem = amph()

    D1_ctrl_yerr_hi = D1_speed_trig_dff_ctrl_all + D1_speed_trig_dff_ctrl_sem
    D1_ctrl_yerr_lo = D1_speed_trig_dff_ctrl_all - D1_speed_trig_dff_ctrl_sem

    D2_ctrl_yerr_hi = D2_speed_trig_dff_ctrl_all + D2_speed_trig_dff_ctrl_sem
    D2_ctrl_yerr_lo = D2_speed_trig_dff_ctrl_all - D2_speed_trig_dff_ctrl_sem

    D1_amph_yerr_hi = D1_speed_trig_dff_amph_all + D1_speed_trig_dff_amph_sem
    D1_amph_yerr_lo = D1_speed_trig_dff_amph_all - D1_speed_trig_dff_amph_sem

    D2_amph_yerr_hi = D2_speed_trig_dff_amph_all + D2_speed_trig_dff_amph_sem
    D2_amph_yerr_lo = D2_speed_trig_dff_amph_all - D2_speed_trig_dff_amph_sem

    x = range(51)

    plt.figure(figsize=(5, 9))
    plt.subplot(211)
    plt.plot(D1_speed_trig_dff_ctrl_all, color='k', label='D1 ctrl')
    plt.fill_between(x, D1_ctrl_yerr_hi, D1_ctrl_yerr_lo, color='k', alpha=0.2)
    # plt.plot(D2_speed_trig_dff_ctrl_all, color='k', label='D2 ctrl')
    # plt.fill_between(x, D2_ctrl_yerr_hi, D2_ctrl_yerr_lo, color='k', alpha=0.2)
    x_default = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    x_new = ['-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5']
    plt.xticks(x_default, x_new)
    plt.xlabel('Time (s) from speed bout (> 1 cm/s)')
    plt.ylabel('Ca activity (dff)')
    plt.title('CTRL')
    plt.suptitle('Speed triggered Ca activity')
    plt.legend()

    plt.subplot(212)
    plt.plot(D1_speed_trig_dff_amph_all, color='b', label='D1 amph')
    plt.fill_between(x, D1_amph_yerr_hi, D1_amph_yerr_lo, color='b', alpha=0.2)
    # plt.plot(D2_speed_trig_dff_amph_all, color='r', label='D2 amph')
    # plt.fill_between(x, D2_amph_yerr_hi, D2_amph_yerr_lo, color='r', alpha=0.2)
    x_default = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    x_new = ['-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5']
    plt.xticks(x_default, x_new)
    plt.xlabel('Time (s) from speed bout (> 1 cm/s)')
    plt.ylabel('Ca activity (dff)')
    plt.title('AMPH')
    plt.legend()
    plt.show()

    return