# imports
import argparse
import os

INPUT_FILE_PATH = 'input'
SOLUTIONS_PATH = 'output/solutions'
SEARCH_PATH = 'output/search'
HEIGHT = WIDTH = 6

# def format_solution(initial_board, runtime, search_path, solution_path_length, solution_path, method, id):
def format_solution(initial_board, method, id, final_board):
    board = ' '.join(initial_board)
    output_file = f'{SOLUTIONS_PATH}/{method}-sol-{id}.txt'
    if not os.path.exists(SOLUTIONS_PATH):
        os.makedirs(SOLUTIONS_PATH)

    initial_grid, initial_fuel, car_dict = get_grid_and_fuel(initial_board)
    final_grid, final_fuel, car_dict = get_grid_and_fuel(final_board)

    initial_fuel = ', '.join(initial_fuel)
    final_fuel = ' '.join(final_fuel).replace(':','')

    with open(output_file, 'w') as file:
        file.write(f'Initial board configuration: {board}\n\n')
        file.writelines(output_file_grid(initial_grid))
        file.write(f'\nCar fuel available: {initial_fuel}\n\n')
        file.write(f'Runtime: {0}\n') # todo get runtime val
        file.write(f'Search path length: {0}\n') # todo get search path length
        file.write(f'Solution path length: {0}\n') # todo get solution path length
        file.write(f'Solution path: {0}\n\n') # todo get solution path
        file.writelines(format_solution_path('')) # todo pass solution path
        file.write(f'\n\n! {final_fuel}\n\n')
        file.writelines(f'{output_file_grid(final_grid)}') # todo pass final grid

def determine_all_cars():
    return

def format_search():
    return

# for outputing to output files
def format_solution_path(solution_path):
    return ''

# for outputing to output files
def determine_all_fuel_levels(fuel, car_dict):
    # for car in car_dict:
    ret = []

    fuel_dict = {}
    for car in fuel:
        letter = car[0]
        amount = car[1:]
        fuel_dict[letter] = amount

    for car in car_dict:
        if car in fuel_dict:
            ret.append(f'{car}:{fuel_dict[car]}')
            letter, amount, orientation = car_dict[car]
            car_dict[car] = (letter, int(fuel_dict[car]), orientation)
        ret.append(f'{car}:100')
    
    return ret

# for outputing to output file
def output_file_grid(grid):
    ret = ''
    for row in grid:
        nl = ' '
        for j, col in enumerate(row):
            if j == WIDTH - 1:
                nl = '\n'
            ret += f'{col}{nl}'
    return ret

# get a dict of all the cars and their sizes
def car_sizes(grid):
    car_dict = {}
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            cell = cell.strip()
            if cell == '.':
                continue
            elif cell in car_dict:
                size, fuel, orientation = car_dict[cell]
                car_dict[cell] = (size + 1, fuel, orientation)
                continue
            orientation = get_orientation(cell, r, c, grid)
            car_dict[cell] = (1, 100, orientation) # size, fuel, oritentation ('v', 'h')
    return car_dict

# Get matrix representation of board and list of fuel levels
def get_grid_and_fuel(test_case):
    # create the grid
    grid = [[test_case[0][i+(j*WIDTH)] for i in range(WIDTH)] for j in range(HEIGHT)]

    # # determine all cars and their occurences and orientation
    car_dict = car_sizes(grid)

    # create the fuel levels
    fuel = determine_all_fuel_levels(test_case[1:], car_dict)
    # fuel = test_case[1:]
    return grid, fuel, car_dict

# for outputing to console
def output_grid_console(fuel, grid, case):
    flevels = f'Fuel levels for: {fuel}' if len(fuel) else 'All fuel levels 100'
    print(f'Case {case}: {flevels}')
    for row in grid:
        print(row)

def get_orientation(car, row, col, grid):
    orientation = 'h'
    if row + 1 < HEIGHT and grid[row + 1][col] == car:
        orientation = 'v'
    elif row - 1 >= 0 and grid[row - 1][col] == car:
        orientation = 'v'
    return orientation

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

    # for outputting to console (as of right now)
    fuel_list = []
    grid_list = []
    car_dict_list = []

    # process the test cases
    for i, test_case in enumerate(test_cases):
        grid, fuel, car_dict = get_grid_and_fuel(test_case)
        
        fuel_list.append(fuel)
        grid_list.append(grid)
        car_dict_list.append(car_dict)

        # todo run algorithms
        print(grid)
        # todo optimize this
        format_solution(test_case, 'test', i+1, test_case)

    # Print the grid to console and its fuel levels
    case = 0
    for fuel, grid in zip(fuel_list, grid_list):
        output_grid_console(fuel, grid, case)
        case += 1

    # output TODO
    # For each grid:
    #   For each search algorithm (UCS, GBFS, A*):
        # output to two paths: the solution and the search
        # for GBFS and A*: have each heuristic in a separate file

    # search output file:
        # f(n) = ? g(n) = ? h(n) = ?, state = new board state

