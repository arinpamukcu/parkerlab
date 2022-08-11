# y-axis: Ca event rate (event/min)
# x-axis: Locomotor speed bin (cm/s)
# bin: <0.5, 0.5-1, 1-2, 2-4, 4-8, 8-14

from mars import *
from calcium_old import *
from info import *
from time import sleep
from progressbar import progressbar

# for i in progressbar(range(100), redirect_stdout=True):
#     sleep(0.1)

def event_per_speed():
    event_per_speed = []
    event_per_speed_dict = {}

    drugs = get_drug()
    dose = 'Vehicle'
    for drug in drugs:

        experiments, animal_ids = get_animal_id(drug, dose)

        for experiment in experiments:
            print(experiment)

            calcium_ctrl, calcium_amph, neuron, time_ctrl, time_amph = get_calcium_data(drug, dose, experiment)
            eventcount_ctrl, eventcount_amph = binarize_calcium(drug, dose, experiment)

            feature_count, feature_names, features_ctrl, features_amph = mars_features(drug, dose, experiment)

            bin1_events_ctrl, bin2_events_ctrl, bin3_events_ctrl, bin4_events_ctrl, bin5_events_ctrl, bin6_events_ctrl = (
                [] for i in range(6))
            bin1_events_amph, bin2_events_amph, bin3_events_amph, bin4_events_amph, bin5_events_amph, bin6_events_amph = (
                [] for i in range(6))
            bin1_duration_ctrl, bin2_duration_ctrl, bin3_duration_ctrl, bin4_duration_ctrl, bin5_duration_ctrl, bin6_duration_ctrl = (
                0 for i in range(6))
            bin1_duration_amph, bin2_duration_amph, bin3_duration_amph, bin4_duration_amph, bin5_duration_amph, bin6_duration_amph = (
                0 for i in range(6))

            for ft in range(0, feature_count):
                if feature_names[ft] == 'speed':
                    for t in range(0, len(features_ctrl)):
                        if features_ctrl[t, ft] < 0.5:
                            bin1_events_ctrl.append(eventcount_ctrl[t])
                            bin1_duration_ctrl += 1
                        if 0.5 < features_ctrl[t, ft] < 1:
                            bin2_events_ctrl.append(eventcount_ctrl[t])
                            bin2_duration_ctrl += 1
                        if 1 < features_ctrl[t, ft] < 2:
                            bin3_events_ctrl.append(eventcount_ctrl[t])
                            bin3_duration_ctrl += 1
                        if 2 < features_ctrl[t, ft] < 4:
                            bin4_events_ctrl.append(eventcount_ctrl[t])
                            bin4_duration_ctrl += 1
                        if 4 < features_ctrl[t, ft] < 8:
                            bin5_events_ctrl.append(eventcount_ctrl[t])
                            bin5_duration_ctrl += 1
                        if 8 < features_ctrl[t, ft] < 14:
                            bin6_events_ctrl.append(eventcount_ctrl[t])
                            bin6_duration_ctrl += 1

                    event_per_speed_ctrl = [(np.sum(bin1_events_ctrl)/bin1_duration_ctrl)*300,
                                            (np.sum(bin2_events_ctrl)/bin2_duration_ctrl)*300,
                                            (np.sum(bin3_events_ctrl)/bin3_duration_ctrl)*300,
                                            (np.sum(bin4_events_ctrl)/bin4_duration_ctrl)*300,
                                            (np.sum(bin5_events_ctrl)/bin5_duration_ctrl)*300,
                                            (np.sum(bin6_events_ctrl)/bin6_duration_ctrl)*300]

                    for t in range(0, len(features_amph)):
                        if features_amph[t, ft] < 0.5:
                            bin1_events_amph.append(eventcount_amph[t])
                            bin1_duration_amph += 1
                        if 0.5 < features_amph[t, ft] < 1:
                            bin2_events_amph.append(eventcount_amph[t])
                            bin2_duration_amph += 1
                        if 1 < features_amph[t, ft] < 2:
                            bin3_events_amph.append(eventcount_amph[t])
                            bin3_duration_amph += 1
                        if 2 < features_amph[t, ft] < 4:
                            bin4_events_amph.append(eventcount_amph[t])
                            bin4_duration_amph += 1
                        if 4 < features_amph[t, ft] < 8:
                            bin5_events_amph.append(eventcount_amph[t])
                            bin5_duration_amph += 1
                        if 8 < features_amph[t, ft] < 14:
                            bin6_events_amph.append(eventcount_amph[t])
                            bin6_duration_amph += 1

                    event_per_speed_amph = [(np.sum(bin1_events_amph)/bin1_duration_amph)*300,
                                            (np.sum(bin2_events_amph)/bin2_duration_amph)*300,
                                            (np.sum(bin3_events_amph)/bin3_duration_amph)*300,
                                            (np.sum(bin4_events_amph)/bin4_duration_amph)*300,
                                            (np.sum(bin5_events_amph)/bin5_duration_amph)*300,
                                            (np.sum(bin6_events_amph)/bin6_duration_amph)*300]

            event_per_speed_concat = np.concatenate((event_per_speed_ctrl, event_per_speed_amph), axis=0)
            event_per_speed.append(event_per_speed_concat)
            event_per_speed_dict[experiment] = event_per_speed_concat

            print(event_per_speed_concat)

    return event_per_speed_dict
