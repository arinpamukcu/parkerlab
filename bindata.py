# Created by Arin Pamukcu, PhD on August 2022

# y-axis: Ca event rate (event/min)
# x-axis: Locomotor speed bin (cm/s)

from data import *
from info import *
from mars import *
from scipy.io import savemat
from collections import defaultdict
import matplotlib.pyplot as plt
import pickle as pkl
import pandas as pd
import numpy as np
import pdb
# pdb.set_trace()

def turn_bins(speed_data, turn_data, speed1, speed2, eventmean_data):
    left60_events, left30_events, forward0_events, right30_events, right60_events = ([] for i in range(5))
    left60_duration, left30_duration, forward0_duration, right30_duration, right60_duration = (0 for i in range(5))

    for fr in range(0, len(turn_data)):
        if speed1 < speed_data[fr] <= speed2 and -75 < turn_data[fr] <= -45:
            left60_events.append(eventmean_data[fr])
            left60_duration += 1
        if speed1 < speed_data[fr] <= speed2 and -45 < turn_data[fr] <= -15:
            left30_events.append(eventmean_data[fr])
            left30_duration += 1
        if speed1 < speed_data[fr] <= speed2 and -15 < turn_data[fr] <= 15:
            forward0_events.append(eventmean_data[fr])
            forward0_duration += 1
        if speed1 < speed_data[fr] <= speed2 and 15 < turn_data[fr] <= 45:
            right30_events.append(eventmean_data[fr])
            right30_duration += 1
        if speed1 < speed_data[fr] <= speed2 and 45 < turn_data[fr] <= 75:
            right60_events.append(eventmean_data[fr])
            right60_duration += 1

    eventrate_vs_turn_speed = [(np.sum(left60_events) / left60_duration) * 300,
                               (np.sum(left30_events) / left30_duration) * 300,
                               (np.sum(forward0_events) / forward0_duration) * 300,
                               (np.sum(right30_events) / right30_duration) * 300,
                               (np.sum(right60_events) / right60_duration) * 300]

    duration_vs_turn_speed = [left60_duration, left30_duration, forward0_duration, right30_duration, right60_duration]

    return eventrate_vs_turn_speed, duration_vs_turn_speed


def speed_bins(speed_data, turn_data, turn_angle, eventmean_data):
    speed1_events, speed2_events, speed3_events, speed4_events, speed5_events = ([] for i in range(5))
    speed1_duration, speed2_duration, speed3_duration, speed4_duration, speed5_duration = (0 for i in range(5))

    for fr in range(0, len(turn_data)):
        if speed_data[fr] <= 0.5 and turn_angle-15 < turn_data[fr] <= turn_angle+15:
            speed1_events.append(eventmean_data[fr])
            speed1_duration += 1
        if 0.5 < speed_data[fr] <= 1 and turn_angle-15 < turn_data[fr] <= turn_angle+15:
            speed2_events.append(eventmean_data[fr])
            speed2_duration += 1
        if 1 < speed_data[fr] <= 2 and turn_angle-15 < turn_data[fr] <= turn_angle+15:
            speed3_events.append(eventmean_data[fr])
            speed3_duration += 1
        if 2 < speed_data[fr] <= 4 and turn_angle-15 < turn_data[fr] <= turn_angle+15:
            speed4_events.append(eventmean_data[fr])
            speed4_duration += 1
        if 4 < speed_data[fr] <= 8 and turn_angle-15 < turn_data[fr] <= turn_angle+15:
            speed5_events.append(eventmean_data[fr])
            speed5_duration += 1

    eventrate_vs_speed_turn = [(np.sum(speed1_events) / speed1_duration) * 300,
                               (np.sum(speed2_events) / speed2_duration) * 300,
                               (np.sum(speed3_events) / speed3_duration) * 300,
                               (np.sum(speed4_events) / speed4_duration) * 300,
                               (np.sum(speed5_events) / speed5_duration) * 300]

    duration_vs_speed_turn = [speed1_duration, speed2_duration, speed3_duration, speed4_duration, speed5_duration]

    return eventrate_vs_speed_turn, duration_vs_speed_turn


def angvel_bins(speed_data, turn_data, speed1, speed2, eventmean_data):
    angvel1_events, angvel2_events, angvel3_events, angvel4_events, angvel5_events = ([] for i in range(5))
    angvel1_duration, angvel2_duration, angvel3_duration, angvel4_duration, angvel5_duration = (0 for i in range(5))
    turn_dt = turn_data[1:] - turn_data[:-1]

    for fr in range(0, len(turn_data)):
        if speed1 < speed_data[fr] <= speed2 and -50 < np.mean(turn_dt[fr-2:fr+2]) <= -30:  # turn right
            angvel1_events.append(eventmean_data[fr])
            angvel1_duration += 1
        if speed1 < turn_data[fr] <= speed2 and -30 < np.mean(turn_dt[fr - 2:fr + 2]) <= -10:  # turn right
            angvel2_events.append(eventmean_data[fr])
            angvel2_duration += 1
        if speed1 < turn_data[fr] <= speed2 and -10 < np.mean(turn_dt[fr - 2:fr + 2]) <= 10:  # center
            angvel3_events.append(eventmean_data[fr])
            angvel3_duration += 1
        if speed1 < turn_data[fr] <= speed2 and 10 < np.mean(turn_dt[fr - 2:fr + 2]) <= 30:  # turn left
            angvel4_events.append(eventmean_data[fr])
            angvel4_duration += 1
        if speed1 < turn_data[fr] <= speed2 and 30 < np.mean(turn_dt[fr - 2:fr + 2]) <= 50:  # turn left
            angvel5_events.append(eventmean_data[fr])
            angvel5_duration += 1

    eventrate_vs_angvel = [(np.sum(angvel1_events) / angvel1_duration) * 300,
                           (np.sum(angvel2_events) / angvel2_duration) * 300,
                           (np.sum(angvel3_events) / angvel3_duration) * 300,
                           (np.sum(angvel4_events) / angvel4_duration) * 300,
                           (np.sum(angvel5_events) / angvel5_duration) * 300]

    duration_vs_angvel = [angvel1_duration, angvel2_duration, angvel3_duration, angvel4_duration, angvel5_duration]

    return eventrate_vs_angvel, duration_vs_angvel



