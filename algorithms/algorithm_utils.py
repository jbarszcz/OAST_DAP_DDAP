from net.Demand import Demand
from net.Solution import Solution
from itertools import product
from typing import List
import random


def get_solutions_for_one_demand(demand: Demand) -> List[Solution]:  # get all flow combinations for one demand
    volume_split = range(demand.volume + 1)
    volume_split_for_each_path = [volume_split for i in range(demand.get_number_of_paths())]

    volume_split_combinations = [combination for combination in product(*volume_split_for_each_path) if
                                 sum(combination) == demand.volume]

    solutions = [Solution(create_flow_value_mapping(combination, demand)) for combination in volume_split_combinations]
    return solutions


def create_flow_value_mapping(combination: tuple, demand: Demand):
    flow_volume_mappings = {}  # kolumna_tabeli
    for demand_path in demand.demand_paths:
        path_id = demand_path.path_id
        flow_xdp = (demand.id, path_id)
        flow_volume_mappings[flow_xdp] = combination[path_id - 1]
    return flow_volume_mappings


def add_mappings(old: dict, new: dict) -> dict:
    return {**old, **new}


def coin_toss() -> bool:
    return random.random() > 0.5

# X = namedtuple("X", ["demand", "path"])
