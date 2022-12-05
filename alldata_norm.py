# Created by Arin Pamukcu, PhD on August 2022 in Chicago, IL

from info import *
import numpy as np
import pickle as pkl
import pdb
from scipy.io import savemat

def timespent():
    drugs = ['haloperidol', 'olanzapine', 'clozapine', 'mp10']
    bases = ['ctrl', 'amph']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'rear', 'other_rest', 'other_move']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()
    animals = D1_animals + D2_animals

    eventtime_ctrl = {}
    normtime = {}
    normtime['vehicle'] = {}
    normtime['vehicle']['amph'] = {}

    for animal in animals:
        normtime['vehicle']['amph'][animal] = {}

        for metric in metrics:
            eventtime_ctrl[animal] = np.nanmean([alldata[d]['vehicle']['ctrl'][animal][metric]['time']
                                                 for d in alldata.keys()
                                                 if animal in alldata[d]['vehicle']['ctrl'].keys()])

            if (eventtime_ctrl[animal] > 1. / 180.):
                normtime['vehicle']['amph'][animal][metric] \
                    = np.nanmean([alldata[d]['vehicle']['amph'][animal][metric]['time']
                                  for d in alldata.keys()
                                  if animal in alldata[d]['vehicle']['ctrl'].keys()]) / eventtime_ctrl[animal] * 100.
            else:
                normtime['vehicle']['amph'][animal][metric] = 'NaN'

    for drug in drugs:
        normtime[drug] = {}

        for base in bases:
            normtime[drug][base] = {}

            for animal in alldata[drug]['highdose'][base].keys():
                normtime[drug][base][animal] = {}

                for metric in metrics:

                    if (animal in alldata[drug]['vehicle'][base].keys()) \
                            and (alldata[drug]['vehicle']['ctrl'][animal][metric]['time'] > (1. / 180.)):

                        normtime[drug][base][animal][metric] = [((alldata[drug]['highdose'][base][animal][metric]['time']
                                                                  / alldata[drug]['vehicle']['ctrl'][animal][metric]['time'])) * 100.]
                    else:
                        normtime[drug][base][animal][metric] = 'NaN'

    pkl.dump(normtime, open("norm_timespent.pkl", "wb"))
    savemat("norm_timespent.mat", normtime)

    return normtime


def eventrate():
    drugs = ['haloperidol', 'olanzapine', 'clozapine', 'mp10']
    bases = ['ctrl', 'amph']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'rear', 'other_rest', 'other_move']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()
    animals = D1_animals + D2_animals

    # animals = []
    # if spn == 'D1':
    #     animals = D1_animals
    # elif spn == 'D2':
    #     animals = D2_animals

    normrate = {}
    normrate['vehicle'] = {}
    normrate['vehicle']['amph'] = {}
    for animal in animals:
        normrate['vehicle']['amph'][animal] = {}

    cutoff_time = 5.

    eventrate_ctrl, eventtime_ctrl, eventtime_amph, tempdata = ({} for i in range(4))

    for animal in animals:
        eventrate_ctrl[animal], eventtime_ctrl[animal], eventtime_amph[animal], tempdata[animal] = ({} for i in range(4))

        for metric in metrics:

            eventrate_ctrl[animal][metric] = np.nansum([alldata[d]['vehicle']['ctrl'][animal][metric]['rate'] *
                                                        alldata[d]['vehicle']['ctrl'][animal][metric]['time'] * 900
                                                        for d in alldata.keys()
                                                        if animal in alldata[d]['vehicle']['ctrl'].keys()])
            eventtime_ctrl[animal][metric] = np.nansum([alldata[d]['vehicle']['ctrl'][animal][metric]['time'] * 900
                                                        for d in alldata.keys()
                                                        if animal in alldata[d]['vehicle']['ctrl'].keys()])
            eventtime_amph[animal][metric] = np.nansum([alldata[d]['vehicle']['amph'][animal][metric]['time'] * 2700
                                                        for d in alldata.keys()
                                                        if animal in alldata[d]['vehicle']['amph'].keys()])
            eventrate_ctrl[animal][metric] = eventrate_ctrl[animal][metric] / eventtime_ctrl[animal][metric]

            if (eventtime_ctrl[animal][metric] > 20.) and (eventtime_amph[animal][metric] > 20.):
                tempdata[animal][metric] = \
                    np.nansum([alldata[d]['vehicle']['amph'][animal][metric]['rate'] *
                               alldata[d]['vehicle']['amph'][animal][metric]['time'] * 2700
                               for d in alldata.keys()
                               if animal in alldata[d]['vehicle']['ctrl'].keys()
                               and alldata[d]['vehicle']['amph'][animal][metric]['time'] > (cutoff_time / 2700.)])

                normrate['vehicle']['amph'][animal][metric] = \
                    (tempdata[animal][metric] / (eventtime_amph[animal][metric] * eventrate_ctrl[animal][metric])) * 100

            else:
                normrate['vehicle']['amph'][animal][metric] = 'NaN'

    for drug in drugs:
        normrate[drug] = {}

        for base in bases:
            normrate[drug][base] = {}

            if base == 'ctrl':
                cutoff = cutoff_time / 900.
            elif base == 'amph':
                cutoff = cutoff_time / 2700.

            for animal in animals:
                normrate[drug][base][animal] = {}

                for metric in metrics:

                    if (animal in alldata[drug]['vehicle'][base].keys()) \
                            and (animal in alldata[drug]['highdose'][base].keys()) \
                            and (alldata[drug]['highdose'][base][animal][metric]['time'] > cutoff) \
                            and (eventtime_ctrl[animal][metric] > 20.):

                        normrate[drug][base][animal][metric] = ((alldata[drug]['highdose'][base][animal][metric]['rate']
                                                                 / eventrate_ctrl[animal][metric]) * 100.)

                    else:
                        normrate[drug][base][animal][metric] = 'NaN'
            # pdb.set_trace()


    # filename = "norm_eventrate"
    pkl.dump(normrate, open("norm_eventrate.pkl", "wb"))
    savemat("norm_eventrate.mat", normrate)

    return normrate


def separate_spns(spn, event):
    # events = ['time', 'rate']
    drugs = ['haloperidol', 'olanzapine', 'clozapine', 'mp10']
    # doses = ['vehicle', 'lowdose', 'highdose']
    bases = ['ctrl', 'amph']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'rear', 'other_rest', 'other_move']

    if event == 'time':
        filename = "norm_timespent.pkl"
    elif event == 'rate':
        filename = "norm_eventrate.pkl"

    normdata = pkl.load(open(filename, "rb"))
    D1_animals, D2_animals = D1_D2_names()

    animals = []
    if spn == 'D1':
        animals = D1_animals
    elif spn == 'D2':
        animals = D2_animals

    data = {}

    for drug in drugs:
        data[drug] = {}

        # for dose in doses:
        #     data[drug][dose] = {}

        for base in bases:
            data[drug][base] = np.ndarray((len(metrics), len(animals)), dtype=object)

            for i, metric in enumerate(metrics):

                for j, animal in enumerate(animals):

                    if animal in normdata[drug][base].keys():
                        data[drug][base][i, j] = normdata[drug][base][animal][metric]

                    else:
                        data[drug][base][i, j] = 'NaN'

    filename = 'norm_' + spn + '_' + event + '.mat'

    savemat(filename, data)

    return data
