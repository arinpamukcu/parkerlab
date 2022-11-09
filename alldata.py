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
    # TRY just right vs left turn, here or when plotting

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


# def get_rearing_grooming(annotated_data, eventmean_data):
#
#     behavior_events = []
#     behavior_duration = 0
#
#     for fr in range(0, len(annotated_data)):
#         if annotated_data == 1.:
#             behavior_events.append(eventmean_data[fr])
#             behavior_duration
#
#     behavior = [behavior_duration / len(annotated_data), np.sum(behavior_events) * 5 / behavior_duration]
#
#     return behavior


def get_behavior(speed_data, turn_data, groom_data, eventmean_data):

    acc_events, dec_events, rest_events, move_events, right_events, left_events, groom_events, other_events \
        = ([] for i in range(7))
    acc_duration, dec_duration, rest_duration, move_duration, right_duration, left_duration, groom_duration, other_duration \
        = (0 for i in range(7))

    speed_dt = speed_data[1:] - speed_data[:-1]
    turn_dt = turn_data[1:] - turn_data[:-1]

    for fr in range(1, len(turn_data) - 1):
        if speed_data[fr] <= 0.5:
            rest_events.append(eventmean_data[fr])
            rest_duration += 1
        if 0.5 < speed_data[fr]:
            move_events.append(eventmean_data[fr])
            move_duration += 1
        if groom_data[fr] == 1:
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
        else:
            other_events.append(eventmean_data[fr])
            other_duration += 1

    # number of behavior per behavior time, event rate (event/min) during behavior
    acc = [acc_duration / len(speed_data), np.sum(acc_events) * 5 / acc_duration]
    dec = [dec_duration / len(speed_data), np.sum(dec_events) * 5 / dec_duration]
    rest = [rest_duration / len(speed_data), np.sum(rest_events) * 5 / rest_duration]
    move = [move_duration / len(speed_data), np.sum(move_events) * 5 / move_duration]
    right_turn = [right_duration / len(turn_data), np.sum(right_events) * 5 / right_duration]
    left_turn = [left_duration / len(turn_data), np.sum(left_events) * 5 / left_duration]
    groom = [groom_duration / len(turn_data), np.sum(groom_events) * 5 / groom_duration]
    other = [other_duration / len(turn_data), np.sum(other_events) * 5 / other_duration]

    return acc, dec, rest, move, right_turn, left_turn, groom, other


def get_metrics(drug, dose):
    experiments, animals, _, _ = get_animal_id(drug, dose)

    data_ctrl = {}
    data_amph = {}

    for experiment, animal in zip(experiments, animals):
        data_ctrl[animal] = {}
        data_amph[animal] = {}

        print(experiment)

        # get values for speed or turn
        speed_ctrl, speed_amph, _, _, eventmean_ctrl, eventmean_amph, neuron, time_ctrl, time_amph \
            = get_ca_data(drug, dose, experiment)
        turn_angle_ctrl, turn_angle_amph \
            = get_mars_features(drug, dose, experiment)
        grooming_ctrl, grooming_amph \
            = get_classifiers(drug, dose, experiment, 'grooming')

        # # get values for each animal for that drug & dose
        # acc_ctrl, dec_ctrl, rest_ctrl, move_ctrl = get_speed(speed_ctrl, eventmean_ctrl)
        # acc_amph, dec_amph, rest_amph, move_amph = get_speed(speed_amph, eventmean_amph)
        # right_turn_ctrl, left_turn_ctrl = get_turns(turn_angle_ctrl, eventmean_ctrl)
        # right_turn_amph, left_turn_amph = get_turns(turn_angle_amph, eventmean_amph)
        acc_ctrl, dec_ctrl, rest_ctrl, move_ctrl, right_turn_ctrl, left_turn_ctrl, groom_ctrl, other_ctrl \
            = get_behavior(speed_ctrl, turn_angle_ctrl, grooming_ctrl, eventmean_ctrl)
        acc_amph, dec_amph, rest_amph, move_amph, right_turn_amph, left_turn_amph, groom_amph, other_amph \
            = get_behavior(speed_amph, turn_angle_amph, grooming_amph, eventmean_amph)

        # append values for each animal to a list
        data_ctrl[animal]['eventrate'] = eventmean_ctrl
        data_ctrl[animal]['speed'] = speed_ctrl
        data_ctrl[animal]['turn'] = turn_angle_ctrl
        data_ctrl[animal]['acc'] = acc_ctrl
        data_ctrl[animal]['dec'] = dec_ctrl
        data_ctrl[animal]['rest'] = rest_ctrl
        data_ctrl[animal]['move'] = move_ctrl
        data_ctrl[animal]['right_turn'] = right_turn_ctrl
        data_ctrl[animal]['left_turn'] = left_turn_ctrl
        data_ctrl[animal]['groom'] = groom_ctrl
        data_ctrl[animal]['other'] = other_ctrl

        data_amph[animal]['eventrate'] = eventmean_amph
        data_amph[animal]['speed'] = speed_amph
        data_amph[animal]['turn'] = turn_angle_amph
        data_amph[animal]['acc'] = acc_amph
        data_amph[animal]['dec'] = dec_amph
        data_amph[animal]['rest'] = rest_amph
        data_amph[animal]['move'] = move_amph
        data_amph[animal]['right_turn'] = right_turn_amph
        data_amph[animal]['left_turn'] = left_turn_amph
        data_amph[animal]['groom'] = groom_amph
        data_amph[animal]['other'] = other_amph

    return data_ctrl, data_amph


def get_alldata():

    drugs = ['clozapine', 'haloperidol', 'mp10', 'olanzapine']
    doses = ['vehicle', 'lowdose', 'highdose']
    # doses = ['vehicle', 'highdose']

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


