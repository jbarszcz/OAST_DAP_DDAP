from net import Net
import math
import random
from pprint import pformat

INITIAL_COST = float('inf')  # for evolutionary algorithms


class Chromosome(object):
    def __init__(self, allocation_pattern: dict):
        self.allocation_pattern = allocation_pattern
        self.link_values = []  # link loads (DAP) / link sizes (DDAP)
        self.number_of_genes = 0
        self.z = INITIAL_COST

    def add_flow_values(self, new_mappings: dict):
        self.allocation_pattern = {**self.allocation_pattern, **new_mappings}

    def get_gene(self, demand_id):
        return {key: value for key, value in self.allocation_pattern.items() if key[0] == demand_id}

    def add_gene(self, gene: dict):
        self.add_flow_values(gene)
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
        link_values = [0] * len(net.links)
        paths = net.get_all_demand_paths()
        for link_id, link in enumerate(links):
            volume_sum = 0
            for path in paths:
                if link_id + 1 in path.links:
                    volume = self.allocation_pattern.get((path.demand_id, path.path_id))
                    volume_sum += volume
            link_values[link_id] = math.ceil(volume_sum / link.module) if problem == "DDAP" else volume_sum
            self.link_values = link_values

    def calculate_z(self, net: Net, problem: str):
        return self.calculate_ddap_cost(net) if problem == "DDAP" else self.calculate_dap_cost(net)

    def calculate_ddap_cost(self, net) -> float:
        z = 0
        for link_id, link_size in enumerate(self.link_values):
            z += net.links[link_id].unit_cost * link_size
        self.z = z
        return z

    def calculate_dap_cost(self, net):
        z = float('-inf')
        for i, link_load in enumerate(self.link_values):
            _z = link_load - net.links[i].number_of_modules * net.links[i].module
            if _z > z:
                z = _z
        self.z = z
        return z

    def __str__(self):
        text = "Flows for (demand, path):\n" + \
               pformat(self.allocation_pattern) + \
               f"\n\nLink loads/sizes:" f" {self.link_values}" \
               f"\nz = {self.z}"
        return text
