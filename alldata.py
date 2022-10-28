# Created by Arin Pamukcu, PhD on August 2022
# histogras for time spent doing particular action

from data import *
from info import *
from mars import *
from scipy.io import savemat
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
import pdb

def get_speed(speed_data, eventmean_data):

    acc_events, dec_events, freeze_events, rest_events, move_events = ([] for i in range(5))
    acc_duration, dec_duration, freeze_duration, rest_duration, move_duration = (0 for i in range(5))

    for fr in range(0, len(speed_data) - 5):
        if speed_data[fr] <= 0.5 and (np.mean(speed_data[fr + 1:fr + 5]) - np.mean(speed_data[fr - 5:fr - 1])) > 1:
            acc_events.append(eventmean_data[fr])
            acc_duration += 1
        if 0.5 < speed_data[fr] <= 8 and (np.mean(speed_data[fr + 1:fr + 5]) - np.mean(speed_data[fr - 5:fr - 1])) < 1:
            dec_events.append(eventmean_data[fr])
            dec_duration += 1
        if speed_data[fr] <= 0.1:
            freeze_events.append(eventmean_data[fr])
            freeze_duration += 1
        if speed_data[fr] <= 0.5:
            rest_events.append(eventmean_data[fr])
            rest_duration += 1
        if 0.5 < speed_data[fr] <= 5:
            move_events.append(eventmean_data[fr])
            move_duration += 1

    # number of behavior per behavior time, event rate (event/min) during behavior
    acc = [acc_duration / len(speed_data), np.sum(acc_events) * 5 / acc_duration]
    dec = [dec_duration / len(speed_data), np.sum(dec_events) * 5 / dec_duration]
    freeze = [freeze_duration/len(speed_data), np.sum(freeze_events)*5/freeze_duration]
    rest = [rest_duration/len(speed_data), np.sum(rest_events)*5/rest_duration]
    move = [move_duration/len(speed_data), np.sum(move_events)*5/move_duration]

    return acc, dec, freeze, rest, move


def get_turns(turn_data, eventmean_data):

    lefttocenter_events, centertoright_events, forward_events, \
    centertoleft_events, righttocenter_events = ([] for i in range(5))
    lefttocenter_duration, centertoright_duration, forward_duration, \
    centertoleft_duration, righttocenter_duration = (0 for i in range(5))
    turn_dt = turn_data[1:] - turn_data[:-1]

    for fr in range(2, len(turn_data) - 2):
        if turn_data[fr] <= -10 and np.mean(turn_dt[fr-2:fr+2]) >= 10:  # turn right, from left to center
            lefttocenter_events.append(eventmean_data[fr])
            lefttocenter_duration += 1
        if -10 < turn_data[fr] < 10 and np.mean(turn_dt[fr-2:fr+2]) >= 10:  # turn right, from center to right
            centertoright_events.append(eventmean_data[fr])
            centertoright_duration += 1
        if -10 < turn_data[fr] < 10 and -10 < np.mean(turn_dt[fr-2:fr+2]) < 10:
            forward_events.append(eventmean_data[fr])
            forward_duration += 1
        if -10 < turn_data[fr] < 10 and np.mean(turn_dt[fr-2:fr+2]) <= -10:  # turn left, from center to left
            centertoleft_events.append(eventmean_data[fr])
            centertoleft_duration += 1
        if turn_data[fr] >= 10 and np.mean(turn_dt[fr-2:fr+2]) <= -10:  # turn left, from right to center
            righttocenter_events.append(eventmean_data[fr])
            righttocenter_duration += 1

    # frequency of behavior, event rate during behavior
    lefttocenter = [lefttocenter_duration/len(turn_data), np.sum(lefttocenter_events)*5/lefttocenter_duration]
    centertoright = [centertoright_duration/len(turn_data), np.sum(centertoright_events)*5/centertoright_duration]
    forward = [forward_duration/len(turn_data), np.sum(forward_events)*5/forward_duration]
    centertoleft = [centertoleft_duration/len(turn_data), np.sum(centertoleft_events)*5/centertoleft_duration]
    righttocenter = [righttocenter_duration/len(turn_data), np.sum(righttocenter_events)*5/righttocenter_duration]

    return lefttocenter, centertoright, forward, centertoleft, righttocenter


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
        acc_ctrl, dec_ctrl, freeze_ctrl, rest_ctrl, move_ctrl = get_speed(speed_ctrl, eventmean_ctrl)
        acc_amph, dec_amph, freeze_amph, rest_amph, move_amph = get_speed(speed_amph, eventmean_amph)
        lefttocenter_ctrl, centertoright_ctrl, forward_ctrl, \
        centertoleft_ctrl, righttocenter_ctrl = get_turns(turn_angle_ctrl, eventmean_ctrl)
        lefttocenter_amph, centertoright_amph, forward_amph, \
        centertoleft_amph, righttocenter_amph = get_turns(turn_angle_amph, eventmean_amph)

        # append values for each animal to a list
        data_ctrl[animal]['acc'] = acc_ctrl
        data_ctrl[animal]['dec'] = dec_ctrl
        data_ctrl[animal]['freeze'] = freeze_ctrl
        data_ctrl[animal]['rest'] = rest_ctrl
        data_ctrl[animal]['move'] = move_ctrl
        data_ctrl[animal]['lefttocenter'] = lefttocenter_ctrl
        data_ctrl[animal]['centertoright'] = centertoright_ctrl
        data_ctrl[animal]['forward'] = forward_ctrl
        data_ctrl[animal]['centertoleft'] = centertoleft_ctrl
        data_ctrl[animal]['righttocenter'] = righttocenter_ctrl

        data_amph[animal]['acc'] = acc_amph
        data_amph[animal]['dec'] = dec_amph
        data_amph[animal]['freeze'] = freeze_amph
        data_amph[animal]['rest'] = rest_amph
        data_amph[animal]['move'] = move_amph
        data_amph[animal]['lefttocenter'] = lefttocenter_amph
        data_amph[animal]['centertoright'] = centertoright_amph
        data_amph[animal]['forward'] = forward_amph
        data_amph[animal]['centertoleft'] = centertoleft_amph
        data_amph[animal]['righttocenter'] = righttocenter_amph

    return data_ctrl, data_amph