def get_metrics(drug, dose):
    experiments, animals, _, _ = get_animal_id(drug, dose)

    speedbins_ctrl, speedbins_amph, \
    turnbins_ctrl, turnbins_amph, \
    angvelbins_ctrl, angvelbins_amph = ({} for i in range(6))

    for experiment, animal in zip(experiments, animals):
        speedbins_ctrl[animal], speedbins_amph[animal], \
        turnbins_ctrl[animal], turnbins_amph[animal], \
        angvelbins_ctrl[animal], angvelbins_amph[animal] = ({} for i in range(6))

        print(experiment)

        # get values for speed or turn
        speed_ctrl, speed_amph, _, _, eventmean_ctrl, eventmean_amph, \
        _, time_ctrl, time_amph = get_ca_data(drug, dose, experiment)
        turn_ctrl, turn_amph, _, _ = get_mars_features(drug, dose, experiment)

        # get values for each animal for that drug & dose
        eventrate_speed_right2_ctrl, duration_speed_right2_ctrl = speed_bins(speed_ctrl, turn_ctrl, 60, eventmean_ctrl)
        eventrate_speed_right1_ctrl, duration_speed_right1_ctrl = speed_bins(speed_ctrl, turn_ctrl, 30, eventmean_ctrl)
        eventrate_speed_forward_ctrl, duration_speed_forward_ctrl = speed_bins(speed_ctrl, turn_ctrl, 0, eventmean_ctrl)
        eventrate_speed_left1_ctrl, duration_speed_left1_ctrl = speed_bins(speed_ctrl, turn_ctrl, -30, eventmean_ctrl)
        eventrate_speed_left2_ctrl, duration_speed_left2_ctrl = speed_bins(speed_ctrl, turn_ctrl, -60, eventmean_ctrl)
        eventrate_speed_right2_amph, duration_speed_right2_amph = speed_bins(speed_amph, turn_amph, 60, eventmean_amph)
        eventrate_speed_right1_amph, duration_speed_right1_amph = speed_bins(speed_amph, turn_amph, 30, eventmean_amph)
        eventrate_speed_forward_amph, duration_speed_forward_amph = speed_bins(speed_amph, turn_amph, 0, eventmean_amph)
        eventrate_speed_left1_amph, duration_speed_left1_amph = speed_bins(speed_amph, turn_amph, -30, eventmean_amph)
        eventrate_speed_left2_amph, duration_speed_left2_amph = speed_bins(speed_amph, turn_amph, -60, eventmean_amph)

        eventrate_turn_rest_ctrl, duration_turn_rest_ctrl = turn_bins(speed_ctrl, turn_ctrl, 0, 0.5, eventmean_ctrl)
        eventrate_turn_move_ctrl, duration_turn_move_ctrl = turn_bins(speed_ctrl, turn_ctrl, 0.5, 8, eventmean_ctrl)
        eventrate_turn_rest_amph, duration_turn_rest_amph = turn_bins(speed_amph, turn_amph, 0, 0.5, eventmean_amph)
        eventrate_turn_move_amph, duration_turn_move_amph = turn_bins(speed_amph, turn_amph, 0.5, 8, eventmean_amph)

        eventrate_angvel_rest_ctrl, duration_angvel_rest_ctrl = angvel_bins(speed_ctrl, turn_ctrl, 0, 0.5, eventmean_ctrl)
        eventrate_angvel_move_ctrl, duration_angvel_move_ctrl = angvel_bins(speed_ctrl, turn_ctrl, 0.5, 8, eventmean_ctrl)
        eventrate_angvel_rest_amph, duration_angvel_rest_amph = angvel_bins(speed_amph, turn_amph, 0, 0.5, eventmean_amph)
        eventrate_angvel_move_amph, duration_angvel_move_amph = angvel_bins(speed_amph, turn_amph, 0.5, 8, eventmean_amph)

        # append values for each animal to a list
        speedbins_ctrl[animal]['right60'] = eventrate_speed_right2_ctrl, duration_speed_right2_ctrl
        speedbins_ctrl[animal]['right30'] = eventrate_speed_right1_ctrl, duration_speed_right1_ctrl
        speedbins_ctrl[animal]['forward0'] = eventrate_speed_forward_ctrl, duration_speed_forward_ctrl
        speedbins_ctrl[animal]['left30'] = eventrate_speed_left1_ctrl, duration_speed_left1_ctrl
        speedbins_ctrl[animal]['left60'] = eventrate_speed_left2_ctrl, duration_speed_left2_ctrl
        turnbins_ctrl[animal]['rest'] = eventrate_turn_rest_ctrl, duration_turn_rest_ctrl
        turnbins_ctrl[animal]['move'] = eventrate_turn_move_ctrl, duration_turn_move_ctrl
        angvelbins_ctrl[animal]['rest'] = eventrate_angvel_rest_ctrl, duration_angvel_rest_ctrl
        angvelbins_ctrl[animal]['move'] = eventrate_angvel_move_ctrl, duration_angvel_move_ctrl

        speedbins_amph[animal]['right60'] = eventrate_speed_right2_amph, duration_speed_right2_amph
        speedbins_amph[animal]['right30'] = eventrate_speed_right1_amph, duration_speed_right1_amph
        speedbins_amph[animal]['forward0'] = eventrate_speed_forward_amph, duration_speed_forward_amph
        speedbins_amph[animal]['left30'] = eventrate_speed_left1_amph, duration_speed_left1_amph
        speedbins_amph[animal]['left60'] = eventrate_speed_left2_amph, duration_speed_left2_amph
        turnbins_amph[animal]['rest'] = eventrate_turn_rest_amph, duration_turn_rest_amph
        turnbins_amph[animal]['move'] = eventrate_turn_move_amph, duration_turn_move_amph
        angvelbins_amph[animal]['rest'] = eventrate_angvel_rest_amph, duration_angvel_rest_amph
        angvelbins_amph[animal]['move'] = eventrate_angvel_move_amph, duration_angvel_move_amph

        # stop: for speed < 0.5, turn bins at -60, -30, 0, 30, 60 nose-neck-tail angle
        # move: for 0.5 < speed < 8, turn bins at -60, -30, 0, 30, 60
        # right60: for 60 nose-neck-tail angle, speed bins at 0.5, 0.5-1, 1-2, 2-4, 4-8,
        # right30: for 30 nose-neck-tail angle, speed bins at 0.5, 0.5-1, 1-2, 2-4, 4-8
        # straight0: for 0 nose-neck-tail angle, speed bins at 0.5, 0.5-1, 1-2, 2-4, 4-8
        # left30: for -30 nose-neck-tail angle, speed bins at 0.5, 0.5-1, 1-2, 2-4, 4-8
        # left60: for -60 nose-neck-tail angle, speed bins at 0.5, 0.5-1, 1-2, 2-4, 4-8

    return speedbins_ctrl, speedbins_amph, turnbins_amph, turnbins_ctrl, angvelbins_ctrl, angvelbins_amph


