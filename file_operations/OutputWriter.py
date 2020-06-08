from net.Solution import Solution
from net.Net import Net


class OutputWriter:
    def __init__(self, net):
        self.net = net

    def save_solution(self, solution: Solution, file_name: str):
        with open(file_name, "w+") as out_file:
            # number of links
            number_of_link_loads = len(solution.link_sizes)
            out_file.write(f"{number_of_link_loads}\n\n")

            for link_id, fibers in enumerate(solution.link_sizes):
                out_file.write(f"{link_id + 1} ")
                signals = self.net.links[link_id].module * fibers
                out_file.write(f"{signals} ")
                out_file.write(f"{fibers}\n")

            out_file.write("\n")
            number_of_demands = len(self.net.demands)

            out_file.write(f"{number_of_demands}\n\n")

            for i in range(number_of_demands):
                gene = solution.get_gene(i + 1)
                used_flows = {key: val for key, val in gene.items() if val > 0}
                out_file.write(f"{i + 1} ")
                out_file.write(f"{len(used_flows)}\n")

                for key in used_flows.keys():
                    out_file.write(f"{key[1]} {used_flows[key]}\n")
                out_file.write("\n")

            print(f"Output saved to: {file_name}")
