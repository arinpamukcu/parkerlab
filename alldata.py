# Created by Arin Pamukcu, PhD on August 2022 in Chicago, IL

from data import *
from info import *
from mars import *
from scipy.io import savemat
import numpy as np
import pickle as pkl
import pdb

def get_speed(speed_data, eventmean_data):

    acc_events, dec_events, rest_events, move_events = ([] for i in range(4))
    acc_duration, dec_duration, rest_duration, move_duration = (0 for i in range(4))
    speed_dt = speed_data[1:] - speed_data[:-1]

    for fr in range(0, len(speed_data) - 2):
        if speed_dt[fr] > 0.25:
            acc_events.append(eventmean_data[fr])
            acc_duration += 1
        if speed_dt[fr] < -0.25:
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
    rest = [rest_duration / len(speed_data), np.sum(rest_events) * 5 / rest_duration]
    move = [move_duration / len(speed_data), np.sum(move_events) * 5 / move_duration]

    return acc, dec, rest, move


def get_turns(turn_data, eventmean_data):

    right_events, left_events = ([] for i in range(2))
    right_duration, left_duration = (0 for i in range(2))
    turn_dt = turn_data[1:] - turn_data[:-1]

    for fr in range(1, len(turn_data) - 1):
        if np.mean(turn_dt[fr - 1:fr + 1]) >= 30:  # turn right
            right_events.append(eventmean_data[fr])
            right_duration += 1
        if np.mean(turn_dt[fr - 1:fr + 1]) <= -30:  # turn left
            left_events.append(eventmean_data[fr])
            left_duration += 1

    # frequency of behavior, event rate during behavior
    right_turn = [right_duration / len(turn_data), np.sum(right_events) * 5 / right_duration]
    left_turn = [left_duration / len(turn_data), np.sum(left_events) * 5 / left_duration]

    return right_turn, left_turn


def get_behavior(speed_data, turn_data, groom_data, rear_data, eventmean_data):

    acc_events, dec_events, rest_events, move_events, right_events, left_events, \
    groom_events, rear_events, other_rest_events, other_move_events = ([] for i in range(10))
    acc_duration, dec_duration, rest_duration, move_duration, right_duration, left_duration, \
    groom_duration, rear_duration, other_rest_duration, other_move_duration = (0 for i in range(10))

    speed_dt = speed_data[1:] - speed_data[:-1]
    turn_dt = turn_data[1:] - turn_data[:-1]

    for fr in range(2, len(turn_data) - 2):
        if speed_data[fr] <= 0.5:
            rest_events.append(eventmean_data[fr])
            rest_duration += 1
        if 0.5 < speed_data[fr]:
            move_events.append(eventmean_data[fr])
            move_duration += 1
        if any(x == 1 for x in rear_data[fr - 2:fr + 3]):
            rear_events.append(eventmean_data[fr])
            rear_duration += 1
        elif any(x == 1 for x in groom_data[fr - 2:fr + 3]):
            groom_events.append(eventmean_data[fr])
            groom_duration += 1
        elif np.mean(turn_dt[fr - 1:fr + 1]) >= 30:  # turn right
            right_events.append(eventmean_data[fr])
            right_duration += 1
        elif np.mean(turn_dt[fr - 1:fr + 1]) <= -30:  # turn left
            left_events.append(eventmean_data[fr])
            left_duration += 1
        elif speed_dt[fr] > 0.25:
            acc_events.append(eventmean_data[fr])
            acc_duration += 1
        elif speed_dt[fr] < -0.25:
            dec_events.append(eventmean_data[fr])
            dec_duration += 1
        elif speed_data[fr] <= 0.5:
            other_rest_events.append(eventmean_data[fr])
            other_rest_duration += 1
        elif 0.5 < speed_data[fr]:
            other_move_events.append(eventmean_data[fr])
            other_move_duration += 1

    # number of behavior per behavior time, event rate (event/min) during behavior
    acc = [acc_duration / len(speed_data), np.sum(acc_events) * 5 / acc_duration]
    dec = [dec_duration / len(speed_data), np.sum(dec_events) * 5 / dec_duration]
    rest = [rest_duration / len(speed_data), np.sum(rest_events) * 5 / rest_duration]
    move = [move_duration / len(speed_data), np.sum(move_events) * 5 / move_duration]
    right_turn = [right_duration / len(turn_data), np.sum(right_events) * 5 / right_duration]
    left_turn = [left_duration / len(turn_data), np.sum(left_events) * 5 / left_duration]
    groom = [groom_duration / len(turn_data), np.sum(groom_events) * 5 / groom_duration]
    rear = [rear_duration / len(turn_data), np.sum(rear_events) * 5 / rear_duration]
    other_rest = [other_rest_duration / len(turn_data), np.sum(other_rest_events) * 5 / other_rest_duration]
    other_move = [other_move_duration / len(turn_data), np.sum(other_move_events) * 5 / other_move_duration]

    return acc, dec, rest, move, right_turn, left_turn, groom, rear, other_rest, other_move