def get_bins():

    drugs = ['clozapine', 'haloperidol', 'mp10', 'olanzapine']
    doses = ['vehicle', 'lowdose', 'highdose']

    bindata = {}
    for drug in drugs:
        bindata[drug] = {}

        for dose in doses:
            print(drug, dose)

            bindata[drug][dose], \
            bindata[drug][dose]['ctrl'], bindata[drug][dose]['amph'], \
            bindata[drug][dose]['ctrl']['speed'], bindata[drug][dose]['amph']['speed'], \
            bindata[drug][dose]['amph']['speed'], bindata[drug][dose]['amph']['turn'], \
            bindata[drug][dose]['ctrl']['angvel'], bindata[drug][dose]['amph']['angvel'] = ({} for i in range(9))
            speedbins_ctrl, speedbins_amph, turnbins_ctrl, turnbins_amph, \
            angvelbins_ctrl, angvelbins_amph = get_metrics(drug, dose)
            _, animals, _, _ = get_animal_id(drug, dose)
            bindata[drug][dose]['ctrl']['speed'] = speedbins_ctrl
            bindata[drug][dose]['amph']['speed'] = speedbins_amph
            bindata[drug][dose]['ctrl']['turn'] = turnbins_ctrl
            bindata[drug][dose]['amph']['turn'] = turnbins_amph
            bindata[drug][dose]['ctrl']['angvel'] = angvelbins_ctrl
            bindata[drug][dose]['amph']['angvel'] = angvelbins_amph

    pkl.dump(bindata, open("bindata.pkl", "wb"))
    savemat("bindata.mat", bindata)
    # alldata = pickle.load(open("alldata.pkl", "rb"))

    return bindata

