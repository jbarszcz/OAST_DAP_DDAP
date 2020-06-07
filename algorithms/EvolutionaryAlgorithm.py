from net.Solution import Solution
from net.Demand import Demand
from net.Net import Net
from typing import List
from itertools import product
from algorithms.algorithm_utils import *
import random
import math
import copy


class EvolutionaryAlgorithm:
    def __init__(self, seed: int,
                 net: Net,
                 number_of_chromosomes: int,
                 max_generations_without_improvement: int,
                 percent_of_best_chromosomes: float,
                 crossover_probability: float,
                 mutation_probability: float
                 ):

        random.seed(seed)
        self.net = net
        self.number_of_chromosomes = number_of_chromosomes
        self.generation = 1
        self.max_generations_without_improvement = max_generations_without_improvement
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability

        self.percent_of_best_chromosomes = percent_of_best_chromosomes
        self.number_of_best_chromosomes = round(number_of_chromosomes * percent_of_best_chromosomes)
        self.population_padding = number_of_chromosomes - self.number_of_best_chromosomes

    def ddap(self) -> Solution:
        population = self.get_initial_population()

        while not self.end():
            best_chromosome_previous_generation = Solution({})

            for chromosome in population:
                if chromosome.calculate_ddap_cost(self.net) < best_chromosome_previous_generation.cost:
                    best_chromosome_previous_generation = copy.deepcopy(chromosome)

            # sortowanie populacji wg kosztów chromosomów
            population = self.select_fittest(population, best_chromosome_previous_generation, algorithm="DDAP")

            # krzyzowanie
            crossed_population = []
            while population:
                parents = random.sample(population, 2)
                population.remove(parents[0])
                population.remove(parents[1])
                crossed_population += (self.crossover(parents) if self.crossover_occurs() else parents)

            population = crossed_population

            # mutacja
            for chromosome in population:
                if self.mutation_occurs():  # chromosome mutation
                    for i in range(chromosome.number_of_genes):
                        if self.mutation_occurs():  # gene mutation
                            chromosome.mutate_gene(i + 1)

            for chromosome in population:
                chromosome.calculate_link_capacities(self.net)
                chromosome.calculate_ddap_cost(self.net)

            print(f"Generation: {self.generation} cost: {best_chromosome_previous_generation.cost}")
            self.generation += 1

        print("End")
        return Solution({})

    def select_fittest(self, population: List, padding_chromosome: Solution, algorithm: str):
        sort_criteria = (lambda x: x.cost) if algorithm == "DDAP" else (
            lambda x: x.number_of_links_with_exceeded_capacity)
        population.sort(key=sort_criteria)
        best_chromosomes = population[:self.number_of_best_chromosomes]
        padding = [copy.deepcopy(best_chromosomes[i]) for i in range(self.population_padding)] # to nie powinny być identyczne chromosomy, tylko X najlepszych chromosomów
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
            chromosome.calculate_link_capacities(self.net)
            chromosomes.append(chromosome)

        random.shuffle(chromosomes)

        return chromosomes

    def end(self) -> bool:
        return False

    def crossover_occurs(self) -> bool:
        return random.random() < self.crossover_probability

    def mutation_occurs(self) -> bool:
        occurance = random.random() < self.mutation_probability
        return occurance
