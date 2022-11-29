# Created by Arin Pamukcu, PhD on August 2022 in Chicago, IL

from info import *
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
import pdb


def timespent_vehicle():

    # doses = ['vehicle', 'highdose']
    # drugs = ['haloperidol', 'olanzapine', 'clozapine', 'mp10']
    bases = ['ctrl', 'amph']
    # metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'other']
    metrics = ['acc', 'dec', 'right_turn', 'left_turn', 'groom', 'rear', 'other_rest', 'other_move']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()
    animals = D1_animals + D2_animals

    fig, ax = plt.subplots(figsize=(8, 4))
    x = 0
    for metric in metrics:
        x = x + 2
        tempdata = {}
        for base in bases:
            for animal in animals:
                tempdata[animal] = np.nanmean([alldata[d]['vehicle'][base][animal][metric]['time'] * 100
                                               for d in alldata.keys()
                                               if animal in alldata[d]['vehicle'][base].keys()
                                               and alldata[d]['vehicle']['ctrl'][animal][metric]['time'] > (1. / 180.)])

            data = list(tempdata.values())
            mean = np.nanmean(data)
            sem = np.nanstd(data) / np.sqrt(len(data))
            if base == 'ctrl':
                ax.bar(x, mean, yerr=sem, width=1, color='k')
            else:
                ax.bar(x, mean, yerr=sem, width=1, color='fuchsia')
            x = x + 1

    plt.suptitle('percent time spent performing behaviors')
    plt.legend(['control', 'amph'])
    # x_default = [2.5, 6.5, 10.5, 14.5, 18.5, 22.5, 26.5, 30.5, 34.5]
    x_default = [2.5, 6.5, 10.5, 14.5, 18.5, 22.5, 26.5, 30.5]
    plt.xticks(x_default, metrics)
    plt.xticks(fontsize=8)
    plt.ylabel('percent time of full trial duration (%)')
    plt.ylim((0, 100))
    plt.show()

    return


def timespent_drugs(base):

    drugs = ['haloperidol', 'olanzapine', 'clozapine',  'mp10']
    # bases = ['ctrl', 'amph']
    metrics = ['acc', 'dec', 'right_turn', 'left_turn', 'groom', 'rear', 'other_rest', 'other_move']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()
    animals = D1_animals + D2_animals

    fig, ax = plt.subplots(figsize=(10, 4))

    x = 0
    for metric in metrics:
        tempdata = {}
        baseline = {}

        x = x + 2
        for animal in animals:

            baseline[animal] = np.nanmean([alldata[d]['vehicle']['ctrl'][animal][metric]['time']
                                           for d in alldata.keys()
                                           if animal in alldata[d]['vehicle']['ctrl'].keys()])
            if baseline[animal] > 1. / 180.:
                tempdata[animal] = np.nanmean([alldata[d]['vehicle']['amph'][animal][metric]['time']
                                               for d in alldata.keys()
                                               if animal in alldata[d]['vehicle']['ctrl'].keys()]) / baseline[animal] * 100.

        data = list(tempdata.values())
        mean = np.nanmean(data)
        sem = np.nanstd(data) / np.sqrt(len(data))
        if metric == 'acc':
            ax.bar(x, mean, yerr=sem, width=1, color='fuchsia', label='amph')
        else:
            ax.bar(x, mean, yerr=sem, width=1, color='fuchsia')
        # ax.plot([x] * len(data), data, 'k.')
        x = x + 1.5

        # colors = ['orangered', 'royalblue', 'forestgreen', 'darkviolet']
        colors = ['red', 'teal', 'blue', 'limegreen']
        for drug, color in zip(drugs, colors):

            # a = (0.5 if base == 'ctrl' else 1)
            x = x + 0.5
            data = [((alldata[drug]['highdose'][base][a][metric]['time']
                      / alldata[drug]['vehicle']['ctrl'][a][metric]['time'])) * 100.
                    for a in alldata[drug]['highdose'][base].keys()
                    if a in alldata[drug]['vehicle'][base].keys()
                    and alldata[drug]['vehicle']['ctrl'][a][metric]['time'] > (1. / 180.)]

            mean = np.nanmean(data)
            sem = np.nanstd(data) / np.sqrt(len(data))
            if metric == 'acc':
                ax.bar(x, mean, yerr=sem, width=1, color=color, alpha=1, label=drug + '-' + base)
            else:
                ax.bar(x, mean, yerr=sem, width=1, color=color, alpha=1)
            # ax.plot([x]*len(data), data, 'k.')
            x = x + 1
            # a = a + 0.5

    plt.axhspan(0, 100, alpha=0.2, color='k', zorder=0)
    # plt.axhline(y=100, color='k', alpha=0.2, linestyle=':')
    plt.suptitle('fraction of time spent compared to veh-ctrl')
    x_default = [5, 14.5, 24, 33.5, 43, 52.5, 62, 71.5]
    plt.xticks(x_default, metrics)
    plt.xticks(fontsize=8)
    plt.ylabel('% change from vehicle control')
    plt.ylim((0, 350))
    plt.legend()
    plt.show()

    return


