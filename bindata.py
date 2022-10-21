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

def turn_bins(speed_data, turn_data , speed1, speed2, eventmean_data):
    left60_events, left30_events, straight_events, right30_events, right60_events = ([] for i in range(5))
    left60_duration, left30_duration, straight_duration, right30_duration, right60_duration = (0 for i in range(5))

    for fr in range(0, len(turn_data)):
        if speed1 < speed_data[fr] <= speed2 and -70 < turn_data[fr] < -50:
            left60_events.append(eventmean_data[fr])
            left60_duration += 1
        if speed1 < speed_data[fr] <= speed2 and -40 < turn_data[fr] < -20:
            left30_events.append(eventmean_data[fr])
            left30_duration += 1
        if speed1 < speed_data[fr] <= speed2 and -10 < turn_data[fr] < 10:
            straight_events.append(eventmean_data[fr])
            straight_duration += 1
        if speed1 < speed_data[fr] <= speed2 and 20 < turn_data[fr] < 40:
            right30_events.append(eventmean_data[fr])
            right30_duration += 1
        if speed1 < speed_data[fr] <= speed2 and 50 < turn_data[fr] < 70:
            right60_events.append(eventmean_data[fr])
            right60_duration += 1

    eventrate_vs_turn_speed = [(np.sum(left60_events) / left60_duration) * 300,
                               (np.sum(left30_events) / left30_duration) * 300,
                               (np.sum(straight_events) / straight_duration) * 300,
                               (np.sum(right30_events) / right30_duration) * 300,
                               (np.sum(right60_events) / right60_duration) * 300]

    return eventrate_vs_turn_speed


def speed_bins(speed_data, turn_data, turn_angle, eventmean_data):
    speed01_events, speed02_events, speed03_events, speed04_events, speed05_events, speed06_events = ([] for i in range(6))
    speed01_duration, speed02_duration, speed03_duration, speed04_duration, speed05_duration, speed06_duration = (0 for i in range(6))

    for fr in range(0, len(turn_data)):
        if speed_data[fr] <= 0.5 and turn_angle-10 < turn_data[fr] < turn_angle+10:
            speed01_events.append(eventmean_data[fr])
            speed01_duration += 1
        if 0.5 < speed_data[fr] <= 1 and turn_angle-10 < turn_data[fr] < turn_angle+10:
            speed02_events.append(eventmean_data[fr])
            speed02_duration += 1
        if 1 < speed_data[fr] <= 2 and turn_angle-10 < turn_data[fr] < turn_angle+10:
            speed03_events.append(eventmean_data[fr])
            speed03_duration += 1
        if 2 < speed_data[fr] <= 4 and turn_angle-10 < turn_data[fr] < turn_angle+10:
            speed04_events.append(eventmean_data[fr])
            speed04_duration += 1
        if 4 < speed_data[fr] <= 8 and turn_angle-10 < turn_data[fr] < turn_angle+10:
            speed05_events.append(eventmean_data[fr])
            speed05_duration += 1
        if 8 < speed_data[fr] <= 14 and turn_angle-10 < turn_data[fr] < turn_angle+10:
            speed06_events.append(eventmean_data[fr])
            speed06_duration += 1

    eventrate_vs_speed_turn = [(np.sum(speed01_events) / speed01_duration) * 300,
                               (np.sum(speed02_events) / speed02_duration) * 300,
                               (np.sum(speed03_events) / speed03_duration) * 300,
                               (np.sum(speed04_events) / speed04_duration) * 300,
                               (np.sum(speed05_events) / speed05_duration) * 300,
                               (np.sum(speed06_events) / speed06_duration) * 300]

    return eventrate_vs_speed_turn


