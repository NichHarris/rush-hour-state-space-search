
class Heuristics:

    def __init__(self, board, WIDTH=6, HEIGHT=6, LAMBDA=2.5):
        self.board = board
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.LAMBDA = LAMBDA

    # Heuristic 1: Number of blocking vehicles
    def perform_h1(self):
        # Count blocking cars in front of ambulance
        blocking_count = 0
        prev_vehicle = ''
        ambulance_passed = False

        # Define and search third row 
        end_row = int(self.WIDTH * self.HEIGHT/2)
        start_row = int(end_row - self.WIDTH)
        for i in range(start_row, end_row):
            car = self.board[i]
            if car == 'A':
                ambulance_passed = True
            # Count blocking car if ambulance passed, car is present, and car not already counted
            elif ambulance_passed and car != '.' and car != prev_vehicle:
                blocking_count += 1
                prev_vehicle = car
        
        return blocking_count
    
    # Heuristic 2: Number of blocked positions
    def perform_h2(self):
        # Count blocking cars in front of ambulance
        blocking_pos = 0
        ambulance_passed = False

        # Define and search third row 
        end_row = int(self.WIDTH * self.HEIGHT/2)
        start_row = int(end_row - self.WIDTH)
        for i in range(start_row, end_row):
            car = self.board[i]
            if car == 'A':
                ambulance_passed = True
            # Count blocking positions if ambulance passed and car is present
            elif ambulance_passed and car != '.':
                blocking_pos += 1
        
        return blocking_pos

    # Heuristic 3: Multiplied h1 with lambda
    def perform_h3(self):
        return self.perform_h1() * self.LAMBDA

    # Heuristic 4: Number of blocking vehicles plus minimum number of own blocking vehicles
    # - Estimate minimum number of moves to unblock the block vehicles and clear out the solution path by calculating minimum number of vehicles blocking the blocking vehicles
    def perform_h4(self):
        # Count blocking cars in front of ambulance
        blocking_count = 0
    
        prev_vehicle = ''
        prev_block_up, prev_block_down = 0, 0
        min_unblock_count = 0
        ambulance_passed = False

        # Define and search third row 
        start_third_ind = int(self.WIDTH * self.HEIGHT/2 - self.WIDTH)
        for i in range(0, self.WIDTH):
            car = self.board[start_third_ind + i]
            if car == 'A':
                ambulance_passed = True
            # Count blocking car if ambulance passed and car is present
            elif ambulance_passed and car != '.':
                if prev_vehicle != car:
                    blocking_count += 1
                
                # Search vertically for blocking cars 
                # TODO: Check orientation of car and only add blocking if vertically oriented
                prev_vehicle = car
                j = start_third_ind + i
                while j - self.WIDTH > 0:
                    j -= self.WIDTH
                    up_car = self.board[j]
                    if up_car != prev_vehicle:
                        prev_block_up += 1
                        prev_vehicle = up_car
                
                prev_vehicle = car
                j = start_third_ind + i
                while j + self.WIDTH < self.WIDTH*self.HEIGHT:
                    j += self.WIDTH
                    down_car = self.board[j]
                    if down_car != prev_vehicle:
                        prev_block_down += 1
                        prev_vehicle = down_car
                
                blocking_count += min(prev_block_up, prev_block_down)
                prev_vehicle = car
                prev_block_down = prev_block_up = 0


        return blocking_count