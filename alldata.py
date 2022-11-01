# Created by Arin Pamukcu, PhD on August 2022 in Chicago, IL

from data import *
from info import *
from mars import *
from scipy.io import savemat
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
import pdb

def get_speed(speed_data, eventmean_data):

    acc_events, dec_events, rest_events, move_events = ([] for i in range(4))
    acc_duration, dec_duration, rest_duration, move_duration = (0 for i in range(4))
    speed_dt = speed_data[1:] - speed_data[:-1]

    for fr in range(0, len(speed_data) - 2):
        # if np.mean(speed_dt[fr:fr + 2]) > 0:  #06
        # if speed_data[fr - 2] < speed_data[fr - 1] < speed_data[fr]:  # 05
        # if speed_dt[fr - 2] < speed_dt[fr - 1] < speed_dt[fr]:  # 04
        # if np.mean(speed_data[fr - 2:fr]) <= 0.5 and np.mean(speed_dt[fr:fr + 5]) > 0:  # 03
        if np.mean(speed_dt[fr:fr + 2]) > 0:  # 02
        # if speed_dt[fr] > 0:  # 01
            acc_events.append(eventmean_data[fr])
            acc_duration += 1
        # if np.mean(speed_dt[fr:fr + 2]) < 0:  # 06
        # if speed_data[fr - 2] > speed_data[fr - 1] > speed_data[fr]:  # 05
        # if speed_dt[fr - 2] > speed_dt[fr - 1] > speed_dt[fr]:  # 04
        # if np.mean(speed_data[fr:fr + 2]) <= 0.5 and np.mean(speed_dt[fr - 2:fr]) < 0:  # 03
        if np.mean(speed_dt[fr:fr + 2]) < 0:  # 02
        # if speed_dt[fr] < 0:  # 01
            dec_events.append(eventmean_data[fr])
            dec_duration += 1
        if speed_data[fr] <= 0.5:
            rest_events.append(eventmean_data[fr])
            rest_duration += 1
        if 0.5 < speed_data[fr]:
            move_events.append(eventmean_data[fr])
            move_duration += 1

    # number of behavior per behavior time, event rate (event/min) during behavior
    acc = [acc_duration / len(speed_data), np.sum(acc_events) * 5 / acc_duration]
    dec = [dec_duration / len(speed_data), np.sum(dec_events) * 5 / dec_duration]
    rest = [rest_duration/len(speed_data), np.sum(rest_events)*5/rest_duration]
    move = [move_duration/len(speed_data), np.sum(move_events)*5/move_duration]

    return acc, dec, rest, move


