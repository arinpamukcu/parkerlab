# Created by Arin Pamukcu, PhD on August 2022 in Chicago, IL

import statsmodels.api as sm

# Use the shifted_frames  to concatenate feature values with shifted feature values according to defined frame number.
# Currently set up for future shifts "feature future" --can also change it to past shifts "feature history"
#
# featureData: data you want to use for this function.
# featureList: add this if you want to specify a list of indexes for the features to use for this function.
# frameShift: number of frames to be shifted

def shifted_frames(feature_data, feature_list, spike_shift, frame_shift):

    if feature_list is None:
        featureData_shifted = feature_data[spike_shift:-frame_shift, :]
        # print(featureData_shifted.shape)
        for i in range(0, frame_shift - 1):
            shifted = feature_data[spike_shift + i:-(frame_shift - i), :]
            featureData_shifted = np.concatenate((featureData_shifted, shifted), axis=1)

    else:
        featureData_shifted = feature_data[spike_shift:-frame_shift, feature_list]
        # print(featureData_shifted.shape)
        for i in range(0, frame_shift - 1):
            shifted = feature_data[spike_shift + i:-(frame_shift - i), feature_list]
            featureData_shifted = np.concatenate((featureData_shifted, shifted), axis=1)

    print(featureData_shifted.shape)

    return featureData_shifted


# def perform_glm(eventrate):
#     timeSplit = 1500
#
#     feature_train = all_move_bouts[timeSplit:]
#     feature_test = all_move_bouts[:timeSplit]
#
#     # fit GLM to single cell raw
#     events_train = sm.add_constant(eventrate[:, timeSplit:].T, prepend=False)
#     events_test = sm.add_constant(eventrate[:, :timeSplit].T, prepend=False)
#
#     # fit GLM to single cell spike
#     spike_train = sm.add_constant(peaktime_ctrl[:,:timeSplit].T, prepend=False)
#     spike_test = sm.add_constant(peaktime_ctrl[:,timeSplit:].T, prepend=False)