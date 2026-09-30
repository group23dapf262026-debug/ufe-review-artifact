import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

plt.rcParams.update({
    "font.family": "Liberation Serif",
    "mathtext.fontset": "stix",
    "font.size": 13,
    "axes.linewidth": 0.8,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

# Palette in the style of the Meta-IFD figures
EOA = "#F7BE16"      # EOA node (gold)
EOA_EDGE = "#C79100"
CA = "#2F4F8F"       # CA node (navy)
TRANS = "#C8961E"    # trans arrow
CALL = "#2F5FA8"     # call arrow
GREY = "#D4D4D4"     # context nodes / edges
GREY_D = "#9A9A9A"
INK = "#1F1F1F"
INK2 = "#555555"
PANEL = "#F3F5F9"
PANEL_EDGE = "#C9CFDA"
ACCENT = "#C0392B"   # highlight (trans_in_sum)


def node(ax, x, y, kind, r=0.22, label=None, alpha=1.0, fs=13, z=5):
    fc = {"eoa": EOA, "ca": CA, "grey": GREY}[kind]
    ec = {"eoa": EOA_EDGE, "ca": "#1D355F", "grey": "#BDBDBD"}[kind]
    ax.add_patch(Circle((x, y), r, fc=fc, ec=ec, lw=1.0, alpha=alpha, zorder=z))
    if label:
        col = "white" if kind == "ca" else INK
        ax.text(x, y, label, ha="center", va="center", fontsize=fs,
                style="italic", color=col, zorder=z + 1)


def arrow(ax, p, q, color, r=0.22, lw=2.0, style="-|>", ms=13, rad=0.0, z=3, ls="-", sa=11, sb=11):
    a = FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=color,
                        lw=lw, shrinkA=sa, shrinkB=sb,
                        connectionstyle=f"arc3,rad={rad}", zorder=z, linestyle=ls)
    ax.add_patch(a)
    return a


def box(ax, x, y, w, h, fc=PANEL, ec=PANEL_EDGE, lw=1.0, r=0.08, z=1, ls="-"):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       fc=fc, ec=ec, lw=lw, zorder=z, linestyle=ls)
    ax.add_patch(p)
    return p


def save(fig, name):
    import os
    out = os.environ.get("FIG_OUT", "/kaggle/working/figures" if os.path.isdir("/kaggle/working") else "figures")
    out = out.rstrip("/") + "/"
    os.makedirs(out, exist_ok=True)
    fig.savefig(out + name + ".pdf", bbox_inches="tight", pad_inches=0.03)
    fig.savefig(out + name + ".png", dpi=300, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def audit_text(fig, min_pt=5.5, print_width_pt=None):
    """Text-layout gate (after scientific-figure-suite G18): overlap, clipping, font size at print scale."""
    import itertools
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    W, H = fig.bbox.width, fig.bbox.height
    scale = 1.0 if print_width_pt is None else print_width_pt / (fig.get_figwidth() * 72)
    items = []
    for t in fig.findobj(matplotlib.text.Text):
        if not t.get_visible() or not t.get_text().strip():
            continue
        bb = t.get_window_extent(r)
        items.append((t.get_text().replace("\n", " | ")[:45], bb, t.get_fontsize() * scale))
    issues = []
    for name, bb, fs in items:
        if fs < min_pt:
            issues.append(f"SMALL {fs:.1f}pt: {name}")
        if bb.x0 < -1 or bb.y0 < -1 or bb.x1 > W + 1 or bb.y1 > H + 1:
            issues.append(f"CLIPPED: {name}")
    for (n1, b1, _), (n2, b2, _) in itertools.combinations(items, 2):
        if b1.overlaps(b2):
            ix = min(b1.x1, b2.x1) - max(b1.x0, b2.x0); iy = min(b1.y1, b2.y1) - max(b1.y0, b2.y0)
            if ix > 1 and iy > 1:
                issues.append(f"OVERLAP: '{n1}' x '{n2}'")
    print(f"[text audit] {len(items)} text elements, {len(issues)} issues, print scale {scale:.2f}")
    for i in issues:
        print("   ", i)
    return issues