def get_vehicle():
    drugs = ['clozapine', 'haloperidol', 'mp10', 'olanzapine']
    turnfts = ['right60', 'right30', 'forward0', 'left30', 'left60']
    speedfts = ['rest', 'move']
    speedftss = ['move']

    bindata = pkl.load(open("bindata.pkl", "rb"))

    # speed
    byanimal_speed_ctrl = defaultdict(list)
    byanimal_speed_amph = defaultdict(list)
    for drug in drugs:
        for animal, animalvals in bindata[drug]['vehicle']['ctrl']['speed'].items():
            byanimal_speed_ctrl[animal].append(animalvals)
        for animal, animalvals in bindata[drug]['vehicle']['amph']['speed'].items():
            byanimal_speed_amph[animal].append(animalvals)

    bindata_vehicle = {}
    bindata_vehicle['speed'] = {}
    bindata_vehicle['speed']['ctrl'] = {}
    bindata_vehicle['speed']['amph'] = {}
    for animal in byanimal_speed_ctrl.keys():
        bindata_vehicle['speed']['ctrl'][animal] = {}
        bindata_vehicle['speed']['amph'][animal] = {}
        for ft in turnfts:
            tempc, tempa = ([] for i in range(2))
            for n in range(0, len(byanimal_speed_ctrl[animal])):
                tempc.append(byanimal_speed_ctrl[animal][n][ft])
                bindata_vehicle['speed']['ctrl'][animal][ft] = np.mean(tempc, axis=0).tolist()
            for n in range(0, len(byanimal_speed_amph[animal])):
                tempa.append(byanimal_speed_amph[animal][n][ft])
                bindata_vehicle['speed']['amph'][animal][ft] = np.mean(tempa, axis=0).tolist()

    # turns
    byanimal_turn_ctrl = defaultdict(list)
    byanimal_turn_amph = defaultdict(list)
    for drug in drugs:
        for animal, animalvals in bindata[drug]['vehicle']['ctrl']['turn'].items():
            byanimal_turn_ctrl[animal].append(animalvals)
        for animal, animalvals in bindata[drug]['vehicle']['amph']['turn'].items():
            byanimal_turn_amph[animal].append(animalvals)

    bindata_vehicle['turn'] = {}
    bindata_vehicle['turn']['ctrl'] = {}
    bindata_vehicle['turn']['amph'] = {}
    for animal in byanimal_speed_ctrl.keys():
        bindata_vehicle['turn']['ctrl'][animal] = {}
        bindata_vehicle['turn']['amph'][animal] = {}
        for ft in speedfts:
            tempc, tempa = ([] for i in range(2))
            for n in range(0, len(byanimal_turn_ctrl[animal])):
                tempc.append(byanimal_turn_ctrl[animal][n][ft])
                bindata_vehicle['turn']['ctrl'][animal][ft] = np.mean(tempc, axis=0).tolist()
            for n in range(0, len(byanimal_turn_amph[animal])):
                tempa.append(byanimal_turn_amph[animal][n][ft])
                bindata_vehicle['turn']['amph'][animal][ft] = np.mean(tempa, axis=0).tolist()

    # angvel
    byanimal_angvel_ctrl = defaultdict(list)
    byanimal_angvel_amph = defaultdict(list)
    for drug in drugs:
        for animal, animalvals in bindata[drug]['vehicle']['ctrl']['angvel'].items():
            byanimal_angvel_ctrl[animal].append(animalvals)
        for animal, animalvals in bindata[drug]['vehicle']['amph']['angvel'].items():
            byanimal_angvel_amph[animal].append(animalvals)

    bindata_vehicle['angvel'] = {}
    bindata_vehicle['angvel']['ctrl'] = {}
    bindata_vehicle['angvel']['amph'] = {}
    for animal in byanimal_speed_ctrl.keys():
        bindata_vehicle['angvel']['ctrl'][animal] = {}
        bindata_vehicle['angvel']['amph'][animal] = {}
        for ft in speedftss:
            tempc, tempa = ([] for i in range(2))
            for n in range(0, len(byanimal_angvel_ctrl[animal])):
                tempc.append(byanimal_angvel_ctrl[animal][n][ft])
                bindata_vehicle['angvel']['ctrl'][animal][ft] = np.mean(tempc, axis=0).tolist()
            for n in range(0, len(byanimal_angvel_amph[animal])):
                tempa.append(byanimal_angvel_amph[animal][n][ft])
                bindata_vehicle['angvel']['amph'][animal][ft] = np.mean(tempa, axis=0).tolist()

    pkl.dump(bindata_vehicle, open("bindata_vehicle.pkl", "wb"))
    savemat("bindata_vehicle.mat", bindata_vehicle)

    return bindata_vehicle


