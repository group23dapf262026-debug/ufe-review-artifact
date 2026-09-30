"""Fig. 1 (top row only). Framework figure in the visual language of Meta-IFD Fig. 3, drawn at LNCS text width (122 mm).
(a) top: end-to-end framework; (b) UFE construction; legend row."""
from common import *
from lncs import export, MIN_PT
import lncs as _l
plt.rcParams.update(_l.STYLE)
from matplotlib.patches import Polygon

MM = 1 / 25.4
W, H = 122, 93.2
DY = 38.8   # legend lifted directly under the framework row; panel (b) moved to Fig. 2
fig = plt.figure(figsize=(W * MM, (H - DY) * MM))
ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
ax.set_xlim(0, W); ax.set_ylim(DY, H); ax.set_aspect("equal")

K = "#2C3E50"; G = "#5D6D7E"
plt.rcParams["text.color"] = K
import os as _os
_PALS = {  # source light, source edge, source back, UFE light, UFE edge, UFE back
    "A": ("#DCE6F2", "#4C72B0", "#EEF3F9", "#F6D5BE", "#C4622D", "#FBEDE3"),
    "B": ("#D9EAD3", "#4E8A3E", "#EDF5EA", "#E4D7EE", "#6C4A93", "#F3EDF8"),
    "C": ("#E3E3E3", "#5A5A5A", "#F2F2F2", "#F2C9C4", "#9E2A2B", "#FAE6E4"),
    "D": ("#D6E4E4", "#2F6F73", "#EBF3F3", "#F7E3B5", "#A0761B", "#FBF2DC"),
}
_PALS["E"] = ("#DCE8F5", "#2F6DB5", "#EEF4FB", "#FBDDC3", "#D2691E", "#FDEEE1")   # blue / orange
BL, BL_E, SRC_BACK, OR, OR_E, UFE_BACK = _PALS[_os.environ.get("PAL", "E")]
GR, GR_L = "#7B52AB", "#EFE8F7"     # graph input (purple)
MD, MD_L = "#2E8B57", "#E6F4EC"     # models and predictions (green)
BL_D = "#2C3E50"

EOA_F, EOA_E, TR = "#FFFFFF", "#7B52AB", "#7B52AB"                       # UFE (hatched) / EOA / transfer
PEACH, PEACH_E = "#FFFFFF", "#8C8C8C"
PANEL, PANEL_E = "#FFFFFF", "#8C8C8C"
GREEN, GREEN_E = "#F0F0F0", "#5D6D7E"
RED = "#A61C1C"


def t(x, y, s, fs=7.0, ha="center", va="center", **kw):
    ax.text(x, y, s, fontsize=max(fs, MIN_PT), ha=ha, va=va, zorder=8, **kw)


def rbox(x, y, w, h, fc, ec, lw=0.6, r=1.2, ls="-", z=1):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw,
                                ls=ls, zorder=z))


def vec(x, y, n, cw=1.05, h=2.3, kind="src", z=4):
    for k in range(n):
        if kind == "src":
            ax.add_patch(Rectangle((x + k * cw, y), cw, h, fc=BL, ec=BL_E, lw=0.35, zorder=z))
        else:
            ax.add_patch(Rectangle((x + k * cw, y), cw, h, fc=OR, ec=OR_E, lw=0.35, hatch="////", zorder=z))
    return x + n * cw


def stack(x, y, n, kind, cw=1.05, h=2.3, rows=3, label="N"):
    """stacked account cards: each card = rows x n feature matrix (one row per account)."""
    w = n * cw + 1.6
    hh = rows * (h + 0.6) + 1.0
    for s in (2, 1, 0):
        ox, oy = s * 0.9, s * 0.9
        rbox(x + ox, y + oy, w, hh, fc="white" if s == 0 else (SRC_BACK if kind == "src" else UFE_BACK),
             ec=BL_E if kind == "src" else OR_E, lw=0.5, r=0.5, z=2 + (2 - s))
    for r_ in range(rows):
        vec(x + 0.8, y + 0.5 + r_ * (h + 0.6), n, cw, h, kind, z=6)
    t(x + w + 1.8, y - 1.7, label, fs=6.2, ha="right")
    return x + w + 1.8


def hollow(p, q, w=1.6):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=f"simple,head_width={w*2.4},head_length={w*1.8},tail_width={w}",
                                 fc="white", ec="#9A9A9A", lw=0.6, zorder=5))


def line(p, q, c=G, lw=0.7, ls="-", ms=5, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms, color=c, lw=lw, linestyle=ls,
                                 shrinkA=0, shrinkB=0, connectionstyle=f"arc3,rad={rad}", zorder=5))


def trap(x, y, w, h, label, fc="#F2F2F2", ec=K):
    ax.add_patch(Polygon([(x, y), (x + w, y + h * 0.18), (x + w, y + h * 0.82), (x, y + h)], closed=True,
                         fc=fc, ec=ec, lw=0.6, zorder=6))
    t(x + w / 2, y + h / 2, label, fs=6.4, weight="bold", linespacing=1.1)


