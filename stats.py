# Created by Arin Pamukcu, PhD on August 2022
# histogras for time spent doing particular action

from data import *
from info import *
from mars import *
import numpy as np
import matplotlib.pyplot as plt
import pickle
import pdb

def get_speed(speed_data, eventmean_data):

    nospeed_events, lospeed_events, midspeed_events, hispeed_events, acc_events = ([] for i in range(5))
    nospeed_duration, lospeed_duration, midspeed_duration, hispeed_duration, acc_duration = (0 for i in range(5))

    for fr in range(0, len(speed_data) - 5):
        if speed_data[fr] < 1:
            nospeed_events.append(eventmean_data[fr])
            nospeed_duration += 1
        if 1 < speed_data[fr] <= 5:
            lospeed_events.append(eventmean_data[fr])
            lospeed_duration += 1
        if 5 < speed_data[fr] <= 10:
            midspeed_events.append(eventmean_data[fr])
            midspeed_duration += 1
        if 10 < speed_data[fr]:
            hispeed_events.append(eventmean_data[fr])
            hispeed_duration += 1
        if speed_data[fr] < 2 and (np.mean(speed_data[fr + 1:fr + 5]) - np.mean(speed_data[fr - 5:fr - 1])) > 1:
            acc_events.append(eventmean_data[fr])
            acc_duration += 1

    nospeed = [nospeed_duration/5, np.sum(nospeed_events)*5/nospeed_duration]
    lospeed = [lospeed_duration/5, np.sum(lospeed_events)*5/lospeed_duration]
    midspeed = [midspeed_duration/5, np.sum(midspeed_events)*5/midspeed_duration]
    hispeed = [hispeed_duration/5, np.sum(hispeed_events)*5/hispeed_duration]
    acc = [acc_duration/5, np.sum(acc_events)*5/acc_duration]

    return nospeed, lospeed, midspeed, hispeed, acc


def get_turns(turn_data, eventmean_data):

    right_turn_events, left_turn_events, straight_events = ([] for i in range(3))
    right_turn_duration, left_turn_duration, straight_duration = (0 for i in range(3))

    for fr in range(0, len(turn_data) - 5):
        if turn_data[fr] > 20 and turn_data[fr] > turn_data[fr + 1] > turn_data[fr + 2] > turn_data[fr + 3] > turn_data[fr + 4]:
            right_turn_events.append(eventmean_data[fr])
            right_turn_duration += 1
        elif turn_data[fr] < -20 and turn_data[fr] < turn_data[fr + 1] < turn_data[fr + 2] < turn_data[fr + 3] < turn_data[fr + 4]:
            left_turn_events.append(eventmean_data[fr])
            left_turn_duration += 1
        elif -20 < turn_data[fr] < 20:
            straight_events.append(eventmean_data[fr])
            straight_duration += 1

    right_turn = [right_turn_duration/5, np.sum(right_turn_events)*5/straight_duration]
    left_turn = [left_turn_duration/5, np.sum(left_turn_events)*5/straight_duration]
    straight = [straight_duration/5, np.sum(straight_events)*5/straight_duration]

    return right_turn, left_turn, straight


def get_metrics(drug, dose):
    experiments, animals, _, _ = get_animal_id(drug, dose)

    data_ctrl = {}
    data_amph = {}

    for experiment, animal in zip(experiments, animals):
        data_ctrl[animal] = {}
        data_amph[animal] = {}

        print(experiment)

        # get values for speed or turn
        speed_ctrl, speed_amph, _, _, eventmean_ctrl, eventmean_amph, \
        neuron, time_ctrl, time_amph = get_data(drug, dose, experiment)
        turn_angle_ctrl, turn_angle_amph, _, _ = mars_feature(drug, dose, experiment)

        # get values for each animal for that drug & dose
        nospeed_ctrl, lospeed_ctrl, midspeed_ctrl, hispeed_ctrl, acc_ctrl = get_speed(speed_ctrl, eventmean_ctrl)
        nospeed_amph, lospeed_amph, midspeed_amph, hispeed_amph, acc_amph = get_speed(speed_amph, eventmean_amph)
        right_turn_ctrl, left_turn_ctrl, straight_ctrl = get_turns(turn_angle_ctrl, eventmean_ctrl)
        right_turn_amph, left_turn_amph, straight_amph = get_turns(turn_angle_amph, eventmean_amph)

        # append values for each animal to a list
        data_ctrl[animal]['nospeed'] = nospeed_ctrl
        data_ctrl[animal]['lospeed'] = lospeed_ctrl
        data_ctrl[animal]['midspeed'] = midspeed_ctrl
        data_ctrl[animal]['hispeed'] = hispeed_ctrl
        data_ctrl[animal]['acc'] = acc_ctrl
        data_ctrl[animal]['right_turn'] = right_turn_ctrl
        data_ctrl[animal]['left_turn'] = left_turn_ctrl
        data_ctrl[animal]['straight'] = straight_ctrl

        data_amph[animal]['nospeed'] = nospeed_amph
        data_amph[animal]['lospeed'] = lospeed_amph
        data_amph[animal]['midspeed'] = midspeed_amph
        data_amph[animal]['hispeed'] = hispeed_amph
        data_amph[animal]['acc'] = acc_amph
        data_amph[animal]['right_turn'] = right_turn_amph
        data_amph[animal]['left_turn'] = left_turn_amph
        data_amph[animal]['straight'] = straight_amph

    return data_ctrl, data_amph


