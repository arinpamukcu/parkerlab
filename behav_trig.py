# Created by Arin Pamukcu, PhD on August 2022
# TO-DO: flip this analysis to have a speed (thresholded) trig avg

from data import *
from info import *
from feature_neurons import *
import matplotlib.pyplot as plt
import pdb

def event_trig_avg():

    spike_trig_avg_all = []

    drugs = ['Clozapine']
    # drugs = get_drug()
    dose = 'Vehicle'
    for drug in drugs:
        print(drug)

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)
        spike_trig_avg_perdrug = []

        for experiment in experiments:
            print(experiment)

            speed_ctrl, speed_amph, calcium_ctrl_events, calcium_amph_events, \
            eventmean_ctrl, eventmean_amph, neuron, time_ctrl, time_amph = get_data(drug, dose, experiment)

            # if you just want to use speed neurons for your analysis
            speed_neurons = get_speed_neurons(drug, dose, experiment)

            # remove events in first 25 and last 25 frames (is this okay to do?)
            window = 25
            window_zeros = np.zeros((len(speed_neurons), window))
            speed_neurons_modified = np.hstack((window_zeros, speed_neurons[:, window:-window]))
            speed_neurons_modified = np.hstack((speed_neurons_modified, window_zeros))

            # find spike triggered average per neuron and per all
            spike_trig_avg_peranimal = []

            for neuron in range(0, len(speed_neurons_modified)):
                spike_trig = []
                for frame in range(0, time_ctrl):
                    if speed_neurons_modified[neuron, frame] == 1: #if speed neurons have an event
                        spike_trig.append(speed_ctrl[frame-25:frame+26])

                    pdb.set_trace()
                spike_trig_avg = np.mean(spike_trig, axis=0)
                spike_trig_avg_peranimal.append(spike_trig_avg)

            spike_trig_avg_peranimal = np.mean(spike_trig_avg_peranimal, axis=0)
            spike_trig_avg_perdrug.append(spike_trig_avg_peranimal)

        spike_trig_avg_perdrug = np.mean(spike_trig_avg_perdrug, axis=0)
        spike_trig_avg_all.append(spike_trig_avg_perdrug)

    spike_trig_avg_all = np.mean(spike_trig_avg_all, axis=0)
    print(spike_trig_avg_all)

    plt.figure(figsize=(6, 4))
    plt.plot(spike_trig_avg_all, color='k')
    x_default = [0, 25, 50]
    x_new = ['-25', '0', '+25']
    plt.xticks(x_default, x_new)
    plt.ylim((0, 5))
    plt.xlabel('Frames from event time at 0')
    plt.ylabel('Speed (cm/s)')
    plt.title("Event triggered average")
    plt.legend()
    plt.show()

    return

