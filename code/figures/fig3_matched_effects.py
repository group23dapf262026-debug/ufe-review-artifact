"""Figure 3: matched effects across six model families.
(a) Macro-F1 change Plus - Baseline, mean over 20 partitions with Nadeau-Bengio 95% CI.
(b) False-positive rate, Baseline -> Plus (means over the same 20 partitions).
All numbers are copied from data/fig3_matched_effects.csv (= Table 3 of the paper); nothing is estimated here."""
import csv
import os

from lncs import *

HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, "data", "fig3_matched_effects.csv"))))
models = [r["model"] for r in rows]
ys = list(range(len(rows)))[::-1]

fig = plt.figure(figsize=(TEXT_W * MM, 52 * MM))
axA = fig.add_axes([0.125, 0.19, 0.39, 0.70])
axB = fig.add_axes([0.600, 0.19, 0.385, 0.70], sharey=axA)

# ---------------- (a) Macro-F1 change forest plot ----------------
axA.axvline(0, color=GREY, lw=0.7, ls=(0, (3, 2)), zorder=1)
for y, r in zip(ys, rows):
    d, lo, hi = float(r["delta_pp"]), float(r["ci_lo"]), float(r["ci_hi"])
    axA.plot([lo, hi], [y, y], color=UFE, lw=1.3, solid_capstyle="butt", zorder=2)
    for v in (lo, hi):
        axA.plot([v, v], [y - 0.17, y + 0.17], color=UFE, lw=0.9, zorder=2)
    axA.plot(d, y, "o", ms=4.2, mfc=UFE, mec=UFE, zorder=3)
    axA.text(14.35, y, r["wins"], ha="right", va="center", fontsize=7.2, color=INK)
axA.text(14.35, len(rows) - 0.35, "Plus > Baseline", ha="right", va="center", fontsize=7.2,
         color=GREY, style="italic")
axA.set_xlim(-0.8, 14.5)
axA.set_xticks([0, 2, 4, 6, 8, 10, 12])
axA.set_ylim(-0.6, len(rows) - 0.1)
axA.set_yticks(ys)
axA.set_yticklabels(models)
axA.set_xlabel("Macro-F1 change: Plus − Baseline (pp)")
axA.text(0.0, 1.035, "(a) Macro-F1 change, NB 95% CI", transform=axA.transAxes, fontsize=7.5, weight="bold",
         ha="left", va="bottom")

# ---------------- (b) FPR dumbbell ----------------
for y, r in zip(ys, rows):
    b, p = float(r["fpr_baseline"]), float(r["fpr_plus"])
    # Keep the arrowhead clear of both markers.  A relative gap retains a
    # visible shaft even for Meta-IFD, whose two means are close.
    gap = min(0.25, 0.18 * (b - p))
    axB.annotate("", xy=(p + gap, y), xytext=(b - gap, y),
                 arrowprops=dict(arrowstyle="-|>", color=GREY, lw=0.8, mutation_scale=6, shrinkA=0, shrinkB=0),
                 zorder=2)
    axB.plot(b, y, "o", ms=4.4, mfc="white", mec=GREY, mew=0.9, zorder=3)
    axB.plot(p, y, "o", ms=4.4, mfc=UFE, mec=UFE, zorder=3)
axB.set_xlim(0, 17.5)
axB.set_xticks([0, 4, 8, 12, 16])
axB.set_xlabel("False-positive rate (%)")
axB.tick_params(axis="y", labelleft=False)
axB.text(0.0, 1.035, "(b) False-positive rate (lower is better)", transform=axB.transAxes, fontsize=7.5, weight="bold",
         ha="left", va="bottom")
h1, = axB.plot([], [], "o", ms=4.4, mfc="white", mec=GREY, mew=0.9, ls="none", label="Baseline")
h2, = axB.plot([], [], "o", ms=4.4, mfc=UFE, mec=UFE, ls="none", label="Plus")
axB.legend(handles=[h1, h2], loc="lower right", bbox_to_anchor=(1.0, 0.13), frameon=False, handletextpad=0.2,
           borderaxespad=0.2, labelspacing=0.3)

for ax in (axA, axB):
    ax.grid(axis="x", color="#E6E6E6", lw=0.5, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)

export(fig, "fig3_matched_effects")
