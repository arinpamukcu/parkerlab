# Created by Arin Pamukcu, PhD on August 2022 in Chicago, IL

from info import *
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
import pdb


def timespent_vehicle():

    # doses = ['vehicle', 'highdose']
    drugs = ['haloperidol', 'olanzapine', 'clozapine', 'mp10']
    bases = ['ctrl', 'amph']
    # metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'other']
    metrics = ['acc', 'dec', 'right_turn', 'left_turn', 'groom', 'other']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()
    animals = D1_animals + D2_animals

    fig, ax = plt.subplots(figsize=(6, 5))
    x = 0
    for metric in metrics:
        x = x + 2
        a = 1
        tempdata = {}
        for base in bases:
            for animal in animals:
                tempdata[animal] = np.nanmean([alldata[d]['vehicle'][base][animal][metric][0] * 100
                                               for d in alldata.keys()
                                               if animal in alldata[d]['vehicle'][base].keys()
                                               and alldata[d]['vehicle']['ctrl'][animal][metric][0] > (1. / 180.)])
            data = list(tempdata.values())
            mean = np.nanmean(data)
            sem = np.nanstd(data) / np.sqrt(len(data))
            ax.bar(x, mean, yerr=sem, width=1, color='k', alpha=a)
            x = x + 1
            a = a * 0.5
            # pdb.set_trace()

    plt.suptitle('percent time spent performing behaviors')
    plt.legend(['control', 'amph'])
    # x_default = [2.5, 6.5, 10.5, 14.5, 18.5, 22.5, 26.5, 30.5]
    x_default = [2.5, 6.5, 10.5, 14.5, 18.5, 22.5]
    plt.xticks(x_default, metrics)
    plt.xticks(fontsize=8)
    plt.ylabel('percent time of full trial duration (%)')
    plt.ylim((0, 100))
    plt.show()

    return


def timespent_drugs(base):

    drugs = ['haloperidol', 'olanzapine', 'clozapine',  'mp10']
    bases = ['ctrl', 'amph']
    # metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'other']
    metrics = ['acc', 'dec', 'right_turn', 'left_turn', 'groom', 'other']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()
    animals = D1_animals + D2_animals

    fig, ax = plt.subplots(figsize=(10, 5))

    x = 0
    for metric in metrics:

        x = x + 2
        tempdata = {}
        for animal in animals:
            tempdata[animal] = np.nanmean([((alldata[d]['vehicle']['amph'][animal][metric][0]
                                             / alldata[d]['vehicle']['ctrl'][animal][metric][0])) * 100.
                                           for d in alldata.keys()
                                           if animal in alldata[d]['vehicle']['ctrl'].keys()
                                           and alldata[d]['vehicle']['ctrl'][animal][metric][0] > (1. / 180.)])

        data = list(tempdata.values())
        mean = np.nanmean(data)
        sem = np.nanstd(data) / np.sqrt(len(data))
        if metric == 'acc':
            ax.bar(x, mean, yerr=sem, width=1, color='k', label='amph')
        else:
            ax.bar(x, mean, yerr=sem, width=1, color='k')
        # ax.plot([x] * len(data), data, 'k.')
        x = x + 1.5

        colors = ['orangered', 'royalblue', 'forestgreen', 'darkviolet']
        for drug, color in zip(drugs, colors):
            a = (0.5 if base == 'ctrl' else 1)
            x = x + 0.5
            # for base in bases:
            data = [((alldata[drug]['highdose'][base][a][metric][0]
                      / alldata[drug]['vehicle']['ctrl'][a][metric][0])) * 100.
                    for a in alldata[drug]['highdose'][base].keys()
                    if a in alldata[drug]['vehicle'][base].keys()
                    and alldata[drug]['vehicle']['ctrl'][a][metric][0] > (1. / 180.)]
            mean = np.nanmean(data)
            sem = np.nanstd(data) / np.sqrt(len(data))
            if metric == 'acc':
                ax.bar(x, mean, yerr=sem, width=1, color=color, alpha=a, label=drug + '-' + base)
            else:
                ax.bar(x, mean, yerr=sem, width=1, color=color, alpha=a)
            # ax.plot([x]*len(data), data, 'k.')
            x = x + 1
            a = a + 0.5

    plt.axhspan(0, 100, alpha=0.2, color='k', zorder=0)
    # plt.axhline(y=100, color='k', alpha=0.2, linestyle=':')
    plt.suptitle('fraction of time spent compared to veh-ctrl')
    # x_default = [8, 21.5, 35, 48.5, 62, 75.5, 89, 102.5]
    # x_default = [8, 21.5, 35, 48.5, 62, 75.5]
    x_default = [5, 14.5, 24, 33.5, 43, 52.5]
    plt.xticks(x_default, metrics)
    plt.xticks(fontsize=8)
    plt.ylabel('% change from vehicle control')
    plt.ylim((0, 400))
    plt.legend()
    plt.show()

    return


