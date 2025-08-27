import json
import argparse
from tetris.sim import simulate_game

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", default="best_snapshot.json")
    ap.add_argument("--sheets",   default="sheets.txt")
    ap.add_argument("--runmeta",  default="run_meta.json")
    args = ap.parse_args()

    with open(args.snapshot, "r", encoding="utf-8") as f:
        snap = json.load(f)

    genome = snap["genome"]
    pieces = snap.get("pieces")

    simulate_game(genome, write_frames=True, piece_sequence=pieces)

    fitness = simulate_game(genome, write_frames=False, piece_sequence=pieces)

    meta = {
        "generation": snap.get("generation", "best"),
        "fitness": float(fitness),
        "genome": [float(x) for x in genome],
    }
    with open(args.runmeta, "w", encoding="utf-8") as f:
        json.dump(meta, f)

    print(f"OK: napisano {args.sheets} i {args.runmeta}")

if __name__ == "__main__":
    main()
