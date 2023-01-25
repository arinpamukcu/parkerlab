# Created by Arin Pamukcu, PhD on August 2022 in Chicago, IL

from info import *
from calcium import *
import statsmodels.api as sm
import pickle as pkl
import pdb

# Use the shifted_frames  to concatenate feature values with shifted feature values according to defined frame number.
# Currently set up for future shifts "feature future" --can also change it to past shifts "feature history"


def shifted_frames(data, list, spike_shift, frame_shift):
    # data: data you want to use for this function.
    # list: add this if you want to specify a list of indexes for the features to use for this function.
    # frameshift: number of frames to be shifted

    if list is None:
        data_shifted = data[spike_shift:-frame_shift, :]
        # print(featureData_shifted.shape)
        for i in range(0, frame_shift - 1):
            shifted = data[spike_shift + i:-(frame_shift - i), :]
            data_shifted = np.concatenate((data_shifted, shifted), axis=1)

    else:
        data_shifted = data[spike_shift:-frame_shift, list]
        # print(featureData_shifted.shape)
        for i in range(0, frame_shift - 1):
            shifted = data[spike_shift + i:-(frame_shift - i), list]
            data_shifted = np.concatenate((data_shifted, shifted), axis=1)

    # print(data_shifted.shape)

    return data_shifted


def data_prep(drug, dose, base):

    experiments, animals, _, _ = get_animal_id(drug, dose)

    alldata = pkl.load(open("alldata.pkl", "rb"))
    D1_animals, D2_animals = D1_D2_names()
    # animals = D1_animals + D2_animals

    d1_eventmean_ctrl, d1_eventmean_amph, d1_speed_ctrl, d1_speed_amph = ([] for i in range(4))
    d2_eventmean_ctrl, d2_eventmean_amph, d2_speed_ctrl, d2_speed_amph = ([] for i in range(4))

    for experiment, animal in zip(experiments, animals):
        print(experiment)
        print(animal)

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

    # pdb.set_trace()

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

    return d1_eventmean_ctrl, d1_eventmean_amph, d1_speed_ctrl, d1_speed_amph, \
           d2_eventmean_ctrl, d2_eventmean_amph, d2_speed_ctrl, d2_speed_amph