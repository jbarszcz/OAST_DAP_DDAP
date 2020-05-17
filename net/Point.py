class Point:
    def __init__(self, demand_id, path_id):
        self.demand_id = demand_id
        self.path_id = path_id

    # def __hash__(self):
    #     return hash((self.demand_id, self.path_id))
    #
    # def __eq__(self, other):
    #     return (self.demand_id, self.path_id) == (other.demand_id, other.path_id)
    #
    # def __ne__(self, other):
    #     return not (self == other)