def get_metrics(drug, dose):
    experiments, animals, _, _ = get_animal_id(drug, dose)

    speedbins_ctrl = {}
    turnbins_ctrl = {}
    speedbins_amph = {}
    turnbins_amph = {}

    for experiment, animal in zip(experiments, animals):
        speedbins_ctrl[animal] = {}
        turnbins_ctrl[animal] = {}
        speedbins_amph[animal] = {}
        turnbins_amph[animal] = {}

        print(experiment)

        # get values for speed or turn
        speed_ctrl, speed_amph, _, _, eventmean_ctrl, eventmean_amph, _, _, _ = get_data(drug, dose, experiment)
        turn_ctrl, turn_amph, _, _ = mars_feature(drug, dose, experiment)

        # get values for each animal for that drug & dose
        eventrate_turn_stop_ctrl = turn_bins(speed_ctrl, turn_ctrl, 0, 0.5, eventmean_ctrl)
        eventrate_turn_move_ctrl = turn_bins(speed_ctrl, turn_ctrl, 0.5, 8, eventmean_ctrl)
        eventrate_turn_stop_amph = turn_bins(speed_amph, turn_amph, 0, 0.5, eventmean_amph)
        eventrate_turn_move_amph = turn_bins(speed_amph, turn_amph, 0.5, 8, eventmean_amph)

        eventrate_speed_right2_ctrl = speed_bins(speed_ctrl, turn_ctrl, 60, eventmean_ctrl)
        eventrate_speed_right1_ctrl = speed_bins(speed_ctrl, turn_ctrl, 30, eventmean_ctrl)
        eventrate_speed_straight_ctrl = speed_bins(speed_ctrl, turn_ctrl, 0, eventmean_ctrl)
        eventrate_speed_left1_ctrl = speed_bins(speed_ctrl, turn_ctrl, -30, eventmean_ctrl)
        eventrate_speed_left2_ctrl = speed_bins(speed_ctrl, turn_ctrl, -60, eventmean_ctrl)
        eventrate_speed_right2_amph = speed_bins(speed_amph, turn_amph, 60, eventmean_amph)
        eventrate_speed_right1_amph = speed_bins(speed_amph, turn_amph, 30, eventmean_amph)
        eventrate_speed_straight_amph = speed_bins(speed_amph, turn_amph, 0, eventmean_amph)
        eventrate_speed_left1_amph = speed_bins(speed_amph, turn_amph, -30, eventmean_amph)
        eventrate_speed_left2_amph = speed_bins(speed_amph, turn_amph, -60, eventmean_amph)

        # append values for each animal to a list
        turnbins_ctrl[animal]['stop'] = eventrate_turn_stop_ctrl
        turnbins_ctrl[animal]['move'] = eventrate_turn_move_ctrl
        speedbins_ctrl[animal]['right60'] = eventrate_speed_right2_ctrl
        speedbins_ctrl[animal]['right30'] = eventrate_speed_right1_ctrl
        speedbins_ctrl[animal]['straight0'] = eventrate_speed_straight_ctrl
        speedbins_ctrl[animal]['left30'] = eventrate_speed_left1_ctrl
        speedbins_ctrl[animal]['left60'] = eventrate_speed_left2_ctrl

        turnbins_amph[animal]['stop'] = eventrate_turn_stop_amph
        turnbins_amph[animal]['move'] = eventrate_turn_move_amph
        speedbins_amph[animal]['right60'] = eventrate_speed_right2_amph
        speedbins_amph[animal]['right30'] = eventrate_speed_right1_amph
        speedbins_amph[animal]['straight0'] = eventrate_speed_straight_amph
        speedbins_amph[animal]['left30'] = eventrate_speed_left1_amph
        speedbins_amph[animal]['left60'] = eventrate_speed_left2_amph

        # stop: for speed < 0.5, turn bins at -60, -30, 0, 30, 60 nose-neck-tail angle
        # move: for 0.5 < speed < 8, turn bins at -60, -30, 0, 30, 60
        # right2: for 60 nose-neck-tail angle, speed bins at 0.5, 0.5-1, 1-2, 2-4, 4-8, 8-14
        # right1: for 30 nose-neck-tail angle, speed bins at 0.5, 0.5-1, 1-2, 2-4, 4-8, 8-14
        # straight: for 0 nose-neck-tail angle, speed bins at 0.5, 0.5-1, 1-2, 2-4, 4-8, 8-14
        # left1: for -30 nose-neck-tail angle, speed bins at 0.5, 0.5-1, 1-2, 2-4, 4-8, 8-14
        # left2: for -60 nose-neck-tail angle, speed bins at 0.5, 0.5-1, 1-2, 2-4, 4-8, 8-14

    return speedbins_ctrl, turnbins_ctrl, speedbins_amph, turnbins_amph


