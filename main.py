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
ANALYSIS_FILE_PATH = 'output/analysis.txt'
HEIGHT = WIDTH = 6

def write_analysis_file(puzzle, method, heuristic, id, search_path_len):
    output_file = f'output/analysis.txt'
    
    with open(output_file, 'a') as file:
        solution_node = ''
        if puzzle.solution_node is None:
            solution_node = 'None'
        else:
            solution_node = puzzle.solution_node.path_cost
        file.write(f'{id:<13}\t {method.upper():<9}\t {heuristic:<9}\t {solution_node:<15}\t {search_path_len:<13}\t {puzzle.runtime:<7}\n')

# format solution file
def write_solution_file(puzzle, method, id, search_path_len, heuristic):
    output_file = f'{SOLUTIONS_PATH}/{method}-sol-{id}.txt'
    if heuristic != '':
        output_file = f'{SOLUTIONS_PATH}/{method}-{heuristic}-sol-{id}.txt'

    if not os.path.exists(SOLUTIONS_PATH):
        os.makedirs(SOLUTIONS_PATH)

    with open(output_file, 'w') as file:
        # check if solution exists
        if puzzle.solution_node is not None:
            solution_len, formated_path, fuel_list = display_solution_path(puzzle.solution_node)
            file.write(f'Initial board configuration: {puzzle.board}\n\n')
            file.writelines(output_file_board(puzzle.board))
            file.write(f'\nCar fuel available: {format_fuel_list(puzzle.car_dict)}\n\n')
            file.write(f'Runtime: {puzzle.runtime}\n') 
            file.write(f'Search path length: {search_path_len}\n') 
            file.write(f'Solution path length: {solution_len}\n') 
            file.write(f'Solution path: {format_solution_path(puzzle.solution_node)}\n\n')
            file.writelines(formated_path)
            file.write(f'\n\n! {fuel_list}\n')
            file.writelines(f'{output_file_board(puzzle.solution_node.board)}')
        else:
            file.write(f'Initial board configuration: {puzzle.board}\n\n')
            file.writelines(output_file_board(puzzle.board))
            file.write(f'\nCar fuel available: {format_fuel_list(puzzle.car_dict)}\n\n')
            file.write('Sorry, could not solve the puzzle as specified.\nError: no solution found\n\n')
            file.write(f'Runtime: {puzzle.runtime}\n')

# format search file
def write_search_file(closed, method, id, heuristic):
    f_n = 0
    g_n = 0
    h_n = 0

    ret = []
    search_path = []
    for key in closed.keys():
        search_path.append(key)
        
    start = search_path.pop(0)

    # sort search path
    if method == 'astar':
        f_n = start.total_cost
        g_n = start.path_cost
        h_n = start.heuristic_cost
        search_path.sort(key=lambda x: x.total_cost)
    elif method == 'gbfs':
        f_n = h_n = start.heuristic_cost
        search_path.sort(key=lambda x: x.heuristic_cost)
    elif method == 'ucs':
        f_n = g_n = start.path_cost
        search_path.sort(key=lambda x: x.path_cost)

    ret.append(f'{f_n:>2} {g_n:>2} {h_n:>2} {start.board}')

    for node in search_path:
        board = node.board
        car_dict = node.car_dict

        fuel_list = ''
        if method == 'astar':
            f_n = node.total_cost
            g_n = node.path_cost
            h_n = node.heuristic_cost
        elif method == 'gbfs':
            f_n = h_n = node.heuristic_cost
        elif method == 'ucs':
            f_n = g_n = node.path_cost

        while node.parent is not None:
            car = node.action[0]
            curr_fuel_list = fuel_list.split(' ')
            exists = False

            for cf in curr_fuel_list:
                if cf == '':
                    break

                if cf[0] == car:
                    fuel_list = fuel_list.replace(cf, f'{car}{car_dict[car][2]}')
                    exists = True
                    break
            if not exists:
                fuel_list += f'{car}{car_dict[car][2]} '
            node = node.parent
        ret.append(f'{f_n:>2} {g_n:>2} {h_n:>2} {board} {fuel_list}')

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

# for outputing to output files
def format_fuel_list(car_dict):
    ret = ''

    for car in car_dict:
        ret += f'{car}:{car_dict[car][2]} '

    return ret

# for outputing to output files
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
# dict= {car: (size, start_index, fuel, orientation, is_removed)}
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

# get fuel for car from input list
def get_fuel(car, fuel_list):
    for fuel in fuel_list:
        if car == fuel[0]:
            return int(fuel[1])

    return 100

# get orientation of car from board
def get_orientation(car, index, grid):
    orientation = 'v'

    if index % WIDTH == 0 and grid[index + 1] == car:
        orientation = 'h'
    elif index % WIDTH == WIDTH - 1 and grid[index - 1] == car:
        orientation = 'h'
    elif grid[index - 1] == car or grid[index + 1] == car:
        orientation = 'h' 

    return orientation

