# This file contains the information relating to a puzzel board

# This includes:
#   - the board
#   - the cars:
#       - size
#       - start index
#       - fuel
#       - orientation
#   - the final runtime
#   - the solution Node

class Puzzle:
    def __init__(self, board, car_dict):
        self.board = board
        self.car_dict = car_dict
        self.runtime = 0
        self.solution_node = None

    def __str__(self):
        return f'Puzzle: {self.board}'

    # determine if puzzle is in goal state
    # goal state is exit contains 'AA'
    def is_goal(self, board):
        puzzle_exit = board[16:18]
        return puzzle_exit == 'AA'