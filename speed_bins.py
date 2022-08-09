# y-axis: Ca event rate (event/min)
# x-axis: Locomotor speed bin (cm/s)
# bin: <0.5, 0.5-1, 1-2, 2-4, 4-8, 8-14

from mars import *
from calcium import *
from test import *

def event_per_speed():
    event_per_speed = []
    event_per_speed_dict = {}

    # drugs = get_drug()
    drugs = ['SCH23390']
    dose = 'Vehicle'
    for drug in drugs:

        animal_ids = get_animal_id(drug, dose)

        for animal_id in animal_ids:
            print(animal_id)

            speed_ctrl, speed_amph, eventmean_ctrl, eventmean_amph, neuron = get_new_calcium_data(drug, dose, animal_id)

            bin1_events_ctrl, bin2_events_ctrl, bin3_events_ctrl, bin4_events_ctrl, bin5_events_ctrl, bin6_events_ctrl = (
                [] for i in range(6))
            bin1_events_amph, bin2_events_amph, bin3_events_amph, bin4_events_amph, bin5_events_amph, bin6_events_amph = (
                [] for i in range(6))
            bin1_duration_ctrl, bin2_duration_ctrl, bin3_duration_ctrl, bin4_duration_ctrl, bin5_duration_ctrl, bin6_duration_ctrl = (
                0 for i in range(6))
            bin1_duration_amph, bin2_duration_amph, bin3_duration_amph, bin4_duration_amph, bin5_duration_amph, bin6_duration_amph = (
                0 for i in range(6))

            for t in range(0, len(speed_ctrl)):
                if speed_ctrl[t] < 0.5:
                    bin1_events_ctrl.append(eventmean_ctrl[t])
                    bin1_duration_ctrl += 1
                if 0.5 < speed_ctrl[t] < 1:
                    bin2_events_ctrl.append(eventmean_ctrl[t])
                    bin2_duration_ctrl += 1
                if 1 < speed_ctrl[t] < 2:
                    bin3_events_ctrl.append(eventmean_ctrl[t])
                    bin3_duration_ctrl += 1
                if 2 < speed_ctrl[t] < 4:
                    bin4_events_ctrl.append(eventmean_ctrl[t])
                    bin4_duration_ctrl += 1
                if 4 < speed_ctrl[t] < 8:
                    bin5_events_ctrl.append(eventmean_ctrl[t])
                    bin5_duration_ctrl += 1
                if 8 < speed_ctrl[t] < 14:
                    bin6_events_ctrl.append(eventmean_ctrl[t])
                    bin6_duration_ctrl += 1

            event_per_speed_ctrl = [(np.sum(bin1_events_ctrl)/bin1_duration_ctrl)*300,
                                    (np.sum(bin2_events_ctrl)/bin2_duration_ctrl)*300,
                                    (np.sum(bin3_events_ctrl)/bin3_duration_ctrl)*300,
                                    (np.sum(bin4_events_ctrl)/bin4_duration_ctrl)*300,
                                    (np.sum(bin5_events_ctrl)/bin5_duration_ctrl)*300,
                                    (np.sum(bin6_events_ctrl)/bin6_duration_ctrl)*300]
            # divide by time spent per binned speed or divide by 5hz*60 (300)

            for t in range(0, len(speed_amph)):
                if speed_amph[t] < 0.5:
                    bin1_events_amph.append(eventmean_amph[t])
                    bin1_duration_amph += 1
                if 0.5 < speed_amph[t] < 1:
                    bin2_events_amph.append(eventmean_amph[t])
                    bin2_duration_amph += 1
                if 1 < speed_amph[t] < 2:
                    bin3_events_amph.append(eventmean_amph[t])
                    bin3_duration_amph += 1
                if 2 < speed_amph[t] < 4:
                    bin4_events_amph.append(eventmean_amph[t])
                    bin4_duration_amph += 1
                if 4 < speed_amph[t] < 8:
                    bin5_events_amph.append(eventmean_amph[t])
                    bin5_duration_amph += 1
                if 8 < speed_amph[t] < 14:
                    bin6_events_amph.append(eventmean_amph[t])
                    bin6_duration_amph += 1

            event_per_speed_amph = [(np.sum(bin1_events_amph)/bin1_duration_amph)*300,
                                    (np.sum(bin2_events_amph)/bin2_duration_amph)*300,
                                    (np.sum(bin3_events_amph)/bin3_duration_amph)*300,
                                    (np.sum(bin4_events_amph)/bin4_duration_amph)*300,
                                    (np.sum(bin5_events_amph)/bin5_duration_amph)*300,
                                    (np.sum(bin6_events_amph)/bin6_duration_amph)*300]

            event_per_speed_concat = np.concatenate((event_per_speed_ctrl, event_per_speed_amph), axis=0)
            event_per_speed.append(event_per_speed_concat)
            event_per_speed_dict[animal_id] = event_per_speed_concat

            print(event_per_speed_concat)

    return event_per_speed_dict

