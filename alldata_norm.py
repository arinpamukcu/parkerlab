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

    normdata = {}
    normdata['vehicle'] = {}
    normdata['vehicle']['amph'] = {}

    for animal in animals:
        normdata['vehicle']['amph'][animal] = {}
        baseline = {}

        for metric in metrics:
            baseline[animal] = np.nanmean([alldata[d]['vehicle']['ctrl'][animal][metric]['time']
                                           for d in alldata.keys()
                                           if animal in alldata[d]['vehicle']['ctrl'].keys()])

            if (baseline[animal] > 1. / 180.):
                normdata['vehicle']['amph'][animal][metric] \
                    = np.nanmean([alldata[d]['vehicle']['amph'][animal][metric]['time']
                                  for d in alldata.keys()
                                  if animal in alldata[d]['vehicle']['ctrl'].keys()]) / baseline[animal] * 100.
            else:
                normdata['vehicle']['amph'][animal][metric] = 'NaN'

    for drug in drugs:
        normdata[drug] = {}

        for base in bases:
            normdata[drug][base] = {}

            for animal in alldata[drug]['highdose'][base].keys():
                normdata[drug][base][animal] = {}

                for metric in metrics:

                    if (animal in alldata[drug]['vehicle'][base].keys()) and (alldata[drug]['vehicle']['ctrl'][animal][metric]['time'] > (1. / 180.)):

                        normdata[drug][base][animal][metric] = [((alldata[drug]['highdose'][base][animal][metric]['time']
                                                                  / alldata[drug]['vehicle']['ctrl'][animal][metric]['time'])) * 100.]
                    else:
                        normdata[drug][base][animal][metric] = 'NaN'

    pkl.dump(normdata, open("normdata_timespent.pkl", "wb"))
    savemat("normdata_timespent.mat", normdata)

    return normdata


def eventrate():
    drugs = ['haloperidol', 'olanzapine', 'clozapine', 'mp10']
    bases = ['ctrl', 'amph']
    metrics = ['rest', 'move', 'acc', 'dec', 'right_turn', 'left_turn', 'groom', 'rear', 'other_rest', 'other_move']

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()
    animals = D1_animals + D2_animals

    normdata = {}
    normdata['vehicle'] = {}

    cutoff_time = 5.

    for animal in animals:
        normdata['vehicle'][animal] = {}
        tempdata = {}
        eventrate_ctrl = {}
        eventtime_ctrl = {}
        eventtime_amph = {}

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

                normdata['vehicle'][animal] = (tempdata[animal] / (eventtime_amph[animal] * eventrate_ctrl[animal])) * 100

    for drug in drugs:
        normdata[drug] = {}

        for base in bases:
            normdata[drug][base] = {}

            if base == 'ctrl':
                cutoff = cutoff_time / 900.
            elif base == 'amph':
                cutoff = cutoff_time / 2700.

            for animal in alldata[drug]['highdose'][base].keys():
                normdata[drug][base][animal] = {}

                for metric in metrics:

                    if (animal in alldata[drug]['vehicle'][base].keys())
                        and (animal in alldata[drug]['highdose'][base].keys())
                        and (alldata[drug]['highdose'][base][animal][metric]['time'] > cutoff)
                        and (eventtime_ctrl[animal] > 20.):
                        normdata[drug][base][animal][metric] = ((alldata[drug]['highdose'][base][animal][metric]['rate']
                                                                 / eventrate_ctrl[animal]) * 100.)

    pkl.dump(normdata, open("normdata_timespent.pkl", "wb"))
    savemat("normdata_timespent.mat", normdata)

    return normdata