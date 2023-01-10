# Created by Arin Pamukcu, PhD on August 2022 in Chicago, IL

from info import *
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
from scipy.io import savemat
import pdb


def eventtime_vehicle():

    bases = ['ctrl', 'amph']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'rear', 'other_rest', 'other_move']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()
    animals = D1_animals + D2_animals

    fig, ax = plt.subplots(figsize=(8, 4))

    timedata = {}
    cutoff = 5.  # seconds

    x = 0
    for metric in metrics:
        tempdata = {}
        timedata[metric] = np.ndarray((len(animals), len(bases)), dtype=np.float)
        timedata[metric].fill(np.NaN)

        x = x + 2
        for j, base in enumerate(bases):

            if base == 'ctrl':
                cutoff_frame = cutoff / 900.
            elif base == 'amph':
                cutoff_frame = cutoff / 2700.

            for i, animal in enumerate(animals):

                if (metric == 'rest' or metric == 'move'):
                    tempdata[animal] = np.nanmean([alldata[d]['vehicle'][base][animal][metric]['time'] * 100
                                                   for d in alldata.keys()
                                                   if animal in alldata[d]['vehicle'][base].keys()
                                                   and alldata[d]['vehicle'][base][animal][metric]['time'] > (cutoff * 4. / 2700.)])

                    timedata[metric][i, j] = tempdata[animal]

                else:
                    tempdata[animal] = np.nanmean([alldata[d]['vehicle'][base][animal][metric]['time'] * 100
                                                   for d in alldata.keys()
                                                   if animal in alldata[d]['vehicle'][base].keys()
                                                   and alldata[d]['vehicle'][base][animal][metric]['time'] > (cutoff * 4. / 2700.)])

                    timedata[metric][i, j] = tempdata[animal]

            data = list(tempdata.values())
            mean = np.nanmean(data)
            sem = np.nanstd(data) / np.sqrt(len(data))

            if base == 'ctrl':
                ax.bar(x, mean, yerr=sem, width=1, color='gray')
            else:
                ax.bar(x, mean, yerr=sem, width=1, color='black')
            x = x + 1

    savemat("eventtime_vehicle.mat", timedata)

    plt.suptitle('percent time spent performing behaviors')
    plt.legend(['control', 'amph'])
    x_default = [2.5, 6.5, 10.5, 14.5, 18.5, 22.5, 26.5, 30.5, 34.5, 38.5]
    plt.xticks(x_default, metrics)
    plt.xticks(fontsize=8)
    plt.ylabel('percent time of full trial duration (%)')
    plt.ylim((0, 100))
    plt.show()

    return


