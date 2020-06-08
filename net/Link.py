class Link:

    def __init__(self, data):
        self.node1 = data[0]
        self.node2 = data[1]
        self.number_of_modules = int(data[2])
        self.unit_cost = int(data[3])
        self.module = int(data[4])