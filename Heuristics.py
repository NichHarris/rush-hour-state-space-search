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
        blocking_cars = 0
        prev_vehicle = '.'

        # Define and search third row
        # get the index to the right of ambulance = start_index + length
        end_ambulance = self.car_dict['A'][1] + self.car_dict['A'][0]
        end_exit_row = int(WIDTH * HEIGHT/2 - 1)

        if end_ambulance - 1 == end_exit_row:
            return blocking_cars

        for i in range(end_ambulance, end_exit_row + 1):
            car_letter = self.board[i]
            if car_letter != '.' and prev_vehicle != car_letter:
                blocking_cars += 1
                prev_vehicle = car_letter
        
        return blocking_cars
    
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
        blocking_cars = 0
        prev_vehicle = '.'

        # Define and search third row
        # get the index to the right of ambulance = start_index + length
        end_ambulance = self.car_dict['A'][1] + self.car_dict['A'][0]
        end_exit_row = int(WIDTH * HEIGHT/2 - 1)

        if end_ambulance - 1 == end_exit_row:
            return blocking_cars

        for i in range(end_ambulance, end_exit_row + 1):
            car_letter = self.board[i]
            if car_letter != '.':
                if self.car_dict[car_letter][2] <= 0:
                    return float('inf')
                else:
                    prev_block_down = 0
                    prev_block_up = 0

                    # Count blocking car if ambulance passed and car is present
                    if prev_vehicle != car_letter:
                        blocking_cars += 1

                    # Check orientation of car and only add blocking if vertically oriented
                    if self.car_dict[car_letter][3] == 'v':
                        # Search vertically for blocking cars 
                        prev_vehicle = car_letter
                        j =  i
                        while j - WIDTH > 0:
                            j -= WIDTH
                            up_car = self.board[j]
                            if up_car != prev_vehicle:
                                if up_car != '.':
                                    prev_block_up += 1
                                prev_vehicle = up_car

                        prev_vehicle = car_letter
                        j =  i
                        while j + WIDTH < WIDTH*HEIGHT:
                            j += WIDTH
                            down_car = self.board[j]
                            if down_car != prev_vehicle:
                                if down_car != '.':
                                    prev_block_down += 1
                                prev_vehicle = down_car

                        blocking_cars += min(prev_block_up, prev_block_down)
                        prev_vehicle = car_letter
        
        return blocking_cars