def eventtime_drugs(setbase):

    drugs = ['haloperidol', 'olanzapine', 'clozapine',  'mp10']
    bases = ['ctrl', 'amph']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'rear', 'other_rest', 'other_move']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()
    animals = D1_animals + D2_animals

    fig, ax = plt.subplots(figsize=(12, 4))

    timedata = {}
    cutoff = 5.  # seconds

    x = 0
    for metric in metrics:
        tempdata = {}
        basetime_ctrl = {}
        timedata[metric] = np.ndarray((len(animals), len(drugs)+2), dtype=object)
        timedata[metric].fill(np.NaN)

        x = x + 2
        for j, base in enumerate(bases):

            for i, animal in enumerate(animals):
                basetime_ctrl[animal] = np.nanmean([alldata[d]['vehicle']['ctrl'][animal][metric]['time']
                                               for d in alldata.keys()
                                               if animal in alldata[d]['vehicle']['ctrl'].keys()])

                if basetime_ctrl[animal] > cutoff / 900.:
                    tempdata[animal] = np.nanmean([alldata[d]['vehicle'][base][animal][metric]['time'] * 100
                                                   for d in alldata.keys()
                                                   if animal in alldata[d]['vehicle'][base].keys()])

                    timedata[metric][i, j] = tempdata[animal]

            data = list(tempdata.values())
            mean = np.nanmean(data)
            sem = np.nanstd(data) / np.sqrt(len(data))

            if (metric == 'acc') and (base == 'ctrl'):
                ax.bar(x, mean, yerr=sem, width=1, color='gray', alpha=1, label='ctrl')
            elif (metric == 'acc') and (base == 'amph'):
                ax.bar(x, mean, yerr=sem, width=1, color='black', alpha=1, label='amph')
            elif base == 'ctrl':
                ax.bar(x, mean, yerr=sem, width=1, color='gray')
            elif base == 'amph':
                ax.bar(x, mean, yerr=sem, width=1, color='black', alpha=1)
            x = x + 1.5

        colors = ['orangered', 'royalblue', 'forestgreen', 'darkviolet']
        for drug, color in zip(drugs, colors):
            x = x + 0.5
            drugdata = {}

            for i, animal in enumerate(animals):

                if (animal in alldata[drug]['vehicle'][setbase].keys()) and (
                        animal in alldata[drug]['highdose'][setbase].keys()) and (
                        alldata[drug]['vehicle']['ctrl'][animal][metric]['time'] > (cutoff / 900.)):

                    drugdata[animal] = [(alldata[drug]['highdose'][setbase][animal][metric]['time']) * 100]

                    timedata[metric][i, drugs.index(drug)+2] = drugdata[animal]

            data = list(drugdata.values())
            mean = np.nanmean(data)
            sem = np.nanstd(data) / np.sqrt(len(data))

            if metric == 'acc':
                ax.bar(x, mean, yerr=sem, width=1, color=color, alpha=1, label=drug + '-' + base)
            else:
                ax.bar(x, mean, yerr=sem, width=1, color=color, alpha=1)
            x = x + 1

    filename = "eventtime_drugs" + "_" + setbase + ".mat"
    savemat(filename, timedata)

    # plt.axhspan(0, 1, alpha=0.4, color='gray', zorder=0)
    # plt.axhline(y=100, color='k', alpha=0.2, linestyle=':')
    plt.suptitle('% time spent performing behavior')
    x_default = [4.5, 15.5, 26.5, 37.5, 48.5, 59.5, 70.5, 81.5, 92.5, 103.5]
    plt.xticks(x_default, metrics)
    plt.xticks(fontsize=8)
    plt.ylabel('% time spent performing behavior')
    # plt.ylim((0, 1))
    plt.legend()
    plt.show()

    return


