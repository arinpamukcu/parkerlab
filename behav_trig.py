# Created by Arin Pamukcu, PhD on August 2022
# TO-DO: flip this analysis to have a speed (thresholded) trig avg

from data import *
from info import *
from mars import *
from feature_neurons import *
import matplotlib.pyplot as plt
import pdb

def behav_trig_avg():

    behav_trig_avg_all = []

    drugs = ['Clozapine']
    # drugs = get_drug()
    dose = 'Vehicle'
    for drug in drugs:
        print(drug)

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)
        behav_trig_avg_perdrug = []

        for experiment in experiments:
            print(experiment)

            _, _, calcium_ctrl_dff, calcium_amph_dff, _, _, \
            eventmean_ctrl, eventmean_amph, neuron_count, time_ctrl, time_amph = get_data(drug, dose, experiment)

            _, _, mars_left_angle_ctrl, mars_left_angle_amph, _, _ = mars_feature(drug, dose, experiment)

            # remove events in first 25 and last 25 frames (is this okay to do?)
            window = 25
            mars_left_angle_ctrl_modified = mars_left_angle_ctrl[window:-window]  # 4450
            mars_left_angle_amph_modified = mars_left_angle_amph[window:-window]

            mars_right_angle_ctrl_modified = mars_left_angle_ctrl[window:-window]  # 13450
            mars_right_angle_amph_modified = mars_left_angle_amph[window:-window]

            # find spike triggered average per neuron and per all
            behav_trig_avg_ctrl_neurons = []
            for neuron in range(0, neuron_count):
                # print(neuron)
                behav_trig_avg_ctrl = []
                for frame in range(0, len(mars_left_angle_ctrl_modified) - 4):
                    if mars_left_angle_ctrl_modified[frame] > mars_left_angle_ctrl_modified[frame + 1] > \
                            mars_left_angle_ctrl_modified[frame + 2] > mars_left_angle_ctrl_modified[frame + 3] > \
                            mars_left_angle_ctrl_modified[frame + 4]:
                        behav_trig_avg_ctrl.append((calcium_ctrl_dff[neuron, frame - 25:frame + 26]))

                behav_trig_avg_ctrl_perneuron = np.mean(behav_trig_avg_ctrl, axis=0)
                behav_trig_avg_ctrl_neurons.append(behav_trig_avg_ctrl_perneuron)

            behav_trig_avg_ctrl_peranimal = np.mean(behav_trig_avg_ctrl_neurons, axis=0)
            behav_trig_avg_perdrug.append(behav_trig_avg_ctrl_peranimal)

        behav_trig_avg_perdrug = np.mean(behav_trig_avg_perdrug, axis=0)
        behav_trig_avg_all.append(behav_trig_avg_perdrug)

    behav_trig_avg_all = np.mean(behav_trig_avg_all, axis=0)
    print(behav_trig_avg_all)

    plt.figure(figsize=(6, 4))
    plt.plot(behav_trig_avg_all, color='k')
    x_default = [0, 25, 50]
    x_new = ['-25', '0', '+25']
    plt.xticks(x_default, x_new)
    plt.ylim((0, 5))
    plt.xlabel('Frames from event time at 0')
    plt.ylabel('Speed (cm/s)')
    plt.title("Left turn triggered spike average")
    plt.legend()
    plt.show()

    return

