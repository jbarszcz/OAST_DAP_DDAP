import math
import itertools
from net.Point import Point
import collections


def get_all_combinations_for_demand(demand):
    # number_of_combinations_for_one_demand = math.comb(demand.get_number_of_paths() + demand.volume - 1,
    #                                                   demand.get_number_of_paths() - 1)
    _list = range(demand.volume + 1)
    lists = [_list for i in range(demand.get_number_of_paths())]
    solutions = []

    combinations = [combination for combination in itertools.product(*lists) if sum(combination) == demand.volume]
    for combination in combinations:
        map_values_of_one_demand = {}
        for demand_path in demand.demand_paths:
            path_id = demand_path.path_id
            map_values_of_one_demand[Point(demand.id, path_id)] = combination[path_id - 1]
        solutions.append(Solution(map_values_of_one_demand))
    return solutions


def get_solutions(net):
    all_combinations_all_demands = [get_all_combinations_for_demand(demand) for demand in net.demands]
    indexes = [range(len(combination)) for combination in all_combinations_all_demands]
    combinations_indexes = list(itertools.product(*indexes))

    print("hello")


class Solution(object):
    # def __init__(self, cost: float, values: []):
    #     self.cost = cost
    #     self.values = values

    def __init__(self, map_values):
        self.map_values = map_values

    # def compare(self, other):
    #     if other.cost < self.cost:
    #         return other
    #     elif other.cost == self.cost:
    #         self.append(other.values[0])
    #         return self
    #     else:
    #         return self
    #
    # def append(self, new_solution: []):
    #     self.values.append(new_solution)

    # def print(self, network: Network, solve_number: int):
    #
    #     row_format = "{:<7}" + "{:^5}" * network.number_of_demands
    #     demand_list = ["[%s]" % x for x in range(1, network.number_of_demands + 1)]
    #     path_list = ["[%s]" % x for x in range(1, network.longest_demand_path + 1)]
    #     transposed_data = zip(*self.values[solve_number])
    #
    #     print('Routes: \\ Demands:')
    #     print(row_format.format("", *demand_list))
    #     for path_id, row in enumerate(transposed_data):
    #         print(row_format.format(path_list[path_id], *row))
    #     print(row_format.format("h(d):",
    #                             *[network.demands_list[x].demand_volume for x in range(len(network.demands_list))]))
    #     print("Solution cost: {}".format(self.cost))
    #     print("Is solution valid: {}".format(self.validate(network, solve_number)))
    #     print()
    #
    # def validate(self, network: Network, solve_number: int):
    #     valid = True
    #     for demand in range(len(self.values[solve_number])):
    #         demand_passed = sum(self.values[solve_number][demand])
    #         valid = valid and (demand_passed >= network.demands_list[demand].demand_volume)
    #
    #     return valid