def norm_eventtime_drugs(base):

    drugs = ['haloperidol', 'olanzapine', 'clozapine',  'mp10']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'rear', 'other_rest', 'other_move']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()
    animals = D1_animals + D2_animals

    cutoff = 5.  # seconds
    if base == 'ctrl':
        cutoff_frame = cutoff / 900.
    elif base == 'amph':
        cutoff_frame = cutoff / 2700.

    fig, ax = plt.subplots(figsize=(12, 4))
    timedata = {}

    x = 0
    for metric in metrics:
        tempdata = {}
        basetime_ctrl = {}
        timedata[metric] = np.ndarray((len(animals), len(drugs)+1), dtype=object)
        timedata[metric].fill(np.NaN)

        x = x + 2
        for i, animal in enumerate(animals):

            basetime_ctrl[animal] = np.nanmean([alldata[d]['vehicle']['ctrl'][animal][metric]['time']
                                                for d in alldata.keys()
                                                if animal in alldata[d]['vehicle']['ctrl'].keys()])

            if (metric == 'rest' or metric == 'move'):

                tempdata[animal] = np.nanmean([alldata[d]['vehicle']['amph'][animal][metric]['time']
                                               / alldata[d]['vehicle']['ctrl'][animal][metric]['time']
                                               for d in alldata.keys()
                                               if animal in alldata[d]['vehicle']['ctrl'].keys()
                                               and alldata[d]['vehicle']['ctrl'][animal][metric]['time'] != 0
                                               and alldata[d]['vehicle']['amph'][animal][metric]['time'] > (cutoff * 4. / 2700.)])
                tempdata[animal] = (tempdata[animal] / basetime_ctrl[animal])
                timedata[metric][i, 0] = tempdata[animal]

            else:

                tempdata[animal] = np.nanmean([alldata[d]['vehicle']['amph'][animal][metric]['time']
                                               / alldata[d]['vehicle']['ctrl'][animal][metric]['time']
                                               for d in alldata.keys()
                                               if animal in alldata[d]['vehicle']['ctrl'].keys()
                                               and alldata[d]['vehicle']['ctrl'][animal][metric]['time'] != 0
                                               and alldata[d]['vehicle']['amph'][animal][metric]['time'] > (cutoff / 2700.)])
                tempdata[animal] = (tempdata[animal] / basetime_ctrl[animal])
                timedata[metric][i, 0] = tempdata[animal]

        data = list(tempdata.values())
        mean = np.nanmean(data)
        sem = np.nanstd(data) / np.sqrt(len(data))
        if metric == 'acc':
            ax.bar(x, mean, yerr=sem, width=1, color='black', label='amph')
        else:
            ax.bar(x, mean, yerr=sem, width=1, color='black')
        x = x + 1.5

        colors = ['orangered', 'royalblue', 'forestgreen', 'darkviolet']
        for drug, color in zip(drugs, colors):
            x = x + 0.5
            drugdata = {}

            for i, animal in enumerate(animals):

                if (metric == 'rest' or metric == 'move') \
                        and (animal in alldata[drug]['vehicle'][base].keys()) \
                        and (animal in alldata[drug]['highdose'][base].keys()) \
                        and (alldata[drug]['vehicle'][base][animal][metric]['time'] > (cutoff_frame * 4)):

                    # drugdata[animal] = [((alldata[drug]['highdose'][base][animal][metric]['time']
                    #           / alldata[drug]['vehicle']['ctrl'][animal][metric]['time']))]
                    drugdata[animal] = (alldata[drug]['highdose'][base][animal][metric]['time'] / basetime_ctrl[animal])

                    timedata[metric][i, drugs.index(drug)+1] = drugdata[animal]

                elif (animal in alldata[drug]['vehicle'][base].keys()) \
                        and (animal in alldata[drug]['highdose'][base].keys()) \
                        and (alldata[drug]['vehicle'][base][animal][metric]['time'] > (cutoff_frame)):

                    # drugdata[animal] = [((alldata[drug]['highdose'][base][animal][metric]['time']
                    #           / alldata[drug]['vehicle']['ctrl'][animal][metric]['time']))]
                    drugdata[animal] = (alldata[drug]['highdose'][base][animal][metric]['time'] / basetime_ctrl[animal])

                    timedata[metric][i, drugs.index(drug)+1] = drugdata[animal]

            data = list(drugdata.values())
            mean = np.nanmean(data)
            sem = np.nanstd(data) / np.sqrt(len(data))

            if metric == 'acc':
                ax.bar(x, mean, yerr=sem, width=1, color=color, alpha=1, label=drug + '-' + base)
            else:
                ax.bar(x, mean, yerr=sem, width=1, color=color, alpha=1)
            x = x + 1

    filename = "normalized_eventtime_drugs" + "_" + base + ".mat"
    savemat(filename, timedata)

    plt.axhspan(0, 1, alpha=0.4, color='gray', zorder=0)
    plt.suptitle('fraction of time spent compared to veh-ctrl')
    x_default = [5, 14.5, 24, 33.5, 43, 52.5, 62, 71.5, 81, 90.5]
    plt.xticks(x_default, metrics)
    plt.xticks(fontsize=8)
    plt.ylabel('fold change from vehicle control')
    plt.legend()
    plt.show()

    return


