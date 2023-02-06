# Created by Arin Pamukcu, PhD on August 2022 in Chicago, IL
# predict spikes from behavioral features

from info import *
from mars import *
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

    d1_events_ctrl, d1_events_amph, d1_network_ctrl, d1_network_amph, d1_speed_ctrl, d1_speed_amph, \
    d1_turn_ctrl, d1_turn_amph, d1_groom_ctrl, d1_groom_amph, d1_rear_ctrl, d1_rear_amph = ([] for i in range(12))
    d2_events_ctrl, d2_events_amph, d2_network_ctrl, d2_network_amph, d2_speed_ctrl, d2_speed_amph, \
    d2_turn_ctrl, d2_turn_amph, d2_groom_ctrl, d2_groom_amph, d2_rear_ctrl, d2_rear_amph = ([] for i in range(12))

    for experiment, animal in zip(experiments, animals):
        # print(experiment)

        _, _, calcium_ctrl_processed, calcium_amph_processed, \
        _, _, _, = get_calcium_dff(drug, dose, experiment)
        speed_ctrl, speed_amph, events_ctrl, events_amph, eventmean_ctrl, eventmean_amph, \
        _, _, _ = get_calcium_events(drug, dose, experiment)

        turn_ctrl, turn_amph = get_mars_features(drug, dose, experiment)
        groom_ctrl, groom_amph = get_classifier(drug, dose, experiment, 'grooming')
        rear_ctrl, rear_amph = get_classifier(drug, dose, experiment, 'rearing')

        if len(turn_ctrl) != 4500:
            pad_size = 4500 - len(turn_ctrl)
            turn_ctrl = np.pad(turn_ctrl, (0, pad_size), mode='constant', constant_values='nan')
            groom_ctrl = np.pad(groom_ctrl, (0, pad_size), mode='constant', constant_values='nan')
            rear_ctrl = np.pad(rear_ctrl, (0, pad_size), mode='constant', constant_values='nan')
        if len(turn_amph) != 13500:
            pad_size = 13500 - len(turn_amph)
            turn_amph = np.pad(turn_amph, (0, pad_size), mode='constant', constant_values='nan')
            groom_amph = np.pad(groom_amph, (0, pad_size), mode='constant', constant_values='nan')
            rear_amph = np.pad(rear_amph, (0, pad_size), mode='constant', constant_values='nan')
        else:
            pass

        if animal in alldata[drug][dose]['ctrl'].keys():
            if animal in D1_animals:
                print('D1_animal: ' + experiment)

                d1_events_ctrl = np.hstack((d1_events_ctrl, events_ctrl[0, :-shift]))
                d1_events_amph = np.hstack((d1_events_amph, events_ctrl[0, :-shift]))

                d1_network_ctrl = np.hstack((d1_network_ctrl, eventmean_ctrl[:-shift]))
                d1_network_amph = np.hstack((d1_network_amph, eventmean_amph[:-shift]))

                speed_ctrl_shifted = feature_future(speed_ctrl[:], shift).T
                speed_amph_shifted = feature_future(speed_amph[:], shift).T
                turn_ctrl_shifted = feature_future(turn_ctrl[:], shift).T
                turn_amph_shifted = feature_future(turn_amph[:], shift).T
                groom_ctrl_shifted = feature_future(groom_ctrl[:], shift).T
                groom_amph_shifted = feature_future(groom_amph[:], shift).T
                rear_ctrl_shifted = feature_future(rear_ctrl[:], shift).T
                rear_amph_shifted = feature_future(rear_amph[:], shift).T

                d1_speed_ctrl.extend(speed_ctrl_shifted)
                d1_speed_amph.extend(speed_amph_shifted)
                d1_turn_ctrl.extend(turn_ctrl_shifted)
                d1_turn_amph.extend(turn_amph_shifted)
                d1_groom_ctrl.extend(groom_ctrl_shifted)
                d1_groom_amph.extend(groom_amph_shifted)
                d1_rear_ctrl.extend(rear_ctrl_shifted)
                d1_rear_amph.extend(rear_amph_shifted)

            elif animal in D2_animals:
                print('D2_animal: ' + experiment)

                d2_events_ctrl = np.hstack((d2_events_ctrl, events_ctrl[0, :-shift]))
                d2_events_amph = np.hstack((d2_events_amph, events_ctrl[0, :-shift]))

                d2_network_ctrl = np.hstack((d2_network_ctrl, eventmean_ctrl[:-shift]))
                d2_network_amph = np.hstack((d2_network_amph, eventmean_amph[:-shift]))

                speed_ctrl_shifted = feature_future(speed_ctrl[:], shift).T
                speed_amph_shifted = feature_future(speed_amph[:], shift).T
                turn_ctrl_shifted = feature_future(turn_ctrl[:], shift).T
                turn_amph_shifted = feature_future(turn_amph[:], shift).T
                groom_ctrl_shifted = feature_future(groom_ctrl[:], shift).T
                groom_amph_shifted = feature_future(groom_amph[:], shift).T
                rear_ctrl_shifted = feature_future(rear_ctrl[:], shift).T
                rear_amph_shifted = feature_future(rear_amph[:], shift).T

                d2_speed_ctrl.extend(speed_ctrl_shifted)
                d2_speed_amph.extend(speed_amph_shifted)
                d2_turn_ctrl.extend(turn_ctrl_shifted)
                d2_turn_amph.extend(turn_amph_shifted)
                d2_groom_ctrl.extend(groom_ctrl_shifted)
                d2_groom_amph.extend(groom_amph_shifted)
                d2_rear_ctrl.extend(rear_ctrl_shifted)
                d2_rear_amph.extend(rear_amph_shifted)

    # add 10 seconds of feature future
    d1_speed_ctrl_shifted = np.array(d1_speed_ctrl).T
    d1_speed_amph_shifted = np.array(d1_speed_amph).T
    d1_turn_ctrl_shifted = np.array(d1_turn_ctrl).T
    d1_turn_amph_shifted = np.array(d1_turn_amph).T
    d1_groom_ctrl_shifted = np.array(d1_groom_ctrl).T
    d1_groom_amph_shifted = np.array(d1_groom_amph).T
    d1_rear_ctrl_shifted = np.array(d1_rear_ctrl).T
    d1_rear_amph_shifted = np.array(d1_rear_amph).T

    d2_speed_ctrl_shifted = np.array(d2_speed_ctrl).T
    d2_speed_amph_shifted = np.array(d2_speed_amph).T
    d2_turn_ctrl_shifted = np.array(d2_turn_ctrl).T
    d2_turn_amph_shifted = np.array(d2_turn_amph).T
    d2_groom_ctrl_shifted = np.array(d2_groom_ctrl).T
    d2_groom_amph_shifted = np.array(d2_groom_amph).T
    d2_rear_ctrl_shifted = np.array(d2_rear_ctrl).T
    d2_rear_amph_shifted = np.array(d2_rear_amph).T

    # pdb.set_trace()

    d1_ctrl_regressor = np.vstack((d1_speed_ctrl_shifted, d1_turn_ctrl_shifted, d1_groom_ctrl_shifted, d1_rear_ctrl_shifted, d1_network_ctrl))
    d1_amph_regressor = np.vstack((d1_speed_amph_shifted, d1_turn_amph_shifted, d1_groom_amph_shifted, d1_rear_amph_shifted, d1_network_amph))
    d2_ctrl_regressor = np.vstack((d2_speed_ctrl_shifted, d2_turn_ctrl_shifted, d2_groom_ctrl_shifted, d2_rear_ctrl_shifted, d2_network_ctrl))
    d2_amph_regressor = np.vstack((d2_speed_amph_shifted, d2_turn_amph_shifted, d2_groom_amph_shifted, d2_rear_amph_shifted, d2_network_amph))

    pkl.dump(d1_events_ctrl, open("d1_events_ctrl.pkl", "wb"))
    pkl.dump(d1_ctrl_regressor, open("d1_ctrl_regressor.pkl", "wb"))
    pkl.dump(d1_events_amph, open("d1_events_amph.pkl", "wb"))
    pkl.dump(d1_amph_regressor, open("d1_amph_regressor.pkl", "wb"))

    return d1_events_ctrl, d1_ctrl_regressor, d1_events_amph, d1_amph_regressor, \
           d2_events_ctrl, d2_ctrl_regressor, d2_events_amph, d2_amph_regressor


def perform_glm():
    # experiments, animals, _, _ = get_animal_id(drug, dose)

    # d1_events_ctrl, d1_ctrl_regressor, d1_event_amph, d1_amph_regressor, \
    # d2_events_ctrl, d2_ctrl_regressor, d2_event_amph, d2_amph_regressor = prep_data(drug, dose, shift)

    d1_event_amph = pkl.load(open("d1_events_amph.pkl", "rb"))
    d1_amph_regressor = pkl.load(open("d1_amph_regressor.pkl", "rb"))

    ttsplit = int(13500 / 4)

    event_train = d1_event_amph[:ttsplit]
    event_test = d1_event_amph[ttsplit:]

    feature_train = sm.add_constant(d1_amph_regressor[:, :ttsplit], prepend=False)
    feature_test = sm.add_constant(d1_amph_regressor[:, ttsplit:], prepend=False)

    pdb.set_trace()

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
    # plt.xlim(0, 1400)
    plt.ylabel('spike count')

    ax = plt.subplot(2, 1, 2)
    plt.plot(event_predict, label='glm reconstruct, R2=', color='k')
    # plt.xlim(0, 1400)
    plt.xlabel('time (5Hz)')
    plt.ylabel('spike count')

    plt.legend()
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
