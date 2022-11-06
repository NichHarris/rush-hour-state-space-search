# imports
import argparse
import os

INPUT_FILE_PATH = 'input'
SOLUTIONS_PATH = 'output/solutions'
SEARCH_PATH = 'output/search'
HEIGHT = WIDTH = 6

# def format_solution(initial_board, runtime, search_path, solution_path_length, solution_path, method, id):
def format_solution(board, initial_fuel, method, id, final_board):
    output_file = f'{SOLUTIONS_PATH}/{method}-sol-{id}.txt'
    if not os.path.exists(SOLUTIONS_PATH):
        os.makedirs(SOLUTIONS_PATH)

    final_fuel = ', '.join(initial_fuel).replace(':','')
    initial_fuel = ', '.join(initial_fuel)

    with open(output_file, 'w') as file:
        file.write(f'Initial board configuration: {board}\n\n')
        file.writelines(output_file_grid(board))
        file.write(f'\nCar fuel available: {initial_fuel}\n\n')
        file.write(f'Runtime: {0}\n') # todo get runtime val
        file.write(f'Search path length: {0}\n') # todo get search path length
        file.write(f'Solution path length: {0}\n') # todo get solution path length
        file.write(f'Solution path: {0}\n\n') # todo get solution path
        file.writelines(format_solution_path('')) # todo pass solution path
        file.write(f'\n\n! {final_fuel}\n\n')
        file.writelines(f'{output_file_grid(final_board)}') # todo pass final grid

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

    for i in range(WIDTH, WIDTH*HEIGHT + 1, WIDTH):
        ret += ' '.join(grid[i-WIDTH:i]) + '\n'
    return ret

# get a dict of all the cars and their sizes
def car_sizes(grid, fuel_list):
    car_dict = {}

    for i, car in enumerate(grid):
        if car == '.':
            continue
        elif car in car_dict:
            size, fuel, orientation = car_dict[car]
            car_dict[car] = (size + 1, fuel, orientation)
            continue
        car_dict[car] = (1, get_fuel(car, fuel_list), get_orientation(car, i, grid))
    return car_dict

# Get matrix representation of board and list of fuel levels
def get_grid_and_fuel(test_case):
    grid = test_case[0]

    # # determine all cars and their occurences and orientation
    car_dict = car_sizes(grid, test_case[1:])

    # create the fuel levels
    fuel = determine_all_fuel_levels(test_case[1:], car_dict)
    # fuel = test_case[1:]
    return grid, fuel, car_dict

# for outputing to console
def output_grid_console(fuel, grid, case):
    flevels = f'Fuel levels for: {fuel}'
    print(f'Case {case}: {flevels}')
    for i in range(WIDTH, WIDTH*HEIGHT, WIDTH):
        print(' '.join(grid[i-WIDTH:i]))


def get_orientation(car, index, grid):
    orientation = 'v'
    if index % WIDTH == 0 and grid[index + 1] == car:
        orientation = 'h'
    elif index % WIDTH == WIDTH - 1 and grid[index - 1] == car:
        orientation = 'h'
    elif grid[index - 1] == car or grid[index + 1] == car:
        orientation = 'h' 

    return orientation

def get_fuel(car, fuel_list):
    for fuel in fuel_list:
        if car == fuel[0]:
            return int(fuel[1])
    return 100

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

    # # process the test cases
    for i, test_case in enumerate(test_cases):
        grid, fuel, car_dict = get_grid_and_fuel(test_case)
        
        fuel_list.append(fuel)
        grid_list.append(grid)
        car_dict_list.append(car_dict)

        format_solution(grid, fuel, 'test', i+1, grid)

    # # Print the grid to console and its fuel levels
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

