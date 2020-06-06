from net.NetParser import NetParser
from algorithms import BruteForceAlgorithm
from algorithms.EvolutionaryAlgorithm import EvolutionaryAlgorithm

#NET_FILE_NAME = "input_files/net4.txt"
NET_FILE_NAME = "input_files/net12_1.txt"
#NET_FILE_NAME = "input_files/net12_2.txt"

if __name__ == "__main__":
    net_parser = NetParser()
    net = net_parser.parse_file(NET_FILE_NAME)

#    solution = BruteForceAlgorithm.compute(net, problem="DDAP") if NET_FILE_NAME =="input_files/net4.txt" else print("Dont brick your computer!")

    # lucky seed 12398789708769875786956486745464
    alg = EvolutionaryAlgorithm(seed=12398789708769875786956486745464,
                                net=net,
                                number_of_chromosomes=1000,
                                max_generations_without_improvement=10,
                                percent_of_best_chromosomes=0.7,
                                crossover_probability=0.6,
                                mutation_probability=0.00
                                ).ddap()

