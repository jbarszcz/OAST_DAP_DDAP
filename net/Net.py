from net.Demand import Demand
from net.Link import Link


class Net:
    def __init__(self):
        self.links = []
        self.demands = []

    def get_link(self, link_id) -> Link:
        return self.links[link_id - 1]

    def get_demand(self, demand_id) -> Demand:
        return self.demands[demand_id - 1]
