import math
import itertools
from net.Flow import Flow
import collections
import sys


def compute(net):
    demands = net.demands
    solutions = get_solutions(demands)
    calculate_link_capacities(net, solutions)


def calculate_link_capacities(net, solutions):
    links = net.links
    capacities = [0] * len(net.links)
    paths = list(itertools.chain.from_iterable([demand.demand_paths for demand in net.demands]))  # do refactoru

    for i, link in enumerate(links):
        flow_sum = 0.0
        for j, demand_path in paths:
            pass


def get_all_combinations_for_demand(demand):
    _list = range(demand.volume + 1)
    lists = [_list for i in range(demand.get_number_of_paths())]

    volume_split_combinations = [combination for combination in itertools.product(*lists) if
                                 sum(combination) == demand.volume]

    solutions = [Solution(create_flow_value_mapping(combination, demand)) for combination in volume_split_combinations]
    return solutions


def create_flow_value_mapping(combination, demand):
    flow_volume_mappings = {}  # kolumna_tabeli
    for demand_path in demand.demand_paths:
        path_id = demand_path.path_id
        flow_xdp = (demand.id, path_id)
        flow_volume_mappings[flow_xdp] = combination[path_id - 1]
    return flow_volume_mappings


def get_solutions(demands):
    # dla kazdego demandu jak moga sie rozkladac przeplywy
    all_combinations_all_demands = [get_all_combinations_for_demand(demand) for demand in demands]

    # blizniacza lista do powyzszej - kazdy rozklad przeplywow w demandzie otrzymuje swoj indeks
    indexes = [range(len(combination)) for combination in all_combinations_all_demands]

    # iloczyn kartezjanski - wszystkie kombinacje wszystkich rozkladlow dla kazdego demandu (10*15*6*6*10*15). Na ostatniej pozycji wartosci sa od 0 do 14, bo demand 6 ma 14 roznych kombinacji
    solution_indexes = list(itertools.product(*indexes))

    number_of_solutions = len(solution_indexes)
    solutions = [get_solution(all_combinations_all_demands, i, solution_indexes) for i in range(number_of_solutions)]

    return solutions


# use: for idx, val in enumerate(ints): print(idx, val)
def get_solution(all_combinations_all_demands, i, solution_indexes):
    print(i)
    new_complete_solution = Solution({})
    current_solution = solution_indexes[i]
    for demand_index in range(len(current_solution)):  # to zawsze bedzie 6 dla net4 bo jest 6 demandow
        combination_index = current_solution[demand_index]
        solution_mapping = all_combinations_all_demands[demand_index][combination_index]
        new_complete_solution.add_mappings(solution_mapping.flow_volume_mappings)
    return new_complete_solution


class Solution(object):
    def __init__(self, flow_volume_mappings: dict):
        self.flow_volume_mappings = flow_volume_mappings  # slownik mapujacy tuple (demand_id, path_id) na volume jaki jest przydzialony

    def add_mappings(self, new_mappings: dict):
        self.flow_volume_mappings = {**self.flow_volume_mappings, **new_mappings}
