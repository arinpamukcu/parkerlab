# Created by Arin Pamukcu, PhD on August 2022

from data import *
# from mars import *
# from calcium import *

def get_speed_neurons(drug, dose, experiment):
    speed_ctrl, speed_amph, calcium_ctrl_events, calcium_amph_events, \
    eventmean_ctrl, eventmean_amph, neuron_count, time_ctrl, time_amph = get_data(drug, dose, experiment)

    speed_neurons = []
    for neuron in range(0, neuron_count):
        event_time = []
        for frame in range(0, time_ctrl):
            if calcium_ctrl_events[neuron, frame] == 1:
                event_time.append(frame)
        # look for those neurons that have events (event_time is not just 0)
        # if average of speed at the current frame up until 5 frames later is more than 0.5 cm/s
        if len(event_time) != 0 and all(np.mean(speed_ctrl[time:time + 5]) >= 0.5 for time in event_time) is True:
            speed_neurons.append(calcium_ctrl_events[neuron, :])

    speed_neurons = np.array(speed_neurons)

    return speed_neurons

# if you use our old data format:
# def speed_neurons(drug, dose, experiment):
#     calcium_ctrl, calcium_amph, neuron, time_ctrl, time_amph = get_calcium_data(drug, dose, experiment)
#     events_ctrl, events_amph = binarize_calcium(drug, dose, animal_id)
#     feature_count, feature_names, features_ctrl, features_amph = mars_features(drug, dose, experiment)
#
#     for ft in range(0, feature_count):
#         if feature_names[ft] == 'speed':
#             mars_speed_ctrl = features_ctrl[ft]
#             mars_speed_amph = features_amph[ft]
#
#     speed_neurons = []
#     for neuron in range(0, neuron):
#         event_time = []
#         for frame in range(0, time_ctrl):
#             if events_ctrl[neuron, frame] == 1:
#                 event_time.append(frame)
#         if all(np.mean(mars_speed_ctrl[time:time + 5]) >= 0.5 for time in event_time) is True:
#             speed_neurons.append(events_ctrl[neuron, :])
#             print(neuron)
#
#     print(len(speed_neurons))