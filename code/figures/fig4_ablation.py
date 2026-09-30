"""Figure 4: ablation exact-edge Random Forest ablation over 10 predefined partitions.
(a) Macro-F1 mean +/- SD per feature configuration.  (b) Predefined paired comparisons:
four superiority tests (mean delta, NB 95% CI) and the shuffled control (TOST, 90% CI, margin +/-0.5 pp).
Numbers are read verbatim from the two CSV files in the local data directory."""
import csv
import os

from matplotlib.patches import Rectangle
from lncs import *

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "data", "fig4a_ablation_configs.csv"), encoding="utf-8-sig", newline="") as f:
    A = list(csv.DictReader(f))
with open(os.path.join(HERE, "data", "fig4b_paired_comparisons.csv"), encoding="utf-8-sig", newline="") as f:
    B = list(csv.DictReader(f))

fig = plt.figure(figsize=(TEXT_W * MM, 104 * MM))
L, Wd = 0.385, 0.435
axA = fig.add_axes([L, 0.615, Wd, 0.335])
axB = fig.add_axes([L, 0.105, Wd, 0.365])

# ---------------- (a) configurations ----------------
style = {"source": dict(c=SRC, mfc=SRC, ls="-", mk="s", ms=4.0), "ufe": dict(c=UFE, mfc=UFE, ls="-", mk="o", ms=4.2),
         "shuffled": dict(c=GREY, mfc="white", ls=(0, (2.5, 1.5)), mk="o", ms=4.2)}
ya = list(range(len(A)))[::-1]
axA.axvline(float(A[0]["mean"]), color=SRC, lw=0.6, ls=(0, (3, 2)), zorder=1)
for y, r in zip(ya, A):
    m, sd, st = float(r["mean"]), float(r["sd"]), style[r["kind"]]
    axA.plot([m - sd, m + sd], [y, y], color=st["c"], lw=1.2, ls=st["ls"], zorder=2)
    for v in (m - sd, m + sd):
        axA.plot([v, v], [y - 0.17, y + 0.17], color=st["c"], lw=0.9, zorder=2)
    axA.plot(m, y, st["mk"], ms=st["ms"], mfc=st["mfc"], mec=st["c"], mew=0.9, zorder=3)
    axA.text(1.03, y, f"{m:.2f} ± {sd:.2f}", transform=axA.get_yaxis_transform(), ha="left", va="center", fontsize=7.2)
axA.set_xlim(95.0, 99.6)
axA.set_xticks([95, 96, 97, 98, 99])
axA.set_ylim(-0.6, len(A) - 0.4)
config_labels = [r["configuration"] for r in A]
config_labels = ["Source + other 11 UFE (8 varying)" if x == "Source + other 11 UFE" else x
                 for x in config_labels]
axA.set_yticks(ya); axA.set_yticklabels(config_labels)
axA.set_xlabel("Macro-F1 (%), mean ± SD over 10 partitions")
axA.text(float(A[0]["mean"]) + 0.06, ya[0] + 0.34, "Source 14 mean", fontsize=7.0,
         color=SRC, ha="left", va="center")
axA.text(-0.72, 1.06, "(a) Feature configurations", transform=axA.transAxes, fontsize=7.5, weight="bold",
         ha="left", va="bottom")

# ---------------- (b) paired comparisons ----------------
yb = list(range(len(B)))[::-1]
for y, r in zip(yb, B):
    d, lo, hi = float(r["delta_pp"]), float(r["ci_lo"]), float(r["ci_hi"])
    tost = r["test"].startswith("TOST")
    if tost:   # equivalence region only behind the shuffled row
        axB.add_patch(Rectangle((-0.5, y - 0.36), 1.0, 0.72, fc="#ECEEF0", ec=GREY_L, lw=0.5, zorder=0))
    c = GREY if tost else UFE_D
    axB.plot([lo, hi], [y, y], color=c, lw=1.2, ls=(0, (2.5, 1.5)) if tost else "-", zorder=2)
    for v in (lo, hi):
        axB.plot([v, v], [y - 0.17, y + 0.17], color=c, lw=0.9, zorder=2)
    axB.plot(d, y, "D" if tost else "o", ms=3.9 if tost else 4.2, mfc="white" if tost else c, mec=c, mew=0.9,
             zorder=3)
    axB.text(1.03, y, r["decision"], transform=axB.get_yaxis_transform(), ha="left", va="center", fontsize=7.2,
             style="italic" if r["decision"] != "Pass" else "normal")
axB.axvline(0, color=GREY, lw=0.7, ls=(0, (3, 2)), zorder=1)
axB.text(0.55, yb[-1] - 0.05, "TOST, 90% CI,\nmargin ±0.5 pp", ha="left", va="center", fontsize=7.0, color=GREY,
         linespacing=1.0)
axB.set_xlim(-0.8, 4.2)
axB.set_xticks([0, 1, 2, 3, 4])
axB.set_ylim(-0.6, len(B) - 0.4)
axB.set_yticks(yb); axB.set_yticklabels([r["comparison"] for r in B])
axB.set_xlabel("Paired Macro-F1 difference (pp); NB 95% CI unless marked")
axB.text(-0.72, 1.05, "(b) Predefined paired comparisons", transform=axB.transAxes, fontsize=7.5, weight="bold",
         ha="left", va="bottom")
axB.text(1.03, len(B) - 0.35, "Decision", transform=axB.get_yaxis_transform(), ha="left", va="center",
         fontsize=7.2, color=GREY, style="italic")

for ax in (axA, axB):
    ax.grid(axis="x", color="#E6E6E6", lw=0.5, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
export(fig, "fig4_ablation")
