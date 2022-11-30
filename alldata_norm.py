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

    savemat("normdata_timespent.mat", normtime)

    return normtime


def eventrate(spn):
    drugs = ['haloperidol', 'olanzapine', 'clozapine', 'mp10']
    bases = ['ctrl', 'amph']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'rear', 'other_rest', 'other_move']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()
    # animals = D1_animals + D2_animals

    animals = []
    if spn == 'D1':
        animals = D1_animals
    elif spn == 'D2':
        animals = D2_animals

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

    filename = 'normdata_eventrate_' + spn + '.mat'
    savemat(filename, normrate)

    return normrate