# This file contains the information relating to a puzzel board

# This includes:
#   - the board
#   - the cars:
#       - size
#       - start index
#       - fuel
#       - orientation
#   - the goal state
#   - the test case string
#   - the final runtime
#   - the total search path
#   - the optimal solution path
#   - the final fuel levels

class Puzzle:
    def __init__(self, board, test_case, car_dict):
        self.board = board
        self.test_case = test_case
        self.car_dict = car_dict
        self.runtime = 0
        self.search_path = []
        self.solution_path = []
        self.final_fuel = []
        self.solution_node = None

    def __str__(self):
        return f'Puzzle: {self.board}'

    def set_solution_node(self, node):
        self.solution_node = node

    def get_solution_node(self):
        return self.solution_node

    def get_board(self):
        return self.board

    def get_test_case(self):
        return self.test_case

    def get_car_dict(self):
        return self.car_dict

    def get_runtime(self):
        return self.runtime

    def set_runtime(self, runtime):
        self.runtime = runtime
    
    def get_search_path(self):
        return self.search_path
    
    def set_search_path(self, search_path):
        self.search_path = search_path

    def get_solution_path(self):
        return self.solution_path
    
    def set_solution_path(self, solution_path):
        self.solution_path = solution_path

    def get_final_fuel(self):
        return self.final_fuel

    def set_final_fuel(self, final_fuel):
        self.final_fuel = final_fuel

    # determine if puzzle is in goal state
    def is_goal(self, board):
        puzzle_exit = board[16:18]
        return puzzle_exit == 'AA' # goal state is exit contains 'AA'