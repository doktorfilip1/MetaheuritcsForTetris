import random
from .individual import Individual

def mutate(ind: Individual, rate: float = 0.2, step: float = 0.3):
    for i in range(len(ind.code)):
        if random.random() < rate:
            ind.code[i] = max(0.0, min(1.0, ind.code[i] + random.uniform(-step, step)))
    ind.fitness = None
