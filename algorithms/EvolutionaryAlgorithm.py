from net.Chromosome import Chromosome
from net.Net import Net
from typing import List
import random
import copy
from time import time
import algorithms


class EvolutionaryAlgorithm:
    def __init__(self,
                 problem: str,
                 seed: int,
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

        self.problem = problem
        self.net = net
        self.number_of_chromosomes = number_of_chromosomes
        self.generation = 0
        self.no_progress = 0
        self.mutations = 0
        self.max_generations = max_generations
        self.max_mutations = max_mutations
        self.max_no_progress_generations = max_no_progress_generations
        self.max_time = max_time
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability

        self.start_time = None
        self.history = []

        self.percent_of_best_chromosomes = percent_of_best_chromosomes
        self.number_of_best_chromosomes = round(number_of_chromosomes * percent_of_best_chromosomes)
        self.population_padding = number_of_chromosomes - self.number_of_best_chromosomes

    def compute(self) -> Chromosome:
        population = self._get_initial_population()
        final_solution = Chromosome({})
        self.start_time = time()

        while not self._end():
            self.generation += 1
            best_chromosome_in_generation = Chromosome({})

            for chromosome in population:
                chromosome.calculate_links_for_problem(self.net, self.problem)
                if chromosome.calculate_z(self.net, self.problem) < best_chromosome_in_generation.z:
                    best_chromosome_in_generation = copy.deepcopy(
                        chromosome)

            self.history.append(best_chromosome_in_generation)

            print(f"Generation: {self.generation} cost: {best_chromosome_in_generation.z}")

            if best_chromosome_in_generation.z < final_solution.z:
                final_solution = copy.deepcopy(best_chromosome_in_generation)
                self.no_progress = 0
            else:
                self.no_progress += 1

            # eliminacja najslabszych osobnikow
            population = self._select_fittest(population)

            # krzyzowanie
            crossed_population = []
            while len(population) > 1:
                parents = random.sample(population, 2)
                population.remove(parents[0])
                population.remove(parents[1])
                crossed_population += (self._crossover(parents) if self._crossover_occurs() else parents)

            population += crossed_population

            # mutacja
            for chromosome in population:
                if self._mutation_occurs():  # chromosome mutation
                    for i in range(chromosome.number_of_genes):
                        if self._mutation_occurs():  # gene mutation
                            chromosome.mutate_gene(i + 1)
                            self.mutations += 1

        print(f"Computation ended in {round(time() - self.start_time, 2)} s.")
        return final_solution

    def _select_fittest(self, population: List):
        population.sort(key=lambda x: x.z)
        best_chromosomes = population[:self.number_of_best_chromosomes]
        padding = [copy.deepcopy(best_chromosomes[i]) for i in range(self.population_padding)]
        return best_chromosomes + padding

    def _crossover(self, parents):
        father = parents[0]
        mother = parents[1]
        brother = Chromosome({})
        sister = Chromosome({})

        number_of_genes = father.number_of_genes

        for gene_number in range(number_of_genes):
            if self._coin_toss():
                brother.add_gene(father.get_gene(gene_number + 1))
                sister.add_gene(mother.get_gene(gene_number + 1))
            else:
                brother.add_gene(mother.get_gene(gene_number + 1))
                sister.add_gene(father.get_gene(gene_number + 1))

        return [brother, sister]

    def _get_initial_population(self) -> List:
        all_genes_combinations = [algorithms.get_all_possible_chromosomes_with_one_gene(demand) for demand in
                                  self.net.demands]
        chromosomes = []

        for i in range(self.number_of_chromosomes):
            chromosome = Chromosome({})
            for gene_combination in all_genes_combinations:
                gene = random.choice(gene_combination).allocation_pattern
                chromosome.add_gene(gene)
            chromosome.calculate_links_for_problem(self.net, problem=self.problem)
            chromosomes.append(chromosome)

        random.shuffle(chromosomes)
        return chromosomes

    def _end(self) -> bool:
        time_exceeded = time() - self.start_time >= self.max_time
        if time_exceeded:
            print("Computation stopped because of time limit.")
            return True

        generations_exceeded = self.generation >= self.max_generations
        if generations_exceeded:
            print("Computation stopped because of generations limit.")
            return True

        mutations_exceeded = self.mutations >= self.max_mutations
        if mutations_exceeded:
            print("Computation stopped because of mutations limit.")
            return True

        no_progress = self.no_progress >= self.max_no_progress_generations
        if no_progress:
            print("Computation stopped because of no progress limit.")
            return True

        return False

    def _crossover_occurs(self) -> bool:
        return random.random() < self.crossover_probability

    def _mutation_occurs(self) -> bool:
        return random.random() < self.mutation_probability

    @staticmethod
    def _coin_toss() -> bool:
        return random.random() > 0.5
