# Created by Arin Pamukcu, PhD on August 2022
# histogras for time spent doing particular action

from data import *
from info import *
from mars import *
import numpy as np
import matplotlib.pyplot as plt

def speed():
    # drugs = ['Clozapine']
    drugs = get_drug()
    dose = 'Vehicle'

    for drug in drugs:

        experiments, D1_folders, D2_folders = get_animal_id(drug, dose)

        for experiment in experiments:
            print(experiment + '_right')

            speed_ctrl, speed_amph, _, _, _, _, \
            eventmean_ctrl, eventmean_amph, neuron, time_ctrl, time_amph = get_data(drug, dose, experiment)

            _, _, _, _, mars_right_angle_ctrl, mars_right_angle_amph = mars_feature(drug, dose, experiment)

            speed_ctrl_frames = []
            for frame in range(0, len(speed_ctrl) - 4):
                if 1 < speed_ctrl[frame] < speed_ctrl[frame + 1] < speed_ctrl[frame + 2] < \
                        speed_ctrl[frame + 3] < speed_ctrl[frame + 4]:
                    speed_ctrl_frames.append(frame)

    return