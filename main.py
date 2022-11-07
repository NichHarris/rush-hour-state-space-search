# imports
import argparse
import os
from Puzzle import Puzzle
from Node import Node
from queue import PriorityQueue
import time

INPUT_FILE_PATH = 'input'
SOLUTIONS_PATH = 'output/solutions'
SEARCH_PATH = 'output/search'
HEIGHT = WIDTH = 6

# def format_solution(initial_board, runtime, search_path, solution_path_length, solution_path, method, id):
def write_solution_file(board, initial_fuel, method, id, final_board):
    output_file = f'{SOLUTIONS_PATH}/{method}-sol-{id}.txt'
    if not os.path.exists(SOLUTIONS_PATH):
        os.makedirs(SOLUTIONS_PATH)

    final_fuel = ', '.join(initial_fuel).replace(':','')
    initial_fuel = ', '.join(initial_fuel)

    with open(output_file, 'w') as file:
        file.write(f'Initial board configuration: {board}\n\n')
        file.writelines(output_file_board(board))
        file.write(f'\nCar fuel available: {initial_fuel}\n\n')
        file.write(f'Runtime: {0}\n') # todo get runtime val
        file.write(f'Search path length: {0}\n') # todo get search path length
        file.write(f'Solution path length: {0}\n') # todo get solution path length
        file.write(f'Solution path: {0}\n\n') # todo get solution path
        file.writelines(format_solution_path('')) # todo pass solution path
        file.write(f'\n\n! {final_fuel}\n\n')
        file.writelines(f'{output_file_board(final_board)}') # todo pass final grid

def write_search_file():
    return

# for outputing to output files
def format_solution_path(solution_path):
    return ''

# for outputing to output file
def output_file_board(board):
    ret = ''

    for i in range(WIDTH, WIDTH*HEIGHT + 1, WIDTH):
        ret += ' '.join(board[i-WIDTH:i]) + '\n'
    return ret

# get a dict of all the cars and their sizes
def get_car_dict(board, fuel_list):
    car_dict = {}
    for i, car in enumerate(board):
        if car == '.':
            continue
        elif car in car_dict:
            size, start, fuel, orientation = car_dict[car]
            car_dict[car] = (size + 1, start, fuel, orientation)
            continue
        car_dict[car] = (1, i, get_fuel(car, fuel_list), get_orientation(car, i, board))
    return car_dict

def get_fuel(car, fuel_list):
    for fuel in fuel_list:
        if car == fuel[0]:
            return int(fuel[1])
    return 100

def get_orientation(car, index, grid):
    orientation = 'v'
    if index % WIDTH == 0 and grid[index + 1] == car:
        orientation = 'h'
    elif index % WIDTH == WIDTH - 1 and grid[index - 1] == car:
        orientation = 'h'
    elif grid[index - 1] == car or grid[index + 1] == car:
        orientation = 'h' 

    return orientation

# for outputing to console
def output_board_console(fuel, grid, case):
    flevels = f'Fuel levels for: {fuel}'
    print(f'Case {case}: {flevels}')
    for i in range(WIDTH, WIDTH*HEIGHT + 1, WIDTH):
        print(' '.join(grid[i-WIDTH:i]))

def uniform_cost_search(goal, start):
    unf_cost = 1 # for up, down, left, right

    # if any car reachers indexes: (.... [2][4], [2][5]) then it is removed from the grid and replaced with '.'
    # goal: when ['A', 'A'] is in position [2][4] and [2][5] then this is the goal state, we have finished 
    # the search and can return the path taken to get to this state, and its cost, and the total search path

    # check if car has fuel remaining
    if car in car_dict:
        size, fuel = car_dict[car]
        if fuel == 0:
            # cant move this car
            ret = false
    return

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

    puzzle_list = []
    # process the test cases into puzzles
    for test_case in test_cases:
        board = test_case[0]
        car_dict = get_car_dict(board, test_case[1:])

        puzzle_list.append(Puzzle(board, test_case, car_dict))

    # solve the puzzles
    for puzzle in puzzle_list:

        # start timer
        start_time = time.time()

        visited = set()
        pqueue = PriorityQueue()
        start = Node(None, 0, puzzle.car_dict, puzzle.board)
        pqueue.put((0, start))

        while not pqueue.empty():
            cost, node = pqueue.get(block=False)
            if node not in visited:
                visited.add(node)

                children = node.calculate_children()
                if puzzle.is_goal(node.board):
                    print(puzzle.is_goal(node.board))
                
                for child in children:
                    if child not in visited:
                        pqueue.put((child.cost, child))

        # end timer
        puzzle.set_runtime(time.time() - start_time)
        print(puzzle.runtime)


    




    # output TODO
    # For each grid:
    #   For each search algorithm (UCS, GBFS, A*):
        # output to two paths: the solution and the search
        # for GBFS and A*: have each heuristic in a separate file

    # search output file:
        # f(n) = ? g(n) = ? h(n) = ?, state = new board state

        # f(n) = ?
        # g(n) = node with lowest path cost
        # h(n) = heuristic value

    # methods = ['ucs', 'gbfs', 'astar']
    # for method in methods:
    #     for num, puzzle in enumerate(puzzle_list):
    #         fuel_levels = []
    #         for car in puzzle.car_dict:
    #             fuel_levels.append(f'{car}: {puzzle.car_dict[car][2]}')
    #         write_solution_file(puzzle.board, fuel_levels, method, (num + 1), puzzle.board)

    # Only move in X or Y
    # Slide into free position
    # Move vehicle has same cost in all directions, irrespective of distance moved
    # A A respresents the ambulance
    # Each vehicle has fuel, number of positions it can move
    # Reaching 3f will take the vehicle out of the board (goal: AA reach 3f)

    # From start position, determine next moves