class Demand:

    def __init__(self, data, demand_id):
        self.node1 = data[0]
        self.node2 = data[1]
        self.volume = data[2]
        self.id = demand_id
        self.demand_paths = []

        # 1 2 3 -> z jakiego wezla (1) do jakiego (2) i o jakiej wielkosci (3)