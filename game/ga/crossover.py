import random
from .individual import Individual

def single_point(p1: Individual, p2: Individual):
    point = random.randint(1, len(p1.code) - 1)
    c1 = p1.clone(); c2 = p2.clone()
    c1.code = p1.code[:point] + p2.code[point:]
    c2.code = p2.code[:point] + p1.code[point:]
    c1.fitness = None; c2.fitness = None
    return c1, c2
