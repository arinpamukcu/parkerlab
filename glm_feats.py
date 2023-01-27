# Created by Arin Pamukcu, PhD on January 2023 in Chicago, IL
# predict behavior from spikes

import statsmodels.api as sm
import pickle as pkl
from info import *
from mars import *
from alldata import *

# check which neurons have a strong decoding weight for speed
# to use poisson glm, you can choose a max speed and round all data to the next integer

def data_prep(eventrate):
    timeSplit = 1500

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()
    animals = D1_animals + D2_animals

    for experiment, animal in zip(experiments, animals):
        if animal in alldata[drug][dose][base].keys():
            _, _, neuron, time_ctrl, time_amph, \
            calcium_ctrl_processed, calcium_amph_processed = get_calcium_dff(drug, dose, experiment)
            print(animal)
            dimred['vehicle'].append(calcium_ctrl_processed)
            pdb.set_trace()

    fulldata_ctrl, fulldata_amph, metric_ctrl, metric_amph = get_metrics(drug, dose)

    feature_train = all_move_bouts[timeSplit:]
    feature_test = all_move_bouts[:timeSplit]

    # fit GLM to single cell raw
    events_train = sm.add_constant(eventrate[:, timeSplit:].T, prepend=False)
    events_test = sm.add_constant(eventrate[:, :timeSplit].T, prepend=False)

    # fit GLM to single cell spike
    spike_train = sm.add_constant(peaktime_ctrl[:,:timeSplit].T, prepend=False)
    spike_test = sm.add_constant(peaktime_ctrl[:,timeSplit:].T, prepend=False)

    return