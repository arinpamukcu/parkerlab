# Created by Arin Pamukcu, PhD on August 2022 in Chicago, IL
# predict spikes from behavioral features

from info import *
from calcium import *
import statsmodels.api as sm
import pickle as pkl
import pdb


def feature_future(data, featureshift):
    # Use this to vertically concatenate data with shifted data.

    data_shifted = np.array(data[0:-featureshift])
    for i in range(1, featureshift + 1):
        shifted = np.array(data[i:(len(data)-(featureshift - i))])
        data_shifted = np.vstack((data_shifted, shifted))

    return data_shifted


def spike_history(data, spikeshift):
    # Use this to vertically concatenate data with shifted data.

    data_shifted = np.array(data[spikeshift:])
    for i in range(1, spikeshift + 1):
        shifted = np.array(data[spikeshift - i: -i])
        data_shifted = np.vstack((data_shifted, shifted))

    return data_shifted


def prep_data(drug, dose, base, shift):

    experiments, animals, _, _ = get_animal_id(drug, dose)

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()
    # animals = D1_animals + D2_animals

    d1_eventmean_ctrl, d1_eventmean_amph, d1_speed_ctrl, d1_speed_amph = ([] for i in range(4))
    d2_eventmean_ctrl, d2_eventmean_amph, d2_speed_ctrl, d2_speed_amph = ([] for i in range(4))

    for experiment, animal in zip(experiments, animals):
        print(experiment)

        _, _, calcium_ctrl_processed, calcium_amph_processed, \
        _, _, _, = get_calcium_dff(drug, dose, experiment)
        speed_ctrl, speed_amph, calcium_ctrl_events, calcium_amph_events, eventmean_ctrl, eventmean_amph, \
        _, _, _ = get_calcium_events(drug, dose, experiment)

        if animal in alldata[drug][dose][base].keys():
            if animal in D1_animals:
                d1_eventmean_ctrl.extend(eventmean_ctrl)
                d1_eventmean_amph.extend(eventmean_amph)

                d1_speed_ctrl.extend(speed_ctrl)
                d1_speed_amph.extend(speed_amph)

            elif animal in D2_animals:
                d2_eventmean_ctrl.extend(eventmean_ctrl)
                d2_eventmean_amph.extend(eventmean_amph)

                d2_speed_ctrl.extend(speed_ctrl)
                d2_speed_amph.extend(speed_amph)

    # add 10 seconds of feature future
    d1_speed_ctrl_shifted = feature_future(d1_speed_ctrl[:], shift)
    d1_speed_amph_shifted = feature_future(d1_speed_amph[:], shift)
    d2_speed_ctrl_shifted = feature_future(d2_speed_ctrl[:], shift)
    d2_speed_amph_shifted = feature_future(d2_speed_amph[:], shift)

    d1_eventmean_ctrl = np.array(d1_eventmean_ctrl[:-shift])
    d1_eventmean_amph = np.array(d1_eventmean_amph[:-shift])
    d2_eventmean_ctrl = np.array(d2_eventmean_ctrl[:-shift])
    d2_eventmean_amph = np.array(d2_eventmean_amph[:-shift])

    pdb.set_trace()

    return d1_speed_ctrl_shifted, d1_speed_amph_shifted, d2_speed_ctrl_shifted, d2_speed_amph_shifted, \
           d1_eventmean_ctrl, d1_eventmean_amph, d2_eventmean_ctrl, d2_eventmean_amph


def perform_glm(drug, dose, base, shift):

    d1_speed_ctrl_shifted, d1_speed_amph_shifted, d2_speed_ctrl_shifted, d2_speed_amph_shifted, \
    d1_eventmean_ctrl, d1_eventmean_amph, d2_eventmean_ctrl, d2_eventmean_amph = prep_data(drug, dose, base, shift)

    ttsplit = len(d1_eventmean_ctrl) * .20

    event_train = d1_eventmean_ctrl[:ttsplit]
    event_test = d1_eventmean_ctrl[ttsplit:]

    feature_train = d1_speed_ctrl_shifted[:,:ttsplit]
    feature_test = d1_speed_ctrl_shifted[:,ttsplit:]

    return

    # need events + shifted features (hmm?)

    # feature_train = all_move_bouts[timeSplit:]
    # feature_test = all_move_bouts[:timeSplit]
    #
    # # fit GLM to single cell raw
    # calcium_raw_train = sm.add_constant(eventrate[:, timeSplit:].T, prepend=False)
    # calcium_raw_test = sm.add_constant(eventrate[:, :timeSplit].T, prepend=False)
    #
    # # fit GLM to single cell spike
    # calcium_events_train = sm.add_constant(peaktime_ctrl[:,:timeSplit].T, prepend=False)
    # calcium_events_test = sm.add_constant(peaktime_ctrl[:,timeSplit:].T, prepend=False)
