class Link:

    def __init__(self, data):
        self.node1 = data[0]  # node1 id
        self.node2 = data[1]  # node2 id
        self.number_of_modules = int(data[2])  # do DAP - przeplywnosc (number of fibre pairs in cable)
        self.unit_cost = int(data[3])  # do DDAP
        self.module = int(data[4])  # do DDAP
