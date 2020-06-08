from net import Net
import math
import random
from pprint import pformat

INITIAL_COST = float('inf')  # for evolutionary algorithms


class Solution(object):
    def __init__(self, flow_volume_mappings: dict):
        # slownik mapujacy tuple (demand_id, path_id) na volume jaki jest przydzialony
        self.allocation_pattern = flow_volume_mappings
        self.link_sizes = []
        self.number_of_links_with_exceeded_capacity = 0
        self.cost = INITIAL_COST
        self.number_of_genes = 0
        self.maximum_link_overload = INITIAL_COST

    def add_mappings(self, new_mappings: dict):
        self.allocation_pattern = {**self.allocation_pattern, **new_mappings}

    def get_gene(self, demand_id):
        return {key: value for key, value in self.allocation_pattern.items() if key[0] == demand_id}

    def add_gene(self, gene: dict):
        self.add_mappings(gene)
        self.number_of_genes += 1

    def mutate_gene(self, gene_number):
        gene = self.get_gene(gene_number)
        if len(gene) > 1:  # we cant mutate gene with only one value
            flows = random.sample(list(gene), 2)
            if self.allocation_pattern[flows[0]] > 0:
                self.allocation_pattern[flows[0]] -= 1
                self.allocation_pattern[flows[1]] += 1

    def calculate_links(self, net: Net, problem: str):
        links = net.links
        link_sizes = [0] * len(net.links)
        link_loads = [0] * len(net.links)
        paths = net.get_all_demand_paths()
        for link_id, link in enumerate(links):
            volume_sum = 0
            for path in paths:
                if link_id + 1 in path.links:
                    volume = self.allocation_pattern.get((path.demand_id, path.path_id))
                    volume_sum += volume
            link_sizes[link_id] = math.ceil(volume_sum / link.module)  # wyklad str 14
            link_loads[link_id] = volume_sum
        self.link_sizes = link_sizes
        self.link_loads = link_loads

    def calculate_ddap_cost(self, net) -> float:
        z = 0
        for link_id, link_size in enumerate(self.link_sizes):
            z += net.links[link_id].unit_cost * link_size
        self.cost = z
        return z

    def calculate_dap_cost(self, net):
        z = float('-inf')
        for i, link_load in enumerate(self.link_loads):
            _z = link_load - net.links[i].number_of_modules * net.links[i].module
            # _z = link_load - net.links[i].number_of_modules * net.links[i].module
            if _z > z:
                z = _z
        self.maximum_link_overload = z
        return z

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

    def __str__(self):
        text = "Flows for (demand, path):\n" + pformat(
            self.allocation_pattern) + f"\n\nLink loads: {self.link_sizes}\n\nCost: {self.cost}"
        # return text
        # return str(self.allocation_pattern)
        # return str(hash(str(self.allocation_pattern))) + " " + str(self.allocation_pattern)
        return text
