import os
import numpy as np

# upload MARS data
# MARS_ctrl = '/content/' + mouse + '_raw_feat_top_v1_8.npz'
# MARS_amph = '/content/' + mouse + '_amph_raw_feat_top_v1_8.npz'

def get_mars_dir(drug, dose, animal_id):
    behavior_dir = 'R:\Basic_Sciences\Phys\Kennedylab\Parkerlab\Behavior'

    animal_id_amph = animal_id + '_amph'

    mars_ctrl_output = 'Control\output_v1_8'
    mars_amph_output = 'Amph\output_v1_8'

    mars_ctrl_file = animal_id + '_raw_feat_top_v1_8.npz'
    mars_amph_file = animal_id + '_amph_raw_feat_top_v1_8.npz'

    mars_ctrl_dir = os.path.join(behavior_dir, drug, dose, mars_ctrl_output, animal_id, mars_ctrl_file)
    mars_amph_dir = os.path.join(behavior_dir, drug, dose, mars_amph_output, animal_id_amph, mars_amph_file)

    return mars_ctrl_dir, mars_amph_dir


def mars_features(drug, dose, animal_id):

    mars_ctrl_dir, mars_amph_dir = get_mars_dir(drug, dose, animal_id)

    mars_ctrl = np.load(mars_ctrl_dir)
    mars_amph = np.load(mars_amph_dir)

    # define
    feature_names = mars_ctrl['features']
    features_ctrl_all = mars_ctrl['data_smooth'][0]
    features_amph_all = mars_amph['data_smooth'][0]

    # downsample
    features_ctrl_some = np.nan_to_num(features_ctrl_all[12000:30000, :])
    features_amph_some = np.nan_to_num(features_amph_all[12000:66000, :])
    features_ctrl = features_ctrl_some[::4, :]
    features_amph = features_amph_some[::4, :]

    return feature_names, features_ctrl, features_amph
