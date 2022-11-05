# imports
import numpy as np
# import pandas as pd
import argparse
import json

INPUT_FILE_PATH = 'input'
SOLUTIONS_PATH = 'output/solutions'
SEARCH_PATH = 'output/search'

HEIGHT = WIDTH = 6


def format_solution(initial_board, runtime, search_path, solution_path_length, solution_path, method, id):
    board = ' '.join(initial_board)
    output_file = f'{SOLUTIONS_PATH}/{method}-sol-{id}.txt'
    with open(output_file, 'w') as file:
        file.write(f'Initial board oncfiguration: {board}')
    return

def format_grid(fuels, grid):
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

    format_grid(fuels, grid_list)
    print(fuels)

    # output TODO
    # For each grid:
    #   For each search algorithm (UCS, GBFS, A*):
        # output to two paths: the solution and the search
        # for GBFS and A*: have each heuristic in a separate file
    
    # solution output file:
        #Initial board
        # board format

        # lsit of fuel levels

        # runtime
        # search path length
        #solution path moves
        # solution path
        # solution path breakdown, ex: A down 1 new_fuel_lvl  updated_grid car_fuel_lvl

        # final fuel levels
        # final board

    # search output file:
        # f(n) = ? g(n) = ? h(n) = ?, state = new board state

