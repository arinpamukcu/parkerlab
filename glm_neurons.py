# Created by Arin Pamukcu, PhD on August 2022 in Chicago, IL
# predict spikes from behavioral features

from info import *
from calcium import *
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
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


def prep_data(drug, dose, shift):

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

        if animal in alldata[drug][dose]['ctrl'].keys():
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

    # pdb.set_trace()

    pkl.dump(d1_speed_ctrl_shifted, open("d1_speed_ctrl_shifted.pkl", "wb"))
    pkl.dump(d1_speed_amph_shifted, open("d1_speed_amph_shifted.pkl", "wb"))

    pkl.dump(d1_eventmean_ctrl, open("d1_eventmean_ctrl.pkl", "wb"))
    pkl.dump(d1_eventmean_amph, open("d1_eventmean_amph.pkl", "wb"))

    return d1_speed_ctrl_shifted, d1_speed_amph_shifted, d2_speed_ctrl_shifted, d2_speed_amph_shifted, \
           d1_eventmean_ctrl, d1_eventmean_amph, d2_eventmean_ctrl, d2_eventmean_amph


def perform_glm():

    # d1_speed_ctrl_shifted, d1_speed_amph_shifted, d2_speed_ctrl_shifted, d2_speed_amph_shifted, \
    # d1_eventmean_ctrl, d1_eventmean_amph, d2_eventmean_ctrl, d2_eventmean_amph = prep_data(drug, dose, base, shift)

    d1_speed_ctrl_shifted = pkl.load(open("d1_speed_ctrl_shifted.pkl", "rb"))
    d1_eventmean_ctrl = pkl.load(open("d1_eventmean_ctrl.pkl", "rb"))

    ttsplit = int(len(d1_eventmean_ctrl) / 4)

    event_train = d1_eventmean_ctrl[:ttsplit]
    event_test = d1_eventmean_ctrl[ttsplit:]

    feature_train = sm.add_constant(d1_speed_ctrl_shifted[:, :ttsplit].T, prepend=False)
    feature_test = sm.add_constant(d1_speed_ctrl_shifted[:, ttsplit:].T, prepend=False)

    # pdb.set_trace()

    glm = sm.GLM(event_train, feature_train, sm.families.Poisson())
    glm_fit = glm.fit_regularized(method='elastic_net')

    # reconstruct and predict spike from feature
    event_predict = gaussian_filter1d(glm_fit.predict(feature_test), sigma=1)
    # event_predict = glm_fit.predict(feature_test)

    # glm_xcor = np.correlate(spike_test,spike_predict)
    glm_corrcoef = np.corrcoef(event_test, event_predict)
    glm_r2 = r2_score(event_test, event_predict)

    plt.figure(figsize=(10, 4))
    # plt.plot(spike_test, label='original')

    ax = plt.subplot(2, 1, 1)
    plt.plot(event_test, label='original', color='k')
    plt.xlim(0, 1400)
    plt.ylabel('spike count')
    plt.legend()

    ax = plt.subplot(2, 1, 2)
    plt.plot(event_predict, label='glm reconstruct, R2=', color='k')
    plt.xlim(0, 1400)
    plt.legend()
    plt.xlabel('time (5Hz)')
    plt.ylabel('spike count')
    plt.show()

    return glm_corrcoef, glm_r2

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
