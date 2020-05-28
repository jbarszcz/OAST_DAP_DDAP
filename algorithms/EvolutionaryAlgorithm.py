from net.Solution import Solution
from net.Demand import Demand
from net.Net import Net
from typing import List
from itertools import product
from algorithms.algorithm_utils import *
import random


class EvolutionaryAlgorithm:
    def __init__(self, seed: int, net: Net, number_of_chromosomes: int):
        random.seed(seed)
        self.net = net
        self.number_of_chromosomes = number_of_chromosomes

    def ddap(self) -> Solution:
        initial_population = self.get_initial_population()
        best_cost = float('inf')

        # tutaj petla while not stop

        best_solution_of_generation = Solution({})
        for chromosome in initial_population:
            population_cost = 0
            cost = chromosome.calculate_ddap_cost(self.net)
            if cost:
                pass #######

        return Solution({})

    def get_initial_population(self):
        all_genes = [get_solutions_for_one_demand(demand) for demand in
                     # dla kazdego demandu lista kombinacji sciezek i przeplywow
                     self.net.demands]

        chromosomes = []
        for i in range(self.number_of_chromosomes):  # tworzymy chromosomy, czyli losowe rozwiazania dla kazdego demandu
            chromosome_values = {}
            for gene in all_genes:
                random_int = random.randint(0, len(gene) - 1)
                allocation_pattern = random.choice(gene).allocation_pattern
                chromosome_values = add_mappings(chromosome_values, allocation_pattern)
                chromosome = Solution(chromosome_values)
            chromosome.calculate_link_capacities(self.net)
            chromosomes.append(chromosome)

        population = [random.choice(chromosomes) for _ in range(self.number_of_chromosomes)]  # dlaczego tak jest??

        return population