def eoa(x, y, r=1.3, fc=EOA_F, ec=EOA_E, z=7):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=ec, lw=0.6, zorder=z))


def ca(x, y, s=2.3, z=7):
    ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc=GR_L, ec=GR, lw=0.6, zorder=z))


def edge(p, q, kind, sa=1.5, sb=1.5, lw=0.8):
    c, ls = (GR, "-") if kind == "call" else (TR, (0, (2.2, 1.3)))
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=4.5, color=c, lw=lw, linestyle=ls,
                                 shrinkA=sa * 2.83, shrinkB=sb * 2.83, zorder=6))


# ============================== (a) framework ==============================
yA, yB = 71.0, 53.0            # upper (source / Baseline) and lower (UFE / Plus) streams
# released processed graph (input data, not a model): horizontal box with a mini graph
GX0, GX1, GY0, GY1 = 1.0, 61.5, 80.3, 92.4
rbox(GX0, GY0, GX1 - GX0, GY1 - GY0, GR_L, GR, lw=0.8, r=0.8)
t(GX0 + 1.5, 90.6, "Released processed HEIG-Phish graph", fs=6.6, ha="left", weight="bold")
gp = {"a": (4.0, 86.6), "b": (9.5, 87.4), "c": (14.5, 86.0), "d": (6.5, 82.6), "e": (12.5, 82.4)}
edge(gp["a"], gp["b"], "trans", sa=1.1, sb=1.1, lw=0.7); edge(gp["d"], gp["b"], "trans", sa=1.1, sb=1.1, lw=0.7)
edge(gp["b"], gp["c"], "call", sa=1.1, sb=1.1, lw=0.7); edge(gp["e"], gp["c"], "call", sa=1.1, sb=1.1, lw=0.7)
edge(gp["d"], gp["e"], "trans", sa=1.1, sb=1.1, lw=0.7)
eoa(*gp["a"], r=0.95); eoa(*gp["b"], r=0.95); eoa(*gp["d"], r=0.95); eoa(*gp["e"], r=0.95); ca(*gp["c"], s=1.7)
t(18.5, 86.6, "EOA / CA nodes, call / transfer edges", fs=6.3, ha="left")
t(18.5, 83.4, "14 source features per node", fs=6.3, ha="left")
# split: source features X (upper lane) and incident edges for UFE (lower lane)
TX = 6.0
ax.plot([TX, TX], [GY0, yB + 2.4], color=G, lw=0.8, zorder=5)
ax.add_patch(Circle((TX, yA + 2.4), 0.45, fc=G, ec="none", zorder=7))
line((TX, yA + 2.4), (13.3, yA + 2.4), lw=0.8)
line((TX, yB + 2.4), (13.3, yB + 2.4), lw=0.8)
ax.text(TX - 1.5, (yA + yB) / 2 + 2.4, "incident edges", rotation=90, fontsize=7.0, ha="center", va="center",
        color=G, style="italic", zorder=8)
# source stream
t(39.0, 76.3, r"Source features $X$", fs=6.3, weight="bold")
sx_end = stack(13.6, yA - 1.0, 14, "src", cw=0.85, rows=2, label=r"$N\times14$")
# UFE stream: construction callout then stacked UFE
rbox(13.6, yB - 3.5, 13.8, 11.8, UFE_BACK, OR_E, lw=0.7, r=1.0, ls=(0, (3, 1.6)))
t(20.5, yB + 5.4, "UFE", fs=7, weight="bold")
t(20.5, yB + 2.2, "construction", fs=6.2)
t(20.5, yB - 1.2, "(label-free)", fs=6.2, style="italic", color=K)
line((27.45, yB + 2.4), (30.0, yB + 2.4), ms=4.5)
t(35.4, yB + 10.8, r"UFE $U$", fs=6.5, weight="bold")
ux_end = stack(30.1, yB - 2.4, 12, "ufe", cw=0.75, label=r"$N\times12$")
# ---- Baseline input (upper): X, N x 14
BX = 52.6
hollow((sx_end + 2.6, yA + 2.4), (BX - 0.6, yA + 2.4))
t(BX + 5.4, yA + 5.9, r"Baseline: $X$", fs=6.3)
vec(BX, yA + 1.25, 14, cw=0.84, h=2.3, kind="src")
t(BX + 5.9, yA - 1.6, r"$N\times14$", fs=6.2)
# ---- Plus input (lower): Concat(X, U) -> [X || U], N x 26
bx0, bw, bh = 43.5, 7.7, 4.0
cyp = yB + 2.4
ax.add_patch(Rectangle((bx0, cyp - bh / 2), bw, bh, fc="white", ec=OR_E, lw=0.7, zorder=7))
t(bx0 + bw / 2, cyp, "Concat", fs=5.9)
line((ux_end - 0.1, cyp), (bx0 - 0.05, cyp), ms=4.5)                 # U  -> Concat
brx = 46.2                                                     # X branches down into Concat
ax.add_patch(Circle((brx, yA + 2.4), 0.45, fc=G, ec="none", zorder=7))
line((brx, yA + 2.4), (brx, cyp + bh / 2 + 0.05))
t(brx - 0.8, (yA + cyp) / 2 + 1.0, r"$X$", fs=6.2, ha="right", color=G)
line((bx0 + bw + 0.05, cyp), (BX - 0.1, cyp), ms=4.5)                 # Concat -> Plus
t(BX + 5.85, yB + 5.9, r"Plus: $[X\,\Vert\,U]$", fs=6.3)
e = vec(BX, yB + 1.25, 14, cw=0.45, h=2.3, kind="src")
vec(e, yB + 1.25, 12, cw=0.45, h=2.3, kind="ufe")
t(BX + 5.85, yB - 1.6, r"$N\times26$", fs=6.2)
# ---- model block: one family m, two separately trained models (two lanes)
LX0, LX1 = 64.5, 121.0
rbox(LX0, 76.4, LX1 - LX0, 16.0, MD_L, MD, lw=0.7, r=0.8)
t(LX0 + 1.5, 90.9, "Model family", fs=7.3, ha="left", weight="bold")
t(LX0 + 1.5, 87.9, r"$m\in\{$LR, RF, LightGBM,", fs=7.0, ha="left")
t(LX0 + 4.6, 84.4, r"GAT, GraphSAGE, Meta-IFD$\}$", fs=7.0, ha="left")
t(LX0 + 1.5, 81.0, "Tabular: features", fs=7.0, ha="left", style="italic", color=G)
t(LX0 + 1.5, 78.5, "Graph: features + graph structure", fs=7.0, ha="left", style="italic", color=G)
MB0, MB1, mh = 68.2, 81.4, 5.0
for yy in (yA + 2.4, yB + 2.4):
    hollow((64.6, yy), (MB0 - 0.2, yy))
    rbox(MB0, yy - mh / 2, MB1 - MB0, mh, MD_L, MD, lw=0.9, r=0.5, z=6)
    t((MB0 + MB1) / 2, yy, r"Model $M_m$", fs=6.4, weight="bold")
