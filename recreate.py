# y-axis: Ca event rate (event/min)
# x-axis: Locomotor speed bin (cm/s)
# bin: <0.5, 0.5-1, 1-2, 2-4, 4-8, 8-14

from mars import *
from calcium import *
from test import *
from time import sleep
from progressbar import progressbar

def event_vs_speed():

    event_per_speed = []
    event_per_speed_dict = {}

    drugs = get_drug()
    dose = 'Vehicle'
    for drug in drugs:

        animal_ids = get_animal_id(drug, dose)
        for animal_id in animal_ids:
            print(animal_id)
            # for i in progressbar(range(100), redirect_stdout=True):
            #     sleep(0.1)

            feature_names, features_ctrl, features_amph = mars_features(drug, dose, animal_id)
            eventcount_ctrl, eventcount_amph = binarize_calcium(drug, dose, animal_id)

            bin01_ctrl = []
            bin02_ctrl = []
            bin03_ctrl = []
            bin04_ctrl = []
            bin05_ctrl = []
            bin06_ctrl = []
            for t in range(0, len(features_ctrl)):
                if features_ctrl[t, 34] < 0.5:
                    bin01_ctrl.append(eventcount_ctrl[t])
                if 0.5 < features_ctrl[t, 34] < 1:
                    bin02_ctrl.append(eventcount_ctrl[t])
                if 1 < features_ctrl[t, 34] < 2:
                    bin03_ctrl.append(eventcount_ctrl[t])
                if 2 < features_ctrl[t, 34] < 4:
                    bin04_ctrl.append(eventcount_ctrl[t])
                if 4 < features_ctrl[t, 34] < 8:
                    bin05_ctrl.append(eventcount_ctrl[t])
                if 8 < features_ctrl[t, 34] < 14:
                    bin06_ctrl.append(eventcount_ctrl[t])

            event_per_speed_ctrl = [np.mean(bin01_ctrl), np.mean(bin02_ctrl), np.mean(bin03_ctrl), np.mean(bin04_ctrl),
                                    np.mean(bin05_ctrl), np.mean(bin06_ctrl)]
            # print(event_per_speed_ctrl)

            bin01_amph = []
            bin02_amph = []
            bin03_amph = []
            bin04_amph = []
            bin05_amph = []
            bin06_amph = []
            for t in range(0, len(features_amph)):
                if features_amph[t, 34] < 0.5:
                    bin01_amph.append(eventcount_amph[t])
                if 0.5 < features_amph[t, 34] < 1:
                    bin02_amph.append(eventcount_amph[t])
                if 1 < features_amph[t, 34] < 2:
                    bin03_amph.append(eventcount_amph[t])
                if 2 < features_amph[t, 34] < 4:
                    bin04_amph.append(eventcount_amph[t])
                if 4 < features_amph[t, 34] < 8:
                    bin05_amph.append(eventcount_amph[t])
                if 8 < features_amph[t, 34] < 14:
                    bin06_amph.append(eventcount_amph[t])

            event_per_speed_amph = [np.mean(bin01_amph), np.mean(bin02_amph), np.mean(bin03_amph), np.mean(bin04_amph),
                                    np.mean(bin05_amph), np.mean(bin06_amph)]

            event_per_speed_concat = np.concatenate((event_per_speed_ctrl, event_per_speed_amph), axis=0)
            event_per_speed.append(event_per_speed_concat)
            event_per_speed_dict[animal_id] = event_per_speed_concat

            print(event_per_speed_concat)

    return event_per_speed_dict
