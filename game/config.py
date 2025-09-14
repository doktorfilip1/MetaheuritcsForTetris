from dataclasses import dataclass

@dataclass
class GAConfig:

    gens: int = 150
    pop_size: int = 50
    genome_size: int = 6
    elitism: int = 1
    mutation_rate: float = 0.25
    max_steps: int = None

    selection: str = "tournament"   # "tournament" | "roulette" | "boltzmann"
    tournament_k: int = 3

    stagnation_patience: int = 10
    immigrant_fraction: float = 0.3

    seed: int = 42
    write_frames_steps: int = 800