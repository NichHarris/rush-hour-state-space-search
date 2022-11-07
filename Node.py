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
            # can move up or down
            if orientation == 'h':
                top, bottom = index, HEIGHT*size - index
                # we are at the top of the board, can only move down
                if top < HEIGHT:
                    pass
                # can only move up
                elif bottom >= GRID - WIDTH:
                    pass
                # can move up or down
                else:
                    pass
            else: # can move left or right
                left, right = index, index + size - 1
                # we are at the left of the board, can only move right
                if left == 0:
                    # check number of free spaces to the right
                    free_spaces = 0
                    right_wall = index + WIDTH - size
                    for i in range(right, right_wall):
                        if self.board[i] == '.':
                            free_spaces += 1
                    

                # can only move left
                elif (right + 1) % WIDTH == 0:
                    free_spaces = 0
                    left_wall = index - WIDTH + size
                    for i in range(left, left_wall, -1): #todo check here for out of bounds
                        if self.board[i] == '.':
                            free_spaces += 1
                    
                # can move left or right
                else:   
                    left_wall = int(index / WIDTH) * WIDTH
                    right_wall = left_wall + WIDTH
                    
                    
        return children

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