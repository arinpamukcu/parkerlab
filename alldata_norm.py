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

                    if (animal in alldata[drug]['vehicle'][base].keys()) and (alldata[drug]['vehicle']['ctrl'][animal][metric]['time'] > (1. / 180.)):

                        normtime[drug][base][animal][metric] = [((alldata[drug]['highdose'][base][animal][metric]['time']
                                                                  / alldata[drug]['vehicle']['ctrl'][animal][metric]['time'])) * 100.]
                    else:
                        normtime[drug][base][animal][metric] = 'NaN'

    pkl.dump(normtime, open("normdata_timespent.pkl", "wb"))
    savemat("normdata_timespent.mat", normtime)

    return normtime


def eventrate():
    drugs = ['haloperidol', 'olanzapine', 'clozapine', 'mp10']
    bases = ['ctrl', 'amph']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'rear', 'other_rest', 'other_move']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()
    animals = D1_animals + D2_animals

    eventrate_ctrl = {}
    eventtime_ctrl = {}
    eventtime_amph = {}
    tempdata = {}
    normrate = {}
    normrate['vehicle'] = {}

    cutoff_time = 5.

    for animal in animals:
        normrate['vehicle'][animal] = {}

        for metric in metrics:
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

                normrate['vehicle'][animal] = (tempdata[animal] / (eventtime_amph[animal] * eventrate_ctrl[animal])) * 100

    for drug in drugs:
        normrate[drug] = {}

        for base in bases:
            normrate[drug][base] = {}

            if base == 'ctrl':
                cutoff = cutoff_time / 900.
            elif base == 'amph':
                cutoff = cutoff_time / 2700.

            for animal in alldata[drug]['highdose'][base].keys():
                normrate[drug][base][animal] = {}

                for metric in metrics:
                    # pdb.set_trace()

                    if (animal in alldata[drug]['vehicle'][base].keys()) \
                            and (alldata[drug]['highdose'][base][animal][metric]['time'] > cutoff) \
                            and (eventtime_ctrl[animal] > 20.):

                        normrate[drug][base][animal][metric] = ((alldata[drug]['highdose'][base][animal][metric]['rate']
                                                                 / eventrate_ctrl[animal]) * 100.)

    pkl.dump(normrate, open("normdata_eventrate.pkl", "wb"))
    savemat("normdata_eventrate.mat", normrate)

    return normrate