def eventrate_vehicle(spn):

    # doses = ['vehicle', 'highdose']
    # drugs = ['haloperidol', 'olanzapine', 'clozapine', 'mp10']
    bases = ['ctrl', 'amph']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'rear', 'other_rest', 'other_move']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()

    animals = []
    if spn == 'D1':
        animals = D1_animals
    elif spn == 'D2':
        animals = D2_animals

    fig, ax = plt.subplots(figsize=(8, 4))

    x = 0
    for metric in metrics:
        x = x + 2

        tempdata = {}
        eventrate_ctrl = {}
        eventtime_ctrl = {}
        eventtime_amph = {}
        for base in bases:

            cutoff_time = 5.
            if base == 'ctrl':
                cutoff = cutoff_time / 900.
            else:
                cutoff = cutoff_time / 2700.

            for animal in animals:
                eventrate_ctrl[animal] = np.nansum([alldata[d]['vehicle']['ctrl'][animal][metric]['rate'] *
                                                    alldata[d]['vehicle']['ctrl'][animal][metric]['time'] * 900.
                                                    for d in alldata.keys()
                                                    if animal in alldata[d]['vehicle']['ctrl'].keys()])
                eventtime_ctrl[animal] = np.nansum([alldata[d]['vehicle']['ctrl'][animal][metric]['time'] * 900.
                                                    for d in alldata.keys()
                                                    if animal in alldata[d]['vehicle']['ctrl'].keys()])
                eventtime_amph[animal] = np.nansum([alldata[d]['vehicle']['amph'][animal][metric]['time'] * 2700.
                                                    for d in alldata.keys()
                                                    if animal in alldata[d]['vehicle']['amph'].keys()])
                eventrate_ctrl[animal] = eventrate_ctrl[animal] / eventtime_ctrl[animal]

                if (eventtime_ctrl[animal] > 20.) and (eventtime_amph[animal] > 20.):
                    tempdata[animal] = np.nansum([alldata[d]['vehicle'][base][animal][metric]['rate'] *
                                                  alldata[d]['vehicle'][base][animal][metric]['time'] * (cutoff_time/cutoff)
                                                  for d in alldata.keys()
                                                  if animal in alldata[d]['vehicle']['ctrl'].keys()
                                                  and alldata[d]['vehicle'][base][animal][metric]['time'] > cutoff])
                    if base == 'ctrl':
                        tempdata[animal] = tempdata[animal] / eventtime_ctrl[animal]
                    elif base == 'amph':
                        tempdata[animal] = tempdata[animal] / eventtime_amph[animal]

            data = list(tempdata.values())
            mean = np.nanmean(data)
            sem = np.nanstd(data) / np.sqrt(len(data))
            if base == 'ctrl':
                ax.bar(x, mean, yerr=sem, width=1, color='k')
            else:
                ax.bar(x, mean, yerr=sem, width=1, color='fuchsia')
            # ax.plot([x] * len(data), data, 'k.')
            x = x + 1

    plt.suptitle(str(spn) + ' SPN event rate during performing behaviors')
    plt.legend(['control', 'amph'])
    x_default = [2.5, 6.5, 10.5, 14.5, 18.5, 22.5, 26.5, 30.5, 34.5, 38.5]
    plt.xticks(x_default, metrics)
    plt.xticks(fontsize=8)
    plt.ylabel('event rate (events/s)')
    plt.ylim((0, 0.05))
    plt.show()

    return


