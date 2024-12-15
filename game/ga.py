import random

class Individual:
    def __init__(self, genome_size):
        # Težinski faktori za različite aspekte igre
        self.code = [random.uniform(-1, 1) for _ in range(genome_size)]
        self.fitness = None

    def calcFit(self, simulate_game):
        # Fitness funkcija simulira igru i vraća rezultat (npr. broj poena)
        self.fitness = simulate_game(self.code)
        return self.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness


def selection(population):
    TOURNAMENT_SIZE = 5
    best = None
    for _ in range(TOURNAMENT_SIZE):
        candidate = random.choice(population)
        if best is None or candidate.fitness > best.fitness:
            best = candidate
    return best


def crossover(parent1, parent2):
    point = random.randint(1, len(parent1.code) - 1)
    child1 = Individual(len(parent1.code))
    child2 = Individual(len(parent1.code))
    child1.code = parent1.code[:point] + parent2.code[point:]
    child2.code = parent2.code[:point] + parent1.code[point:]
    return child1, child2


def mutation(individual, mutation_rate=0.1):
    for i in range(len(individual.code)):
        if random.uniform(0, 1) < mutation_rate:
            individual.code[i] += random.uniform(-0.5, 0.5)
            individual.code[i] = max(-1, min(1, individual.code[i]))


# Dummy funkcija koja simulira igru i vraća rezultat na osnovu težinskih faktora
def simulate_game(weights):
    # Ova funkcija treba da simulira Tetris i koristi težinske faktore
    # Za jednostavnost, vraća nasumičan rezultat zasnovan na težinama
    return random.randint(0, 100) + sum(weights)


# Parametri genetskog algoritma
GENS = 50
POPULATION_SIZE = 50
GENOME_SIZE = 5  # Broj težinskih faktora (može se proširiti)

# Inicijalizacija populacije
population = [Individual(GENOME_SIZE) for _ in range(POPULATION_SIZE)]

# Prva evaluacija populacije
for individual in population:
    individual.calcFit(simulate_game)

# Glavna petlja genetskog algoritma
for generation in range(GENS):
    population.sort(reverse=True)
    new_population = []

    # Elitizam: Prenos najboljih jedinki
    ELITISM_COUNT = POPULATION_SIZE // 10
    new_population.extend(population[:ELITISM_COUNT])

    # Kreiranje nove populacije crossover-om i mutacijom
    while len(new_population) < POPULATION_SIZE:
        parent1 = selection(population)
        parent2 = selection(population)
        child1, child2 = crossover(parent1, parent2)
        mutation(child1)
        mutation(child2)
        child1.calcFit(simulate_game)
        child2.calcFit(simulate_game)
        new_population.append(child1)
        if len(new_population) < POPULATION_SIZE:
            new_population.append(child2)

    population = new_population

    # Najbolji pojedinac u generaciji
    best_individual = max(population, key=lambda ind: ind.fitness)
    print(f"Generation {generation + 1}: Best fitness = {best_individual.fitness}")

# Najbolji rezultat nakon evolucije
best_individual = max(population, key=lambda ind: ind.fitness)
print("Best genome:", best_individual.code)
