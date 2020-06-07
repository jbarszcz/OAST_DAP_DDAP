from net.Solution import Solution
from net.Demand import Demand
from net.Net import Net
from typing import List
from itertools import product


def compute(net: Net, problem: str):
    demands = net.demands
    solutions = get_all_solutions(demands)
    print("calculating link capacities...")
    for solution in solutions:
        solution.calculate_link_capacities(net)

    if problem == "DDAP":
        print("solving ddap with bruteforce method...")
        ddap_solution = ddap(solutions, net)
        return ddap_solution

    if problem == "DAP":
        dap_solution = dap(solutions, net)
        print(dap_solution) if dap_solution else print("Couldn't solve the DAP problem.")
        return dap_solution


def ddap(solutions: List[Solution], net: Net) -> Solution:
    print("current best cost is: ", end="")
    best_cost = float("inf")
    best_solution = None
    for solution in solutions:
        cost = solution.calculate_ddap_cost(net)
        if cost < best_cost:
            best_cost = cost
            best_solution = solution
            print(f" {best_cost}", end="")
    print("\n-------")
    print(f"final best cost: {best_cost}")
    return best_solution


# def dap(solutions: List[Solution], net: Net):
#     for solution in solutions:
#         finished = True
#         for i, link_load in enumerate(solution.link_loads):
#             # odejmujemy obciazenie od pojemnosci lacza
#             if min(0, net.links[i].number_of_modules - link_load) < 0:
#                 finished = False
#                 break  # pojemnosc przekroczona
#         if finished:
#             return solution
#     return None

def dap(solutions: List[Solution], net: Net):
    print("current best cost is: ", end="")
    best_cost = float("inf")
    best_solution = None
    for solution in solutions:
        cost = solution.calculate_dap_cost(net)
        if cost < best_cost:
            best_cost = cost
            best_solution = solution
            print(f" {best_cost}", end="")
    print("\n-------")
    print(f"final best cost: {best_cost}")
    return best_solution


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


def get_all_solutions(demands: List[Demand]) -> List[Solution]:  # get all combinations of demands solutions
    # dla kazdego demandu jak moga sie rozkladac przeplywy
    all_combinations_all_demands = [get_solutions_for_one_demand(demand) for demand in demands]

    # blizniacza lista do powyzszej - kazdy rozklad przeplywow w demandzie otrzymuje swoj indeks
    indexes = [range(len(combination)) for combination in all_combinations_all_demands]

    # Iloczyn kartezjanski - wszystkie kombinacje wszystkich rozkladlow dla kazdego demandu
    # dla net4 = 810000(10*15*6*6*10*15).
    # Na ostatniej pozycji wartosci sa od 0 do 14, bo demand 6 ma 14 roznych kombinacji
    solution_indexes = list(product(*indexes))

    print("generating all possible solutions... ", end="")
    solutions = [get_complete_solution(all_combinations_all_demands, current_solution_index) for current_solution_index
                 in solution_indexes]
    print(f"{len(solutions)} found.")
    return solutions


def get_complete_solution(demand_combination_matrix: List[List[Solution]], current_solution: tuple) -> Solution:
    mapping = {}
    for demand_index, combination_index in enumerate(
            current_solution):  # to zawsze bedzie 6 dla net4 bo jest 6 demandow
        solution = demand_combination_matrix[demand_index][combination_index]
        mapping = _add_mappings(mapping, solution.allocation_pattern)
    return Solution(mapping)


def _add_mappings(old: dict, new: dict) -> dict:
    return {**old, **new}
