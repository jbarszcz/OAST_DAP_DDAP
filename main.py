from net.NetParser import NetParser
from algorithms import BruteForceAlgorithm
from algorithms.EvolutionaryAlgorithm import EvolutionaryAlgorithm

NET_FILE_NAME = "input_files/net4.txt"

if __name__ == "__main__":
    net_parser = NetParser()
    net = net_parser.parse_file(NET_FILE_NAME)

    # solution = BruteForceAlgorithm.compute(net, problem="DDAP")

    alg = EvolutionaryAlgorithm(seed=123,
                                net=net,
                                number_of_chromosomes=10,
                                max_generations_without_improvement=10,
                                percent_of_best_chromosomes=0.7,
                                crossover_probability=1.0
                                )
    a = alg.ddap()
