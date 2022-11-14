# imports
import argparse
import os
from Puzzle import Puzzle
from Node import Node
from Heuristics import Heuristics
from queue import PriorityQueue
import time
import copy

INPUT_FILE_PATH = 'input'
SOLUTIONS_PATH = 'output/solutions'
SEARCH_PATH = 'output/search'
HEIGHT = WIDTH = 6

def write_solution_file(puzzle, method, id, search_path_len, heuristic):
    output_file = f'{SOLUTIONS_PATH}/{method}-sol-{id}.txt'
    if heuristic != '':
        output_file = f'{SOLUTIONS_PATH}/{method}-{heuristic}-sol-{id}.txt'

    if not os.path.exists(SOLUTIONS_PATH):
        os.makedirs(SOLUTIONS_PATH)

    with open(output_file, 'w') as file:
        if puzzle.solution_node is not None:
            solution_len, formated_path, fuel_list = display_solution_path(puzzle.solution_node)
            file.write(f'Initial board configuration: {puzzle.board}\n\n')
            file.writelines(output_file_board(puzzle.board))
            file.write(f'\nCar fuel available: {format_fuel_list(puzzle.car_dict)}\n\n')
            file.write(f'Runtime: {puzzle.runtime}\n') # todo get runtime val
            file.write(f'Search path length: {search_path_len}\n') # todo get search path length
            file.write(f'Solution path length: {solution_len}\n') # todo get solution path length
            file.write(f'Solution path: {format_solution_path(puzzle.solution_node)}\n\n') # todo get solution path
            file.writelines(formated_path) # todo pass solution path
            file.write(f'\n\n! {fuel_list}\n')
            file.writelines(f'{output_file_board(puzzle.solution_node.board)}') # todo pass final grid
        else:
            file.write(f'Initial board configuration: {puzzle.board}\n\n')
            file.writelines(output_file_board(puzzle.board))
            file.write(f'\nCar fuel available: {format_fuel_list(puzzle.car_dict)}\n\n')
            file.write('Sorry, could not solve the puzzle as specified.\nError: no solution found\n\n')
            file.write(f'Runtime: {puzzle.runtime}\n') # todo get runtime val

def write_search_file(closed, method, id, heuristic):
    f_n = 0
    g_n = 0
    h_n = 0

    ret = []
    search_path = []
    for key in closed.keys():
        search_path.append(key)
        
    start = search_path.pop(0)
    ret.append(f'{f_n} {g_n} {h_n} {start.board}')

    # sort search path
    if method == 'gbfs':
        search_path.sort(key=lambda x: x.heuristic_cost)
    else:
        search_path.sort(key=lambda x: x.total_cost)


    # sort search path
    for node in search_path:
        board = node.board
        car_dict = node.car_dict

        fuel_list = ''
        f_n = node.total_cost + node.heuristic_cost
        g_n = node.total_cost
        h_n = node.heuristic_cost

        while node.parent is not None:
            car = node.action[0]
            fuel_list += f'{car}{car_dict[car][2]} '
            node = node.parent
        ret.append(f'{f_n} {g_n} {h_n} {board} {fuel_list}')

    printout = '\n'.join(ret)

    output_file = f'{SEARCH_PATH}/{method}-search-{id}.txt'
    if heuristic != '':
        output_file = f'{SEARCH_PATH}/{method}-{heuristic}-search-{id}.txt'

    if not os.path.exists(SEARCH_PATH):
        os.makedirs(SEARCH_PATH)

    with open(output_file, 'w') as file:
        file.writelines(printout)

# for outputing to output files
def format_solution_path(node):
    ret = []

    while node.parent is not None:
        ret.append(node.action)
        node = node.parent

    return '; '.join(ret[::-1])

def format_fuel_list(car_dict):
    ret = ''

    for car in car_dict:
        ret += f'{car}:{car_dict[car][2]} '

    return ret

def display_solution_path(node):

    solution_path = []
    ret = []
    count = 0
    while node.parent is not None:
        count += 1
        solution_path.append([node.action, node.board, node.car_dict])
        node = node.parent
    
    solution_path = solution_path[::-1]
    car_fuel = {}
    fuel_list = ''
    for path in solution_path:
        action = path[0].split(' ')
        car = action[0]
        board = path[1]
        car_dict = path[2]
        car_fuel[car] = car_dict[car][2]

        fuel_list = ''
        for cf in car_fuel:
            fuel_list += f'{cf}{car_fuel[cf]} '
        
        ret.append(f'{car}{action[1]:>6} {action[2]} \t{car_fuel[car]:>2} {board} {fuel_list}')

    return count, '\n'.join(ret), fuel_list

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

        if car in car_dict:
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

def get_solution_path(node):
    actions = []

    while node.parent is not None:
        action = [node.board, node.action, node.car_dict]
        actions.append(action)
        node = node.parent

    return actions[::-1]