def eventrate_vehicle(spn):

    bases = ['ctrl', 'amph']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'rear', 'other_rest', 'other_move']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()

    animals = []
    if spn == 'D1':
        animals = D1_animals
    elif spn == 'D2':
        animals = D2_animals

    cutoff = 5.  # seconds

    fig, ax = plt.subplots(figsize=(10, 4))
    ratedata = {}

    x = 0
    for metric in metrics:
        x = x + 2

        tempdata = {}
        ratedata[metric] = np.ndarray((len(animals), len(bases)), dtype=object)
        ratedata[metric].fill(np.NaN)

        for j, base in enumerate(bases):

            if base == 'ctrl':
                cutoff_frame = cutoff / 900.
            elif base == 'amph':
                cutoff_frame = cutoff / 2700.

            for i, animal in enumerate(animals):

                if (metric == 'rest' or metric == 'move'):

                    tempdata[animal] = np.nanmean([alldata[d]['vehicle'][base][animal][metric]['rate'] * 60
                                                   for d in alldata.keys()
                                                   if animal in alldata[d]['vehicle']['ctrl'].keys()
                                                   and alldata[d]['vehicle'][base][animal][metric]['time'] > (cutoff_frame * 4)])
                    ratedata[metric][i, j] = tempdata[animal]

                else:

                    tempdata[animal] = np.nanmean([alldata[d]['vehicle'][base][animal][metric]['rate'] * 60
                                                   for d in alldata.keys()
                                                   if animal in alldata[d]['vehicle']['ctrl'].keys()
                                                   and alldata[d]['vehicle'][base][animal][metric]['time'] > (cutoff_frame)])
                    ratedata[metric][i, j] = tempdata[animal]

            data = list(tempdata.values())
            mean = np.nanmean(data)
            sem = np.nanstd(data) / np.sqrt(len(data))
            if base == 'ctrl':
                ax.bar(x, mean, yerr=sem, width=1, color='gray')
            else:
                ax.bar(x, mean, yerr=sem, width=1, color='black')
            x = x + 1

    filename = spn + "_" + "eventrate_vehicle.mat"
    savemat(filename, ratedata)

    plt.suptitle(str(spn) + ' SPN event rate during performing behaviors')
    plt.legend(['control', 'amph'])
    x_default = [2.5, 6.5, 10.5, 14.5, 18.5, 22.5, 26.5, 30.5, 34.5, 38.5]
    plt.xticks(x_default, metrics)
    plt.xticks(fontsize=8)
    plt.ylabel('event rate (events/s)')
    plt.show()

    return


