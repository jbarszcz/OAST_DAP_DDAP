from net import Net
import math


class Solution(object):
    def __init__(self, flow_volume_mappings: dict):
        # slownik mapujacy tuple (demand_id, path_id) na volume jaki jest przydzialony
        self.flow_volume_mappings = flow_volume_mappings
        self.link_capacities = []
        self.number_of_links_with_exceeded_capacity = 0

    def add_mappings(self, new_mappings: dict):
        self.flow_volume_mappings = {**self.flow_volume_mappings, **new_mappings}

    def calculate_link_capacities(self, net: Net) -> list:
        links = net.links
        capacities = [0] * len(net.links)
        paths = net.get_all_demand_paths()
        for link_id, link in enumerate(links):
            volume_sum = 0
            for path in paths:
                if link_id + 1 in path.links:
                    volume = self.flow_volume_mappings.get((path.demand_id, path.path_id))
                    volume_sum += volume
            capacities[link_id] = math.ceil(volume_sum / link.module)

        self.link_capacities = capacities
        return self.link_capacities
