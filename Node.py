# This file contains the information relating to a Node

# This includes:
#   - the parent node
#   - the current board state
#   - the action taken to get to this state
#   - the updated car dictionary
#   - the total cost to reach this state
#   - the heuristic value of the node
#   - the cost of the path + heuristic

HEIGHT = WIDTH = 6
GRID = HEIGHT * WIDTH
class Node:
    def __init__(self, parent, path_cost, car_dict, board, action):
        self.parent = parent
        self.path_cost = path_cost
        self.heuristic_cost = 0
        self.total_cost = 0
        self.car_dict = car_dict
        self.board = board
        self.action = action

    # define the functionality of the < operate for the Node object
    def __lt__(self, other):
        return self.path_cost < other.path_cost

    # determine what object is used to compare for hashing and equality
    def __key(self):
        return self.board

    # compute if current node is equal to an existing visited node
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.__key() == other.__key()
        return NotImplemented

    # define the functionality of the hashing function for the Node object
    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return (f'Board: {self.board}, Move: {self.action}')

    # update the heuristic and total cost of the node
    def set_heuristic_cost(self, heuristic):
        self.heuristic_cost = heuristic
        self.total_cost = self.path_cost + heuristic

    # determine all possible moves from the current board state
    def calculate_children(self):
        children = [] # list of Nodes, each node will have updated parent (self), total cost, car_dict, board
        for car in self.car_dict:
            size, index, fuel, orientation, is_removed = self.car_dict[car]
            car_removed = False

            # if the car has been removed during the iteration, ignore
            if is_removed:
                continue
            
            # remove car from board if at exit
            if self.board[17] == car and orientation == 'h':
                new_board = self.board.replace(car, '.')
                is_removed = True
                
                action = f'{car} exit 0'
                new_car_dict = self.car_dict.copy()
                new_car_dict[car] = (size, index, fuel, orientation, is_removed)
                node = Node(self, self.path_cost + 1, new_car_dict, new_board, action)
                children.append(node)
                continue
            
            # if the car has no fuel remaining, ignore
            if fuel <= 0:
                continue

            # get the spaces around the car, dependant on the orientation
            (free_spaces) = self.get_spaces(size, orientation, index)

            # DIRECTIONS: DOWN = -1, UP = 1, LEFT = -1, RIGHT = 1
            # -1 equivalent to back, 1 to front
            node = None
            move_directions = (1, -1)

            # now for this specific car, we calculate the boards for the possible moves it can make
            # each move will produce a new board i.e. a new node (B left 3) will produce 3 boards, left 1, left 2, left 3, these are produced from
            # the original board self.board
            for free_space, move_direction in zip(free_spaces, move_directions):
                max_dist = free_space if free_space < fuel else fuel

                # determine the action based on the orientation and move direction
                move_action = ''
                if move_direction == 1:
                    move_action = 'down' if orientation == 'v' else 'right'
                else:
                    move_action = 'up' if orientation == 'v' else 'left'

                # determine the start and end index of ther car, and the step needed
                start, end, step = index, HEIGHT*(size - 1) + index if orientation == 'v' else index + size - 1, HEIGHT if orientation == 'v' else 1
                for move in range(max_dist, 0, -1):
                    temp_fuel = fuel
                    if temp_fuel < move:
                        continue
                    temp_fuel -= move

                    # create the action string
                    action = f'{car} {move_action} {move}'

                    # update the board
                    new_board, new_index = self.update_board(self.board, move, move_direction, start, end, step)

                    # check if new board is the goal state
                    if self.is_goal(new_board):
                        # we have found the goal state
                        # we push the move to the child nodes
                        # then we return and move back up the tree
                        new_car_dict = self.car_dict.copy()
                        new_car_dict[car] = (size, new_index, temp_fuel, orientation, True)
                        node = Node(self, self.path_cost + 1, new_car_dict, new_board, action)
                        return [node]

                    # remove car from board if at exit
                    if new_board[17] == car and orientation == 'h':
                        new_board = new_board.replace(car, '.')
                        car_removed = True

                    # create new node with update info
                    new_car_dict = self.car_dict.copy()
                    new_car_dict[car] = (size, new_index, temp_fuel, orientation, car_removed)
                    node = Node(self, self.path_cost + 1, new_car_dict, new_board, action)
                    children.append(node)

                    # skip if car was removed
                    if (car_removed):
                        break
                
                # skip if car was removed
                if (car_removed):
                    break
        return children

    # update board
    def update_board(self, board, move, direction, start, end, step):

        first, last = start, end
        step = step * direction

        # turn board into array
        board = [*board]

        # swap the car with the empty spaces
        for shift in range(move):
            if direction == 1:
                board[first], board[last+step] = board[last+step], board[first]
            else:
                board[last], board[first+step] = board[first+step], board[last]
            first += step
            last += step

        # turn array back into string
        board = ''.join(board)
        return board[:GRID], first

    # determine if puzzle is in goal state
    def is_goal(self, board):
        puzzle_exit = board[16:18]
        return puzzle_exit == 'AA' # goal state is exit contains 'AA'

    # get the spaces around the car
    def get_spaces(self, size, orientation, index):
        free_spaces_front = free_spaces_back = 0
        # can move up or down
        if orientation == 'v':
            top, bottom = index, HEIGHT*(size - 1) + index
            top_wall = top % WIDTH
            bottom_wall = top_wall + GRID - HEIGHT

            # we are at the top of the board, can only move down
            if bottom < bottom_wall:
                free_spaces_front = self.get_free_spaces(bottom + HEIGHT, bottom_wall + 1, HEIGHT)
            if top > top_wall:
                free_spaces_back = self.get_free_spaces(top - HEIGHT, top_wall - 1, -HEIGHT)
        else: # can move left or right
            left, right = index, index + size - 1
            left_wall = int(left / WIDTH) * WIDTH
            right_wall = left_wall + WIDTH

            if right < right_wall - 1:
                free_spaces_front = self.get_free_spaces(right + 1, right_wall, 1)
            if left > left_wall:
                free_spaces_back = self.get_free_spaces(left - 1, left_wall - 1, -1)
        return free_spaces_front, free_spaces_back

    # count the number of free spaces in a given direction
    def get_free_spaces(self, start, end, step):
        free_spaces = 0
        for i in range(start, end, step):
            if self.board[i] == '.':
                free_spaces += 1
            else:
                break
        return free_spaces