def eventrate_drugs(spn, setbase):

    drugs = ['haloperidol', 'olanzapine', 'clozapine', 'mp10']
    bases = ['ctrl', 'amph']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'rear', 'other_rest', 'other_move']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()

    animals = []
    if spn == 'D1':
        animals = D1_animals
    elif spn == 'D2':
        animals = D2_animals

    cutoff = 5.

    fig, ax = plt.subplots(figsize=(12, 4))
    eventdata = {}

    x = 0
    for metric in metrics:
        x = x + 2

        tempdata = {}
        eventtime = {}
        eventtime_ctrl = {}
        eventtime_amph = {}

        eventdata[metric] = np.ndarray((len(animals), len(drugs) + 2), dtype=object)
        eventdata[metric].fill(np.NaN)

        for j, base in enumerate(bases):
            if base == 'ctrl':
                cutoff_frame = cutoff / 900.
            else:
                cutoff_frame = cutoff / 2700.

            for i, animal in enumerate(animals):

                eventtime[animal] = np.nansum([alldata[d]['vehicle'][base][animal][metric]['time'] * (cutoff / cutoff_frame)
                                               for d in alldata.keys()
                                               if animal in alldata[d]['vehicle']['ctrl'].keys()])
                eventtime_ctrl[animal] = np.nansum([alldata[d]['vehicle']['ctrl'][animal][metric]['time'] * 900
                                                    for d in alldata.keys()
                                                    if animal in alldata[d]['vehicle']['ctrl'].keys()])
                eventtime_amph[animal] = np.nansum([alldata[d]['vehicle']['amph'][animal][metric]['time'] * 2700
                                                    for d in alldata.keys()
                                                    if animal in alldata[d]['vehicle']['amph'].keys()])

                if (eventtime_ctrl[animal] > cutoff) and (eventtime_amph[animal] > cutoff):

                    tempdata[animal] = np.nansum([alldata[d]['vehicle'][base][animal][metric]['rate'] *
                                                  alldata[d]['vehicle'][base][animal][metric]['time'] *
                                                  (cutoff / cutoff_frame)
                                                  for d in alldata.keys()
                                                  if animal in alldata[d]['vehicle']['ctrl'].keys()
                                                  and alldata[d]['vehicle'][base][animal][metric]['time'] > cutoff_frame])

                    tempdata[animal] = tempdata[animal] / eventtime[animal] * 60

                    eventdata[metric][i, j] = tempdata[animal]

            data = list(tempdata.values())
            mean = np.nanmean(data)
            sem = np.nanstd(data) / np.sqrt(len(data))
            if (metric == 'acc') and (base == 'ctrl'):
                ax.bar(x, mean, yerr=sem, width=1, color='gray', alpha=1, label='ctrl')
            elif (metric == 'acc') and (base == 'amph'):
                ax.bar(x, mean, yerr=sem, width=1, color='black', alpha=1, label='amph')
            elif base == 'ctrl':
                ax.bar(x, mean, yerr=sem, width=1, color='gray')
            elif base == 'amph':
                ax.bar(x, mean, yerr=sem, width=1, color='black', alpha=1)
            x = x + 1.5

        colors = ['orangered', 'royalblue', 'forestgreen', 'darkviolet']
        for drug, color in zip(drugs, colors):
            x = x + 0.5
            drugdata = {}

            if setbase == 'ctrl':
                cutoff_drug = cutoff / 900.
            elif setbase == 'amph':
                cutoff_drug = cutoff / 2700.

            for i, animal in enumerate(animals):

                if (animal in alldata[drug]['vehicle'][setbase].keys()) and (
                        animal in alldata[drug]['highdose'][setbase].keys()) and (
                        eventtime_ctrl[animal] > cutoff) and (
                        alldata[drug]['highdose'][setbase][animal][metric]['time'] > cutoff_drug):

                    drugdata[animal] = (alldata[drug]['highdose'][setbase][animal][metric]['rate'] * 60)

                    eventdata[metric][i, drugs.index(drug)+2] = drugdata[animal]

            # print(drug, metric)
            # pdb.set_trace()

            data = list(drugdata.values())
            mean = np.nanmean(data)
            sem = np.nanstd(data) / np.sqrt(len(data))

            if metric == 'acc':
                ax.bar(x, mean, yerr=sem, width=1, color=color, alpha=1, label=drug + '-' + setbase)
            else:
                ax.bar(x, mean, yerr=sem, width=1, color=color, alpha=1)
            x = x + 1

    filename = spn + "_eventrate_drugs" + "_" + setbase + ".mat"
    savemat(filename, eventdata)

    plt.suptitle(str(spn) + ' SPN event rate during performing behaviors')
    x_default = [4.5, 15.5, 26.5, 37.5, 48.5, 59.5, 70.5, 81.5, 92.5, 103.5]
    plt.xticks(x_default, metrics)
    plt.xticks(fontsize=8)
    plt.ylabel('% change in event rate from vehicle control')
    plt.legend()
    plt.show()

    return