def get_alldata():

    drugs = ['clozapine', 'haloperidol', 'mp-10', 'olanzapine']
    doses = ['vehicle', 'lowdose', 'highdose']

    alldata = {}
    for drug in drugs:
        alldata[drug] = {}
        for dose in doses:
            print(drug, dose)
            alldata[drug][dose] = {}
            alldata[drug][dose]['ctrl'] = {}
            alldata[drug][dose]['amph'] = {}
            data_ctrl, data_amph = get_metrics(drug, dose)
            _, animals, _, _ = get_animal_id(drug, dose)
            alldata[drug][dose]['ctrl'] = data_ctrl
            alldata[drug][dose]['amph'] = data_amph

    # pdb.set_trace()

    pickle.dump(alldata, open("fname.pkl", "wb"))
    # alldata = pickle.load(open("fname.pkl", "rb"))

    return alldata


def plot_timespent(drugs, dose):

    bases = ['ctrl', 'amph']
    metrics = ['nospeed', 'lospeed', 'midspeed', 'hispeed', 'acc', 'right_turn', 'left_turn']

    # D1_animals, D2_animals = D1_D2_names()

    alldata = pickle.load(open("fname.pkl", "rb"))
    # alldata = get_alldata()

    plt.figure(figsize=(10, 6))

    for drug in drugs:
        if dose == 'vehicle':
            for base in bases:
                for metric in metrics:
                    y = [alldata[d][dose][base][a][metric] for d in
                         alldata.keys() for a in alldata[d][dose][base].keys()]
                    mean = np.mean(y, axis=0)
                    sem = np.std(y, axis=0) / np.sqrt(len(y))
                    plt.bar(metric + '_' + base, mean[0], yerr=sem[0], width=0.5, color='k')
                    plt.title('n = ' + str(len(y)))
        else:
            for base in bases:
                for metric in metrics:
                    x = [alldata[drug][dose][base][a][metric] for a in alldata[drug][dose][base].keys()]
                    mean = np.mean(x, axis=0)
                    sem = np.std(x, axis=0) / np.sqrt(len(x))
                    plt.bar(metric + '_' + base, mean[0], yerr=sem[0], width=0.5, color='k')
                    plt.title('n = ' + str(len(x)))

    plt.ylabel('time (s)')
    plt.ylim((0, 2500))
    plt.xticks(rotation=30, fontsize=8)
    plt.suptitle(' '.join(drugs) + ', ' + dose)
    plt.show()

    return


def plot_eventrate(drugs, dose):
    bases = ['ctrl', 'amph']
    metrics = ['nospeed', 'lospeed', 'midspeed', 'hispeed', 'acc', 'right_turn', 'left_turn']

    D1_animals, D2_animals = D1_D2_names()

    alldata = pickle.load(open("fname.pkl", "rb"))
    # alldata = get_alldata()

    plt.figure(figsize=(10, 6))
    for drug in drugs:
        if dose == 'vehicle':
            for base in bases:
                for metric in metrics:
                    y = [alldata[d][dose][base][a][metric] for d in
                         alldata.keys() for a in alldata[d][dose][base].keys() if a in D2_animals]
                    mean = np.mean(y, axis=0)
                    sem = np.std(y, axis=0) / np.sqrt(len(y))
                    plt.bar(metric + '_' + base, mean[1], yerr=sem[1], width=0.5, color='k')
                    plt.title('n = ' + str(len(y)))
        else:
            for base in bases:
                for metric in metrics:
                    x = [alldata[drug][dose][base][a][metric] for a in alldata[drug][dose][base].keys() if
                         a in D2_animals]
                    mean = np.mean(x, axis=0)
                    sem = np.std(x, axis=0) / np.sqrt(len(x))
                    plt.bar(metric + '_' + base, mean[1], yerr=sem[1], width=0.5, color='k')
                    plt.title('n = ' + str(len(x)))

    plt.ylabel('event rate (event/s)')
    plt.ylim((0,0.07))
    plt.xticks(rotation=30, fontsize=8)
    plt.suptitle(' '.join(drugs) + ', ' + dose)
    plt.show()

    return