def get_metrics(drug, dose):
    experiments, animals, _, _ = get_animal_id(drug, dose)

    metric_ctrl, metric_amph, fulldata_ctrl, fulldata_amph = ({} for i in range(4))

    for experiment, animal in zip(experiments, animals):
        print(experiment)
        metric_ctrl[animal], metric_amph[animal], fulldata_ctrl[animal], fulldata_amph[animal] = ({} for i in range(4))

        # get values for speed or turn
        speed_ctrl, speed_amph, _, _, eventmean_ctrl, eventmean_amph, neuron, time_ctrl, time_amph \
            = get_ca_data(drug, dose, experiment)
        turn_ctrl, turn_amph \
            = get_mars_features(drug, dose, experiment)
        grooming_ctrl, grooming_amph \
            = get_classifier(drug, dose, experiment, 'grooming')
        rearing_ctrl, rearing_amph \
            = get_classifier(drug, dose, experiment, 'rearing')

        # get values for each animal for that drug & dose
        acc_ctrl, dec_ctrl, rest_ctrl, move_ctrl, right_turn_ctrl, left_turn_ctrl, \
        groom_ctrl, rear_ctrl, other_rest_ctrl, other_move_ctrl \
            = get_behavior(speed_ctrl, turn_ctrl, grooming_ctrl, rearing_ctrl, eventmean_ctrl)
        acc_amph, dec_amph, rest_amph, move_amph, right_turn_amph, left_turn_amph, \
        groom_amph, rear_amph, other_rest_amph, other_move_amph \
            = get_behavior(speed_amph, turn_amph, grooming_amph, rearing_amph, eventmean_amph)

        metric_ctrl[animal]['acc'], metric_ctrl[animal]['dec'], \
        metric_ctrl[animal]['rest'], metric_ctrl[animal]['move'], \
        metric_ctrl[animal]['right_turn'], metric_ctrl[animal]['left_turn'], \
        metric_ctrl[animal]['groom'], metric_ctrl[animal]['rear'], \
        metric_ctrl[animal]['other_rest'], metric_ctrl[animal]['other_move'] = ({} for i in range(10))

        metric_amph[animal]['acc'], metric_amph[animal]['dec'], \
        metric_amph[animal]['rest'], metric_amph[animal]['move'], \
        metric_amph[animal]['right_turn'], metric_amph[animal]['left_turn'], \
        metric_amph[animal]['groom'], metric_amph[animal]['rear'], \
        metric_amph[animal]['other_rest'], metric_amph[animal]['other_move'] = ({} for i in range(10))

        # append values for each animal to the full data list
        fulldata_ctrl[animal]['eventrate_full'] = eventmean_ctrl
        fulldata_ctrl[animal]['speed_full'] = speed_ctrl
        fulldata_ctrl[animal]['turn_full'] = turn_ctrl
        fulldata_ctrl[animal]['rear_full'] = rearing_ctrl
        fulldata_ctrl[animal]['groom_full'] = grooming_ctrl

        fulldata_amph[animal]['eventrate_full'] = eventmean_amph
        fulldata_amph[animal]['speed_full'] = speed_amph
        fulldata_amph[animal]['turn_full'] = turn_amph
        fulldata_amph[animal]['rear_full'] = rearing_amph
        fulldata_amph[animal]['groom_full'] = grooming_amph

        # append values for each animal to the metric data list
        metric_ctrl[animal]['acc']['time'], metric_ctrl[animal]['acc']['rate'] = acc_ctrl
        metric_ctrl[animal]['dec']['time'], metric_ctrl[animal]['dec']['rate'] = dec_ctrl
        metric_ctrl[animal]['rest']['time'], metric_ctrl[animal]['rest']['rate'] = rest_ctrl
        metric_ctrl[animal]['move']['time'], metric_ctrl[animal]['move']['rate'] = move_ctrl
        metric_ctrl[animal]['right_turn']['time'], metric_ctrl[animal]['right_turn']['rate'] = right_turn_ctrl
        metric_ctrl[animal]['left_turn']['time'], metric_ctrl[animal]['left_turn']['rate'] = left_turn_ctrl
        metric_ctrl[animal]['groom']['time'], metric_ctrl[animal]['groom']['rate'] = groom_ctrl
        metric_ctrl[animal]['rear']['time'], metric_ctrl[animal]['rear']['rate'] = rear_ctrl
        metric_ctrl[animal]['other_rest']['time'], metric_ctrl[animal]['other_rest']['rate'] = other_rest_ctrl
        metric_ctrl[animal]['other_move']['time'], metric_ctrl[animal]['other_move']['rate'] = other_move_ctrl

        metric_amph[animal]['acc']['time'], metric_amph[animal]['acc']['rate'] = acc_amph
        metric_amph[animal]['dec']['time'], metric_amph[animal]['dec']['rate'] = dec_amph
        metric_amph[animal]['rest']['time'], metric_amph[animal]['rest']['rate'] = rest_amph
        metric_amph[animal]['move']['time'], metric_amph[animal]['move']['rate'] = move_amph
        metric_amph[animal]['right_turn']['time'], metric_amph[animal]['right_turn']['rate'] = right_turn_amph
        metric_amph[animal]['left_turn']['time'], metric_amph[animal]['left_turn']['rate'] = left_turn_amph
        metric_amph[animal]['groom']['time'], metric_amph[animal]['groom']['rate'] = groom_amph
        metric_amph[animal]['rear']['time'], metric_amph[animal]['rear']['rate'] = rear_amph
        metric_amph[animal]['other_rest']['time'], metric_amph[animal]['other_rest']['rate'] = other_rest_amph
        metric_amph[animal]['other_move']['time'], metric_amph[animal]['other_move']['rate'] = other_move_amph

    return fulldata_ctrl, fulldata_amph, metric_ctrl, metric_amph


