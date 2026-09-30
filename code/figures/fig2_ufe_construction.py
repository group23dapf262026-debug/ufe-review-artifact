"""Framework figure in the visual language of Meta-IFD Fig. 3, drawn at LNCS text width (122 mm).
(a) top: end-to-end framework; (b) UFE construction; legend row."""
from common import *
from lncs import export, MIN_PT
import lncs as _l
plt.rcParams.update(_l.STYLE)
from matplotlib.patches import Polygon

MM = 1 / 25.4
W, H = 122, 90.0
DY = -3.4
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


GREYC = "#B8BEC6"   # non-incident context edges


def gedge(p, q, sa=1.5, sb=1.5):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=4, color=GREYC, lw=0.6,
                                 shrinkA=sa * 2.83, shrinkB=sb * 2.83, zorder=4))


def target(x, y, r=2.4):
    eoa(x, y, r=r, fc=GR, ec=GR, z=8)
    t(x, y, "v", fs=7, style="italic", color="white")


def geoa(x, y, r=1.5):
    ax.add_patch(Circle((x, y), r, fc="white", ec=GREYC, lw=0.6, zorder=7))


# ============================== (a) target neighbourhood ==============================
TOP0, TOP1 = 39.5, 89.0
rbox(1, TOP0, 42, TOP1 - TOP0, "white", PANEL_E, lw=0.6, r=1.2)
t(22, 36.4, "(a) Target EOA neighbourhood", fs=6.8, weight="bold")
import math
V = (22.0, 64.0)
R = 14.0
def pol(deg, r=R):
    return (V[0] + r * math.cos(math.radians(deg)), V[1] + r * math.sin(math.radians(deg)))
N = {"i1": (pol(140), "eoa"), "i2": (pol(190), "eoa"), "c3": (pol(240), "ca"),
     "o1": (pol(295), "eoa"), "o2": (pol(335), "ca"), "k1": (pol(15), "ca"), "k2": (pol(65), "ca")}
P = {k: v[0] for k, v in N.items()}
# context (non-incident) nodes and edges
C = {"g1": pol(108, 22.5), "g2": pol(212, 17.5), "g3": pol(38, 22.5)}
gedge(C["g1"], P["k2"], sa=1.5, sb=1.6); gedge(C["g2"], P["i2"], sa=1.5, sb=1.5)
gedge(C["g3"], P["k1"], sa=1.5, sb=1.6); gedge(P["i1"], C["g1"], sa=1.5, sb=1.5)
for c in C.values():
    geoa(*c)
# incident edges
for k in ("i1", "i2", "c3"):
    edge(P[k], V, "trans", sa=1.6, sb=2.5)
for k in ("o1", "o2"):
    edge(V, P[k], "trans", sa=2.5, sb=1.6)
for k in ("k1", "k2"):
    edge(V, P[k], "call", sa=2.5, sb=1.6)
for k, (p, kind) in N.items():
    (eoa(*p, r=1.5) if kind == "eoa" else ca(*p, s=2.8))
target(*V)

# ============================== (b) relation-direction decomposition ==============================
BX0 = 45.0
rbox(BX0, TOP0, W - 1 - BX0, TOP1 - TOP0, "white", PANEL_E, lw=0.6, r=1.2)
t((BX0 + W - 1) / 2, 36.4, r"(b) Relation–direction decomposition $E_{r,d}(v)$", fs=6.8, weight="bold")
sw, sh = 36.0, 22.5
cells = {("call", "in"): (BX0 + 1.5, 65.0), ("call", "out"): (BX0 + 2.5 + sw, 65.0),
         ("trans", "in"): (BX0 + 1.5, 41.0), ("trans", "out"): (BX0 + 2.5 + sw, 41.0)}
NAME = {"call": "call", "trans": "transfer"}
for (r_, d_), (x0, y0) in cells.items():
    empty = (r_, d_) == ("call", "in")
    rbox(x0, y0, sw, sh, "#F1F2F4" if empty else "white", "#B0B7BF", lw=0.5, r=0.8, z=2)
    t(x0 + 1.4, y0 + sh - 2.4, f"{NAME[r_]}-{d_}", fs=6.4, ha="left", weight="bold")
    cy = y0 + 9.0
    if empty:
        target(x0 + sw / 2, cy + 1.0, r=2.1)
        t(x0 + sw / 2, cy - 4.6, "empty for target EOA", fs=6.2, color=K)
        continue
    ys = {2: (cy + 4.2, cy - 4.2), 3: (cy + 6.0, cy, cy - 6.0)}
    if (r_, d_) == ("call", "out"):
        nbr = ["ca", "ca"]
    elif (r_, d_) == ("trans", "in"):
        nbr = ["eoa", "eoa", "ca"]
    else:
        nbr = ["eoa", "ca"]
    vx, nx = (x0 + 25.0, x0 + 9.0) if d_ == "in" else (x0 + 11.0, x0 + 27.0)
    for kind, yy in zip(nbr, ys[len(nbr)]):
        if d_ == "in":
            edge((nx, yy), (vx, cy), r_, sa=1.6, sb=2.3)
        else:
            edge((vx, cy), (nx, yy), r_, sa=2.3, sb=1.6)
        (eoa(nx, yy, r=1.4) if kind == "eoa" else ca(nx, yy, s=2.6))
    target(vx, cy, r=2.1)

