
HEIGHT = WIDTH = 6
GRID = HEIGHT * WIDTH
class Node:

    def __init__(self, parent, total_cost, car_dict, board, action):
        self.parent = parent
        self.total_cost = total_cost
        self.cost = 1
        self.car_dict = car_dict
        self.board = board
        self.action = action

    def __lt__(self, other):
        return self.cost < other.cost

    def __key(self):
        return self.board

    # compute if current node is equal to an existing visited node
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.__key() == other.__key()
        return NotImplemented

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return (f'Board: {self.board}, Move: {self.action}')

    def setCost(self, cost):
        self.cost = cost

    def calculate_children(self, closed_list):
        children = [] # list of Nodes, each node will have updated parent (self), total cost, car_dict, board
        for car in self.car_dict:
            size, index, fuel, orientation, is_removed = self.car_dict[car]
            car_removed = False
            if fuel <= 0:
                continue

            (free_spaces) = self.get_spaces(size, orientation, index)

            ### Intended DIRECTIONS: DOWN = -1, UP = 1, LEFT = -1, RIGHT = 1
            node = None
            move_directions = (1, -1)

            # now for this specific car, we calculate the boards for the possible moves it can make
            # each move will produce a new board i.e. a new node (B left 3) will produce 3 boards, left 1, left 2, left 3, these are produced from
            # the original board self.board
            for free_space, move_direction in zip(free_spaces, move_directions):
                max_dist = free_space if free_space < fuel else fuel

                move_action = ''
                if move_direction == 1:
                    move_action = 'down' if orientation == 'v' else 'right'
                else:
                    move_action = 'up' if orientation == 'v' else 'left'

                start, end, step = index, HEIGHT*(size - 1) + index if orientation == 'v' else index + size - 1, HEIGHT if orientation == 'v' else 1
                for move in range(max_dist, 0, -1):
                    temp_fuel = fuel
                    if temp_fuel < move:
                        continue
                    temp_fuel -= move

                    # todo: check if move on a horizontal piece puts its into goal position, if it does we can remove it from the board
                    action = f'{car} {move_action} {move}'

                    new_board, new_index = self.update_board(self.board, move, move_direction, start, end, step)
                    if self.is_goal(new_board):
                        # we have found the goal state
                        # we push the move to the child nodes
                        # then we return and move back up the tree
                        new_car_dict = self.car_dict.copy()
                        new_car_dict[car] = (size, new_index, temp_fuel, orientation, True)
                        node = Node(self, self.total_cost + 1, new_car_dict, new_board, action)
                        # children.append(node)
                        return [node]

                    # remove car from board if at exit
                    if new_board[17] == car and orientation == 'h':
                        new_board = new_board.replace(car, '.')
                        car_removed = True

                    new_car_dict = self.car_dict.copy()
                    new_car_dict[car] = (size, new_index, temp_fuel, orientation, True)
                    node = Node(self, self.total_cost + 1, new_car_dict, new_board, action)
                    if node not in closed_list:
                        children.append(node)

                    if (car_removed):
                        break

                if (car_removed):
                    break
        return children

    # update board
    def update_board(self, board, move, direction, start, end, step):

        first, last = start, end
        step = step * direction
        board = [*board]
        for shift in range(move):
            if direction == 1:
                board[first], board[last+step] = board[last+step], board[first]
            else:
                board[last], board[first+step] = board[first+step], board[last]
            first += step
            last += step

        board = ''.join(board)
        return board[:GRID], first

    # determine if puzzle is in goal state
    def is_goal(self, board):
        puzzle_exit = board[16:18]
        return puzzle_exit == 'AA' # goal state is exit contains 'AA'

    # update dictionary with new car positions
    def update_dict(self, move, car, index, fuel, removed):

        # make a copy of the current dict
        car_dict = self.car_dict.copy()

        # get the info for the car from the dict
        size, discard, curr_fuel, oritentation, discard = car_dict[car]
        fuel -= move

        # update the dict entry for the car
        car_dict[car] = (size, index, fuel, oritentation, removed)

        # return the updated dict to be added to the node
        return car_dict

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

    # should just recurse, see comment above @get_spaces
    def get_free_spaces(self, start, end, step):
        free_spaces = 0
        for i in range(start, end, step):
            if self.board[i] == '.':
                free_spaces += 1
            else:
                break
        return free_spaces

    
    def calculate_children_bfs(self):
        # todo redo this entire section using the grid and BFS, then compare the implementation speeds
        grid =  [[self.board[i+(j*WIDTH)] for i in range(WIDTH)] for j in range(HEIGHT)]

        return []

    def get_action(self):
        return self.action