# move up from solution node to start node
# return list of actions
def get_solution_path(node):
    actions = []

    while node.parent is not None:
        action = [node.board, node.action, node.car_dict]
        actions.append(action)
        node = node.parent

    return actions[::-1]

    # determine if puzzle is in goal state
    # goal state is exit contains 'AA'
def is_goal(board):
    puzzle_exit = board[16:18]
    return puzzle_exit == 'AA'

# perform UCS:
# 1. get start node
# 2. add start node to open list
# 3. while open list is not empty:
#     a. get node with lowest path cost
#     b. ignore nodes with current costs higher than best cost
#     c. if node is a better solution, replace best solution
#     d. if node is in closed list, ignore
#     e. if node is in open list:
#         i. if node has lower path cost, replace node in open list
#         ii. else, ignore: there is a better path in the open list already
#     f. expand node into children (possible moves)
# 4. return closed list
def uniform_cost_search(puzzle):
    # start timer
    start_time = time.time()
    # closed set
    closed = {}

    # open queue
    open = PriorityQueue()
    count = 0

    # start condition
    start = Node(None, 0, puzzle.car_dict, puzzle.board, 'start')
    open.put((0, start))

    while not open.empty():
        path_cost, curr_node = open.get(block=False)

        # ignore cases where solution is lower than current path cost
        # checking further paths will only lead to higher costs
        if puzzle.solution_node is not None:
            if curr_node.path_cost >= puzzle.solution_node.path_cost:
                closed[curr_node] = path_cost
                continue
            
        # is it a goal state
        if is_goal(curr_node.board):
            # if we have a solution, replace with better
            if puzzle.solution_node is not None:
                if curr_node.path_cost < puzzle.solution_node.path_cost:
                    puzzle.solution_node = curr_node
                    closed[curr_node] = path_cost
            else:
                puzzle.solution_node = curr_node
                closed[curr_node] = path_cost
            continue

        if curr_node in closed:
            # update parent node...
            if curr_node.path_cost >= closed[curr_node]:
                continue
            else:
                closed[curr_node] = path_cost

        in_open, index = check_in_open(open, curr_node)
        if in_open:
            # we skip since it's already in open, replace if it's a better path
            if open.queue[index][0] > path_cost:
                open.queue[index] = (path_cost, curr_node)
            continue
        else:
            closed[curr_node] = path_cost
            children = curr_node.calculate_children()
            count += 1
            for child in children:
                open.put((child.path_cost, child))
    puzzle.runtime = time.time() - start_time

    return count, closed

# perform GBFS:
# 1. get start node and calculate heuristics
# 2. add start node to open list
# 3. while open list is not empty:
#     a. get node with lowest heuristic cost
#     b. if node is a better solution, replace best solution
#     c. if node is in closed list, ignore
#     d. if node is in open list, ignore
#     e. expand node into children (possible moves), calculate heuristics
#     f. if child not in closed list, add to open list
# 4. return closed list
def greedy_bfs(puzzle, heuristic):
    # start timer
    start_time = time.time()
    # closed set
    closed = {}

    # open queue
    open = PriorityQueue()
    count = 0

    heuristics = Heuristics(puzzle.board, puzzle.car_dict)
    # start condition
    start = Node(None, 0, puzzle.car_dict, puzzle.board, 'start')
    hcost = eval(f'heuristics.perform_{heuristic}()')
    start.set_heuristic_cost(hcost)
    open.put((hcost, start))

    while not open.empty():
        heuristic_cost, curr_node = open.get(block=False)

        # ignore cases where solution is lower than current path cost
        # checking further paths will only lead to higher costs
        if puzzle.solution_node is not None:
            if curr_node.heuristic_cost >= puzzle.solution_node.heuristic_cost:
                closed[curr_node] = heuristic_cost
                continue
        
        if is_goal(curr_node.board):
            if puzzle.solution_node != None:
                # we found a new minimum path length
                if curr_node.path_cost < puzzle.solution_node.path_cost:
                    puzzle.solution_node = curr_node
                    closed[curr_node] = heuristic_cost
            else:
                puzzle.solution_node = curr_node
                closed[curr_node] = heuristic_cost
            continue

        if curr_node in closed:
            continue
        in_open, index = check_in_open(open, curr_node)
        if in_open:
            continue
        else:
            closed[curr_node] = heuristic_cost
            children = curr_node.calculate_children()
            count += 1

            for child in children:
                heuristics = Heuristics(child.board, child.car_dict)
                hcost = eval(f'heuristics.perform_{heuristic}()')
                child.set_heuristic_cost(hcost)
                if child in closed:
                    continue

                open.put((child.heuristic_cost, child))
    puzzle.runtime = time.time() - start_time

    return count, closed