def norm_eventrate_drugs(spn, base):

    drugs = ['haloperidol', 'olanzapine', 'clozapine',  'mp10']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'rear', 'other_rest', 'other_move']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()

    animals = []
    if spn == 'D1':
        animals = D1_animals
    elif spn == 'D2':
        animals = D2_animals

    cutoff = 5.  # seconds
    if base == 'ctrl':
        cutoff_frame = cutoff / 900.
    elif base == 'amph':
        cutoff_frame = cutoff / 2700.

    fig, ax = plt.subplots(figsize=(12, 4))
    ratedata = {}

    x = 0
    for metric in metrics:
        x = x + 2

        tempdata = {}
        baserate_ctrl = {}

        ratedata[metric] = np.ndarray((len(animals), len(drugs) + 1), dtype=object)
        ratedata[metric].fill(np.NaN)

        for i, animal in enumerate(animals):

            baserate_ctrl[animal] = np.nanmean([alldata[d]['vehicle']['ctrl'][animal][metric]['rate'] * 60
                                                for d in alldata.keys()
                                                if animal in alldata[d]['vehicle']['ctrl'].keys()])

            if (metric == 'rest' or metric == 'move'):

                tempdata[animal] = np.nanmean([alldata[d]['vehicle']['amph'][animal][metric]['rate'] * 60
                                              for d in alldata.keys()
                                              if animal in alldata[d]['vehicle']['ctrl'].keys()
                                              and alldata[d]['vehicle']['amph'][animal][metric]['time'] > (cutoff * 4 / 2700.)])
                tempdata[animal] = (tempdata[animal] / baserate_ctrl[animal])
                ratedata[metric][i, 0] = tempdata[animal]

            else:

                tempdata[animal] = np.nanmean([alldata[d]['vehicle']['amph'][animal][metric]['rate'] * 60
                                              for d in alldata.keys()
                                              if animal in alldata[d]['vehicle']['ctrl'].keys()
                                              and alldata[d]['vehicle']['amph'][animal][metric]['time'] > (cutoff / 2700.)])
                tempdata[animal] = (tempdata[animal] / baserate_ctrl[animal])
                ratedata[metric][i, 0] = tempdata[animal]

        data = list(tempdata.values())
        mean = np.nanmean(data)
        sem = np.nanstd(data) / np.sqrt(len(data))
        if metric == 'acc':
            ax.bar(x, mean, yerr=sem, width=1, color='black', alpha=1, label='amph')
        else:
            ax.bar(x, mean, yerr=sem, width=1, color='black', alpha=1)
        x = x + 1.5

        colors = ['orangered', 'royalblue', 'forestgreen', 'darkviolet']
        for drug, color in zip(drugs, colors):
            x = x + 0.5
            drugdata = {}

            for i, animal in enumerate(animals):

                if (metric == 'rest' or metric == 'move') \
                    and (animal in alldata[drug]['vehicle'][base].keys()) \
                    and (animal in alldata[drug]['highdose'][base].keys()) \
                    and (alldata[drug]['highdose'][base][animal][metric]['time'] > cutoff_frame * 4):

                    drugdata[animal] = alldata[drug]['highdose'][base][animal][metric]['rate'] * 60 / baserate_ctrl[animal]
                    ratedata[metric][i, drugs.index(drug)+1] = drugdata[animal]

                elif (animal in alldata[drug]['vehicle'][base].keys()) \
                    and (animal in alldata[drug]['highdose'][base].keys()) \
                    and (alldata[drug]['highdose'][base][animal][metric]['time'] > cutoff_frame):

                    drugdata[animal] = alldata[drug]['highdose'][base][animal][metric]['rate'] * 60 / baserate_ctrl[animal]
                    ratedata[metric][i, drugs.index(drug)+1] = drugdata[animal]

            data = list(drugdata.values())
            mean = np.nanmean(data)
            sem = np.nanstd(data) / np.sqrt(len(data))

            if metric == 'acc':
                ax.bar(x, mean, yerr=sem, width=1, color=color, alpha=1, label=drug + '-' + base)
            else:
                ax.bar(x, mean, yerr=sem, width=1, color=color, alpha=1)
            x = x + 1

    filename = "normalized_" + spn + "_eventrate_drugs" + "_" + base + ".mat"
    savemat(filename, ratedata)

    plt.axhspan(0, 1, alpha=0.4, color='gray', zorder=0)
    # plt.axhline(y=1, color='k', alpha=0.2, linestyle=':')
    plt.suptitle(str(spn) + ' SPN event rate during performing behaviors')
    x_default = [5, 14.5, 24, 33.5, 43, 52.5, 62, 71.5, 81, 90.5]
    plt.xticks(x_default, metrics)
    plt.xticks(fontsize=8)
    plt.ylabel('% change in event rate from vehicle control')
    # plt.ylim((0, 600))
    plt.legend()
    plt.show()

    return


