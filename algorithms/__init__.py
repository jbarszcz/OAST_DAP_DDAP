from net.Demand import Demand
from net.Chromosome import Chromosome
from itertools import product
from typing import List


def get_all_possible_chromosomes_with_one_gene(demand: Demand) -> List[Chromosome]:  # get all flow combinations for one demand
    volume_split = range(demand.volume + 1)
    volume_split_for_each_path = [volume_split for i in range(demand.get_number_of_paths())]

    volume_split_combinations = [combination for combination in product(*volume_split_for_each_path) if
                                 sum(combination) == demand.volume]

    solutions = [Chromosome(create_gene(combination, demand)) for combination in volume_split_combinations]
    return solutions


def create_gene(combination: tuple, demand: Demand):
    allocation_vector = {}  # kolumna_tabeli
    for demand_path in demand.demand_paths:
        path_id = demand_path.path_id
        flow_xdp = (demand.id, path_id)
        allocation_vector[flow_xdp] = combination[path_id - 1]
    return allocation_vector
