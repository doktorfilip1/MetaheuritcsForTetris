import os, re, json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


BASE_DIR = r"C:\Users\Filip\Documents\GitHub\MetaheuritcsForTetris\game\plots"

roulette_path = Path(BASE_DIR) / "roullete_selection.txt"
tournament_path = Path(BASE_DIR) / "tournament_selection.txt"
if not tournament_path.exists():
    tournament_path = Path(BASE_DIR) / "tournament_selection.txt"


out_dir = Path(BASE_DIR) / "results"
out_dir.mkdir(parents=True, exist_ok=True)

GEN_RE   = re.compile(
    r"^Gen\s+(?P<gen>\d+):\s+best_this_gen\s*=\s*(?P<best>[-+]?\d+(\.\d+)?),\s*"
    r"mean_this_gen\s*=\s*(?P<mean>[-+]?\d+(\.\d+)?),\s*genome\s*=\s*(?P<genome>\[[^\]]+\])"
)
BEST_EVER_RE = re.compile(
    r"^Best ever fitness\s*=\s*(?P<best>\d+(\.\d+)?),\s*genome\s*=\s*(?P<genome>\[[^\]]+\])"
)
SEP_RE = re.compile(r"^=+|-{5,}|_{5,}")

def _parse_genome_list(txt):
    try:
        return json.loads(txt.replace(" ", "").replace("'", '"'))
    except Exception:
        import ast
        return ast.literal_eval(txt)

def load_runs_from_file(path: Path, selection_label: str):
    if not path.exists():
        raise FileNotFoundError(f"Nema fajla: {path}")

    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f]

    blocks, cur = [], []
    for ln in lines:
        if SEP_RE.match(ln):
            if cur:
                blocks.append(cur)
                cur = []
        else:
            if ln:
                cur.append(ln)
    if cur:
        blocks.append(cur)

    runs = []
    for bi, block in enumerate(blocks, start=1):
        rows = []
        best_ever = None
        for ln in block:
            m = GEN_RE.match(ln)
            if m:
                gen = int(m.group("gen"))
                best = float(m.group("best"))
                mean = float(m.group("mean"))
                genome = _parse_genome_list(m.group("genome"))
                row = {"gen": gen, "best": best, "mean": mean}
                for i, v in enumerate(genome):
                    row[f"g{i}"] = float(v)
                rows.append(row)
                continue
            b = BEST_EVER_RE.match(ln)
            if b:
                best_ever = {
                    "fitness": float(b.group("best")),
                    "genome": _parse_genome_list(b.group("genome"))
                }
        if rows:
            df = pd.DataFrame(rows).sort_values("gen").reset_index(drop=True)
            df["selection"] = selection_label
            df["run_id"] = bi
            runs.append({"selection": selection_label, "run_id": bi, "gens": df, "best_ever": best_ever})
    return runs

roulette_runs   = load_runs_from_file(roulette_path,   "roulette")
tournament_runs = load_runs_from_file(tournament_path, "tournament")
all_runs = roulette_runs + tournament_runs

df_all = pd.concat([r["gens"] for r in all_runs], ignore_index=True)
best_rows = []
for r in all_runs:
    be = r["best_ever"]
    if be:
        row = {"selection": r["selection"], "run_id": r["run_id"], "best_ever": be["fitness"]}
        for i, v in enumerate(be["genome"]):
            row[f"g{i}"] = float(v)
        best_rows.append(row)
df_best = pd.DataFrame(best_rows)

plt.rcParams.update({
    "figure.figsize": (10, 6),
    "axes.grid": True,
    "axes.edgecolor": "#999999",
    "grid.alpha": 0.25,
    "axes.titleweight": "bold",
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.frameon": False,
})


