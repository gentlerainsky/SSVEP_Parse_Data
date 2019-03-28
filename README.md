# Parse Data for SSVEP

## Instruction

- `pipenv install`
- `pipenv shell`
- add data files (eg. Egg1_OpenBCI-RAW-2019-03-22_17-44-27.txt) in `./four_choice_ssvep/input/`
- change any config in `main.py` eg. `filenames`, `names` and `dates`
- run with `python main.py`
- output will be stored in `./four_choice_ssvep/output/{names}/`
- `data.npy` is the main data file.
- `resting.npy` contains data in resting condition

## Data Description

Data is formatted into 5 dimensional array 

Each dimension represents
- trials - 1 for each trails
- condition - ['noWords', 'wordsAtten', 'wordsNoAtten']
- direction - ['top', 'right', 'down', 'left']
- data point - 250Hz * 10sec = 2500 points
- features - 16 features

current dimension is `(4, 3, 4, 2500, 16)`
- 4 trials
- 3 conditions
- 4 directions
- 2500 rows
- 16 features 

### For example

`d[0][1][10]` - will be the 10th row of trial #0 with condition 'wordsAtten'.

## Note:

Missing Data, for example if direction 'top' is missing from condition 'noWords', all data point will be set as 0.
