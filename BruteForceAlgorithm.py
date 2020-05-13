import math
import itertools


def get_all_combinations_for_demand(demand):
    # number_of_combinations_for_one_demand = math.comb(demand.get_number_of_paths() + demand.volume - 1,
    #                                                   demand.get_number_of_paths() - 1)
    _list = range(demand.volume + 1)
    lists = [_list for i in range(demand.get_number_of_paths())]

    combinations = [combination for combination in itertools.product(*lists) if sum(combination) == demand.volume]

    return combinations