# 1) Linijski graf: best vs mean (svaki run posebno), po selekcijama
for sel in ["tournament", "roulette"]:
    fig, ax = plt.subplots()
    subset = [r for r in all_runs if r["selection"] == sel]
    for r in subset:
        d = r["gens"]
        ax.plot(d["gen"], d["best"], alpha=0.85, label=f"Run {r['run_id']} – best")
        ax.plot(d["gen"], d["mean"], alpha=0.65, linestyle="--", label=f"Run {r['run_id']} – mean")
    ax.set_title(f"{sel.capitalize()} – Best & Mean po generacijama")
    ax.set_xlabel("Generacija")
    ax.set_ylabel("Fitness")
    ax.legend(ncols=2)
    fig.tight_layout()
    fig.savefig(out_dir / f"{sel}_lines_best_mean.png", dpi=160)
    plt.close(fig)


# 2) “Best-ever” bar chart po run-u (grupisano po selekciji)
if not df_best.empty:
    fig, ax = plt.subplots()
    x = np.arange(len(df_best))
    ax.bar(x, df_best["best_ever"])
    ax.set_xticks(x, [f"{s[:3]}-{i}" for s, i in zip(df_best["selection"], df_best["run_id"])], rotation=0)
    ax.set_title("Best-ever po run-u (oba metoda selekcije)")
    ax.set_ylabel("Best-ever fitness")
    fig.tight_layout()
    fig.savefig(out_dir / "best_ever_bar.png", dpi=160)
    plt.close(fig)


# 3) Poboljšanja Δbest po generaciji (histogram + gustina)

def deltas_best(d):
    b = d.sort_values("gen")["best"].to_numpy()
    return np.diff(b)

for sel in ["tournament", "roulette"]:
    deltas = []
    for r in all_runs:
        if r["selection"] != sel:
            continue
        d = deltas_best(r["gens"])
        if len(d) > 0:
            deltas.extend(d.tolist())
    if deltas:
        fig, ax = plt.subplots()
        ax.hist(deltas, bins=40, alpha=0.8)
        ax.set_title(f"{sel.capitalize()} – distribucija poboljšanja Δbest")
        ax.set_xlabel("Δbest (razlika između uzastopnih generacija)")
        ax.set_ylabel("Frekvencija")
        fig.tight_layout()
        fig.savefig(out_dir / f"{sel}_delta_best_hist.png", dpi=160)
        plt.close(fig)


# 4) Heatmap korelacije koeficijenata genome (koristi best-ever genome po run-u)
if not df_best.empty:
    # Uzmi samo g0..g5 kolone koje postoje
    g_cols = [c for c in df_best.columns if c.startswith("g")]
    if len(g_cols) >= 2:
        corr = df_best[g_cols].corr()
        fig, ax = plt.subplots(figsize=(6.8, 6))
        im = ax.imshow(corr.values, aspect="equal")
        ax.set_xticks(range(len(g_cols)), g_cols)
        ax.set_yticks(range(len(g_cols)), g_cols)
        for (i, j), val in np.ndenumerate(corr.values):
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=9)
        ax.set_title("Korelacija best-ever genoma (svi run-ovi)")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        fig.tight_layout()
        fig.savefig(out_dir / "genome_correlation_heatmap.png", dpi=160)
        plt.close(fig)


# 5) Poređenje smoothed krivih (EMA) za BEST po selekciji
def ema(series, alpha=0.15):
    out = []
    prev = None
    for v in series:
        prev = v if prev is None else alpha * v + (1 - alpha) * prev
        out.append(prev)
    return np.array(out)

for sel in ["tournament", "roulette"]:
    fig, ax = plt.subplots()
    for r in [r for r in all_runs if r["selection"] == sel]:
        d = r["gens"].sort_values("gen")
        ax.plot(d["gen"], ema(d["best"], alpha=0.15), label=f"Run {r['run_id']} EMA(best)", alpha=0.9)
    ax.set_title(f"{sel.capitalize()} – EMA(best) po generacijama")
    ax.set_xlabel("Generacija")
    ax.set_ylabel("EMA(best)")
    ax.legend(ncols=2)
    fig.tight_layout()
    fig.savefig(out_dir / f"{sel}_ema_best.png", dpi=160)
    plt.close(fig)

print(f"saved ✅: {out_dir}")