def plot_speedbin_vehicle():
    turnfts = ['right60', 'right30', 'forward0', 'left30', 'left60']
    speedbins = ['0.5', '0.5-1', '1-2', '2-4', '4-8']

    D1_animals, D2_animals = D1_D2_names()
    bindata_vehicle = pkl.load(open("bindata_vehicle.pkl", "rb"))

    for ft in turnfts:
        plt.figure(figsize=(5, 9))
        d1_ctrl, d2_ctrl, d1_amph, d2_amph = ([] for i in range(4))
        for animal in bindata_vehicle['speed']['ctrl'].keys():
            if animal in D1_animals:
                d1_ctrl.append(bindata_vehicle['speed']['ctrl'][animal][ft][0])
                d1_amph.append(bindata_vehicle['speed']['amph'][animal][ft][0])
                for n in range(0, len(speedbins)):
                    if bindata_vehicle['speed']['ctrl'][animal][ft][1][n] < 50:  # 25 frames, 5 seconds
                        d1_ctrl[-1][n] = 'nan'
                    elif bindata_vehicle['speed']['amph'][animal][ft][1][n] < 50:
                        d1_amph[-1][n] = 'nan'
            elif animal in D2_animals:
                d2_ctrl.append(bindata_vehicle['speed']['ctrl'][animal][ft][0])
                d2_amph.append(bindata_vehicle['speed']['amph'][animal][ft][0])
                for n in range(0, len(speedbins)):
                    if bindata_vehicle['speed']['ctrl'][animal][ft][1][n] < 50:
                        d2_ctrl[-1][n] = 'nan'
                    elif bindata_vehicle['speed']['amph'][animal][ft][1][n] < 50:
                        d2_amph[-1][n] = 'nan'

        d1_ctrl_mean = np.ma.masked_invalid(np.array(d1_ctrl, dtype=float)).mean(axis=0)
        d1_ctrl_sem = np.ma.masked_invalid(np.array(d1_ctrl, dtype=float)).std(axis=0) / np.sqrt(len(d1_ctrl))
        d1_amph_mean = np.ma.masked_invalid(np.array(d1_amph, dtype=float)).mean(axis=0)
        d1_amph_sem = np.ma.masked_invalid(np.array(d1_amph, dtype=float)).std(axis=0) / np.sqrt(len(d1_amph))
        plt.subplot(211)
        plt.plot(d1_ctrl_mean, label=str(ft)+'_ctrl', color='k')
        plt.fill_between(range(len(speedbins)), d1_ctrl_mean+d1_ctrl_sem, d1_ctrl_mean-d1_ctrl_sem, color='k', alpha=0.1)
        plt.plot(d1_amph_mean, label=str(ft)+'_amph', color='k', linestyle=':')
        plt.fill_between(range(len(speedbins)), d1_amph_mean+d1_amph_sem, d1_amph_mean-d1_amph_sem, color='k', alpha=0.1)
        x_default = [0, 1, 2, 3, 4]
        x_new = ['<0.5', '0.5-1', '1-2', '2-4', '4-8']
        plt.xticks(x_default, x_new)
        plt.ylim((0, 2.5))
        plt.xlabel('Locomotor speed bin (cm/s)')
        plt.ylabel('Ca event rate (event/min)')
        plt.title('D1 SPNs')
        plt.suptitle('Ca spike per speed bout for turn angles')
        plt.legend()

        d2_ctrl_mean = np.ma.masked_invalid(np.array(d2_ctrl, dtype=float)).mean(axis=0)
        d2_ctrl_sem = np.ma.masked_invalid(np.array(d2_ctrl, dtype=float)).std(axis=0) / np.sqrt(len(d2_ctrl))
        d2_amph_mean = np.ma.masked_invalid(np.array(d2_amph, dtype=float)).mean(axis=0)
        d2_amph_sem = np.ma.masked_invalid(np.array(d2_amph, dtype=float)).std(axis=0) / np.sqrt(len(d2_amph))
        plt.subplot(212)
        plt.plot(d2_ctrl_mean, label=str(ft)+'_ctrl', color='k')
        plt.fill_between(range(len(speedbins)), d2_ctrl_mean+d2_ctrl_sem, d2_ctrl_mean-d2_ctrl_sem, color='k', alpha=0.1)
        plt.plot(d2_amph_mean, label=str(ft)+'_amph', color='k', linestyle=':')
        plt.fill_between(range(len(speedbins)), d2_amph_mean+d2_amph_sem, d2_amph_mean-d2_amph_sem, color='k', alpha=0.1)
        x_default = [0, 1, 2, 3, 4]
        x_new = ['<0.5', '0.5-1', '1-2', '2-4', '4-8']
        plt.xticks(x_default, x_new)
        plt.ylim((0, 2.5))
        plt.xlabel('Locomotor speed bin (cm/s)')
        plt.ylabel('Ca event rate (event/min)')
        plt.title('D2 SPNs')
        plt.suptitle('Ca spike per speed bout for turn angles')
        plt.legend()
        plt.show()

    return


def plot_turnbin_vehicle():
    speedfts = ['rest', 'move']
    turnbins = ['right60', 'right30', 'forward0', 'left30', 'left60']

    D1_animals, D2_animals = D1_D2_names()

    bindata_vehicle = pkl.load(open("bindata_vehicle.pkl", "rb"))

    for ft in speedfts:
        plt.figure(figsize=(5, 9))
        d1_ctrl, d2_ctrl, d1_amph, d2_amph = ([] for i in range(4))
        for animal in bindata_vehicle['turn']['ctrl'].keys():
            if animal in D1_animals:
                d1_ctrl.append(bindata_vehicle['turn']['ctrl'][animal][ft][0])
                d1_amph.append(bindata_vehicle['turn']['amph'][animal][ft][0])
                for n in range(0, len(turnbins)):
                    if bindata_vehicle['turn']['ctrl'][animal][ft][1][n] < 50:  # 25 frames, 5 secs
                        d1_ctrl[-1][n] = 'nan'
                    elif bindata_vehicle['turn']['amph'][animal][ft][1][n] < 50:
                        d1_amph[-1][n] = 'nan'
            elif animal in D2_animals:
                d2_ctrl.append(bindata_vehicle['turn']['ctrl'][animal][ft][0])
                d2_amph.append(bindata_vehicle['turn']['amph'][animal][ft][0])
                for n in range(0, len(turnbins)):
                    if bindata_vehicle['turn']['ctrl'][animal][ft][1][n] < 50:
                        d2_ctrl[-1][n] = 'nan'
                    elif bindata_vehicle['turn']['amph'][animal][ft][1][n] < 50:
                        d2_amph[-1][n] = 'nan'

        d1_ctrl_mean = np.ma.masked_invalid(np.array(d1_ctrl, dtype=float)).mean(axis=0)
        d1_ctrl_sem = np.ma.masked_invalid(np.array(d1_ctrl, dtype=float)).std(axis=0) / np.sqrt(len(d1_ctrl))
        d1_amph_mean = np.ma.masked_invalid(np.array(d1_amph, dtype=float)).mean(axis=0)
        d1_amph_sem = np.ma.masked_invalid(np.array(d1_amph, dtype=float)).std(axis=0) / np.sqrt(len(d1_amph))
        plt.subplot(211)
        plt.plot(d1_ctrl_mean, label=str(ft)+'_ctrl', color='k')
        plt.fill_between(range(len(turnbins)), d1_ctrl_mean+d1_ctrl_sem, d1_ctrl_mean-d1_ctrl_sem, color='k', alpha=0.1)
        plt.plot(d1_amph_mean, label=str(ft)+'_amph', color='k', linestyle=':')
        plt.fill_between(range(len(turnbins)), d1_amph_mean+d1_amph_sem, d1_amph_mean-d1_amph_sem, color='k', alpha=0.1)
        x_default = [0, 1, 2, 3, 4]
        x_new = ['right 60°', 'right 30°', 'forward 0°', 'left 30°', 'left 60°']
        plt.xticks(x_default, x_new)
        plt.ylim((0, 4))
        plt.ylabel('Ca event rate (event/min)')
        plt.title('D1 SPNs')
        plt.suptitle('Ca events for turning angles')
        plt.legend()

        d2_ctrl_mean = np.ma.masked_invalid(np.array(d2_ctrl, dtype=float)).mean(axis=0)
        d2_ctrl_sem = np.ma.masked_invalid(np.array(d2_ctrl, dtype=float)).std(axis=0) / np.sqrt(len(d2_ctrl))
        d2_amph_mean = np.ma.masked_invalid(np.array(d2_amph, dtype=float)).mean(axis=0)
        d2_amph_sem = np.ma.masked_invalid(np.array(d2_amph, dtype=float)).std(axis=0) / np.sqrt(len(d2_amph))
        plt.subplot(212)
        plt.plot(d2_ctrl_mean, label=str(ft)+'_ctrl', color='k')
        plt.fill_between(range(len(turnbins)), d2_ctrl_mean+d2_ctrl_sem, d2_ctrl_mean-d2_ctrl_sem, color='k', alpha=0.1)
        plt.plot(d2_amph_mean, label=str(ft)+'_amph', color='k', linestyle=':')
        plt.fill_between(range(len(turnbins)), d2_amph_mean+d2_amph_sem, d2_amph_mean-d2_amph_sem, color='k', alpha=0.1)
        x_default = [0, 1, 2, 3, 4]
        x_new = ['right 60°', 'right 30°', 'forward 0°', 'left 30°', 'left 60°'];
        plt.xticks(x_default, x_new)
        plt.ylim((0, 4))
        plt.ylabel('Ca event rate (event/min)')
        plt.title('D2 SPNs')
        plt.legend()
        plt.show()

    return


