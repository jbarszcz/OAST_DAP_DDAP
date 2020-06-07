from file_operations.NetParser import NetParser
from algorithms.EvolutionaryAlgorithm import EvolutionaryAlgorithm
from configparser import ConfigParser

# NET_FILE_NAME = "input_files/net4.txt"
NET_FILE_NAME = "input_files/net12_1.txt"
# NET_FILE_NAME = "input_files/net12_2.txt"

if __name__ == "__main__":
    config_parser = ConfigParser()
    config_parser.read("config.ini")

    net_parser = NetParser()
    net = net_parser.parse_file("input_files/" + config_parser.get("general", "input_file"))

    #    solution = BruteForceAlgorithm.compute(net, problem="DDAP") if NET_FILE_NAME =="input_files/net4.txt" else print("Dont brick your computer!")

    # lucky seed 12398789708769875786956486745464 best cost=32 2 130 iteracji
    EA = EvolutionaryAlgorithm(
        net=net,
        seed=config_parser.getint("EA", "seed"),
        number_of_chromosomes=config_parser.getint("EA", "number_of_chromosomes"),
        max_no_progress_generations=config_parser.getint("EA", "max_no_progress_generations"),
        max_generations=config_parser.getint("EA", "max_generations"),
        max_mutations=config_parser.getint("EA", "max_mutations"),
        max_time=config_parser.getint("EA", "max_time"),
        percent_of_best_chromosomes=config_parser.getfloat("EA", "percent_of_best_chromosomes"),
        crossover_probability=config_parser.getfloat("EA", "crossover_probability"),
        mutation_probability=config_parser.getfloat("EA", "mutation_probability")
    )

    problem = config_parser.get("general", "problem")
    solution = None
    if problem == "DDAP":
        solution = EA.ddap()
    elif problem == "DAP":
        solution = EA.dap()
    else:
        print(f"Incorrect problem: {problem}. Choose DAP or DDAP.")

    print(solution)
    pass
