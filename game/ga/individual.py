import random
from dataclasses import dataclass, field
from typing import List, Callable

@dataclass
class Individual:
    genome_size: int
    code: List[float] = field(init=False)
    fitness: float | None = None

    def __post_init__(self):
        self.code = [random.uniform(0, 1) for _ in range(self.genome_size)]

    def evaluate(self, simulate_game: Callable[[list], float]) -> float:
        self.fitness = simulate_game(self.code)
        return self.fitness

    def clone(self) -> "Individual":
        c = Individual(self.genome_size)
        c.code = self.code[:]
        c.fitness = self.fitness
        return c