def plot_angvel_vehicle():
    speedfts = ['rest', 'move']
    turnbins = ['40°/s left', '20° left', '0°/s forward', '20°/s right', '40°/s right']

    D1_animals, D2_animals = D1_D2_names()

    bindata_vehicle = pkl.load(open("bindata_vehicle.pkl", "rb"))

    for ft in speedfts:
        plt.figure(figsize=(5, 9))
        d1_ctrl, d2_ctrl, d1_amph, d2_amph = ([] for i in range(4))
        for animal in bindata_vehicle['angvel']['ctrl'].keys():
            if animal in D1_animals:
                d1_ctrl.append(bindata_vehicle['angvel']['ctrl'][animal][ft][0])
                d1_amph.append(bindata_vehicle['angvel']['amph'][animal][ft][0])
                for n in range(0, len(turnbins)):
                    if bindata_vehicle['angvel']['ctrl'][animal][ft][1][n] < 25:  # 25 frames, 5 secs
                        d1_ctrl[-1][n] = 'nan'
                    elif bindata_vehicle['angvel']['amph'][animal][ft][1][n] < 25:
                        d1_amph[-1][n] = 'nan'
            elif animal in D2_animals:
                d2_ctrl.append(bindata_vehicle['angvel']['ctrl'][animal][ft][0])
                d2_amph.append(bindata_vehicle['angvel']['amph'][animal][ft][0])
                for n in range(0, len(turnbins)):
                    if bindata_vehicle['angvel']['ctrl'][animal][ft][1][n] < 25:
                        d2_ctrl[-1][n] = 'nan'
                    elif bindata_vehicle['angvel']['amph'][animal][ft][1][n] < 25:
                        d2_amph[-1][n] = 'nan'

        d1_ctrl_mean = np.ma.masked_invalid(np.array(d1_ctrl, dtype=float)).mean(axis=0)
        d1_ctrl_sem = np.ma.masked_invalid(np.array(d1_ctrl, dtype=float)).std(axis=0) / np.sqrt(len(d1_ctrl))
        d1_amph_mean = np.ma.masked_invalid(np.array(d1_amph, dtype=float)).mean(axis=0)
        d1_amph_sem = np.ma.masked_invalid(np.array(d1_amph, dtype=float)).std(axis=0) / np.sqrt(len(d1_amph))
        plt.subplot(211)
        plt.plot(d1_ctrl_mean, label=str(ft)+'_ctrl', color='k')
        plt.fill_between(range(len(turnbins)), d1_ctrl_mean+d1_ctrl_sem, d1_ctrl_mean-d1_ctrl_sem, color='k', alpha=0.1)
        plt.plot(d1_amph_mean, label=str(ft)+'_amph', color='k', linestyle=':')
        plt.fill_between(range(len(turnbins)), d1_amph_mean+d1_amph_sem, d1_amph_mean-d1_amph_sem, color='k', alpha=0.1)
        x_default = [0, 1, 2, 3, 4]
        x_new = ['40°/s left', '20° left', '0°/s forward', '20°/s right', '40°/s right']  # +/-10°/s
        plt.xticks(x_default, x_new)
        plt.ylim((0, 4))
        plt.ylabel('Ca event rate (event/min)')
        plt.title('D1 SPNs')
        plt.suptitle('Ca events for angular velocity')
        plt.legend()

        d2_ctrl_mean = np.ma.masked_invalid(np.array(d2_ctrl, dtype=float)).mean(axis=0)
        d2_ctrl_sem = np.ma.masked_invalid(np.array(d2_ctrl, dtype=float)).std(axis=0) / np.sqrt(len(d2_ctrl))
        d2_amph_mean = np.ma.masked_invalid(np.array(d2_amph, dtype=float)).mean(axis=0)
        d2_amph_sem = np.ma.masked_invalid(np.array(d2_amph, dtype=float)).std(axis=0) / np.sqrt(len(d2_amph))
        plt.subplot(212)
        plt.plot(d2_ctrl_mean, label=str(ft)+'_ctrl', color='k')
        plt.fill_between(range(len(turnbins)), d2_ctrl_mean+d2_ctrl_sem, d2_ctrl_mean-d2_ctrl_sem, color='k', alpha=0.1)
        plt.plot(d2_amph_mean, label=str(ft)+'_amph', color='k', linestyle=':')
        plt.fill_between(range(len(turnbins)), d2_amph_mean+d2_amph_sem, d2_amph_mean-d2_amph_sem, color='k', alpha=0.1)
        x_default = [0, 1, 2, 3, 4]
        x_new = ['40°/s left', '20° left', '0°/s forward', '20°/s right', '40°/s right']
        plt.xticks(x_default, x_new)
        plt.ylim((0, 4))
        plt.ylabel('Ca event rate (event/min)')
        plt.title('D2 SPNs')
        plt.legend()
        plt.show()

    return


