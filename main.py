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

        # print(test_case[0])

        # create the grid
        grid = [[test_case[0][i+(j*WIDTH)] for i in range(WIDTH)] for j in range(HEIGHT)]
        grid_list.append(grid)

    # format_grid(fuels, grid_list)
    # print(fuels)


    # Greedy Best-First Search
    # - Add nodes to open list sorted with ascending h(n)
    # - Choose next node with the best h(n)
    
    has_fuel_limitations = len(test_cases[0]) > 1
    print("Fuel limitations!" if has_fuel_limitations else "No fuel limitations")
    
    # prev_car = ''
    # for current_car in test_cases[0][0]:
    #     # Determine next moves
    #     print(current_car)

    #     # Moveable in 
    #     if prev_car == current_car:
    #         print("Check right moves")
    #     else:
    #         prev_car = current_car
        
        
    # Greedy Best-First Search
    # - Add nodes to open list sorted with ascending h(n)
    # - Choose next node with the best h(n)

    puzzle = test_cases[0][0]
    print(puzzle)

    def quick_puzzle():
        for i in range(6, 36, 6):
            print(puzzle[i-6:i])

    # Heuristic 1: Number of blocking vehicles
    def h1(puzzle):
        # Count blocking cars in front of ambulance
        blocking_count = 0
        prev_vehicle = ''
        ambulance_passed = False

        # Define and search third row 
        end_row = int(WIDTH * HEIGHT/2)
        start_row = int(end_row - WIDTH)
        for i in range(start_row, end_row):
            car = puzzle[i]
            if car == 'A':
                ambulance_passed = True
            # Count blocking car if ambulance passed, car is present, and car not already counted
            elif ambulance_passed and car != '.' and car != prev_vehicle:
                blocking_count += 1
                prev_vehicle = car
        
        return blocking_count
    
    # Heuristic 2: Number of blocked positions
    def h2(puzzle):
        # Count blocking cars in front of ambulance
        blocking_pos = 0
        ambulance_passed = False

        # Define and search third row 
        end_row = int(WIDTH * HEIGHT/2)
        start_row = int(end_row - WIDTH)
        for i in range(start_row, end_row):
            car = puzzle[i]
            if car == 'A':
                ambulance_passed = True
            # Count blocking positions if ambulance passed and car is present
            elif ambulance_passed and car != '.':
                blocking_pos += 1
        
        return blocking_pos

    # Heuristic 3: Multiplied h1 with lambda
    LAMBDA = 2.5
    def h3(puzzle):
        return h1(puzzle) * LAMBDA

    # Heuristic 4: Number of blocking vehicles plus minimum number of own blocking vehicles
    # - Estimate minimum number of moves to unblock the block vehicles and clear out the solution path by calculating minimum number of vehicles blocking the blocking vehicles
    def h4(puzzle):
        # Count blocking cars in front of ambulance
        blocking_count = 0
    
        prev_vehicle = ''
        prev_block_up, prev_block_down = 0, 0
        min_unblock_count = 0
        ambulance_passed = False

        # Define and search third row 
        start_third_ind = int(WIDTH * HEIGHT/2 - WIDTH)
        for i in range(0, WIDTH):
            car = puzzle[start_third_ind + i]
            if car == 'A':
                ambulance_passed = True
            # Count blocking car if ambulance passed and car is present
            elif ambulance_passed and car != '.':
                if prev_vehicle != car:
                    blocking_count += 1
                
                # Search vertically for blocking cars 
                # TODO: Check orientation of car and only add blocking if vertically oriented
                prev_vehicle = car
                j = start_third_ind + i
                while j - WIDTH > 0:
                    j -= WIDTH
                    up_car = puzzle[j]
                    if up_car != prev_vehicle:
                        prev_block_up += 1
                        prev_vehicle = up_car
                
                prev_vehicle = car
                j = start_third_ind + i
                while j + WIDTH < WIDTH*HEIGHT:
                    j += WIDTH
                    down_car = puzzle[j]
                    if down_car != prev_vehicle:
                        prev_block_down += 1
                        prev_vehicle = down_car
                
                blocking_count += min(prev_block_up, prev_block_down)
                prev_vehicle = car
                prev_block_down = prev_block_up = 0


        return blocking_count

    # Only move in X or Y
    # Slide into free position
    # Move vehicle has same cost in all directions, irrespective of distance moved
    # A A respresents the ambulance
    # Each vehicle has fuel, number of positions it can move
    # Reaching 3f will take the vehicle out of the board (goal: AA reach 3f)

    # From start position, determine next moves



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

