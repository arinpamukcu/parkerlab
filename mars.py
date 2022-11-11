# Created by Arin Pamukcu, PhD on August 2022

import os
import numpy as np
import annotation_parsers
import pdb

# path
behavior_dir = 'R:\Basic_Sciences\Phys\Kennedylab\Parkerlab\Behavior' #pc
# behavior_dir = '/Volumes/fsmresfiles/Basic_Sciences/Phys/Kennedylab/Parkerlab/Behavior' #mac

def get_mars_dirs(drug, dose, experiment):

    experiment_amph = experiment + '_amph'

    mars_output_ctrl = 'Control/output_v1_8'
    mars_output_amph = 'Amph/output_v1_8'
    #
    # mars_ctrl_file = experiment + '_custom_feat_top_v1_8.npz'
    # mars_amph_file = experiment + '_amph_custom_feat_top_v1_8.npz'
    #
    # mars_ctrl_dir = os.path.join(behavior_dir, drug, dose, mars_ctrl_output, experiment, mars_ctrl_file)
    # mars_amph_dir = os.path.join(behavior_dir, drug, dose, mars_amph_output, experiment_amph, mars_amph_file)

    mars_dir_ctrl = os.path.join(behavior_dir, drug, dose, mars_output_ctrl, experiment)
    mars_dir_amph = os.path.join(behavior_dir, drug, dose, mars_output_amph, experiment_amph)

    return mars_dir_ctrl, mars_dir_amph


def get_mars_data(drug, dose, experiment):

    mars_dir_ctrl, mars_dir_amph = get_mars_dirs(drug, dose, experiment)

    mars_ctrl_feat = experiment + '_custom_feat_top_v1_8.npz'
    mars_amph_feat = experiment + '_amph_custom_feat_top_v1_8.npz'

    mars_ctrl_file = os.path.join(mars_dir_ctrl, mars_ctrl_feat)
    mars_amph_file = os.path.join(mars_dir_amph, mars_amph_feat)

    mars_ctrl = np.load(mars_ctrl_file)
    mars_amph = np.load(mars_amph_file)

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


def get_mars_features(drug, dose, experiment):

    feature_count, feature_names, features_ctrl, features_amph = get_mars_data(drug, dose, experiment)

    for ft in range(0, feature_count):
        # if feature_names[ft] == 'm0_top_speed':
        #     mars_speed_ctrl = features_ctrl[:, ft]
        #     mars_speed_amph = features_amph[:, ft]
        #
        # if feature_names[ft] == 'm0_top_acceleration_head':
        #     mars_acc_ctrl = features_ctrl[:, ft]
        #     mars_acc_amph = features_amph[:, ft]
        #
        # if feature_names[ft] == 'top_m0_angle_to_center':
        #     mars_angle_center_ctrl = features_ctrl[:, ft]
        #     mars_angle_center_amph = features_amph[:, ft]

        if feature_names[ft] == 'top_m0_angle_nose_neck_tail':
            mars_angle_nnt_ctrl = np.sin(features_ctrl[:, ft]) * 180
            mars_angle_nnt_amph = np.sin(features_amph[:, ft]) * 180

    return mars_angle_nnt_ctrl, mars_angle_nnt_amph


def get_classifiers(drug, dose, experiment, behavior):

    mars_dir_ctrl, mars_dir_amph = get_mars_dirs(drug, dose, experiment)

    annot_file_ctrl = experiment + '_top_actions_pred_v1_8.annot'
    annot_file_amph = experiment + '_amph_top_actions_pred_v1_8.annot'

    annot_dir_ctrl = os.path.join(mars_dir_ctrl, annot_file_ctrl)
    annot_dir_amph = os.path.join(mars_dir_amph, annot_file_amph)

    annot_dict_ctrl = annotation_parsers.parse_annot(annot_dir_ctrl)
    annot_dict_amph = annotation_parsers.parse_annot(annot_dir_amph)

    beh_bouts_ctrl = np.zeros((annot_dict_ctrl['behs_bout']['predicted_behaviors']['other'][0][1]))
    if behavior in annot_dict_ctrl['behs_bout']['predicted_behaviors'].keys():
        for bout in range(0, len(annot_dict_ctrl['behs_bout']['predicted_behaviors'][behavior])):
            startframe = annot_dict_ctrl['behs_bout']['predicted_behaviors'][behavior][bout][0]
            endframe = annot_dict_ctrl['behs_bout']['predicted_behaviors'][behavior][bout][1]
            beh_bouts_ctrl[startframe:endframe + 1] = 1

    beh_bouts_ctrl_ = np.nan_to_num(beh_bouts_ctrl[12000:30000])
    behavior_ctrl = beh_bouts_ctrl_[::4]

    beh_bout_amph = np.zeros((annot_dict_amph['behs_bout']['predicted_behaviors']['other'][0][1]))
    if behavior in annot_dict_amph['behs_bout']['predicted_behaviors'].keys():
        for bout in range(0, len(annot_dict_amph['behs_bout']['predicted_behaviors'][behavior])):
            startframe = annot_dict_amph['behs_bout']['predicted_behaviors'][behavior][bout][0]
            endframe = annot_dict_amph['behs_bout']['predicted_behaviors'][behavior][bout][1]
            beh_bout_amph[startframe:endframe + 1] = 1

    beh_bouts_amph_ = np.nan_to_num(beh_bout_amph[12000:66000])
    behavior_amph = beh_bouts_amph_[::4]

    return behavior_ctrl, behavior_amph


# def mars_feature(drug, dose, experiment):
#
#     feature_count, feature_names, features_ctrl, features_amph = mars_data(drug, dose, experiment)
#
#     for ft in range(0, feature_count):
#         if feature_names[ft] == 'speed':
#             mars_speed_ctrl = features_ctrl[:, ft]
#             mars_speed_amph = features_amph[:, ft]
#
#         elif feature_names[ft] == 'angle_head_body_l':
#             mars_left_angle_ctrl = (features_ctrl[:, ft]+math.pi) * 180/math.pi #convert from radians to degrees
#             mars_left_angle_amph = (features_amph[:, ft]+math.pi) * 180/math.pi
#
#         elif feature_names[ft] == 'angle_head_body_r':
#             mars_right_angle_ctrl = features_ctrl[:, ft] * 180/math.pi
#             mars_right_angle_amph = features_amph[:, ft] * 180/math.pi
#
#     return mars_speed_ctrl, mars_speed_amph, \
#            mars_left_angle_ctrl, mars_left_angle_amph, \
#            mars_right_angle_ctrl, mars_right_angle_amph