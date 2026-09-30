"""Figure 5 (optional / Supplementary S1): association and overlap between the 14 source features and the 12 UFE.
Post-hoc, train-and-validation-only audit (2,210 development nodes); no test data.
Reads the audit CSVs verbatim from data/figS1_source_ufe_overlap/.
Columns are reordered for display only; constant features are masked, not shown as 0."""
import json
import os

import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap
from lncs import *

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data", "figS1_source_ufe_overlap")
sp = pd.read_csv(os.path.join(D, "spearman_raw_matrix.csv"), index_col=0)
eq = pd.read_csv(os.path.join(D, "equal_or_close_excluding_both_zero_matrix.csv"), index_col=0)
summ = json.load(open(os.path.join(D, "final_summary.json")))

COLS = [f"{r}_{d}_{s}" for r, d in (("call", "in"), ("call", "out"), ("trans", "in"), ("trans", "out"))
        for s in ("edge_records", "edge_attr0_sum", "edge_attr1_sum")]
ROWS = list(sp.index)
sp, eq = sp.loc[ROWS, COLS], eq.loc[ROWS, COLS]
const_src, const_ufe = set(summ["constant_source_features"]), set(summ["constant_ufe_features"])
mask = np.array([[(r in const_src) or (c in const_ufe) for c in COLS] for r in ROWS])
DIRECT = [("N_return_c", "call_out_edge_attr0_sum"), ("V_return_c", "call_out_edge_attr1_sum"),
          ("N_inv_t", "trans_in_edge_attr0_sum"), ("V_inv_t", "trans_in_edge_attr1_sum")]

# consistency checks against the audit summary (fail loudly rather than draw inconsistent numbers)
assert mask.sum() == summ["constant_or_structurally_zero_pair_count"] == 60
assert (~mask).sum() == 108
assert abs(np.nanmax(eq.values[~mask]) - 0.5895316804407713) < 1e-12
assert not np.isnan(sp.values[~mask]).any()

# display tables written next to the figure (reordered, masked cells = NaN)
out = os.environ.get("FIG_OUT", "final")
os.makedirs(out, exist_ok=True)
sp.mask(mask).to_csv(os.path.join(out, "figS1_panel_a_spearman_display.csv"))
eq.mask(mask).to_csv(os.path.join(out, "figS1_panel_b_equal_or_close_excl_both_zero_display.csv"))

nr, nc = len(ROWS), len(COLS)
fig = plt.figure(figsize=(TEXT_W * MM, 92 * MM))
x0, w, gapx = 0.155, 0.385, 0.045
y0, h = 0.25, 0.50
axA = fig.add_axes([x0, y0, w, h])
axB = fig.add_axes([x0 + w + gapx, y0, w, h])
div = LinearSegmentedColormap.from_list("div", ["#3B6FB0", "#A9C4E4", "#F7F7F7", "#F2B98C", "#B8541A"])
seq = LinearSegmentedColormap.from_list("seq", ["#FFFFFF", "#FBDDC3", "#E6955A", "#B8541A", "#6E300B"])
XE, YE = np.arange(nc + 1) - 0.5, np.arange(nr + 1) - 0.5      # vector cells (pcolormesh, not an image)
imA = axA.pcolormesh(XE, YE, np.ma.masked_array(sp.values, mask), cmap=div, vmin=-1, vmax=1)
imB = axB.pcolormesh(XE, YE, np.ma.masked_array(eq.values, mask), cmap=seq, vmin=0, vmax=1)
for ax in (axA, axB):
    ax.set_xlim(-0.5, nc - 0.5); ax.set_ylim(nr - 0.5, -0.5)

for ax in (axA, axB):
    ax.set_facecolor("white")
    for i in range(nr):
        for j in range(nc):
            if mask[i, j]:
                ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fc="#E4E6E9", ec="#C3C8CE", lw=0.2, hatch="////",
                                       zorder=2))
    for j in (2.5, 5.5, 8.5):
        ax.axvline(j, color="white", lw=1.4, zorder=3)
    for r, c in DIRECT:
        i, j = ROWS.index(r), COLS.index(c)
        ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fc="none", ec=INK, lw=1.1, zorder=4))
    ax.set_xticks(range(nc))
    ax.set_xticklabels([r"$n_e$", r"$\Sigma a_0$", r"$\Sigma a_1$"] * 4, fontsize=7, rotation=90)
    ax.tick_params(axis="x", length=0, pad=1.5, labeltop=True, labelbottom=False)
    ax.set_yticks(range(nr))
    ax.tick_params(axis="y", length=0, pad=1.5)
    for s in ax.spines.values():
        s.set_visible(False)
    for g, name in enumerate(("call-in", "call-out", "transfer-in", "transfer-out")):
        ax.text(g * 3 + 1, -2.55, name, ha="center", va="bottom", fontsize=7,
                color=GREY if g == 0 else INK)
axA.set_yticklabels([r.replace("_", r"\_") if False else r for r in ROWS], fontsize=7)
axB.set_yticklabels([])
axA.text(-0.5, -5.0, "(a) Spearman association", ha="left", va="bottom", fontsize=7.5, weight="bold")
axB.text(-0.5, -5.0, "(b) Equal or close, excluding both-zero", ha="left", va="bottom", fontsize=7.5,
         weight="bold")

cbA = fig.colorbar(imA, cax=fig.add_axes([x0 + 0.03, 0.150, w - 0.06, 0.026]), orientation="horizontal")
cbA.set_label("Spearman correlation", fontsize=7, labelpad=1.5)
cbA.set_ticks([-1, -0.5, 0, 0.5, 1])
cbB = fig.colorbar(imB, cax=fig.add_axes([x0 + w + gapx + 0.03, 0.150, w - 0.06, 0.026]), orientation="horizontal")
cbB.set_label("Equal or close fraction, excluding both-zero", fontsize=7, labelpad=1.5)
cbB.set_ticks([0, 0.25, 0.5, 0.75, 1])
cbB.set_ticklabels(["0", "0.25", "0.50", "0.75", "1"])
for cb in (cbA, cbB):
    cb.solids.set_rasterized(False)
    cb.ax.tick_params(labelsize=7, length=2, width=0.5, pad=1)
    cb.outline.set_linewidth(0.4)

# legend row
ly = 0.035
fig.patches.append(Rectangle((0.155, ly - 0.012), 0.022, 0.03, transform=fig.transFigure, fc="white", ec=INK, lw=1.1))
fig.text(0.183, ly + 0.003, "direct-looking correspondence", fontsize=7, va="center")
fig.patches.append(Rectangle((0.53, ly - 0.012), 0.022, 0.03, transform=fig.transFigure, fc="#E4E6E9",
                             ec="#C3C8CE", lw=0.4, hatch="////"))
fig.text(0.558, ly + 0.003, "constant feature (masked, not 0)", fontsize=7, va="center")

export(fig, "figS1_source_ufe_overlap", out)
