# imports
import numpy as np
# import pandas as pd
import argparse
import json

INPUT_FILE_PATH = 'input'
OUTPUT_FILE_PATH = 'output'
HEIGHT = WIDTH = 6


def format_output(fuels, grid):
    for i, grid in enumerate(grid_list):
        flevels = f'Fuel levels for: {fuels[i]}' if len(fuels[i]) else 'All fuel levels 100'
        print(f'Case {i}: {flevels}')
        for row in grid:
            print(row)

if __name__ == '__main__':
    # parse through the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', type=str, default='sample-input.txt')

    args = parser.parse_args()
    input_file = f'{INPUT_FILE_PATH}/{args.file}'
    
    test_cases = []

    # read the file
    with open(input_file, 'r') as file:
        for line in file.readlines():
            tokens = line.strip().split(' ')

            if tokens[0] == '#' or tokens[0] == '':
                continue
            
            test_cases.append(tokens)

    # process the test cases
    fuels = []
    grid_list = []

    for i, test_case in enumerate(test_cases):
        # create the grid
        fuels.append(test_case[1:])

        print(test_case[0])

        # create the grid
        grid = [[test_case[0][i+(j*WIDTH)] for i in range(WIDTH)] for j in range(HEIGHT)]
        grid_list.append(grid)


    format_output(fuels, grid_list)
    print(fuels)
