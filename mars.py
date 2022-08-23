# Created by Arin Pamukcu, PhD on August 2022

import os
import math
import numpy as np
import pdb

# path for pc
behavior_dir = 'R:\Basic_Sciences\Phys\Kennedylab\Parkerlab\Behavior'

# # path for mac
# behavior_dir = '/Volumes/fsmresfiles/Basic_Sciences/Phys/Kennedylab/Parkerlab/Behavior'

def get_mars_dir(drug, dose, experiment):

    experiment_amph = experiment + '_amph'

    mars_ctrl_output = 'Control\output_v1_8'
    mars_amph_output = 'Amph\output_v1_8'

    mars_ctrl_file = experiment + '_raw_feat_top_v1_8.npz'
    mars_amph_file = experiment + '_amph_raw_feat_top_v1_8.npz'

    mars_ctrl_dir = os.path.join(behavior_dir, drug, dose, mars_ctrl_output, experiment, mars_ctrl_file)
    mars_amph_dir = os.path.join(behavior_dir, drug, dose, mars_amph_output, experiment_amph, mars_amph_file)

    return mars_ctrl_dir, mars_amph_dir


def mars_data(drug, dose, experiment):

    mars_ctrl_dir, mars_amph_dir = get_mars_dir(drug, dose, experiment)

    mars_ctrl = np.load(mars_ctrl_dir)
    mars_amph = np.load(mars_amph_dir)

    # define
    feature_names = mars_ctrl['features']
    feature_count = len(feature_names)
    features_ctrl_all = mars_ctrl['data_smooth'][0]
    features_amph_all = mars_amph['data_smooth'][0]

    # downsample
    features_ctrl_some = np.nan_to_num(features_ctrl_all[12000:30000, :])
    features_amph_some = np.nan_to_num(features_amph_all[12000:66000, :])
    features_ctrl = features_ctrl_some[::4, :]
    features_amph = features_amph_some[::4, :]

    return feature_count, feature_names, features_ctrl, features_amph


def mars_feature(drug, dose, experiment):

    feature_count, feature_names, features_ctrl, features_amph = mars_data(drug, dose, experiment)

    for ft in range(0, feature_count):
        if feature_names[ft] == 'speed':
            mars_speed_ctrl = features_ctrl[:, ft]
            mars_speed_amph = features_amph[:, ft]

        elif feature_names[ft] == 'angle_head_body_l':
            mars_left_angle_ctrl = (features_ctrl[:, ft]+math.pi) * 180/math.pi #convert from radians to degrees
            mars_left_angle_amph = (features_amph[:, ft]+math.pi) * 180/math.pi

        elif feature_names[ft] == 'angle_head_body_r':
            mars_right_angle_ctrl = features_ctrl[:, ft] * 180/math.pi
            mars_right_angle_amph = features_amph[:, ft] * 180/math.pi

    return mars_speed_ctrl, mars_speed_amph, \
           mars_left_angle_ctrl, mars_left_angle_amph, \
           mars_right_angle_ctrl, mars_right_angle_amph