def uniform_cost_search(puzzle):
    # start timer
    start_time = time.time()
    # closed set
    closed = {}

    # open queue
    open = PriorityQueue()
    min_path_length = float('inf')

    # start condition
    start = Node(None, 0, puzzle.car_dict, puzzle.board, 'start')
    open.put((0, start))

    while not open.empty():
        total_cost, curr_node = open.get(block=False)
        in_open, index = check_in_open(open, curr_node)

        if puzzle.solution_node is not None:
            if curr_node.total_cost >= puzzle.solution_node.total_cost:
                closed[curr_node] = total_cost
                continue
        
        if curr_node in closed:
            # we skip since it's already in closed
            continue
        elif in_open:
            # we skip since it's already in open, replace if it's a better path
            if total_cost < open.queue[index][0]:
                open.queue[index] = (total_cost, curr_node)
            continue
        elif puzzle.is_goal(curr_node.board):
            if puzzle.solution_node != None:
                # we found a new minimum path length
                if total_cost < puzzle.solution_node.total_cost:
                    puzzle.solution_node = curr_node
                    closed[curr_node] = total_cost
                    continue
        else:
            closed[curr_node] = total_cost
            children = curr_node.calculate_children()
            
            for child in children:
                if child in closed:
                    if child.total_cost < closed[child]:
                        closed.pop(child)
                    else:
                        continue
                elif puzzle.is_goal(child.board):
                    solution_path, min_path_length = goal_reached(puzzle, child, min_path_length)
                    puzzle.solution_path = solution_path
                    puzzle.solution_node = child
                open.put((child.total_cost, child))
    puzzle.runtime = time.time() - start_time

    return min_path_length, closed

def greedy_bfs(puzzle, heuristic):
    # start timer
    start_time = time.time()
    # closed set
    closed = {}

    # open queue
    open = PriorityQueue()
    min_path_length = float('inf')

    heuristics = Heuristics(puzzle.board, puzzle.car_dict)
    # start condition
    start = Node(None, 0, puzzle.car_dict, puzzle.board, 'start')
    start.heuristic_cost = eval(f'heuristics.perform_{heuristic}()')
    open.put((0, start))

    while not open.empty():
        heuristic_cost, curr_node = open.get(block=False)

        if puzzle.solution_node is not None:
            if curr_node.heuristic_cost >= puzzle.solution_node.heuristic_cost:
                closed[curr_node] = heuristic_cost
                continue
        
        if curr_node in closed:
            # we skip since it's already in closed
            continue
        elif puzzle.is_goal(curr_node.board):
            if puzzle.solution_node != None:
                # we found a new minimum path length
                if curr_node.total_cost < puzzle.solution_node.total_cost:
                    puzzle.solution_node = curr_node
                    closed[curr_node] = curr_node.heuristic_cost
                    continue
        else:
            closed[curr_node] = heuristic_cost
            children = curr_node.calculate_children()
        
            for child in children:
                heuristics = Heuristics(child.board, child.car_dict)
                child.heuristic_cost = eval(f'heuristics.perform_{heuristic}()')
                in_open, index = check_in_open(open, child)
                if child in closed:
                    if child.total_cost < closed[child]:
                        closed.pop(child)
                    else:
                        continue
                elif in_open:
                    continue
                elif puzzle.is_goal(child.board):
                    solution_path, min_path_length = goal_reached(puzzle, child, min_path_length)
                    puzzle.solution_path = solution_path
                    puzzle.solution_node = child

                open.put((child.heuristic_cost, child))
    puzzle.runtime = time.time() - start_time

    return min_path_length, closed

def goal_reached(puzzle, child, min_path_length):
    actions = get_solution_path(child)
    solution_path_length = len(actions)
    solution_path = []

    if solution_path_length < min_path_length:
        min_path_length = solution_path_length
        fuels = ''
        for action in actions:
            car = action[1][0]
            fuels = f'{car}{action[2][car][2]}' + f' {fuels}'
            solution_path.append(action[1])
        puzzle.set_solution_node(child)

    return solution_path, min_path_length

def check_in_open(open, node):
    for i, check in enumerate(open.queue):
        if check[1].board == node.board:
            return True, i

    return False, None

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
    methods = ['ucs', 'gbfs', 'astar']
    for method in methods:
        for i, puzzle in enumerate(puzzle_list):
            if method == 'ucs':
                puzzle_copy = copy.deepcopy(puzzle)
                min_path_length, closed = uniform_cost_search(puzzle_copy)            
                write_solution_file(puzzle_copy, method, i + 1, len(closed), '')
                write_search_file(closed, method, i + 1, '')

            if method == 'gbfs':
                for heuristic in ['h1', 'h2', 'h3', 'h4']:
                    puzzle_copy = copy.deepcopy(puzzle)
                    min_path_length, closed = greedy_bfs(puzzle_copy, heuristic)
                    write_solution_file(puzzle_copy, method, i + 1, len(closed), heuristic)
                    write_search_file(closed, method, i + 1, heuristic)
            else:
                # for heuristic in ['h1', 'h2', 'h3', 'h4']:
                #     puzzle_copy = copy.deepcopy(puzzle)
                #     min_path_length, closed = a_star(puzzle_copy, heuristic)
                #     write_solution_file(puzzle_copy, method, i + 1, len(closed), heuristic)
                #     write_search_file(closed, method, i + 1, heuristic)
                continue