def plot_turnbin_drug(drug, dose):
    speedfts = ['rest', 'move']
    turnbins = ['right60', 'right30', 'forward0', 'left30', 'left60']

    D1_animals, D2_animals = D1_D2_names()

    bindata = pkl.load(open("bindata.pkl", "rb"))

    for ft in speedfts:
        plt.figure(figsize=(5, 9))
        d1_ctrl, d2_ctrl, d1_amph, d2_amph = ([] for i in range(4))
        for animal in bindata[drug][dose]['ctrl']['turn'].keys():
            if animal in D1_animals:
                d1_ctrl.append(bindata[drug][dose]['ctrl']['turn'][animal][ft][0])
                d1_amph.append(bindata[drug][dose]['amph']['turn'][animal][ft][0])
                for n in range(0, len(turnbins)):
                    if bindata[drug][dose]['ctrl']['turn'][animal][ft][1][n] < 50:  # 25 frames, 5 secs
                        d1_ctrl[-1][n] = 'nan'
                    if bindata[drug][dose]['amph']['turn'][animal][ft][1][n] < 50:
                        d1_amph[-1][n] = 'nan'
            if animal in D2_animals:
                d2_ctrl.append(bindata[drug][dose]['ctrl']['turn'][animal][ft][0])
                d2_amph.append(bindata[drug][dose]['amph']['turn'][animal][ft][0])
                for n in range(0, len(turnbins)):
                    if bindata[drug][dose]['ctrl']['turn'][animal][ft][1][n] < 50:
                        d2_ctrl[-1][n] = 'nan'
                    if bindata[drug][dose]['amph']['turn'][animal][ft][1][n] < 50:
                        d2_amph[-1][n] = 'nan'

        plt.subplot(211)
        d1_ctrl_mean = np.ma.masked_invalid(np.array(d1_ctrl, dtype=float)).mean(axis=0)
        d1_ctrl_sem = np.ma.masked_invalid(np.array(d1_ctrl, dtype=float)).std(axis=0) / np.sqrt(len(d1_ctrl))
        d1_amph_mean = np.ma.masked_invalid(np.array(d1_amph, dtype=float)).mean(axis=0)
        d1_amph_sem = np.ma.masked_invalid(np.array(d1_amph, dtype=float)).std(axis=0) / np.sqrt(len(d1_amph))
        plt.plot(d1_ctrl_mean, label=str(ft) + '_ctrl', color='k')
        plt.fill_between(range(len(turnbins)), d1_ctrl_mean+d1_ctrl_sem, d1_ctrl_mean-d1_ctrl_sem, color='k', alpha=0.1)
        plt.plot(d1_amph_mean, label=str(ft) + '_amph', color='k', linestyle=':')
        plt.fill_between(range(len(turnbins)), d1_amph_mean+d1_amph_sem, d1_amph_mean-d1_amph_sem, color='k', alpha=0.1)
        x_default = [0, 1, 2, 3, 4]
        x_new = ['right 60°', 'right 30°', 'straight 0°', 'left 30°', 'left 60°']
        plt.xticks(x_default, x_new)
        plt.ylim((0, 4))
        plt.ylabel('Ca event rate (event/min)')
        plt.title('D1 SPNs')
        plt.suptitle('Ca events for turning angles')
        plt.legend()

        plt.subplot(212)
        d2_ctrl_mean = np.ma.masked_invalid(np.array(d2_ctrl, dtype=float)).mean(axis=0)
        d2_ctrl_sem = np.ma.masked_invalid(np.array(d2_ctrl, dtype=float)).std(axis=0) / np.sqrt(len(d2_ctrl))
        d2_amph_mean = np.ma.masked_invalid(np.array(d2_amph, dtype=float)).mean(axis=0)
        d2_amph_sem = np.ma.masked_invalid(np.array(d2_amph, dtype=float)).std(axis=0) / np.sqrt(len(d2_amph))
        plt.plot(d2_ctrl_mean, label=str(ft) + '_ctrl', color='k')
        plt.fill_between(range(len(turnbins)), d2_ctrl_mean+d2_ctrl_sem, d2_ctrl_mean-d2_ctrl_sem, color='k', alpha=0.1)
        plt.plot(d2_amph_mean, label=str(ft) + '_amph', color='k', linestyle=':')
        plt.fill_between(range(len(turnbins)), d2_amph_mean+d2_amph_sem, d2_amph_mean-d2_amph_sem, color='k', alpha=0.1)
        x_default = [0, 1, 2, 3, 4]
        x_new = ['right 60°', 'right 30°', 'straight 0°', 'left 30°', 'left 60°']
        plt.xticks(x_default, x_new)
        plt.ylim((0, 4))
        plt.ylabel('Ca event rate (event/min)')
        plt.title('D2 SPNs')
        plt.legend()
        plt.show()


