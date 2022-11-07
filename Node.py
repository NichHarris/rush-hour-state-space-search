HEIGHT = WIDTH = 6
GRID = HEIGHT * WIDTH
class Node:

    def __init__(self, parent, total_cost, car_dict, board):
        self.parent = parent
        self.total_cost = total_cost
        self.car_dict = car_dict
        self.board = board

    def __key(self):
        return (self.board, self.parent)

    # compute if current node is equal to an existing visited node
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.__key() == other.__key()
        return NotImplemented

    def __hash__(self):
        return hash(self.__key())

    def add_node(self, value):
        self.nodes[value] = []

    def add_edge(self, from_node, to_node, weight):
        self.nodes[from_node].append(to_node)
        self.nodes[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

    def get_cost(self, from_node, to_node):
        return self.weights[(from_node, to_node)]

    def get_neighbors(self, node):
        return self.nodes[node]

    def is_goal(self):
        ret = False
        if self.get_exit() == 'AA':
            ret = True
        return ret

    def get_exit(self):
        return self.nodes['AA']
        
    def calculate_children(self):
        # get the car that can move
        # get the direction that the car can move
        # move the car
        # add the new node to the queue
        # return the queue
        children = [] # list of Nodes, each node will have updated parent (self), total cost, car_dict, board

        for car in self.car_dict:
            size, index, fuel, orientation = self.car_dict[car]

            # todo redo this entire section using the grid and BFS, then compare the implementation speeds
            grid =  [[self.board[i+(j*WIDTH)] for i in range(WIDTH)] for j in range(HEIGHT)]

            free_spaces_front = free_spaces_back = 0
            # can move up or down
            if orientation == 'v':
                top, bottom = index, HEIGHT*(size - 1) + index
                top_wall = top % WIDTH
                bottom_wall = top_wall + GRID - HEIGHT
                print(top, bottom)
                print(top_wall, bottom_wall)
                # we are at the top of the board, can only move down
                if top == top_wall:
                    if bottom < bottom_wall:
                        free_spaces_front = self.get_free_spaces(bottom + HEIGHT, bottom_wall, HEIGHT)
                    print(f'Vertical move down {car}: {free_spaces_front}')
                # can only move up
                elif bottom == bottom_wall:
                    if top > top_wall:
                        free_spaces_back = self.get_free_spaces(top, top_wall, HEIGHT)
                    print(f'Vertical move up {car}: {free_spaces_back}')
                # can move up or down
                else:
                    if bottom < bottom_wall:
                        free_spaces_front = self.get_free_spaces(bottom + HEIGHT, bottom_wall + 1, HEIGHT) #todo check here for out of bounds
                    if top > top_wall:
                        free_spaces_back = self.get_free_spaces(top - HEIGHT, top_wall - 1, -HEIGHT)
                    print(f'Vertical mid move down {car}: {free_spaces_front}')
                    print(f'Vertical mid move up {car}: {free_spaces_back}')
            else: # can move left or right
                left, right = index, index + size - 1
                left_wall = int(left / WIDTH) * WIDTH
                right_wall = left_wall + WIDTH

                # we are at the left of the board, can only move right
                if left % WIDTH == 0:
                    # check number of free spaces to the right
                    if right < right_wall - 1:
                        free_spaces_front = self.get_free_spaces(right + 1, right_wall, 1)
                    # print(f'Horizontal move right {car}: {free_spaces_front}')
                # can only move left
                elif (right + 1) % WIDTH == 0:
                    if left > left_wall:
                        free_spaces_back = self.get_free_spaces(left - 1, left_wall - 1, -1) #todo check here for out of bounds
                    # print(f'Horizontal move left {car}: {free_spaces_back}')
                # can move left or right
                else:
                    if left > left_wall:
                        free_spaces_front = self.get_free_spaces(left - 1, left_wall - 1, -1) #todo check here for out of bounds
                    if right < right_wall:
                        free_spaces_back = self.get_free_spaces(right + 1, right_wall, 1)
                    # print(f'Horizontal mid move left {car}: {free_spaces_front}')
                    # print(f'Horizontal mid move right {car}: {free_spaces_back}')
        return children

    def get_free_spaces(self, start, end, step):
        free_spaces = 0
        for i in range(start, end, step):
            print(self.board[i])
            if self.board[i] == '.':
                free_spaces += 1
            else:
                break
        return free_spaces


    def calculate_children_bfs(self):
        # todo redo this entire section using the grid and BFS, then compare the implementation speeds
        grid =  [[self.board[i+(j*WIDTH)] for i in range(WIDTH)] for j in range(HEIGHT)]

        return []


# This class will hold the info on a specific state (node of the tree)

# root = Tree()
# root.children = [Tree(), Tree(), Tree() ......]
# for child in root.children:
#     child.children = [Tree(), Tree(), Tree() ......] 
# and so on
# class Tree:
#     def __init__(self):
#         # self.root = self.State()
#         self.children = {}
#         self.weights = {}
#         self.board = None # current board state
#         self.move = None # move that got us to this state
#         self.car_dict = None # dict of all the cars and their sizes, fuel, and orientation


    # class State:
    #     def __init__(self):
    #         self.parent = None # point to parent state
    #         self.board = None # current board state
    #         self.car_dict = None # dict of cars and their sizes, fuels, and orientations