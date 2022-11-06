
class Puzzle:
    def __init__(self, board, test_case, car_dict, runtime=0, search_path=[], solution_path=[]):
        self.board = board
        self.test_case = test_case
        self.runtime = runtime
        self.car_dict = car_dict
        self.search_parh = search_path
        self.solution_path = solution_path
        self.final_fuel = []

    def __str__(self):
        return f'Puzzle: {self.board}'