def get_turns(turn_data, eventmean_data):

    right_events, left_events = ([] for i in range(2))
    right_duration, left_duration = (0 for i in range(2))
    turn_dt = turn_data[1:] - turn_data[:-1]
    # TRY just right vs left turn, here or when plotting

    for fr in range(2, len(turn_data) - 2):
        if np.mean(turn_dt[fr - 2:fr + 2]) >= 30:  # turn right
            right_events.append(eventmean_data[fr])
            right_duration += 1
        # if turn_data[fr] <= -10 and np.mean(turn_dt[fr-2:fr+2]) >= 30:  # turn right, from left to center # TRY higher ang vel
        #     lefttocenter_events.append(eventmean_data[fr])
        #     lefttocenter_duration += 1
        # if -10 < turn_data[fr] < 10 and np.mean(turn_dt[fr-2:fr+2]) >= 30:  # turn right, from center to right
        #     centertoright_events.append(eventmean_data[fr])
        #     centertoright_duration += 1
        # if -10 < turn_data[fr] < 10 and np.mean(turn_dt[fr-2:fr+2]) <= -30:  # turn left, from center to left
        #     centertoleft_events.append(eventmean_data[fr])
        #     centertoleft_duration += 1
        # if turn_data[fr] >= 10 and np.mean(turn_dt[fr-2:fr+2]) <= -30:  # turn left, from right to center
        #     righttocenter_events.append(eventmean_data[fr])
        #     righttocenter_duration += 1
        if np.mean(turn_dt[fr - 2:fr + 2]) <= -30:  # turn left
            left_events.append(eventmean_data[fr])
            left_duration += 1

    # frequency of behavior, event rate during behavior
    right_turn = [right_duration / len(turn_data), np.sum(right_events) * 5 / right_duration]
    left_turn = [left_duration / len(turn_data), np.sum(left_events) * 5 / left_duration]

    return right_turn, left_turn


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
        acc_ctrl, dec_ctrl, rest_ctrl, move_ctrl = get_speed(speed_ctrl, eventmean_ctrl)
        acc_amph, dec_amph, rest_amph, move_amph = get_speed(speed_amph, eventmean_amph)
        right_turn_ctrl, left_turn_ctrl = get_turns(turn_angle_ctrl, eventmean_ctrl)
        right_turn_amph, left_turn_amph = get_turns(turn_angle_amph, eventmean_amph)

        # append values for each animal to a list
        data_ctrl[animal]['acc'] = acc_ctrl
        data_ctrl[animal]['dec'] = dec_ctrl
        data_ctrl[animal]['rest'] = rest_ctrl
        data_ctrl[animal]['move'] = move_ctrl
        data_ctrl[animal]['right_turn'] = right_turn_ctrl
        data_ctrl[animal]['left_turn'] = left_turn_ctrl

        data_amph[animal]['acc'] = acc_amph
        data_amph[animal]['dec'] = dec_amph
        data_amph[animal]['rest'] = rest_amph
        data_amph[animal]['move'] = move_amph
        data_amph[animal]['right_turn'] = right_turn_amph
        data_amph[animal]['left_turn'] = left_turn_amph

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

    bases = ['ctrl', 'amph']
    metrics = ['acc', 'dec', 'rest', 'move', 'right_turn', 'left_turn']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    # alldata = get_alldata()

    # for dose in doses:
    if dose == 'vehicle':
        plt.figure(figsize=(8, 5))
        x = 0
        for metric in metrics:
            a = 1
            x = x + 1
            for base in bases:
                data = [alldata[d][dose][base][a][metric] for d in alldata.keys()
                        for a in alldata[d][dose][base].keys()]
                mean = np.nanmean(data, axis=0)
                sem = np.nanstd(data, axis=0) / np.sqrt(len(data))
                plt.bar(x, mean[0], yerr=sem[0], width=1, color='k', alpha=a)
                a = a - 0.5
                x = x + 1
    else:
        plt.figure(figsize=(8, 5))
        x = 0
        for metric in metrics:
            a = 1
            x = x + 1
            for base in bases:
                data = [alldata[drug][dose][base][a][metric] for a in alldata[drug][dose][base].keys()]
                mean = np.nanmean(data, axis=0)
                sem = np.nanstd(data, axis=0) / np.sqrt(len(data))
                plt.bar(x, mean[0], yerr=sem[0], width=1, color='k', alpha=a)
                a = a - 0.5
                x = x + 1

    # plt.suptitle(' '.join(drug) + ', ' + dose)
    x_default = [1.5, 4.5, 7.5, 10.5, 13.5, 16.5]
    plt.xticks(x_default, metrics)
    # plt.xticks(rotation=20, fontsize=8)
    plt.ylabel('time (s)')
    plt.ylim((0, 1))
    plt.legend(['ctrl', 'amph'])
    plt.show()

    return


def plot_eventrate(drug, dose):

    bases = ['ctrl', 'amph']
    metrics = ['acc', 'dec', 'rest', 'move', 'right_turn', 'left_turn']

    D1_animals, D2_animals = D1_D2_names()

    alldata = pkl.load(open("alldata.pkl", "rb"))
    # alldata = get_alldata()

    # for drug in drugs:
    if dose == 'vehicle':
        plt.figure(figsize=(8, 5))
        x = 0
        for metric in metrics:
            a = 1
            x = x + 1
            for base in bases:
                data = [alldata[d][dose][base][a][metric] for d in
                     alldata.keys() for a in alldata[d][dose][base].keys() if a in D2_animals]
                mean = np.ma.masked_invalid(data).mean(axis=0)
                sem = np.ma.masked_invalid(data).std(axis=0) / np.sqrt(len(data))
                plt.bar(x, mean[1], yerr=sem[1], width=1, color='k', alpha=a)
                a = a - 0.5
                x = x + 1

    else:
        plt.figure(figsize=(8, 5))
        x = 0
        for metric in metrics:
            a = 1
            x = x + 1
            for base in bases:
                data = [alldata[drug][dose][base][a][metric] for a in alldata[drug][dose][base].keys() if
                     a in D2_animals]
                mean = np.ma.masked_invalid(data).mean(axis=0)
                sem = np.ma.masked_invalid(data).std(axis=0) / np.sqrt(len(data))
                plt.bar(x, mean[1], yerr=sem[1], width=1, color='k', alpha=a)
                a = a - 0.5
                x = x + 1

    plt.suptitle(' '.join(drug) + ', ' + base)
    # plt.title('n = ' + str(len(y)))
    # plt.xticks(rotation=20, fontsize=8)
    x_default = [1.5, 4.5, 7.5, 10.5, 13.5, 16.5]
    plt.xticks(x_default, metrics)
    plt.ylabel('event rate (event/s)')
    plt.ylim((0, 0.07))
    plt.show()

    return


