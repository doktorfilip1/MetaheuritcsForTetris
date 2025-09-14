from config import GAConfig
from ga.utils import set_seed
from ga.loop import run_ga
from ga.selection import make_selector
from tetris.sim import simulate_game
import json, os
from pathlib import Path

HERE = Path(__file__).parent
os.chdir(HERE)

SHEETS_PATH = HERE / "sheets.txt"
BEST_EVER_JSON = HERE / "best_ever.json"

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
        snapshot_path="best_ever.json",
        replay_best_after=True,
        replay_limit=cfg.write_frames_steps,
    )

    best_snap = {
        "generation": getattr(best, "generation", None),
        "fitness": float(best.fitness),
        "genome": [float(x) for x in best.code],
        "label": "best-ever",
    }
    BEST_EVER_JSON.write_text(json.dumps(best_snap, ensure_ascii=False), encoding="utf-8")

    print(f"\n[{cfg.selection}] Best-ever: fitness={best.fitness:.2f}, genome={[round(x,4) for x in best.code]}")
    print("Snapshot upisan:", BEST_EVER_JSON.name)

    print("Writing frames to sheets.txt ...")
    try:
        simulate_game(best.code, write_frames=True, max_steps=cfg.write_frames_steps)
    except TypeError:
        simulate_game(best.code, write_frames=True)

    if SHEETS_PATH.exists():
        print("Done. sheets.txt →", SHEETS_PATH.resolve())
    else:
        print(
            "Error"
        )

if __name__ == "__main__":
    main()
