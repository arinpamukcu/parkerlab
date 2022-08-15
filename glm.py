
def perform_glm():
    timeSplit = 1500

    feature_train = all_move_bouts[timeSplit:]
    feature_test = all_move_bouts[:timeSplit]

    # fit GLM to single cell raw
    events_train = sm.add_constant(peaktime_ctrl[:, timeSplit:].T, prepend=False)
    events_test = sm.add_constant(peaktime_ctrl[:, :timeSplit].T, prepend=False)

    # # fit GLM to single cell spike
    # spike_train = sm.add_constant(peaktime_ctrl[:,:timeSplit].T, prepend=False)
    # spike_test = sm.add_constant(peaktime_ctrl[:,timeSplit:].T, prepend=False)