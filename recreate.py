# y-axis: Ca event rate (event/min)
# x-axis: Locomotor speed bin (cm/s)
# bin: <0.5, 0.5-1, 1-2, 2-4, 4-8, 8-14

from mars import *
# from calcium import *
from calcium_jp import *
from test import *
from time import sleep
from progressbar import progressbar

# for i in progressbar(range(100), redirect_stdout=True):
#     sleep(0.1)

def event_vs_speed():
    event_per_speed = []
    event_per_speed_dict = {}

    # drugs = get_drug()
    drugs = ['SCH23390']
    dose = 'Vehicle'
    for drug in drugs:

        animal_ids = get_animal_id(drug, dose)

        for animal_id in animal_ids:
            print(animal_id)

            # calcium_ctrl, calcium_amph, neuron, time_ctrl, time_amph = get_calcium_data(drug, dose, animal_id)
            # eventcount_ctrl, eventcount_amph = binarize_calcium(drug, dose, animal_id)

            eventcount_ctrl, eventcount_amph, neuron = get_calcium_data_jp(drug, dose, animal_id)
            feature_count, feature_names, features_ctrl, features_amph = mars_features(drug, dose, animal_id)

            bin01_events_ctrl = [];
            bin02_events_ctrl = [];
            bin03_events_ctrl = [];
            bin04_events_ctrl = [];
            bin05_events_ctrl = [];
            bin06_events_ctrl = [];
            bin01_events_amph = [];
            bin02_events_amph = [];
            bin03_events_amph = [];
            bin04_events_amph = [];
            bin05_events_amph = [];
            bin06_events_amph = [];
            bin01_duration_ctrl = 0;
            bin02_duration_ctrl = 0;
            bin03_duration_ctrl = 0;
            bin04_duration_ctrl = 0;
            bin05_duration_ctrl = 0;
            bin06_duration_ctrl = 0;
            bin01_duration_amph = 0;
            bin02_duration_amph = 0;
            bin03_duration_amph = 0;
            bin04_duration_amph = 0;
            bin05_duration_amph = 0;
            bin06_duration_amph = 0;

            for ft in range(0, feature_count):
                if feature_names[ft] == 'speed':
                    for t in range(0, len(features_ctrl)):
                        if features_ctrl[t, ft] < 0.5:
                            bin01_events_ctrl.append(eventcount_ctrl[t])
                            bin01_duration_ctrl += 1
                        if 0.5 < features_ctrl[t, ft] < 1:
                            bin02_events_ctrl.append(eventcount_ctrl[t])
                            bin02_duration_ctrl += 1
                        if 1 < features_ctrl[t, ft] < 2:
                            bin03_events_ctrl.append(eventcount_ctrl[t])
                            bin03_duration_ctrl += 1
                        if 2 < features_ctrl[t, ft] < 4:
                            bin04_events_ctrl.append(eventcount_ctrl[t])
                            bin04_duration_ctrl += 1
                        if 4 < features_ctrl[t, ft] < 8:
                            bin05_events_ctrl.append(eventcount_ctrl[t])
                            bin05_duration_ctrl += 1
                        if 8 < features_ctrl[t, ft] < 14:
                            bin06_events_ctrl.append(eventcount_ctrl[t])
                            bin06_duration_ctrl += 1

                    event_per_speed_ctrl = [(np.sum(bin01_events_ctrl)/bin01_duration_ctrl)*300,
                                            (np.sum(bin02_events_ctrl)/bin02_duration_ctrl)*300,
                                            (np.sum(bin03_events_ctrl)/bin03_duration_ctrl)*300,
                                            (np.sum(bin04_events_ctrl)/bin04_duration_ctrl)*300,
                                            (np.sum(bin05_events_ctrl)/bin05_duration_ctrl)*300,
                                            (np.sum(bin06_events_ctrl)/bin06_duration_ctrl)*300]
                    # print(event_per_speed_ctrl)
                    # divide by time spent per binned speed or divide by 5hz*60 (300)

                    for t in range(0, len(features_amph)):
                        if features_amph[t, ft] < 0.5:
                            bin01_events_amph.append(eventcount_amph[t])
                            bin01_duration_amph += 1
                        if 0.5 < features_amph[t, ft] < 1:
                            bin02_events_amph.append(eventcount_amph[t])
                            bin02_duration_amph += 1
                        if 1 < features_amph[t, ft] < 2:
                            bin03_events_amph.append(eventcount_amph[t])
                            bin03_duration_amph += 1
                        if 2 < features_amph[t, ft] < 4:
                            bin04_events_amph.append(eventcount_amph[t])
                            bin04_duration_amph += 1
                        if 4 < features_amph[t, ft] < 8:
                            bin05_events_amph.append(eventcount_amph[t])
                            bin05_duration_amph += 1
                        if 8 < features_amph[t, ft] < 14:
                            bin06_events_amph.append(eventcount_amph[t])
                            bin06_duration_amph += 1

                    event_per_speed_amph = [(np.sum(bin01_events_amph)/bin01_duration_amph)*300,
                                            (np.sum(bin02_events_amph)/bin02_duration_amph)*300,
                                            (np.sum(bin03_events_amph)/bin03_duration_amph)*300,
                                            (np.sum(bin04_events_amph)/bin04_duration_amph)*300,
                                            (np.sum(bin05_events_amph)/bin05_duration_amph)*300,
                                            (np.sum(bin06_events_amph)/bin06_duration_amph)*300]

            event_per_speed_concat = np.concatenate((event_per_speed_ctrl, event_per_speed_amph), axis=0)
            event_per_speed.append(event_per_speed_concat)
            event_per_speed_dict[animal_id] = event_per_speed_concat

            print(event_per_speed_concat)

    return event_per_speed_dict