# ============================== (c) aggregation into 12 features ==============================
CB0, CB1 = 11.0, 33.0
rbox(1, CB0, W - 2, CB1 - CB0, "white", PANEL_E, lw=0.6, r=1.2)
t(61, 8.0, "(c) Aggregation into the 12-dimensional UFE vector", fs=6.8, weight="bold")
t(3.0, 29.6, r"for each group $E_{r,d}(v)$:", fs=6.3, ha="left")
t(4.5, 25.4, r"$g_{r,d,n_e}(v)=|E_{r,d}(v)|$", fs=6.3, ha="left")
t(4.5, 19.8, r"$g_{r,d,\Sigma a_k}(v)=\Sigma_{e\in E_{r,d}(v)}\,a_k(e),\ k\in\{0,1\}$", fs=6.3, ha="left")
t(4.5, 14.2, r"$u_{r,d,s}(v)=\log\!\left(1+g_{r,d,s}(v)\right)$", fs=6.3, ha="left")
hollow((44.0, 22.0), (49.4, 22.0), w=1.3)
cw, gap, x = 5.0, 2.2, 50.6
yc, hc = 19.8, 4.8
groups = [("call-in", True), ("call-out", False), ("transfer-in", False), ("transfer-out", False)]
for gname, zero in groups:
    gx = x
    for j, st in enumerate([r"$n_e$", r"$\Sigma a_0$", r"$\Sigma a_1$"]):
        ax.add_patch(Rectangle((x, yc), cw, hc, fc="#EDEDED" if zero else OR, ec="#BDBDBD" if zero else OR_E,
                               lw=0.4, hatch=None if zero else "///", zorder=6))
        if zero:
            t(x + cw / 2, yc + hc / 2, "0", fs=6.6, color=G)
        t(x + cw / 2, yc + hc + 1.7, st, fs=5.9)
        x += cw
    ax.plot([gx + 0.2, gx + 0.2, x - 0.2, x - 0.2], [yc - 1.0, yc - 1.8, yc - 1.8, yc - 1.0], color=G, lw=0.5)
    t((gx + x) / 2, yc - 3.9, gname, fs=6.2, color=G if zero else K)
    x += gap
t((50.6 + x - gap) / 2, 30.4, r"$\mathbf{u}(v)\in\mathbb{R}^{12}$", fs=6.6)

# ============================== legend ==============================
ly, l2 = 3.4, -0.7
rbox(1, -2.9, W - 2, 8.7, "white", PANEL_E, lw=0.5, r=0.8)
target(4.0, ly, r=1.5); t(6.1, ly, "target EOA", fs=6, ha="left")
eoa(22.0, ly, r=1.0); t(23.6, ly, "EOA", fs=6, ha="left")
ca(31.2, ly, s=1.8); t(32.8, ly, "CA", fs=6, ha="left")
edge((38.6, ly), (43.0, ly), "call", sa=0, sb=0); t(43.6, ly, "call", fs=6, ha="left")
edge((50.0, ly), (54.4, ly), "trans", sa=0, sb=0); t(55.0, ly, "transfer", fs=6, ha="left")
gedge((65.4, ly), (69.8, ly), sa=0, sb=0); t(70.4, ly, "non-incident edge (not aggregated)", fs=6, ha="left")
ax.add_patch(Rectangle((2.5, l2 - 1.2), 3.0, 2.4, fc=OR, ec=OR_E, lw=0.4, hatch="///", zorder=6))
t(6.1, l2, "UFE entry", fs=6, ha="left")
ax.add_patch(Rectangle((18.5, l2 - 1.2), 3.0, 2.4, fc="#EDEDED", ec="#BDBDBD", lw=0.4, zorder=6))
t(22.3, l2, "structurally zero for target EOA", fs=6, ha="left")
t(58.0, l2, r"$a_0, a_1$: released numerical edge attributes", fs=6, ha="left")

export(fig, "fig2_ufe_construction")
