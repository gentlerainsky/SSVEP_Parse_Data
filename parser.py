import pandas as pd
import numpy as np
from collections import defaultdict

def get_dateparse(date_str):
    # return pd.to_datetime(int(x), unit='ms')
    # return pd.to_datetime()
    return lambda time_str: pd.to_datetime(f'{date_str} {time_str}', format='%Y-%m-%d %H:%M:%S.%f')


condition = [
    'noWords',
    'wordsAtten',
    'wordsNoAtten',
]

direction = [
    'up',
    'right',
    'down',
    'left'
]

NUM_TRIALS = 4
SAMPLING_FREQUENCY = 250
NUM_SEC = 10
RESTING_NUM_SEC = 20
NUM_FEATURE = 16
DATE_COLUMN_INDEX = 15
TOTAL_POINTS = SAMPLING_FREQUENCY * NUM_SEC


def equal(x, y):
    if x == y:
        return True
    elif type(x) == float and type(y) == float:
        if np.isnan(x) and np.isnan(y):
            return True
        else:
            return x == y
    else:
        return False


def parse_and_export(date_str, input_filename, output_filename_prefix):
    print('loading', input_filename)
    dateparse = get_dateparse(date_str)
    data = pd.read_csv(
        input_filename,
        parse_dates=[DATE_COLUMN_INDEX],
        date_parser=dateparse,
        comment='%',
        header=None,
        sep=',+\s+',
        engine='python',
        skipfooter=1
    )
    condition_name_count = defaultdict()
    output = defaultdict()
    direction_count = {}
    current_condition_name = data[0][0]
    previous_i = 0
    rest_time_array = []
    current_direction = data[1][0]

    for i in range(1, len(data[0])):
        if i % 10000 == 0:
            print('parsing progress', '%.2f %%' % (i / len(data[0]) * 100))
        if data[0][i] not in condition_name_count:
            condition_name_count[data[0][i]] = 0
            # current_direction = None
        if current_condition_name != data[0][i] or (not equal(current_direction, data[1][i])):
            if current_condition_name not in output:
                output[current_condition_name] = defaultdict()
            subdata = data.iloc[previous_i:i - 1]
            num = subdata.shape[0] // SAMPLING_FREQUENCY
            if current_condition_name == 'restTime':
                num = min(20, num)
            else:
                num = min(10, num)
            excess = subdata.shape[0] - SAMPLING_FREQUENCY * num
            subdata = subdata.iloc[excess:, :NUM_FEATURE]
            # current_direction = subdata.iloc[0, 1]
            if current_condition_name not in direction_count:
                direction_count[current_condition_name] = {}
            if current_direction not in direction_count[current_condition_name]:
                direction_count[current_condition_name][current_direction] = 0
            if current_condition_name == 'restTime':
                rest_time_array.append(subdata.copy())
            else:
                if current_direction not in output[current_condition_name]:
                    output[current_condition_name][current_direction] = {}
                output[current_condition_name][current_direction][direction_count[current_condition_name][current_direction]] = subdata.copy()
            direction_count[current_condition_name][current_direction] += 1
            previous_i = i
            condition_name_count[current_condition_name] += 1
            current_condition_name = data[0][i]
            current_direction = data[1][i]
    output_array = []

    # trials
    for ii in range(NUM_TRIALS):
        # condition
        for jj in range(len(condition)):
            # direction
            for kk in range(len(direction)):
                if direction[kk] not in output[condition[jj]]:
                    output_array += [np.zeros(shape=(TOTAL_POINTS, NUM_FEATURE))]
                else:
                    if ii in output[condition[jj]][direction[kk]]:
                        shape = output[condition[jj]][direction[kk]][ii].shape
                        if shape[0] != TOTAL_POINTS or shape[1] != NUM_FEATURE:
                            value = output[condition[jj]][direction[kk]][ii].to_numpy().copy()
                            value.resize((TOTAL_POINTS, NUM_FEATURE), refcheck=False)
                            # output_array += [output[condition[jj]][direction[kk]][ii]]
                            output_array += [value]
                        else:
                            output_array += [output[condition[jj]][direction[kk]][ii]]
                    else:
                        output_array += [np.zeros(shape=(TOTAL_POINTS, NUM_FEATURE))]
    print('saving', input_filename)
    output_np_array = np.concatenate(output_array, axis=0)
    real_output = output_np_array.reshape((NUM_TRIALS, len(condition), len(direction), TOTAL_POINTS, NUM_FEATURE))
    np.save(output_filename_prefix + 'data', real_output)
    print('save', output_filename_prefix + 'data')
    rest_time = np.concatenate(rest_time_array)
    rest_time_copy = rest_time.copy()
    rest_time_copy.resize((len(rest_time_array), SAMPLING_FREQUENCY * RESTING_NUM_SEC, NUM_FEATURE))
    np.save(output_filename_prefix + 'resting', rest_time_copy)
    print('save', output_filename_prefix + 'resting')
    return real_output


def read_sample(filename):
    data = np.load(filename)
    # trials
    for ii in range(NUM_TRIALS):
        # condition
        print('>>>>>>>>>>>>>>>>>>>>>>>>>ii', ii)
        for jj in range(len(condition)):
            # direction
            print('**********jj', jj)
            for kk in range(len(direction)):
                print('kk', kk)
                print(data[ii][jj][kk][-2:])
    return data


def read_resting_sample(filename):
    data1 = np.load(filename)
    # trials
    for ii in range(NUM_TRIALS):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>iiii', ii)
        print(data1[ii][0:3])
    return data1
