# Created by Arin Pamukcu, PhD on August 2022

from data import *
from info import *
from speed_neurons import *
import matplotlib.pyplot as plt
import pdb

def ctrl():
    D1_spike_trig_avg_ctrl_all = []
    D2_spike_trig_avg_ctrl_all = []

    drugs = get_drug()
    # drugs = ['Clozapine']
    dose = 'Vehicle'
    for drug in drugs:
        print(drug)

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)
        D1_spike_trig_avg_ctrl_perdrug = []
        D2_spike_trig_avg_ctrl_perdrug = []

        for experiment in experiments:
            print(experiment)

            speed_ctrl, speed_amph, _, _, _, _, _, _, \
            neuron_count, time_ctrl, time_amph = get_data(drug, dose, experiment)

            # if you just want to use speed neurons for your analysis
            _, _, _, speed_neuron_ctrl_events, speed_neuron_amph_events = get_speed_neurons(drug, dose, experiment)

            # remove events in first 25 and last 25 frames (is this okay to do?)
            window = 25
            window_zeros = np.zeros((len(speed_neuron_ctrl_events), window))
            speed_neuron_ctrl_modified = np.hstack((window_zeros, speed_neuron_ctrl_events[:, window:-window]))
            speed_neuron_ctrl_modified = np.hstack((speed_neuron_ctrl_modified, window_zeros))

            # find spike triggered average per neuron and per all
            spike_trig_avg_ctrl_peranimal = []

            for neuron in range(0, len(speed_neuron_ctrl_modified)):
                spike_trig_ctrl = []
                for frame in range(0, time_ctrl):

                    # if there is a spike (i.e. 1 in binarized event)
                    if speed_neuron_ctrl_modified[neuron, frame] == 1:
                        spike_trig_ctrl.append(speed_ctrl[frame-25:frame+26]) # TO-DO: plot per neuron

                spike_trig_avg_ctrl = np.mean(spike_trig_ctrl, axis=0)
                spike_trig_avg_ctrl_peranimal.append(spike_trig_avg_ctrl)

            spike_trig_avg_ctrl_peranimal = np.mean(spike_trig_avg_ctrl_peranimal, axis=0)
            # spike_trig_avg_ctrl_perdrug.append(spike_trig_avg_ctrl_peranimal)

            if experiment in D1_folders:
                D1_spike_trig_avg_ctrl_perdrug.append(spike_trig_avg_ctrl_peranimal)

            elif experiment in D2_folders:
                D2_spike_trig_avg_ctrl_perdrug.append(spike_trig_avg_ctrl_peranimal)

        D1_spike_trig_avg_ctrl_perdrug = np.nanmean(D1_spike_trig_avg_ctrl_perdrug, axis=0)
        D2_spike_trig_avg_ctrl_perdrug = np.nanmean(D2_spike_trig_avg_ctrl_perdrug, axis=0)

        D1_spike_trig_avg_ctrl_all.append(D1_spike_trig_avg_ctrl_perdrug)
        D2_spike_trig_avg_ctrl_all.append(D2_spike_trig_avg_ctrl_perdrug)

    D1_spike_trig_avg_ctrl_all = np.nanmean(D1_spike_trig_avg_ctrl_all, axis=0)
    D2_spike_trig_avg_ctrl_all = np.nanmean(D2_spike_trig_avg_ctrl_all, axis=0)

    D1_spike_trig_avg_ctrl_sem = np.std(D1_spike_trig_avg_ctrl_all, axis=0) / np.sqrt(len(D1_spike_trig_avg_ctrl_all))
    D2_spike_trig_avg_ctrl_sem = np.std(D2_spike_trig_avg_ctrl_all, axis=0) / np.sqrt(len(D2_spike_trig_avg_ctrl_all))

    return D1_spike_trig_avg_ctrl_all, D2_spike_trig_avg_ctrl_all, \
           D1_spike_trig_avg_ctrl_sem, D2_spike_trig_avg_ctrl_sem


