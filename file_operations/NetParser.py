from net.Net import Net
from net.Link import Link
from net.Demand import Demand
from net.Route import Route


class NetParser:
    def __init__(self):
        pass

    @staticmethod
    def parse_line(raw_line: str):
        return raw_line.strip().split(" ")

    def parse_file(self, file_name: str):
        net = Net()
        with open(file_name) as net_file:
            # links
            number_of_links = int(net_file.readline())
            for i in range(number_of_links):
                link_data = self.parse_line(net_file.readline())
                link = Link(data=link_data)
                net.links.append(link)

            net_file.readline()  # -1 line
            net_file.readline()  # blank line

            # demands
            number_of_demands = int(net_file.readline())
            net_file.readline()  # blank line

            for demand_number in range(number_of_demands):
                demand_data = self.parse_line(net_file.readline())
                demand = Demand(data=demand_data, demand_id=demand_number + 1)
                number_of_demand_paths = int(net_file.readline())

                for demand_path_number in range(number_of_demand_paths):
                    demand_path_data = self.parse_line(net_file.readline())
                    demand_path = Route(data=demand_path_data, demand_id=demand_number + 1)
                    demand.demand_paths.append(demand_path)

                net.demands.append(demand)
                net_file.readline()  # blank line

        return net