def eventrate_vehicle(spn):

    # doses = ['vehicle', 'highdose']
    # drugs = ['haloperidol', 'olanzapine', 'clozapine', 'mp10']
    bases = ['ctrl', 'amph']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'other']
    # metrics = ['acc', 'dec', 'right_turn', 'left_turn', 'groom', 'other']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()

    animals = []
    if spn == 'D1':
        animals = D1_animals
    elif spn == 'D2':
        animals = D2_animals

    fig, ax = plt.subplots(figsize=(8, 5))
    x = 0
    for metric in metrics:
        x = x + 2
        a = 0.5
        tempdata = {}
        for base in bases:
            for animal in animals:
                tempdata[animal] = np.nanmean([(alldata[d]['vehicle'][base][animal][metric][1])
                                               for d in alldata.keys()
                                               if animal in alldata[d]['vehicle']['ctrl'].keys()
                                               and alldata[d]['vehicle']['ctrl'][animal][metric][0] > (1. / 180.)])
            pdb.set_trace()

            data = list(tempdata.values())
            mean = np.nanmean(data)
            sem = np.nanstd(data) / np.sqrt(len(data))
            ax.bar(x, mean, yerr=sem, width=1, color='k', alpha=a)
            # ax.plot([x] * len(data), data, 'k.')
            x = x + 1
            a = a + 0.5

    plt.suptitle(str(spn) + ' SPN event rate during performing behaviors')
    plt.legend(['control', 'amph'])
    x_default = [2.5, 6.5, 10.5, 14.5, 18.5, 22.5, 26.5, 30.5]
    # x_default = [2.5, 6.5, 10.5, 14.5, 18.5, 22.5]
    plt.xticks(x_default, metrics)
    plt.xticks(fontsize=8)
    plt.ylabel('event rate (events/s)')
    plt.ylim((0, 0.04))
    plt.show()

    return


