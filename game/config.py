from dataclasses import dataclass

@dataclass
class GAConfig:

    gens: int = 25
    pop_size: int = 10
    genome_size: int = 6
    elitism: int = 1
    mutation_rate: float = 0.3
    max_steps: int = None

    selection: str = "tournament"   # "tournament" | "roulette" | "boltzmann"
    tournament_k: int = 2
    temperature0: float = 1.0
    temp_decay: float = 0.99

    stagnation_patience: int = 10
    immigrant_fraction: float = 0.3

    seed: int = 42
    write_frames_steps: int = 800
    log_file: str = "results.csv"
