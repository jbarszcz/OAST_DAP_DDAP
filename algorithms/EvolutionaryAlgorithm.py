from net.Solution import Solution
from net.Demand import Demand
from net.Net import Net
from typing import List
from itertools import product
from algorithms.algorithm_utils import *
import random
import math
import copy
import time


class EvolutionaryAlgorithm:
    def __init__(self, seed: int,
                 net: Net,
                 number_of_chromosomes: int,
                 max_time: int,
                 max_generations: int,
                 max_mutations: int,
                 max_no_progress_generations: int,
                 percent_of_best_chromosomes: float,
                 crossover_probability: float,
                 mutation_probability: float
                 ):

        random.seed(seed)
        self.net = net
        self.number_of_chromosomes = number_of_chromosomes
        self.generation = 1
        self.no_progress = 0
        self.mutations = 0
        self.max_generations = max_generations
        self.max_mutations = max_mutations
        self.max_no_progress_generations = max_no_progress_generations
        self.max_time = max_time
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability

        self.start_time = None

        self.percent_of_best_chromosomes = percent_of_best_chromosomes
        self.number_of_best_chromosomes = round(number_of_chromosomes * percent_of_best_chromosomes)
        self.population_padding = number_of_chromosomes - self.number_of_best_chromosomes

    def ddap(self) -> Solution:
        population = self.get_initial_population()
        final_solution = Solution({})
        self.start_time = time.time()

        while not self.end():
            best_chromosome_in_generation = Solution({})

            for chromosome in population:
                if chromosome.calculate_ddap_cost(self.net) < best_chromosome_in_generation.cost:
                    best_chromosome_in_generation = copy.deepcopy(chromosome)

            if best_chromosome_in_generation.cost < final_solution.cost:
                final_solution = copy.deepcopy(best_chromosome_in_generation)
                self.no_progress = 0
            else:
                self.no_progress += 1

            # sortowanie populacji wg kosztów chromosomów
            population = self.select_fittest(population, algorithm="DDAP")

            # krzyzowanie
            crossed_population = []
            while population:
                parents = random.sample(population, 2)
                population.remove(parents[0])
                population.remove(parents[1])
                crossed_population += (self.crossover(parents) if self._crossover_occurs() else parents)

            population = crossed_population

            # mutacja
            for chromosome in population:
                if self._mutation_occurs():  # chromosome mutation
                    for i in range(chromosome.number_of_genes):
                        if self._mutation_occurs():  # gene mutation
                            chromosome.mutate_gene(i + 1)
                            self.mutations += 1

            for chromosome in population:
                chromosome.calculate_links(self.net)
                chromosome.calculate_ddap_cost(self.net)

            print(f"Generation: {self.generation} cost: {best_chromosome_in_generation.cost}")
            self.generation += 1

        return final_solution

    def dap(self) -> Solution:
        population = self.get_initial_population()
        final_solution = Solution({})
        self.start_time = time.time()

        while not self.end():
            best_chromosome_in_generation = Solution({})

            for chromosome in population:
                if chromosome.calculate_dap_cost(self.net) < best_chromosome_in_generation.maximum_link_overload:
                    best_chromosome_in_generation = copy.deepcopy(chromosome)

            if best_chromosome_in_generation.maximum_link_overload < final_solution.maximum_link_overload:
                final_solution = copy.deepcopy(best_chromosome_in_generation)
                self.no_progress = 0
            else:
                self.no_progress += 1

            # sortowanie populacji wg kosztów chromosomów
            population = self.select_fittest(population, algorithm="DAP")

            # krzyzowanie
            crossed_population = []
            while population:
                parents = random.sample(population, 2)
                population.remove(parents[0])
                population.remove(parents[1])
                crossed_population += (self.crossover(parents) if self._crossover_occurs() else parents)

            population = crossed_population

            # mutacja
            for chromosome in population:
                if self._mutation_occurs():  # chromosome mutation
                    for i in range(chromosome.number_of_genes):
                        if self._mutation_occurs():  # gene mutation
                            chromosome.mutate_gene(i + 1)
                            self.mutations += 1

            for chromosome in population:
                chromosome.calculate_links(self.net)
                chromosome.calculate_dap_cost(self.net)

            print(f"Generation: {self.generation} cost: {best_chromosome_in_generation.maximum_link_overload}")
            self.generation += 1

        return final_solution

    def select_fittest(self, population: List, algorithm: str):
        sort_criteria = (lambda x: x.cost) if algorithm == "DDAP" else (
            lambda x: x.maximum_link_overload)
        population.sort(key=sort_criteria)
        best_chromosomes = population[:self.number_of_best_chromosomes]
        padding = [copy.deepcopy(best_chromosomes[i]) for i in range(
            self.population_padding)]  # to nie powinny być identyczne chromosomy, tylko X najlepszych chromosomów
        return best_chromosomes + padding

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
            chromosome.calculate_links(self.net)
            chromosomes.append(chromosome)

        random.shuffle(chromosomes)

        return chromosomes

    def end(self) -> bool:
        time_exceeded = time.time() - self.start_time > self.max_time
        if time_exceeded:
            print("Computation stopped because of time limit.")
            return True

        generations_exceeded = self.generation > self.max_generations
        if generations_exceeded:
            print("Computation stopped because of generations limit.")
            return True

        mutations_exceeded = self.mutations > self.max_mutations
        if mutations_exceeded:
            print("Computation stopped because of mutations limit.")
            return True

        no_progress = self.no_progress > self.max_no_progress_generations
        if no_progress:
            print("Computation stopped because of no progress limit.")
            return True

        return False

    def _crossover_occurs(self) -> bool:
        return random.random() < self.crossover_probability

    def _mutation_occurs(self) -> bool:
        return random.random() < self.mutation_probability