def get_alldata():

    drugs = ['clozapine', 'haloperidol', 'mp10', 'olanzapine']
    doses = ['vehicle', 'lowdose', 'highdose']

    allmetrics = {}
    fulldata = {}
    for drug in drugs:
        allmetrics[drug] = {}
        fulldata[drug] = {}

        for dose in doses:
            print(drug, dose)

            allmetrics[drug][dose] = {}
            allmetrics[drug][dose]['ctrl'] = {}
            allmetrics[drug][dose]['amph'] = {}

            fulldata[drug][dose] = {}
            fulldata[drug][dose]['ctrl'] = {}
            fulldata[drug][dose]['amph'] = {}

            fulldata_ctrl, fulldata_amph, metric_ctrl, metric_amph = get_metrics(drug, dose)
            _, animals, _, _ = get_animal_id(drug, dose)

            allmetrics[drug][dose]['ctrl'] = metric_ctrl
            allmetrics[drug][dose]['amph'] = metric_amph

            fulldata[drug][dose]['ctrl'] = fulldata_ctrl
            fulldata[drug][dose]['amph'] = fulldata_amph

    pkl.dump(allmetrics, open("allmetrics.pkl", "wb"))
    savemat("allmetrics.mat", allmetrics)

    pkl.dump(fulldata, open("fulldata.pkl", "wb"))
    savemat("fulldata.mat", fulldata)

    return allmetrics, fulldata


def separate_spns(spn, event):
    # events = ['time', 'rate']
    drugs = ['haloperidol', 'olanzapine', 'clozapine', 'mp10']
    doses = ['vehicle', 'lowdose', 'highdose']
    bases = ['ctrl', 'amph']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'rear', 'other_rest', 'other_move']

    allmetrics = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()

    animals = []
    if spn == 'D1':
        animals = D1_animals
    elif spn == 'D2':
        animals = D2_animals

    data = {}

    for drug in drugs:
        data[drug] = {}

        for dose in doses:
            data[drug][dose] = {}

            for base in bases:
                data[drug][dose][base] = np.ndarray((len(metrics), len(animals)))

                for i, metric in enumerate(metrics):

                    for j, animal in enumerate(animals):

                        if animal in allmetrics[drug][dose][base].keys():
                            data[drug][dose][base][i, j] = allmetrics[drug][dose][base][animal][metric][event]

                        else:
                            data[drug][dose][base][i, j] = 'NaN'

    filename = spn + '_' + event + '.mat'

    savemat(filename, data)

    return data





