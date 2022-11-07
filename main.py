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
            size, start, fuel, orientation, is_removed = car_dict[car]
            car_dict[car] = (size + 1, start, fuel, orientation, is_removed)
            continue
        car_dict[car] = (1, i, get_fuel(car, fuel_list), get_orientation(car, i, board), False)
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

def get_solution_path(node):
    actions = [] # reverse this list at the end to get the order (board, action, car_dict)
    while node.parent is not None:
        action = [node.board, node.action, node.car_dict]
        actions.append(action)
        # print(actions)
        node = node.parent

    return actions[::-1]

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
            tokens = line.strip().split(' ')[0].split('#')
            
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

        # closed set
        closed = set()
        # open queue
        open = PriorityQueue()
        start = Node(None, 0, puzzle.car_dict, puzzle.board, 'start')
        open.put((0, start))
        search_path_length = 0
        min_path_length = 10**8
        solution_path = []
        actions = []
        while not open.empty():
            cost, node = open.get(block=False)
            if node not in closed:
                closed.add(node)

                # if puzzle.is_goal(node.board):
                #     print('goal')
                #     print(output_file_board(node.board))
                #     actions = get_solution_path(node)
                #     solution_path_length = len(actions)
                #     if solution_path_length < min_path_length:
                #         min_path_length = solution_path_length
                #         fuels = ''
                #         for action in actions:
                #             car = action[1][0]
                #             fuels = f'{car}{action[2][car][2]}' + f' {fuels}'
                #             solution_path.append(f'{action[1]} {action[2][car][2]} {action[0]} {fuels}')


                children, path = node.calculate_children()
               
                for child in children:
                    if child not in closed:
                        search_path_length += 1
                        # print(child.action)
                        # print(output_file_board(child.board))
                        if puzzle.is_goal(child.board):
                            # # print('goal')
                            # print(output_file_board(child.board))
                            actions = get_solution_path(child)
                            solution_path_length = len(actions)
                            if solution_path_length < min_path_length:
                                min_path_length = solution_path_length
                                fuels = ''
                                for action in actions:
                                    car = action[1][0]
                                    fuels = f'{car}{action[2][car][2]}' + f' {fuels}'
                                    solution_path.append(f'{action[1]} {action[2][car][2]} {action[0]} {fuels}')
                                puzzle.solution_node = child
                            break
                        open.put((child.cost, child))

                # if puzzle.is_goal(node.board):
                #     # move up child to get the solution path
                #     print(puzzle.is_goal(node.board))
                #     break

            # write_solution_file(puzzle.board, puzzle.fuel_list, 'bfs', 1, child.board)
            # write_search_file()
        # end timer
        puzzle.set_runtime(time.time() - start_time)
        print(puzzle.runtime)
        print(search_path_length)
        print(output_file_board(puzzle.solution_node.board))
        print(min_path_length)
        # exit()


    




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