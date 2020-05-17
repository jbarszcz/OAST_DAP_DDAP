class Demand:

    def __init__(self, data, demand_id):
        self.node1 = data[0]
        self.node2 = data[1]
        self.volume = int(data[2]) #hd
        self.id = demand_id
        self.demand_paths = []

    def get_number_of_paths(self):
        return len(self.demand_paths)

        # 1 2 3 -> z jakiego wezla (1) do jakiego (2) i o jakiej wielkosci (3)