import re
import os
from typing import List, Tuple
import matplotlib.pyplot as plt

BASE_DIR = r"C:\Users\Filip\Documents\GitHub\MetaheuritcsForTetris\game\plots"
ROULETTE_FILE = os.path.join(BASE_DIR, "roullete_selection.txt")
TOURNAMENT_FILE = os.path.join(BASE_DIR, "tournament_selection.txt")

GEN_LINE_RE = re.compile(
    r"^Gen\s+(?P<gen>\d+):\s*best_this_gen\s*=\s*(?P<best>[-+]?\d+(?:\.\d+)?)\b",
    re.IGNORECASE,
)

def parse_best_per_gen(path: str) -> List[Tuple[int, float]]:
    out: List[Tuple[int, float]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            m = GEN_LINE_RE.match(line.strip())
            if m:
                g = int(m.group("gen"))
                b = float(m.group("best"))
                out.append((g, b))
    out.sort(key=lambda t: t[0])
    dedup = []
    last_g = None
    for g, b in out:
        if g != last_g:
            dedup.append((g, b))
            last_g = g
    return dedup

def ensure_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def slice_to_n_gens(series: List[Tuple[int, float]], n: int) -> List[Tuple[int, float]]:
    return [(g, b) for (g, b) in series if g <= n]

def plot_pergen_comparison(
    roul: List[Tuple[int, float]],
    tourn: List[Tuple[int, float]],
    n_gens: int,
    save_path: str,
) -> None:

    r_sub = slice_to_n_gens(roul, n_gens)
    t_sub = slice_to_n_gens(tourn, n_gens)

    rx, ry = zip(*r_sub) if r_sub else ([], [])
    tx, ty = zip(*t_sub) if t_sub else ([], [])

    plt.figure(figsize=(12, 6.5))
    plt.plot(rx, ry, color="red", linewidth=2.5, label=f"Roulette (Gen {n_gens})")
    plt.plot(tx, ty, color="blue", linewidth=2.5, label=f"Tournament (Gen {n_gens})")

    # tačke radi lepšeg osećaja promene
    if rx:
        plt.scatter(rx, ry, color="red", s=22)
    if tx:
        plt.scatter(tx, ty, color="blue", s=22)

    plt.title(f"Fitness po generacijama do {n_gens} (Roulette vs. Tournament)")
    plt.xlabel("Generacija")
    plt.ylabel("Fitness (best_this_gen)")
    plt.grid(True, alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()

def main():
    ensure_dir(BASE_DIR)

    roulette_series = parse_best_per_gen(ROULETTE_FILE)
    tournament_series = parse_best_per_gen(TOURNAMENT_FILE)

    for n in (25, 50, 100):
        out_path = os.path.join(BASE_DIR, f"compare_pergen_{n}.png")
        plot_pergen_comparison(roulette_series, tournament_series, n, out_path)
        print(f"[OK]: {out_path}")

if __name__ == "__main__":
    main()