from net.Chromosome import Chromosome
from net.Net import Net


class OutputWriter:
    def __init__(self, net):
        self.net = net

    def save_solution(self, solution: Chromosome, file_name: str):
        with open(file_name, "w+") as out_file:
            number_of_links = len(self.net.links)
            out_file.write(f"{number_of_links}\n\n")

            for link_id in range(number_of_links):
                out_file.write(f"{link_id + 1} ")
                out_file.write(f"{solution.link_loads[link_id]} ")
                out_file.write(f"{solution.link_sizes[link_id]}\n")

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

    @staticmethod
    def save_history(history, file_name: str):
        with open(file_name, "w+") as out_file:
            for generation, solution in enumerate(history):
                out_file.write("#" * 20 + f" Generation: {generation + 1} " + "#" * 20 + "\n\n")
                out_file.write(f"{solution}")
                out_file.write("\n")
                out_file.write("\n")
        print(f"History saved to: {file_name}")
