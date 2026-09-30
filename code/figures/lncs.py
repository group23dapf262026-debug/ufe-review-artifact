"""Shared LNCS figure style: TeX Gyre Termes, 122 mm text width, >= 7 pt text, vector PDF/SVG + 450 dpi PNG.
Palette: graph = muted purple, source features = blue, UFE = earth orange, models = muted green, neutral = grey."""
import glob
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

# TeX Gyre Termes converted to TrueType (otf2ttf.py) so PDF embedding is clean Type 42
_FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
font_manager.fontManager.ttflist = [e for e in font_manager.fontManager.ttflist if "texgyretermes" not in e.fname]
for f in glob.glob(os.path.join(_FD, "texgyretermes-*.ttf")):
    font_manager.fontManager.addfont(f)

MM = 1 / 25.4
TEXT_W = 122.0           # LNCS text width (mm)
MIN_PT = 7.0

GRAPH, GRAPH_L = "#7B52AB", "#EFE8F7"
SRC, SRC_L = "#2F6DB5", "#DCE8F5"
UFE, UFE_L, UFE_D = "#D2691E", "#FBDDC3", "#9A4A12"
MODEL, MODEL_L = "#2E8B57", "#E6F4EC"
INK, GREY, GREY_L = "#2C3E50", "#5D6D7E", "#B8BEC6"

STYLE = {
    "font.family": "TeX Gyre Termes",
    "mathtext.fontset": "custom",
    "mathtext.rm": "TeX Gyre Termes",
    "mathtext.it": "TeX Gyre Termes:italic",
    "mathtext.bf": "TeX Gyre Termes:bold",
    "font.size": 7.5,
    "axes.labelsize": 7.5,
    "xtick.labelsize": 7.2,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 7.2,
    "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
    "axes.edgecolor": INK, "axes.linewidth": 0.6,
    "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.major.size": 2.5, "ytick.major.size": 2.5,
    "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "path",
}
plt.rcParams.update(STYLE)


def audit(fig, min_pt=MIN_PT):
    """Overlap / clipping / font-size gate at true print size (figure is built at 122 mm)."""
    import itertools
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    W, H = fig.bbox.width, fig.bbox.height
    items = []
    for t in fig.findobj(matplotlib.text.Text):
        if not t.get_visible() or not t.get_text().strip():
            continue
        items.append((t.get_text().replace("\n", " | ")[:50], t.get_window_extent(r), t.get_fontsize()))
    issues = []
    for n, bb, fs in items:
        if fs < min_pt - 1e-6:
            issues.append(f"SMALL {fs:.1f}pt: {n}")
        if bb.x0 < -0.5 or bb.y0 < -0.5 or bb.x1 > W + 0.5 or bb.y1 > H + 0.5:
            issues.append(f"CLIPPED: {n}")
    for (n1, b1, _), (n2, b2, _) in itertools.combinations(items, 2):
        if b1.overlaps(b2):
            ix = min(b1.x1, b2.x1) - max(b1.x0, b2.x0); iy = min(b1.y1, b2.y1) - max(b1.y0, b2.y0)
            if ix > 1 and iy > 1:
                issues.append(f"OVERLAP: '{n1}' x '{n2}'")
    width_mm = fig.get_figwidth() * 25.4
    smallest = min(fs for _, _, fs in items)
    print(f"[audit] width {width_mm:.1f} mm, {len(items)} text items, smallest {smallest:.1f} pt, {len(issues)} issues")
    for i in issues:
        print("   ", i)
    return issues


def export(fig, name, out=None):
    out = out or os.environ.get("FIG_OUT", "final")
    os.makedirs(out, exist_ok=True)
    issues = audit(fig)
    base = os.path.join(out, name)
    # no bbox_inches='tight': the canvas is exactly 122 mm wide, so point sizes are final print sizes
    fig.savefig(base + ".pdf")
    fig.savefig(base + ".svg")
    fig.savefig(base + ".png", dpi=450)
    plt.close(fig)
    return issues