def amph():
    D1_spike_trig_avg_amph_all = []
    D2_spike_trig_avg_amph_all = []

    drugs = get_drug()
    # drugs = ['Clozapine']
    dose = 'Vehicle'
    for drug in drugs:
        print(drug + '_amph')

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)
        D1_spike_trig_avg_amph_perdrug = []
        D2_spike_trig_avg_amph_perdrug = []

        for experiment in experiments:
            print(experiment + '_amph')

            speed_ctrl, speed_amph, _, _, _, _, _, _, \
            neuron_count, time_ctrl, time_amph = get_data(drug, dose, experiment)

            # if you just want to use speed neurons for your analysis
            _, _, _, speed_neuron_ctrl_events, speed_neuron_amph_events = get_speed_neurons(drug, dose, experiment)

            # remove events in first 25 and last 25 frames (is this okay to do?)
            window = 25
            window_zeros = np.zeros((len(speed_neuron_ctrl_events), window))

            speed_neuron_amph_modified = np.hstack((window_zeros, speed_neuron_amph_events[:, window:-window]))
            speed_neuron_amph_modified = np.hstack((speed_neuron_amph_modified, window_zeros))

            # find spike triggered average per neuron and per all
            spike_trig_avg_amph_peranimal = []

            for neuron in range(0, len(speed_neuron_amph_modified)):
                spike_trig_amph = []
                for frame in range(0, time_amph):

                    # if there is a spike (i.e. 1 in binarized event)
                    if speed_neuron_amph_modified[neuron, frame] == 1:
                        spike_trig_amph.append(speed_amph[frame - 25:frame + 26])  # TO-DO: plot per neuron

                spike_trig_avg_amph = np.mean(spike_trig_amph, axis=0)
                spike_trig_avg_amph_peranimal.append(spike_trig_avg_amph)

            spike_trig_avg_amph_peranimal = np.mean(spike_trig_avg_amph_peranimal, axis=0)
            # spike_trig_avg_amph_perdrug.append(spike_trig_avg_amph_peranimal)

            if experiment in D1_folders:
                D1_spike_trig_avg_amph_perdrug.append(spike_trig_avg_amph_peranimal)

            elif experiment in D2_folders:
                D2_spike_trig_avg_amph_perdrug.append(spike_trig_avg_amph_peranimal)

        D1_spike_trig_avg_amph_perdrug = np.nanmean(D1_spike_trig_avg_amph_perdrug, axis=0)
        D2_spike_trig_avg_amph_perdrug = np.nanmean(D2_spike_trig_avg_amph_perdrug, axis=0)

        D1_spike_trig_avg_amph_all.append(D1_spike_trig_avg_amph_perdrug)
        D2_spike_trig_avg_amph_all.append(D2_spike_trig_avg_amph_perdrug)

    D1_spike_trig_avg_amph_all = np.nanmean(D1_spike_trig_avg_amph_all, axis=0)
    D2_spike_trig_avg_amph_all = np.nanmean(D2_spike_trig_avg_amph_all, axis=0)

    D1_spike_trig_avg_amph_sem = np.std(D1_spike_trig_avg_amph_all, axis=0) / np.sqrt(len(D1_spike_trig_avg_amph_all))
    D2_spike_trig_avg_amph_sem = np.std(D2_spike_trig_avg_amph_all, axis=0) / np.sqrt(len(D2_spike_trig_avg_amph_all))

    return D1_spike_trig_avg_amph_all, D2_spike_trig_avg_amph_all, \
           D1_spike_trig_avg_amph_sem, D2_spike_trig_avg_amph_sem


def plot():
    D1_spike_trig_avg_ctrl_all, D2_spike_trig_avg_ctrl_all, \
    D1_spike_trig_avg_ctrl_sem, D2_spike_trig_avg_ctrl_sem = ctrl()

    D1_spike_trig_avg_amph_all, D2_spike_trig_avg_amph_all, \
    D1_spike_trig_avg_amph_sem, D2_spike_trig_avg_amph_sem = amph()

    D1_ctrl_yerr_hi = D1_spike_trig_avg_ctrl_all + D1_spike_trig_avg_ctrl_sem
    D1_ctrl_yerr_lo = D1_spike_trig_avg_ctrl_all - D1_spike_trig_avg_ctrl_sem

    D2_ctrl_yerr_hi = D2_spike_trig_avg_ctrl_all + D2_spike_trig_avg_ctrl_sem
    D2_ctrl_yerr_lo = D2_spike_trig_avg_ctrl_all - D2_spike_trig_avg_ctrl_sem

    D1_amph_yerr_hi = D1_spike_trig_avg_amph_all + D1_spike_trig_avg_amph_sem
    D1_amph_yerr_lo = D1_spike_trig_avg_amph_all - D1_spike_trig_avg_amph_sem

    D2_amph_yerr_hi = D2_spike_trig_avg_amph_all + D2_spike_trig_avg_amph_sem
    D2_amph_yerr_lo = D2_spike_trig_avg_amph_all - D2_spike_trig_avg_amph_sem

    x = range(51)

    plt.figure(figsize=(6, 9.5))
    plt.subplot(211)
    plt.plot(D1_spike_trig_avg_ctrl_all, color='k', label='D1 ctrl')
    plt.fill_between(x, D1_ctrl_yerr_hi, D1_ctrl_yerr_lo, color='k', alpha=0.2)
    # plt.plot(D2_spike_trig_avg_ctrl_all, color='k', label='D2 ctrl')
    # plt.fill_between(x, D2_ctrl_yerr_hi, D2_ctrl_yerr_lo, color='k', alpha=0.2)
    x_default = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    x_new = ['-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5']
    plt.xticks(x_default, x_new)
    plt.axvline(x=25, color="grey", linestyle=":")
    plt.xlabel('Time (s) from Ca event')
    plt.ylabel('Speed (cm/s)')
    plt.title('CTRL')
    plt.suptitle('Ca event triggered speed')
    plt.legend()

    plt.subplot(212)
    plt.plot(D1_spike_trig_avg_amph_all, color='b', label='D1 amph')
    plt.fill_between(x, D1_amph_yerr_hi, D1_amph_yerr_lo, color='b', alpha=0.2)
    # plt.plot(D2_spike_trig_avg_amph_all, color='r', label='D2 amph')
    # plt.fill_between(x, D2_amph_yerr_hi, D2_amph_yerr_lo, color='r', alpha=0.2)
    x_default = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    x_new = ['-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5']
    plt.xticks(x_default, x_new)
    plt.axvline(x=25, color="grey", linestyle=":")
    plt.xlabel('Time (s) from Ca event')
    plt.ylabel('Speed (cm/s)')
    plt.title('AMPH')
    plt.legend()
    plt.show()

    return