def get_bindata():

    drugs = ['clozapine', 'haloperidol', 'mp10', 'olanzapine']
    doses = ['vehicle', 'lowdose', 'highdose']

    bindata = {}
    for drug in drugs:
        bindata[drug] = {}
        for dose in doses:
            print(drug, dose)

            bindata[drug][dose] = {}
            bindata[drug][dose]['ctrl'] = {}
            bindata[drug][dose]['amph'] = {}
            bindata[drug][dose]['ctrl']['speed'] = {}
            bindata[drug][dose]['ctrl']['turn'] = {}
            bindata[drug][dose]['amph']['speed'] = {}
            bindata[drug][dose]['amph']['turn'] = {}
            speedbins_ctrl, turnbins_ctrl, speedbins_amph, turnbins_amph = get_metrics(drug, dose)
            _, animals, _, _ = get_animal_id(drug, dose)
            bindata[drug][dose]['ctrl']['speed'] = speedbins_ctrl
            bindata[drug][dose]['ctrl']['turn'] = turnbins_ctrl
            bindata[drug][dose]['amph']['speed'] = speedbins_amph
            bindata[drug][dose]['amph']['turn'] = turnbins_amph

    pkl.dump(bindata, open("bindata.pkl", "wb"))
    savemat("bindata.mat", bindata)
    # alldata = pickle.load(open("alldata.pkl", "rb"))

    return bindata

def get_vehicle():
    drugs = ['clozapine', 'haloperidol', 'mp10', 'olanzapine']
    turnfts = ['right60', 'right30', 'straight0', 'left30', 'left60']
    speedfts = ['stop', 'move']

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

    pkl.dump(bindata_vehicle, open("bindata_vehicle.pkl", "wb"))
    savemat("bindata_vehicle.mat", bindata_vehicle)

    # pdb.set_trace()

    return bindata_vehicle


def plot_speedbin():
    turnfts = ['right60', 'right30', 'straight0', 'left30', 'left60']

    D1_animals, D2_animals = D1_D2_names()
    bindata_vehicle = pkl.load(open("bindata_vehicle.pkl", "rb"))

    n = range(6)
    for ft in turnfts:
        plt.figure(figsize=(5, 9))
        d1_ctrl, d2_ctrl, d1_amph, d2_amph = ([] for i in range(4))
        for animal in bindata_vehicle['speed']['ctrl'].keys():
            if animal in D1_animals:
                d1_ctrl.append(bindata_vehicle['speed']['ctrl'][animal][ft])
                d1_amph.append(bindata_vehicle['speed']['amph'][animal][ft])
            elif animal in D2_animals:
                d2_ctrl.append(bindata_vehicle['speed']['ctrl'][animal][ft])
                d2_amph.append(bindata_vehicle['speed']['amph'][animal][ft])
        d1_ctrl_mean = np.ma.masked_invalid(d1_ctrl).mean(axis=0)
        d1_ctrl_sem = np.ma.masked_invalid(d1_ctrl).std(axis=0) / np.sqrt(len(d1_ctrl))
        d1_amph_mean = np.ma.masked_invalid(d1_amph).mean(axis=0)
        d1_amph_sem = np.ma.masked_invalid(d1_amph).std(axis=0) / np.sqrt(len(d1_amph))
        plt.subplot(211)
        plt.plot(d1_ctrl_mean, label=str(ft)+'_ctrl', color='k')
        plt.fill_between(n, d1_ctrl_mean + d1_ctrl_sem, d1_ctrl_mean - d1_ctrl_sem, color='k', alpha=0.1)
        plt.plot(d1_amph_mean, label=str(ft)+'_amph', color='r')
        plt.fill_between(n, d1_amph_mean + d1_amph_sem, d1_amph_mean - d1_amph_sem, color='r', alpha=0.1)
        x_default = [0, 1, 2, 3, 4, 5]
        x_new = ['<0.5', '0.5-1', '1-2', '2-4', '4-8', '8-14']
        plt.xticks(x_default, x_new)
        plt.ylim((0, 2.5))
        plt.xlabel('Locomotor speed bin (cm/s)')
        plt.ylabel('Ca event rate (event/min)')
        plt.title('D1 SPNs')
        plt.suptitle('Ca spike per speed bout for turn angles')
        plt.legend()

        d2_ctrl_mean = np.ma.masked_invalid(d2_ctrl).mean(axis=0)
        d2_ctrl_sem = np.ma.masked_invalid(d2_ctrl).std(axis=0) / np.sqrt(len(d2_ctrl))
        d2_amph_mean = np.ma.masked_invalid(d2_amph).mean(axis=0)
        d2_amph_sem = np.ma.masked_invalid(d2_amph).std(axis=0) / np.sqrt(len(d2_amph))
        plt.subplot(212)
        plt.plot(d2_ctrl_mean, label=str(ft)+'_ctrl', color='k')
        plt.fill_between(n, d2_ctrl_mean + d2_ctrl_sem, d2_ctrl_mean - d2_ctrl_sem, color='k', alpha=0.1)
        plt.plot(d2_amph_mean, label=str(ft)+'_amph', color='r')
        plt.fill_between(n, d2_amph_mean + d2_amph_sem, d2_amph_mean - d2_amph_sem, color='r', alpha=0.1)
        x_default = [0, 1, 2, 3, 4, 5]
        x_new = ['<0.5', '0.5-1', '1-2', '2-4', '4-8', '8-14']
        plt.xticks(x_default, x_new)
        plt.ylim((0, 2.5))
        plt.xlabel('Locomotor speed bin (cm/s)')
        plt.ylabel('Ca event rate (event/min)')
        plt.title('D2 SPNs')
        plt.suptitle('Ca spike per speed bout for turn angles')
        plt.legend()
        plt.show()

    return