# perform A* (h is not monotonic):
# 1. get start node and calculate heuristics
# 2. add start node to open list
# 3. while open list is not empty:
#     a. get node with lowest total cost (g_n + h_n)
#     b. if node is a better solution, replace best solution
#     c. if node is in closed list:
#         i. if node has lower total cost, remove version from closed list, place node in open list
#     d. if node is in open list: replace with node
#     e. expand node into children (possible moves), calculate heuristics
# 4. return closed list
def a_star(puzzle, heuristic):
    # start timer
    start_time = time.time()
    # closed set
    closed = {}

    # open queue
    open = PriorityQueue()
    count = 0

    heuristics = Heuristics(puzzle.board, puzzle.car_dict)
    # start condition
    start = Node(None, 0, puzzle.car_dict, puzzle.board, 'start')
    hcost = eval(f'heuristics.perform_{heuristic}()')
    start.set_heuristic_cost(hcost)
    open.put((start.total_cost, start))

    while not open.empty():
        total_cost, curr_node = open.get(block=False)

        # ignore cases where solution is lower than current path cost
        # checking further paths will only lead to higher costs
        if puzzle.solution_node is not None:
            if curr_node.path_cost >= puzzle.solution_node.path_cost:
                closed[curr_node] = total_cost
                continue

        if is_goal(curr_node.board):
            if puzzle.solution_node != None:
                # we found a new minimum path length
                if curr_node.path_cost < puzzle.solution_node.path_cost:
                    puzzle.solution_node = curr_node
                    closed[curr_node] = curr_node.total_cost
            else:
                puzzle.solution_node = curr_node
                closed[curr_node] = total_cost
            continue

        if curr_node in closed:
            if closed[curr_node] >= curr_node.total_cost:
                # resuscitate node
                closed.pop(curr_node)
                open.put((curr_node.total_cost, curr_node))
                continue
        
        in_open, index = check_in_open(open, curr_node)
        if in_open:
            if total_cost < open.queue[index][0]:
                open.queue[index] = (total_cost, curr_node)
            continue
        else:
            closed[curr_node] = total_cost
            children = curr_node.calculate_children()
            count += 1

            for child in children:
                heuristics = Heuristics(child.board, child.car_dict)
                hcost = eval(f'heuristics.perform_{heuristic}()')
                child.set_heuristic_cost(hcost)
                if child in closed:
                    if closed[child] >= child.total_cost:
                        # resuscitate node
                        closed.pop(child)
                    else:
                        continue

                open.put((child.total_cost, child))

    puzzle.runtime = time.time() - start_time
    return count, closed

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
        puzzle.solution_node = child

    return solution_path, min_path_length

# check if node is in the open list
def check_in_open(open, node):
    for i, check in enumerate(open.queue):
        if check[1].board == node.board:
            return True, i

    return False, None

if __name__ == '__main__':
    # parse through the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', type=str, default='sample-input.txt')
    # add boolean parser argument
    parser.add_argument('--analysis', '-a', action='store_true')

    args = parser.parse_args()
    input_file = f'{INPUT_FILE_PATH}/{args.file}'
    analysis = args.analysis
    
    test_cases = []
    # read the file
    with open(input_file, 'r') as file:
        for line in file.readlines():
            if line.strip() == '':
                continue
            
            tokens = line.strip().split(' ')
            if tokens[0][0] == '#':
                continue
            test_cases.append(tokens)

    puzzle_list = []
    # process the test cases into puzzles
    for test_case in test_cases:
        board = test_case[0]
        car_dict = get_car_dict(board, test_case[1:])
        puzzle_list.append(Puzzle(board, car_dict))

    if analysis:
        output_file = f'output/analysis.txt'
        if not os.path.exists('output'):
            os.makedirs('output')
        
        with open(output_file, 'w') as file:
            file.write(f'Puzzle Number\t Algorithm\t Heuristic\t Solution Length\t Search Length\t Runtime\n')

    # solve the puzzles
    methods = ['ucs', 'gbfs', 'astar']
    heuristics = ['h1', 'h2', 'h3', 'h4']
    for i, puzzle in enumerate(puzzle_list):
        for method in methods:
            if method == 'ucs':
                puzzle_copy = copy.deepcopy(puzzle)
                count, closed = uniform_cost_search(puzzle_copy)
                if not analysis:       
                    write_solution_file(puzzle_copy, method, i + 1, count, '')
                    write_search_file(closed, method, i + 1, '')
                else:
                    write_analysis_file(puzzle_copy, method, 'NA', i+1, count)
            elif method == 'gbfs':
                for heuristic in heuristics:
                    puzzle_copy = copy.deepcopy(puzzle)
                    count, closed = greedy_bfs(puzzle_copy, heuristic)
                    if not analysis:     
                        write_solution_file(puzzle_copy, method, i + 1, count, heuristic)
                        write_search_file(closed, method, i + 1, heuristic)
                    else:
                        write_analysis_file(puzzle_copy, method, heuristic, i+1, count)
            elif method == 'astar':
                for heuristic in heuristics:
                    puzzle_copy = copy.deepcopy(puzzle)
                    count, closed = a_star(puzzle_copy, heuristic)
                    if not analysis:      
                        write_solution_file(puzzle_copy, method, i + 1, count, heuristic)
                        write_search_file(closed, method, i + 1, heuristic)
                    else:
                        write_analysis_file(puzzle_copy, method, heuristic, i+1, count)
                continue