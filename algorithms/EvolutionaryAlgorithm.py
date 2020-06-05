from net.Solution import Solution
from net.Demand import Demand
from net.Net import Net
from typing import List
from itertools import product
from algorithms.algorithm_utils import *
import random
import math


class EvolutionaryAlgorithm:
    def __init__(self, seed: int, net: Net, number_of_chromosomes: int, max_generations_without_improvement: int,
                 percent_of_best_chromosomes: float, crossover_probability: float):
        random.seed(seed)
        self.net = net
        self.number_of_chromosomes = number_of_chromosomes
        self.generation = 0
        self.max_generations_without_improvement = max_generations_without_improvement
        self.crossover_probability = crossover_probability

        self.percent_of_best_chromosomes = percent_of_best_chromosomes
        self.number_of_best_chromosomes = round(number_of_chromosomes * percent_of_best_chromosomes)
        self.population_padding = number_of_chromosomes - self.number_of_best_chromosomes

    def ddap(self) -> Solution:
        population = self.get_initial_population()
        best_cost = float('inf')
        best_solution = None

        progress_counter = 0
        lack_of_improvement_counter = 0

        while (self.compute_next()):
            best_chromosome = Solution({})
            for chromosome in population:
                if chromosome.calculate_ddap_cost(self.net) < best_chromosome.cost:
                    best_chromosome = chromosome

            # sortowanie populacji wg kosztów chromosomów
            population = self.upgrade_population(population, best_chromosome, "DDAP")

            # krzyzowanie
            children = []
            while population:
                parents = random.sample(population, 2)
                population.remove(parents[0])
                population.remove(parents[1])
                children += (self.crossover(parents) if self.perform_crossover() else parents)

            population = children

            print("End of generation")

        print("End")
        return Solution({})

    def upgrade_population(self, population: List, padding_chromosome: Solution, algorithm: str):
        sort_criteria = (lambda x: x.cost) if algorithm == "DDAP" else (
            lambda x: x.number_of_links_with_exceeded_capacity)
        population.sort(key=sort_criteria)
        best_chromosomes = population[:self.number_of_best_chromosomes]
        return best_chromosomes + [padding_chromosome] * self.population_padding

    def crossover(self, parents):
        father = parents[0]
        mother = parents[1]
        brother = Solution({})
        sister = Solution({})

        number_of_genes = father.number_of_genes

        for gene_number in range(number_of_genes):
            if coin_toss():
                brother.add_gene(father.get_gene(gene_number + 1))
                sister.add_gene(mother.get_gene(gene_number + 1))
            else:
                brother.add_gene(mother.get_gene(gene_number + 1))
                sister.add_gene(father.get_gene(gene_number + 1))

        return [brother, sister]

    def get_initial_population(self) -> List:
        # dla kazdego demandu lista kombinacji sciezek i przeplywow
        all_genes_combinations = [get_solutions_for_one_demand(demand) for demand in self.net.demands]
        chromosomes = []

        # tworzymy chromosomy, czyli losowe rozwiazania dla kazdego demandu
        for i in range(self.number_of_chromosomes):
            chromosome = Solution({})
            for gene_combination in all_genes_combinations:
                gene = random.choice(gene_combination).allocation_pattern
                chromosome.add_gene(gene)
            chromosome.calculate_link_capacities(self.net)
            chromosomes.append(chromosome)

        population = [random.choice(chromosomes) for _ in range(self.number_of_chromosomes)]  # dlaczego tak jest??

        return population

    def compute_next(self) -> bool:
        return True

    def perform_crossover(self) -> bool:
        return random.random() < self.crossover_probability
