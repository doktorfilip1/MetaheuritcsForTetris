from config import GAConfig
from ga.utils import set_seed
from ga.loop import run_ga
from ga.selection import make_selector
from tetris.sim import simulate_game


def make_sim(cfg):
    def f(alpha, **kwargs):
        return simulate_game(alpha, max_steps=cfg.max_steps, **kwargs)
    return f


def main():
    cfg = GAConfig()
    set_seed(cfg.seed)

    selector = make_selector(cfg.selection, k=cfg.tournament_k)

    best, hist = run_ga(
        simulate_game=simulate_game,
        pop_size=cfg.pop_size,
        genome_size=cfg.genome_size,
        gens=cfg.gens,
        elitism=cfg.elitism,
        selector=selector,
        mutation_rate=cfg.mutation_rate,
        stagnation_patience=cfg.stagnation_patience,
        immigrant_fraction=cfg.immigrant_fraction,
        save_best_snapshot=True,
        snapshot_path="best_snapshot.json",
        replay_best_after=True,  # odmah snimi sheets.txt za GUI
        replay_limit=None,
    )

    print(f"\n[{cfg.selection}] Best ever: fitness={best.fitness:.2f}, genome={[round(x,4) for x in best.code]}")
    print("Writing frames to sheets.txt ...")
    simulate_game(best.code, write_frames=True, max_steps=cfg.write_frames_steps)
    print("Done.")

if __name__ == "__main__":
    main()
