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
    nospeed_no, lospeed_no, midspeed_no, hispeed_no, acc_no = (0 for i in range(5))

    for fr in range(0, len(speed_data) - 5):
        if speed_data[fr] < 2 and (np.mean(speed_data[fr + 1:fr + 5]) - np.mean(speed_data[fr - 5:fr - 1])) > 1:
            acc_events.append(eventmean_data[fr])
            acc_no += 1
        if speed_data[fr] <= 0.5:
            nospeed_events.append(eventmean_data[fr])
            nospeed_no += 1
        elif 0.5 < speed_data[fr] <= 5:
            lospeed_events.append(eventmean_data[fr])
            lospeed_no += 1
        elif 5 < speed_data[fr] <= 10:
            midspeed_events.append(eventmean_data[fr])
            midspeed_no += 1
        elif 10 < speed_data[fr]:
            hispeed_events.append(eventmean_data[fr])
            hispeed_no += 1

    # number of behavior per behavior time, event rate (event/min) during behavior
    nospeed = [nospeed_no/len(speed_data), np.mean(nospeed_events)*5/nospeed_no]
    lospeed = [lospeed_no/len(speed_data), np.mean(lospeed_events)*5/lospeed_no]
    midspeed = [midspeed_no/len(speed_data), np.mean(midspeed_events)*5/midspeed_no]
    hispeed = [hispeed_no/len(speed_data), np.mean(hispeed_events)*5/hispeed_no]
    acc = [acc_no/len(speed_data), np.mean(acc_events)*5/acc_no]

    return nospeed, lospeed, midspeed, hispeed, acc


def get_turns(turn_data, eventmean_data):

    right_turn_events, left_turn_events, straight_events = ([] for i in range(3))
    right_turn_no, left_turn_no, straight_no = (0 for i in range(3))
    turn_dt = turn_data[1:] - turn_data[:-1]

    for fr in range(2, len(turn_data) - 2):
        if turn_data[fr] > 10 and np.mean(turn_dt[fr-2:fr+2]) > 10:
        # if turn_data[fr] > 10 and turn_dt(max(fr-2,0):min(fr+2,len(turn_dt)):
            right_turn_events.append(eventmean_data[fr])
            right_turn_no += 1
        elif turn_data[fr] < -10 and np.mean(turn_dt[fr-2:fr+2]) < -10:
            left_turn_events.append(eventmean_data[fr])
            left_turn_no += 1
        # elif -10 < turn_data[fr] < 10:
        elif -10 < turn_data[fr] < 10 and -10 < np.mean(turn_dt[fr - 2:fr + 2]) < 10:
            straight_events.append(eventmean_data[fr])
            straight_no += 1

    # frequency of behavior, event rate during behavior
    right_turn = [right_turn_no/len(turn_data), np.mean(right_turn_events)*5/right_turn_no]
    left_turn = [left_turn_no/len(turn_data), np.mean(left_turn_events)*5/left_turn_no]
    straight = [straight_no/len(turn_data), np.mean(straight_events)*5/straight_no]

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

    pickle.dump(alldata, open("alldata.pkl", "wb"))
    # alldata = pickle.load(open("fname.pkl", "rb"))

    return alldata


def plot_timespent(drug, dose):

    bases = ['ctrl', 'amph']
    metrics = ['nospeed', 'lospeed', 'midspeed', 'hispeed', 'acc', 'right_turn', 'left_turn', 'straight']

    # D1_animals, D2_animals = D1_D2_names()

    alldata = pickle.load(open("alldata.pkl", "rb"))
    # alldata = get_alldata()

    plt.figure(figsize=(10, 6))

    # for drug in drugs:
    if dose == 'vehicle':
        for base in bases:
            for metric in metrics:
                y = [alldata[d][dose][base][a][metric] for d in
                     alldata.keys() for a in alldata[d][dose][base].keys()]
                mean = np.nanmean(y, axis=0)
                sem = np.nanstd(y, axis=0) / np.sqrt(len(y))
                plt.bar(metric + '_' + base, mean[0], yerr=sem[0], width=0.5, color='k')
                plt.title('n = ' + str(len(y)))
    else:
        for base in bases:
            for metric in metrics:
                x = [alldata[drug][dose][base][a][metric] for a in alldata[drug][dose][base].keys()]
                mean = np.nanmean(x, axis=0)
                sem = np.nanstd(x, axis=0) / np.sqrt(len(x))
                plt.bar(metric + '_' + base, mean[0], yerr=sem[0], width=0.5, color='k')
                plt.title('n = ' + str(len(x)))

    plt.ylabel('time (s)')
    plt.ylim((0, 1))
    plt.xticks(rotation=30, fontsize=8)
    plt.suptitle(' '.join(drug) + ', ' + dose)
    plt.show()

    return


def plot_eventrate(drug, dose):
    bases = ['ctrl', 'amph']
    # metrics = ['nospeed', 'lospeed', 'midspeed', 'hispeed', 'acc']
    metrics = ['right_turn', 'left_turn', 'straight']

    D1_animals, D2_animals = D1_D2_names()

    alldata = pickle.load(open("alldata.pkl", "rb"))
    # alldata = get_alldata()

    plt.figure(figsize=(10, 6))
    # for drug in drugs:
    if dose == 'vehicle':
        for base in bases:
            for metric in metrics:
                y = [alldata[d][dose][base][a][metric] for d in
                     alldata.keys() for a in alldata[d][dose][base].keys() if a in D2_animals]
                mean = np.ma.masked_invalid(y).mean(axis=0)
                sem = np.ma.masked_invalid(y).std(axis=0) / np.sqrt(len(y))
                plt.bar(metric + '_' + base, mean[1], yerr=sem[1], width=0.5, color='k')
                plt.title('n = ' + str(len(y)))
    else:
        for base in bases:
            for metric in metrics:
                x = [alldata[drug][dose][base][a][metric] for a in alldata[drug][dose][base].keys() if
                     a in D2_animals]
                # pdb.set_trace()
                mean = np.ma.masked_invalid(x).mean(axis=0) #try mean vs np.ma.masked_invalid(x).mean()
                sem = np.ma.masked_invalid(x).std(axis=0) / np.sqrt(len(x))
                plt.bar(metric + '_' + base, mean[1], yerr=sem[1], width=0.5, color='k')
                plt.title('n = ' + str(len(x)))

    plt.ylabel('event rate (event/s)')
    plt.ylim((0, 0.2))
    plt.xticks(rotation=30, fontsize=8)
    plt.suptitle(drug + ', ' + dose)
    plt.show()

    return
