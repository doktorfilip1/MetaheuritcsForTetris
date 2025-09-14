import random
from typing import List, Callable
from .individual import Individual


def tournament_selection(pop: List[Individual], k: int = 5) -> Individual:
    best = None
    for _ in range(k):
        cand = random.choice(pop)
        if best is None or cand.fitness > best.fitness:
            best = cand
    return best

def roulette_selection(pop: List[Individual]) -> Individual:
    fits = [ind.fitness for ind in pop]
    min_fit = min(fits)
    eps = 1e-9
    weights = [(f - min_fit + eps) for f in fits]
    total = sum(weights)
    if total <= 0:
        return random.choice(pop)
    r = random.random() * total
    cum = 0.0
    for ind, w in zip(pop, weights):
        cum += w
        if cum >= r:
            return ind
    return pop[-1]


def make_selector(name: str, **kwargs) -> Callable[[List[Individual]], Individual]:
    name = name.lower()
    if name == "tournament":
        k = kwargs.get("k", 5)
        return lambda pop: tournament_selection(pop, k=k)
    if name == "roulette":
        return lambda pop: roulette_selection(pop)
    raise ValueError(f"Unknown selection: {name}")