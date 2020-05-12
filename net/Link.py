class Link:

    def __init__(self, data, link_id):
        self.node1 = data[0]
        self.node2 = data[1]
        self.number_of_modules = data[2]
        self.unit_cost = data[3]
        self.module = data[4]
        self.id = link_id

# 1 2 72 1 2 -> z wezla nr 1, do wezla nr 2, 72 moduly, 1 = jednostkowy koszt, cost = modul, a wiec 72*2 = 144 jednostki zapotrzebowania
