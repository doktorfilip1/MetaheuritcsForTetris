from typing import Callable, List, Tuple, Any, Optional, Dict
import json

from .individual import Individual
from .mutation import mutate
from .crossover import single_point

def _write_run_meta(gen_idx: int, best_genome, best_fitness) -> None:
    data = {
        "generation": int(gen_idx),
        "fitness": float(best_fitness),
        "genome": [float(x) for x in best_genome],
    }
    with open("run_meta.json", "w", encoding="utf-8") as f:
        json.dump(data, f)

def _save_snapshot(path: str, data: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)

def run_ga(
    simulate_game: Callable[..., Any],
    pop_size: int,
    genome_size: int,
    gens: int,
    elitism: int,
    selector: Callable[[List[Individual]], Individual],
    mutation_rate: float,
    stagnation_patience: int = 20,
    immigrant_fraction: float = 0.2,
    save_best_snapshot: bool = True,
    snapshot_path: str = "best_snapshot.json",
    replay_best_after: bool = False,
    replay_limit: Optional[int] = None,
) -> Tuple[Individual, List[float]]:

    population = [Individual(genome_size) for _ in range(pop_size)]
    for ind in population:
        ind.evaluate(simulate_game)

    best_hist: List[float] = []
    best_overall = max(population, key=lambda i: i.fitness).clone()

    last_improvement_gen = 0
    best_so_far = best_overall.fitness

    snap = simulate_game(
        best_overall.code,
        write_frames=False,
        capture=True,
        max_steps=replay_limit
    )
    best_snapshot = {
        "generation": 0,
        "fitness": float(best_overall.fitness),
        "genome": best_overall.code[:],
        "pieces": snap.get("pieces_used", []),
        "label": "best-ever",
    }
    if save_best_snapshot:
        _save_snapshot(snapshot_path, best_snapshot)

    for g in range(gens):
        population.sort(key=lambda i: i.fitness, reverse=True)
        new_pop: List[Individual] = []

        new_pop.extend([population[i].clone() for i in range(min(elitism, len(population)))])

        while len(new_pop) < pop_size:
            p1 = selector(population)
            p2 = selector(population)
            c1, c2 = single_point(p1, p2)
            mutate(c1, rate=mutation_rate)
            mutate(c2, rate=mutation_rate)
            new_pop.append(c1)
            if len(new_pop) < pop_size:
                new_pop.append(c2)

        for ind in new_pop:
            ind.evaluate(simulate_game)
        population = new_pop

        best_gen = max(population, key=lambda i: i.fitness)

        if best_gen.fitness > best_so_far:
            best_so_far = best_gen.fitness
            last_improvement_gen = g

        if (g - last_improvement_gen) >= stagnation_patience:
            num_imm = max(1, int(pop_size * immigrant_fraction))
            population.sort(key=lambda i: i.fitness)
            for i in range(num_imm):
                population[i] = Individual(genome_size)
                population[i].evaluate(simulate_game)
            last_improvement_gen = g
            best_gen = max(population, key=lambda i: i.fitness)

        if best_gen.fitness > best_overall.fitness:
            best_overall = best_gen.clone()
            snap = simulate_game(
                best_overall.code,
                write_frames=False,
                capture=True,
                max_steps=replay_limit
            )
            best_snapshot = {
                "generation": g + 1,
                "fitness": float(best_overall.fitness),
                "genome": best_overall.code[:],
                "pieces": snap.get("pieces_used", []),
                "label": "best-ever",
            }
            if save_best_snapshot:
                _save_snapshot(snapshot_path, best_snapshot)

        best_hist.append(best_gen.fitness)

        mean_fit = sum(ind.fitness for ind in population) / len(population)
        print(
            f"Gen {g+1}: best_this_gen = {best_gen.fitness:.2f}, "
            f"mean_this_gen = {mean_fit:.2f}, "
            f"genome = {[round(x, 4) for x in best_gen.code]}"
        )

        _write_run_meta(g + 1, best_gen.code, best_gen.fitness)

    print(
        f"\nBest ever fitness = {best_overall.fitness:.2f}, "
        f"genome = {[round(x, 4) for x in best_overall.code]}"
    )

    final_meta = {
        "generation": int(best_snapshot.get("generation", 0)),
        "fitness": float(best_overall.fitness),
        "genome": [float(x) for x in best_overall.code],
        "label": "best-ever",
    }
    with open("run_meta.json", "w", encoding="utf-8") as f:
        json.dump(final_meta, f)

    if replay_best_after and best_snapshot is not None:
        simulate_game(
            best_snapshot["genome"],
            write_frames=True,
            piece_sequence=best_snapshot.get("pieces", []),
            max_steps=replay_limit,
        )
        print("Replayed best-ever and wrote frames to sheets.txt")

    return best_overall, best_hist