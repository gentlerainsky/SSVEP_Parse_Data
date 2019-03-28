from parser import parse_and_export, read_sample, read_resting_sample
import numpy as np
import sys
import os


np.set_printoptions(threshold=sys.maxsize)

names = [
    'Egg1',
    'Max1',
    'Top1'
]

filenames = [
    'Egg1_OpenBCI-RAW-2019-03-22_17-44-27.txt',
    'Max1_OpenBCI-RAW-2019-03-21_15-31-30.txt',
    'Top1_OpenBCI-RAW-2019-03-21_17-21-49.txt'
]

dates = [
    '2019-03-22',
    '2019-03-21',
    '2019-03-21'
]

get_input_filename = lambda index: f'./four_choice_ssvep/input/{filenames[index]}'
get_output_folder = lambda index: f'./four_choice_ssvep/output/{names[index]}'
get_output_filename_prefix = lambda folder_path, index: f'{folder_path}/'


for i in range(len(names)):
    output_folder = get_output_folder(i)
    os.makedirs(output_folder, exist_ok=True)
    parse_and_export(dates[i], get_input_filename(i), get_output_filename_prefix(output_folder, i))

a = read_sample('./four_choice_ssvep/output/Max1/data.npy')
a = read_resting_sample('./four_choice_ssvep/output/Max1/resting.npy')
# print(a[0])