def plot_turnbin():
    turnfts = ['stop', 'move']

    D1_animals, D2_animals = D1_D2_names()

    bindata_vehicle = pkl.load(open("bindata_vehicle.pkl", "rb"))

    n = range(5)
    for ft in turnfts:
        plt.figure(figsize=(5, 9))
        d1_ctrl, d2_ctrl, d1_amph, d2_amph = ([] for i in range(4))
        for animal in bindata_vehicle['turn']['ctrl'].keys():
            if animal in D1_animals:
                d1_ctrl.append(bindata_vehicle['turn']['ctrl'][animal][ft])
                d1_amph.append(bindata_vehicle['turn']['amph'][animal][ft])
            elif animal in D2_animals:
                d2_ctrl.append(bindata_vehicle['turn']['ctrl'][animal][ft])
                d2_amph.append(bindata_vehicle['turn']['amph'][animal][ft])
        d1_ctrl_mean = np.ma.masked_invalid(d1_ctrl).mean(axis=0)
        d1_ctrl_sem = np.ma.masked_invalid(d1_ctrl).std(axis=0) / np.sqrt(len(d1_ctrl))
        d1_amph_mean = np.ma.masked_invalid(d1_amph).mean(axis=0)
        d1_amph_sem = np.ma.masked_invalid(d1_amph).std(axis=0) / np.sqrt(len(d1_amph))
        # pdb.set_trace()

        plt.subplot(211)
        plt.plot(d1_ctrl_mean, label=str(ft)+'_ctrl', color='k')
        plt.fill_between(n, d1_ctrl_mean + d1_ctrl_sem, d1_ctrl_mean - d1_ctrl_sem, color='k', alpha=0.1)
        plt.plot(d1_amph_mean, label=str(ft)+'_amph', color='r')
        plt.fill_between(n, d1_amph_mean + d1_amph_sem, d1_amph_mean - d1_amph_sem, color='r', alpha=0.1)
        x_default = [0, 1, 2, 3, 4];
        x_new = ['right 60°', 'right 30°', 'straight 0°', 'left 30°', 'left 60°'];
        plt.xticks(x_default, x_new);
        plt.ylim((0, 2.5))
        plt.ylabel('Ca event rate (event/min)')
        plt.title('D1 SPNs')
        plt.suptitle('Ca events for speeds')
        plt.legend()

        d2_ctrl_mean = np.ma.masked_invalid(d2_ctrl).mean(axis=0)
        d2_ctrl_sem = np.ma.masked_invalid(d2_ctrl).std(axis=0) / np.sqrt(len(d2_ctrl))
        d2_amph_mean = np.ma.masked_invalid(d2_amph).mean(axis=0)
        d2_amph_sem = np.ma.masked_invalid(d2_amph).std(axis=0) / np.sqrt(len(d2_amph))
        plt.subplot(212)
        plt.plot(d2_ctrl_mean, label=str(ft)+'_ctrl', color='k')
        plt.fill_between(n, d2_ctrl_mean + d2_ctrl_sem, d2_ctrl_mean - d2_ctrl_sem, color='k', alpha=0.1)
        plt.plot(d2_amph_mean, label=str(ft)+'_amph', color='r')
        plt.fill_between(n, d2_amph_mean + d2_amph_sem, d2_amph_mean - d2_amph_sem, color='r', alpha=0.1)
        x_default = [0, 1, 2, 3, 4];
        x_new = ['right 60°', 'right 30°', 'straight 0°', 'left 30°', 'left 60°'];
        plt.xticks(x_default, x_new);
        plt.ylim((0, 2.5))
        plt.ylabel('Ca event rate (event/min)')
        plt.title('D2 SPNs')
        plt.legend()
        plt.show()

    return