def eventrate_drugs(spn, base):

    drugs = ['haloperidol', 'olanzapine', 'clozapine',  'mp10']
    # bases = ['ctrl', 'amph']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'rear', 'other_rest', 'other_move']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()

    animals = []
    if spn == 'D1':
        animals = D1_animals
    elif spn == 'D2':
        animals = D2_animals

    cutoff_time = 5.
    if base == 'ctrl':
        cutoff = cutoff_time / 900.
    elif base == 'amph':
        cutoff = cutoff_time / 2700.

    fig, ax = plt.subplots(figsize=(12, 4))

    x = 0
    for metric in metrics:
        x = x + 2

        tempdata = {}
        eventrate_ctrl = {}
        eventtime_ctrl = {}
        eventtime_amph = {}

        for animal in animals:
            # [1] is population event rate (per sec)
            # [0] is event time (no of events per trial, 15 or 45 mins for ctrl or amph)

            eventrate_ctrl[animal] = np.nansum([alldata[d]['vehicle']['ctrl'][animal][metric]['rate'] *
                                                alldata[d]['vehicle']['ctrl'][animal][metric]['time'] * 900
                                                for d in alldata.keys()
                                                if animal in alldata[d]['vehicle']['ctrl'].keys()])
            eventtime_ctrl[animal] = np.nansum([alldata[d]['vehicle']['ctrl'][animal][metric]['time'] * 900
                                                for d in alldata.keys()
                                                if animal in alldata[d]['vehicle']['ctrl'].keys()])
            eventtime_amph[animal] = np.nansum([alldata[d]['vehicle']['amph'][animal][metric]['time'] * 2700
                                                for d in alldata.keys()
                                                if animal in alldata[d]['vehicle']['amph'].keys()])
            eventrate_ctrl[animal] = eventrate_ctrl[animal] / eventtime_ctrl[animal]

            if (eventtime_ctrl[animal] > 20.) and (eventtime_amph[animal] > 20.):

                tempdata[animal] = np.nansum([alldata[d]['vehicle']['amph'][animal][metric]['rate'] *
                                              alldata[d]['vehicle']['amph'][animal][metric]['time'] * 2700
                                              for d in alldata.keys()
                                              if animal in alldata[d]['vehicle']['ctrl'].keys()
                                              and alldata[d]['vehicle']['amph'][animal][metric]['time'] > (cutoff_time / 2700.)])

                tempdata[animal] = (tempdata[animal] / (eventtime_amph[animal] * eventrate_ctrl[animal])) * 100

        data = list(tempdata.values())
        mean = np.nanmean(data)
        sem = np.nanstd(data) / np.sqrt(len(data))
        if metric == 'acc':
            ax.bar(x, mean, yerr=sem, width=1, color='fuchsia', alpha=1, label='amph')
        else:
            ax.bar(x, mean, yerr=sem, width=1, color='fuchsia', alpha=1)
        # ax.plot([x]*len(data), data, 'k.')
        # ax.plot([x] * len(data) + np.random.normal(0, 0.15, size=(len(data))), data, 'k.', markersize=3.5)
        x = x + 1.5

        # colors = ['orangered', 'royalblue', 'forestgreen', 'darkviolet']
        colors = ['red', 'teal', 'blue', 'limegreen']
        for drug, color in zip(drugs, colors):
            x = x + 0.5

            # for base in bases:
            data = [((alldata[drug]['highdose'][base][animal][metric]['rate'] / eventrate_ctrl[animal]) * 100.)
                    for animal in animals
                    if animal in alldata[drug]['vehicle'][base].keys()
                    and animal in alldata[drug]['highdose'][base].keys()
                    and eventtime_ctrl[animal] > 20.
                    and alldata[drug]['highdose'][base][animal][metric]['time'] > cutoff]

            # mean = np.ma.masked_invalid(data).mean()
            # sem = np.ma.masked_invalid(data).std() / np.sqrt(len(data))
            mean = np.nanmean(data)
            sem = np.nanstd(data) / np.sqrt(len(data))

            if metric == 'acc':
                ax.bar(x, mean, yerr=sem, width=1, color=color, alpha=1, label=drug + '-' + base)
            else:
                ax.bar(x, mean, yerr=sem, width=1, color=color, alpha=1)
            # ax.plot([x]*len(data), data, 'k.')
            # ax.plot([x] * len(data) + np.random.normal(0, 0.15, size=(len(data))), data, 'k.', markersize=3.5)
            x = x + 1

    plt.axhspan(0, 100, alpha=0.2, color='k', zorder=0)
    # plt.axhline(y=1, color='k', alpha=0.2, linestyle=':')
    plt.suptitle(str(spn) + ' SPN event rate during performing behaviors')
    x_default = [5, 14.5, 24, 33.5, 43, 52.5, 62, 71.5, 81, 90.5]
    plt.xticks(x_default, metrics)
    plt.xticks(fontsize=8)
    plt.ylabel('% change in event rate from vehicle control')
    plt.ylim((0, 600))
    plt.legend()
    plt.show()

    return


def histogram_behavior(metric):
    bases = ['ctrl', 'amph']

    alldata = pkl.load(open("alldata.pkl", "rb"))

    fig, ax = plt.subplots(2, 2, figsize=(8, 7))
    for i, base in enumerate(bases):
        data = [alldata[d]['vehicle'][base][a][metric]
                for d in alldata.keys()
                for a in alldata[d]['vehicle'][base].keys()]
        data = np.mean(np.array(data), axis=0)
        data_dt = data[1:] - data[:-1]

        # plot histogram
        ax[0, i].hist(data_dt, bins=20)
        ax[0, i].set_title(base + ' historagam')

        count, bins_count = np.histogram(data_dt, bins=50)
        pdf = count / sum(count)  # find the PDF of the histogram using count values
        cdf = np.cumsum(pdf)  # use numpy cumsum to calculate the CDF

        ax[1, i].plot(bins_count[1:], pdf, color='r', label='PDF')
        ax[1, i].plot(bins_count[1:], cdf, label='CDF')
        ax[1, i].set_title(base + ' pdf/cdf')

    plt.legend()
    plt.show()

    return

