import pandas as pd
import numpy as np


def get_dateparse(date_str):
    # return pd.to_datetime(int(x), unit='ms')
    # return pd.to_datetime()
    return lambda time_str: pd.to_datetime(f'{date_str} {time_str}', format='%Y-%m-%d %H:%M:%S.%f')


def parse_and_export(date_str, input_filename, output_filename_prefix):
    dateparse = get_dateparse(date_str)
    data = pd.read_csv(input_filename, parse_dates=[15], date_parser=dateparse, comment='%', header=None, sep=',+\s+', engine='python', skipfooter=1)
    condition_name_count = {}
    current_condition_name = data[0][0]
    previous_i = 0

    for i in range(len(data[0])):
        if data[0][i] not in condition_name_count:
            condition_name_count[data[0][i]] = 0

        if current_condition_name != data[0][i]:
            print(i, current_condition_name, condition_name_count[current_condition_name], (i - previous_i) , (i - previous_i) / 250)
            output_filename = f"{output_filename_prefix}_{current_condition_name}_{condition_name_count[current_condition_name]}"
            np.save(output_filename, data.iloc[previous_i:i - 1])
            print(output_filename)

            previous_i = i
            current_condition_name = data[0][i]
            condition_name_count[current_condition_name] += 1


def read(filename):
    data = np.load(filename)
    print(data[0])
    return data