def plot_times():

    drugs = ['haloperidol', 'clozapine', 'olanzapine', 'mp10']
    doses = ['vehicle', 'highdose']
    bases = ['ctrl', 'amph']
    metrics = ['acc', 'dec', 'rest', 'move', 'right_turn', 'left_turn']

    alldata = pkl.load(open("alldata.pkl", "rb"))

    fig, ax = plt.subplots()
    x = 0
    for metric in metrics:
        for dose in doses:
            if dose == 'vehicle':
                colors = ['black', 'gray']
                x = x + 2
                for base, color in zip(bases, colors):
                    data = [alldata[d][dose][base][a][metric] for d in alldata.keys()
                            for a in alldata[d][dose][base].keys()]
                    mean = np.nanmean(data, axis=0)
                    sem = np.nanstd(data, axis=0) / np.sqrt(len(data))
                    print(base)
                    print(mean[0])
                    ax.bar(x, mean[0], yerr=sem[0], width=1, color=color)
                    x = x + 1
            else:
                colors = ['royalblue', 'orangered', 'forestgreen', 'darkviolet']
                for drug, color in zip(drugs, colors):
                    x = x + 0.5
                    data = [alldata[drug][dose]['amph'][a][metric] for a in alldata[drug][dose]['amph'].keys()]
                    mean = np.nanmean(data, axis=0)
                    sem = np.nanstd(data, axis=0) / np.sqrt(len(data))
                    print(drug)
                    print(mean[0])
                    ax.bar(x, mean[0], yerr=sem[0], width=1, color=color, alpha=0.7)
                    x = x + 1

    plt.suptitle('fraction of time spent performing behaviors')
    plt.legend(['ctrl', 'amph', 'haloperidol', 'clozapine', 'olanzapine', 'mp10'])
    x_default = [2.5, 12.5, 22.5, 32.5, 42.5, 52.5]
    # plt.legend(['ctrl', 'amph'])
    # x_default = [2.5, 6.5, 10.5, 14.5, 18.5, 22.5]
    plt.xticks(x_default, metrics)
    plt.xticks(fontsize=8)
    plt.ylabel('time spent fraction')
    plt.ylim((0, 1))
    plt.show()

    return


def plot_events(spn):

    drugs = ['haloperidol', 'clozapine', 'olanzapine', 'mp10']
    doses = ['vehicle', 'highdose']
    bases = ['ctrl', 'amph']
    metrics = ['acc', 'dec', 'rest', 'move', 'right_turn', 'left_turn']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()

    animals = []
    if spn == 'D1':
        animals = D1_animals
    elif spn == 'D2':
        animals = D2_animals

    # plt.figure(figsize=(8, 5))
    fig, ax = plt.subplots()
    x = 0
    for metric in metrics:
        for dose in doses:
            if dose == 'vehicle':
                colors = ['black', 'gray']
                x = x + 2
                for base, color in zip(bases, colors):
                    data = [alldata[d][dose][base][s][metric] for d in
                            alldata.keys() for s in alldata[d][dose][base].keys() if s in animals]
                    mean = np.nanmean(data, axis=0)
                    sem = np.nanstd(data, axis=0) / np.sqrt(len(data))
                    ax.bar(x, mean[1], yerr=sem[1], width=1, color=color)
                    x = x + 1
            else:
                colors = ['royalblue', 'orangered', 'forestgreen', 'darkviolet']
                for drug, color in zip(drugs, colors):
                    x = x + 0.5
                    data = [alldata[drug][dose]['amph'][s][metric] for s in alldata[drug][dose]['amph'].keys() if
                            s in animals]
                    mean = np.nanmean(data, axis=0)
                    sem = np.nanstd(data, axis=0) / np.sqrt(len(data))
                    ax.bar(x, mean[1], yerr=sem[1], width=1, color=color, alpha=0.7)
                    x = x + 1

    plt.suptitle(str(spn) + ' SPN event rate during performing behaviors')
    # plt.title('n = ' + str(len(data)))
    x_default = [2.5, 12.5, 22.5, 32.5, 42.5, 52.5]
    plt.xticks(x_default, metrics)
    plt.xticks(fontsize=8)
    plt.ylabel('event rate (event/s)')
    plt.ylim((0, 0.07))
    plt.legend(['ctrl', 'amph', 'haloperidol', 'clozapine', 'olanzapine', 'mp10'])
    plt.show()

    return
