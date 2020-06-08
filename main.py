from file_operations.NetParser import NetParser
from file_operations.OutputWriter import OutputWriter
from algorithms.EvolutionaryAlgorithm import EvolutionaryAlgorithm
from algorithms import BruteForceAlgorithm
from configparser import ConfigParser
import sys

# zapis trajektorii
# czas optymalizacji

if __name__ == "__main__":
    config_parser = ConfigParser()
    config_parser.read("config.ini")
    solution = None
    net_parser = NetParser()
    net = net_parser.parse_file("input_files/" + config_parser.get("general", "input_file"))

    problem = config_parser.get("general", "problem")
    algorithm = config_parser.get("general", "algorithm")
    input_file = config_parser.get("general", "input_file")

    if problem not in ["DAP", "DDAP"]:
        print(f"Incorrect problem: {problem}. Choose DAP or DDAP.")
        exit()

    if algorithm not in ["BFA", "EA"]:
        print(f"Incorrect problem: {algorithm}. Choose BFA or EA.")
        exit()

    if algorithm == "BFA" and input_file != "net4.txt":
        print("This may hang your computer.")
        exit()

    if algorithm == "BFA":
        solution = BruteForceAlgorithm.compute(net, problem=problem) if input_file in ["net4.txt",
                                                                                       "net_test.txt"] \
            else \
            print("Dont brick your computer!")

    elif algorithm == "EA":

        EA = EvolutionaryAlgorithm(
            problem=problem,
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

        solution = EA.compute()

    output_writer = OutputWriter(net=net)
    output_writer.save_solution(solution=solution, file_name=config_parser.get("general", "output_file"))
