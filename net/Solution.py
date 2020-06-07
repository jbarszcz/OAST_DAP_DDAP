from net import Net
import math
import random
from pprint import pformat

INITIAL_COST = float('inf')  # for evolutionary algorithms


class Solution(object):
    def __init__(self, flow_volume_mappings: dict):
        # slownik mapujacy tuple (demand_id, path_id) na volume jaki jest przydzialony
        self.allocation_pattern = flow_volume_mappings
        self.link_loads = []
        self.number_of_links_with_exceeded_capacity = 0
        self.cost = INITIAL_COST
        self.number_of_genes = 0

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

    def calculate_link_capacities(self, net: Net) -> list:
        links = net.links
        capacities = [0] * len(net.links)
        paths = net.get_all_demand_paths()
        for link_id, link in enumerate(links):
            volume_sum = 0
            for path in paths:
                if link_id + 1 in path.links:
                    volume = self.allocation_pattern.get((path.demand_id, path.path_id))
                    volume_sum += volume
            capacities[link_id] = math.ceil(volume_sum / link.module)

        self.link_loads = capacities
        return self.link_loads

    def calculate_ddap_cost(self, net) -> float:
        cost = 0
        for link_id, link_cost in enumerate(self.link_loads):
            cost += net.links[link_id].unit_cost * self.link_loads[link_id]
        self.cost = cost
        return cost

    def __str__(self):
        text = "Flows for (demand, path):\n" + pformat(
            self.allocation_pattern) + f"\n\nLink loads: {self.link_loads}\n\nCost: {self.cost}"
        # return text
        # return str(self.allocation_pattern)
        # return str(hash(str(self.allocation_pattern))) + " " + str(self.allocation_pattern)
        return text
