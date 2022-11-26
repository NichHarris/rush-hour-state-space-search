# This file contains the information relating to the heuristic functions

# This includes:
#   - the board state
#   - the car dictionary
#   - the lambda value
#   - h1: Number of blocking vehicles
#   - h2: Number of blocked positions
#   - h3: Number of blocking vehicles * LAMBDA
#   - h4: The number of blocked positions, when a blocking vehicle's fuel is 0, h = inf

HEIGHT = WIDTH = 6
GRID = HEIGHT * WIDTH

class Heuristics:

    def __init__(self, board, car_dict, LAMBDA=2.5):
        self.board = board
        self.car_dict = car_dict
        self.LAMBDA = LAMBDA

    # Heuristic 1: Number of blocking vehicles
    def perform_h1(self):
        blocking_cars = {}

        # Define and search third row
        # get the index to the right of ambulance = start_index + length
        end_ambulance = self.car_dict['A'][1] + self.car_dict['A'][0]
        end_exit_row = int(WIDTH * HEIGHT/2 - 1)

        if end_ambulance - 1 == end_exit_row:
            return len(blocking_cars)

        for i in range(end_ambulance, end_exit_row + 1):
            if self.board[i] != '.':
                blocking_cars[self.board[i]] = 1
        
        return len(blocking_cars)
    
    # Heuristic 2: Number of blocked positions
    def perform_h2(self):
        count = 0

        # Define and search third row
        # get the index to the right of ambulance = start_index + length
        end_ambulance = self.car_dict['A'][1] + self.car_dict['A'][0]
        end_exit_row = int(WIDTH * HEIGHT/2 - 1)

        if end_ambulance - 1 == end_exit_row:
            return count

        for i in range(end_ambulance, end_exit_row + 1):
            if self.board[i] != '.':
                count += 1
        
        return count

    # Heuristic 3: Multiplied h1 with lambda
    def perform_h3(self):
        return self.perform_h1() * self.LAMBDA

    # Heuristic 4: return the number of blocking cars, unless the car has no fuel remaining, return infinity
    def perform_h4(self):
        blocking_cars = {}

        # Define and search third row
        # get the index to the right of ambulance = start_index + length
        end_ambulance = self.car_dict['A'][1] + self.car_dict['A'][0]
        end_exit_row = int(WIDTH * HEIGHT/2 - 1)

        if end_ambulance - 1 == end_exit_row:
            return len(blocking_cars)

        for i in range(end_ambulance, end_exit_row + 1):
            if self.board[i] != '.':
                if self.car_dict[self.board[i]][2] <= 0:
                    return float('inf')
                blocking_cars[self.board[i]] = 1
        
        return len(blocking_cars)