def plot_angvel_drug(drug, dose):
    speedfts = ['rest', 'move']
    turnbins = ['40°/s left', '20° left', '0°/s forward', '20°/s right', '40°/s right']

    D1_animals, D2_animals = D1_D2_names()

    bindata = pkl.load(open("bindata.pkl", "rb"))

    for ft in speedfts:
        plt.figure(figsize=(5, 9))
        d1_ctrl, d2_ctrl, d1_amph, d2_amph = ([] for i in range(4))
        for animal in bindata[drug][dose]['ctrl']['angvel'].keys():
            if animal in D1_animals:
                d1_ctrl.append(bindata[drug][dose]['ctrl']['angvel'][animal][ft][0])
                d1_amph.append(bindata[drug][dose]['amph']['angvel'][animal][ft][0])
                for n in range(0, len(turnbins)):
                    if bindata[drug][dose]['ctrl']['angvel'][animal][ft][1][n] < 25:  # 25 frames, 5 secs
                        d1_ctrl[-1][n] = 'nan'
                    elif bindata[drug][dose]['amph']['angvel'][animal][ft][1][n] < 25:
                        d1_amph[-1][n] = 'nan'
            if animal in D2_animals:
                d2_ctrl.append(bindata[drug][dose]['ctrl']['angvel'][animal][ft][0])
                d2_amph.append(bindata[drug][dose]['amph']['angvel'][animal][ft][0])
                for n in range(0, len(turnbins)):
                    if bindata[drug][dose]['ctrl']['angvel'][animal][ft][1][n] < 25:
                        d2_ctrl[-1][n] = 'nan'
                    elif bindata[drug][dose]['amph']['angvel'][animal][ft][1][n] < 25:
                        d2_amph[-1][n] = 'nan'

        plt.subplot(211)
        d1_ctrl_mean = np.ma.masked_invalid(np.array(d1_ctrl, dtype=float)).mean(axis=0)
        d1_ctrl_sem = np.ma.masked_invalid(np.array(d1_ctrl, dtype=float)).std(axis=0) / np.sqrt(len(d1_ctrl))
        d1_amph_mean = np.ma.masked_invalid(np.array(d1_amph, dtype=float)).mean(axis=0)
        d1_amph_sem = np.ma.masked_invalid(np.array(d1_amph, dtype=float)).std(axis=0) / np.sqrt(len(d1_amph))
        plt.plot(d1_ctrl_mean, label=str(ft) + '_ctrl', color='k')
        plt.fill_between(range(len(turnbins)), d1_ctrl_mean+d1_ctrl_sem, d1_ctrl_mean-d1_ctrl_sem, color='k', alpha=0.1)
        plt.plot(d1_amph_mean, label=str(ft) + '_amph', color='k', linestyle=':')
        plt.fill_between(range(len(turnbins)), d1_amph_mean+d1_amph_sem, d1_amph_mean-d1_amph_sem, color='k', alpha=0.1)
        x_default = [0, 1, 2, 3, 4]
        x_new = ['40°/s left', '20° left', '0°/s forward', '20°/s right', '40°/s right']
        plt.xticks(x_default, x_new)
        plt.ylim((0, 4))
        plt.ylabel('Ca event rate (event/min)')
        plt.title('D1 SPNs')
        plt.suptitle('Ca events for angular velocity')
        plt.legend()

        plt.subplot(212)
        d2_ctrl_mean = np.ma.masked_invalid(np.array(d2_ctrl, dtype=float)).mean(axis=0)
        d2_ctrl_sem = np.ma.masked_invalid(np.array(d2_ctrl, dtype=float)).std(axis=0) / np.sqrt(len(d2_ctrl))
        d2_amph_mean = np.ma.masked_invalid(np.array(d2_amph, dtype=float)).mean(axis=0)
        d2_amph_sem = np.ma.masked_invalid(np.array(d2_amph, dtype=float)).std(axis=0) / np.sqrt(len(d2_amph))
        plt.plot(d2_ctrl_mean, label=str(ft) + '_ctrl', color='k')
        plt.fill_between(range(len(turnbins)), d2_ctrl_mean+d2_ctrl_sem, d2_ctrl_mean-d2_ctrl_sem, color='k', alpha=0.1)
        plt.plot(d2_amph_mean, label=str(ft) + '_amph', color='k', linestyle=':')
        plt.fill_between(range(len(turnbins)), d2_amph_mean+d2_amph_sem, d2_amph_mean-d2_amph_sem, color='k', alpha=0.1)
        x_default = [0, 1, 2, 3, 4]
        x_new = ['40°/s left', '20° left', '0°/s forward', '20°/s right', '40°/s right']
        plt.xticks(x_default, x_new)
        plt.ylim((0, 4))
        plt.ylabel('Ca event rate (event/min)')
        plt.title('D2 SPNs')
        plt.legend()
        plt.show()