def get_alldata():

    drugs = ['clozapine', 'haloperidol', 'mp10', 'olanzapine']
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

    pkl.dump(alldata, open("alldata.pkl", "wb"))
    savemat("alldata.mat", alldata)

    return alldata


def plot_timespent(drug, dose):

    # drugs = ['clozapine', 'haloperidol', 'mp10', 'olanzapine']
    doses = ['lowdose', 'highdose']
    bases = ['ctrl', 'amph']
    metrics = ['acc', 'dec', 'freeze', 'rest', 'move',
               'lefttocenter', 'centertoright', 'forward', 'centertoleft', 'righttocenter']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    # alldata = get_alldata()

    # for dose in doses:
    if dose == 'vehicle':
        plt.figure(figsize=(10, 7))
        for base in bases:
            for metric in metrics:
                x = [alldata[d][dose][base][a][metric] for d in
                     alldata.keys() for a in alldata[d][dose][base].keys()]
                mean = np.nanmean(x, axis=0)
                sem = np.nanstd(x, axis=0) / np.sqrt(len(x))
                plt.bar(metric + '_' + base, mean[0], yerr=sem[0], width=0.2, color='k')
                plt.suptitle(' '.join(drug) + ', ' + dose + ', ' + base)
                plt.title('n = ' + str(len(x)))
                plt.xticks(rotation=30, fontsize=8)
                plt.ylabel('time (s)')
                plt.ylim((0, 1))
    else:
        for base in bases:
            plt.figure(figsize=(10, 7))
            for dos in doses:
                for metric in metrics:
                    y = [alldata[drug][dos][base][a][metric] for a in alldata[drug][dos][base].keys()]
                    ymean = np.nanmean(y, axis=0)
                    ysem = np.nanstd(y, axis=0) / np.sqrt(len(y))
                    plt.bar(metric + '_' + dos, ymean[0], yerr=ysem[0], width=0.2, color='k')
                    plt.suptitle(' '.join(drug) + ', ' + base)
                    plt.title('n = ' + str(len(y)))
                    plt.xticks(rotation=30, fontsize=8)
                    plt.ylabel('time (s)')
                    plt.ylim((0, 1))

    plt.show()

    return


def plot_eventrate(drug, dose):

    # drugs = ['clozapine', 'haloperidol', 'mp10', 'olanzapine']
    doses = ['lowdose', 'highdose']
    bases = ['ctrl', 'amph']
    metrics = ['acc', 'dec', 'freeze', 'rest', 'move',
               'lefttocenter', 'centertoright', 'forward', 'centertoleft', 'righttocenter']

    D1_animals, D2_animals = D1_D2_names()

    alldata = pkl.load(open("alldata.pkl", "rb"))
    # alldata = get_alldata()

    # for drug in drugs:
    if dose == 'vehicle':
        plt.figure(figsize=(10, 7))
        for base in bases:
            for metric in metrics:
                x = [alldata[d][dose][base][a][metric] for d in
                     alldata.keys() for a in alldata[d][dose][base].keys() if a in D2_animals]
                xmean = np.ma.masked_invalid(x).mean(axis=0)
                xsem = np.ma.masked_invalid(x).std(axis=0) / np.sqrt(len(x))
                plt.bar(metric + '_' + base, xmean[1], yerr=xsem[1], width=0.2, color='k')
                plt.suptitle(drug + ', ' + dose + ', ' + base + ', D1 SPNs')
                plt.title('n = ' + str(len(x)))
                plt.xticks(rotation=30, fontsize=8)
                plt.ylabel('event rate (event/s)')
                plt.ylim((0, 0.07))

    else:
        for base in bases:
            plt.figure(figsize=(10, 7))
            for dos in doses:
                for metric in metrics:
                    y = [alldata[drug][dos][base][a][metric] for a in alldata[drug][dos][base].keys() if
                         a in D2_animals]
                    ymean = np.ma.masked_invalid(y).mean(axis=0) #try mean vs np.ma.masked_invalid(x).mean()
                    ysem = np.ma.masked_invalid(y).std(axis=0) / np.sqrt(len(y))
                    plt.bar(metric + '_' + dos, ymean[1], yerr=ysem[1], width=0.2, color='k')
                    plt.suptitle(' '.join(drug) + ', ' + base)
                    plt.title('n = ' + str(len(y)))
                    plt.xticks(rotation=30, fontsize=8)
                    plt.ylabel('event rate (event/s)')
                    plt.ylim((0, 0.07))

    plt.show()

    return