# matched but separate: double rule between the two model boxes + note
xm = (MB0 + MB1) / 2
for dx in (-0.35, 0.35):
    ax.plot([xm + dx, xm + dx], [yB + 2.4 + mh / 2 + 0.4, yA + 2.4 - mh / 2 - 0.4], color=G, lw=0.5, zorder=5)
t(xm + 2.2, 67.4, "same family and", fs=6.0, ha="left", color=G)
t(xm + 2.2, 64.8, "configuration,", fs=6.0, ha="left", color=G)
t(xm + 2.2, 61.8, "trained separately", fs=6.0, ha="left", style="italic")
# paired predictions
PP0 = 97.5
rbox(PP0, 51.0, LX1 - PP0, 25.0, "white", MD, lw=0.7, r=0.8)
for yy, lab in ((yA + 2.4, r"$\hat{y}_{\mathrm{Baseline}}$"), (yB + 2.4, r"$\hat{y}_{\mathrm{Plus}}$")):
    line((MB1 + 0.2, yy), (PP0 + 1.6, yy), lw=0.7)
    t(PP0 + 2.2, yy, lab, fs=6.8, ha="left")
t((PP0 + LX1) / 2, 65.3, "Paired", fs=6.3, weight="bold")
t((PP0 + LX1) / 2, 62.7, "predictions", fs=6.3, weight="bold")
t((PP0 + LX1) / 2, 59.6, "Normal / Phishing", fs=5.9, color=G)

_n0 = (len(ax.patches), len(ax.texts), len(ax.lines))
# ============================== legend (full-width row) ==============================
ly = 3.6
rbox(1, 0.8, W - 2, 5.6, "white", PANEL_E, lw=0.5, r=0.8)
eoa(4.0, ly, r=1.0); t(5.6, ly, "EOA", fs=6, ha="left")
ca(13.0, ly, s=1.8); t(14.6, ly, "CA", fs=6, ha="left")
edge((20.0, ly), (24.6, ly), "call", sa=0, sb=0); t(25.2, ly, "call", fs=6, ha="left")
edge((31.0, ly), (35.6, ly), "trans", sa=0, sb=0); t(36.2, ly, "transfer", fs=6, ha="left")
vec(44.5, ly - 1.05, 3, cw=1.0, h=2.1, kind="src"); t(48.1, ly, "source feature", fs=6, ha="left")
vec(64.5, ly - 1.05, 3, cw=1.0, h=2.1, kind="ufe"); t(68.1, ly, "UFE", fs=6, ha="left")
ax.add_patch(Rectangle((73.4, ly - 1.5), 8.4, 3.0, fc="white", ec=OR_E, lw=0.6, zorder=7))
t(77.6, ly, "Concat"); t(82.5, ly, "column-wise join", ha="left")

import matplotlib.transforms as _mt
_tr = _mt.Affine2D().translate(0, DY) + ax.transData
for _a in ax.patches[_n0[0]:] + ax.texts[_n0[1]:] + ax.lines[_n0[2]:]:
    _a.set_transform(_tr)
export(fig, "fig1_ufe_evaluation_framework")