def eventrate_drugs(spn, base):

    drugs = ['haloperidol', 'olanzapine', 'clozapine',  'mp10']
    bases = ['ctrl', 'amph']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'other']
    # metrics = ['acc', 'dec', 'right_turn', 'left_turn', 'groom', 'other']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()

    animals = []
    if spn == 'D1':
        animals = D1_animals
    elif spn == 'D2':
        animals = D2_animals

    fig, ax = plt.subplots(figsize=(10, 5))
    x = 0
    for metric in metrics:
        x = x + 2

        tempdata = {}
        for animal in animals:
            tempdata[animal] = np.nanmean([((alldata[d]['vehicle']['amph'][animal][metric][1]
                                             / alldata[d]['vehicle']['ctrl'][animal][metric][1]) * 100.)
                                           for d in alldata.keys()
                                           if animal in alldata[d]['vehicle']['ctrl'].keys()
                                           and alldata[d]['vehicle']['ctrl'][animal][metric][0] > (1. / 180.)])

        data = list(tempdata.values())
        mean = np.nanmean(data)
        sem = np.nanstd(data) / np.sqrt(len(data))
        if metric == 'acc':
            ax.bar(x, mean, yerr=sem, width=1, alpha=1, color='k', label='amph')
        else:
            ax.bar(x, mean, yerr=sem, width=1, alpha=1, color='k')
        # ax.plot([x]*len(data), data, 'k.')
        x = x + 1.5

        colors = ['orangered', 'royalblue', 'forestgreen', 'darkviolet']
        for drug, color in zip(drugs, colors):
            a = (0.5 if base == 'ctrl' else 1)
            x = x + 0.5

            # for base in bases:
            data = [((alldata[drug]['highdose'][base][animal][metric][1]
                      / alldata[drug]['vehicle']['ctrl'][animal][metric][1]) * 100.)
                    for animal in animals
                    if animal in alldata[drug]['vehicle'][base].keys()
                    and animal in alldata[drug]['highdose'][base].keys()
                    and alldata[drug]['vehicle']['ctrl'][animal][metric][0] > (1. / 180.)]

            mean = np.ma.masked_invalid(data).mean()
            sem = np.ma.masked_invalid(data).std() / np.sqrt(len(data))
            if metric == 'acc':
                ax.bar(x, mean, yerr=sem, width=1, color=color, alpha=a, label=drug + '-' + base)
            else:
                ax.bar(x, mean, yerr=sem, width=1, color=color, alpha=a)
            # ax.plot([x]*len(data), data, 'k.')
            x = x + 1

    plt.axhspan(0, 100, alpha=0.2, color='k', zorder=0)
    # plt.axhline(y=1, color='k', alpha=0.2, linestyle=':')
    plt.suptitle(str(spn) + ' SPN event rate during performing behaviors')
    x_default = [5, 14.5, 24, 33.5, 43, 52.5, 62, 71.5]
    # x_default = [8, 21.5, 35, 48.5, 62, 75.5, 89, 102.5]
    # x_default = [8, 21.5, 35, 48.5, 62, 75.5]
    plt.xticks(x_default, metrics)
    plt.xticks(fontsize=8)
    plt.ylabel('% change in event rate from vehicle control')
    plt.ylim((0, 600))
    plt.legend()
    plt.show()

    return


def eventrates(spn):

    drugs = ['haloperidol', 'clozapine', 'olanzapine', 'mp10']
    doses = ['vehicle', 'highdose']
    bases = ['ctrl', 'amph']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'grooming', 'other']

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
                    data = [alldata[d][dose][base][s][metric][1]
                            for d in alldata.keys()
                            for s in alldata[d][dose][base].keys()
                            if s in animals]
                    mean = np.nanmean(data, axis=0)
                    sem = np.nanstd(data, axis=0) / np.sqrt(len(data))
                    ax.bar(x, mean, yerr=sem, width=1, color=color)
                    x = x + 1
            else:
                colors = ['royalblue', 'orangered', 'forestgreen', 'darkviolet']
                for drug, color in zip(drugs, colors):
                    x = x + 0.5
                    data = [alldata[drug][dose]['amph'][s][metric][1]
                            for s in alldata[drug][dose]['amph'].keys()
                            if s in animals]
                    mean = np.nanmean(data, axis=0)
                    sem = np.nanstd(data, axis=0) / np.sqrt(len(data))
                    ax.bar(x, mean, yerr=sem, width=1, color=color, alpha=0.7)
                    x = x + 1

    plt.suptitle(str(spn) + ' SPN event rate during performing behaviors')
    plt.legend(['ctrl', 'amph', 'haloperidol', 'clozapine', 'olanzapine', 'mp10'])
    x_default = [2.5, 12.5, 22.5, 32.5, 42.5, 52.5, 62.5, 72.5]
    plt.xticks(x_default, metrics)
    plt.xticks(fontsize=8)
    plt.ylabel('event rate (event/s)')
    plt.ylim((0, 0.07))
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

