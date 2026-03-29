"""
Selective Withdrawal Algorithm Schematic for CE-QUAL-W2

Illustrates how the selective withdrawal algorithm determines the fraction
of total outflow withdrawn from each vertical layer through a single
outlet in a dam.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(figsize=(10, 7))

# ── Geometry ───────────────────────────────────────────────────────────
n_layers = 16
seg_left = 1.0
seg_right = 5.8
seg_bottom = 0.5
seg_top = 8.5
layer_h = (seg_top - seg_bottom) / n_layers

# Trapezoidal dam: vertical on left (reservoir side), sloped on right
dam_left = seg_right
dam_top_right = dam_left + 0.35
dam_bot_right = dam_left + 1.0

outlet_y = 3.4
outlet_half = 0.20

zone_top = 7.0
zone_bot = 1.2

# ── Colors ─────────────────────────────────────────────────────────────
arrow_color = "#1A5276"
label_color = "#2C3E50"
bg_color = "#FAFCFD"

fig.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# ── Water layers (depth-graded color) ─────────────────────────────────
for i in range(n_layers):
    y0 = seg_bottom + i * layer_h
    frac = i / (n_layers - 1)
    r = int(0x5A + (0x9E - 0x5A) * frac)
    g = int(0xA8 + (0xDA - 0xA8) * frac)
    b = int(0xB8 + (0xE8 - 0xB8) * frac)
    ax.add_patch(patches.Rectangle(
        (seg_left, y0), seg_right - seg_left, layer_h,
        facecolor=f"#{r:02X}{g:02X}{b:02X}",
        edgecolor="white", linewidth=0.8
    ))

# ── Trapezoidal concrete dam ──────────────────────────────────────────
trap_verts = [
    (dam_left, seg_top),
    (dam_top_right, seg_top),
    (dam_bot_right, seg_bottom),
    (dam_left, seg_bottom),
]
ax.add_patch(patches.Polygon(
    trap_verts, closed=True,
    facecolor="#B0B0B0", edgecolor="#707070", linewidth=1.5, zorder=5
))

# Concrete texture: speckles
rng = np.random.RandomState(42)
for _ in range(180):
    sy = rng.uniform(seg_bottom + 0.1, seg_top - 0.1)
    t = (sy - seg_bottom) / (seg_top - seg_bottom)
    right_at_y = dam_bot_right + t * (dam_top_right - dam_bot_right)
    sx = rng.uniform(dam_left + 0.04, right_at_y - 0.04)
    gray = rng.randint(120, 185)
    ax.plot(sx, sy, '.', color=f"#{gray:02X}{gray:02X}{gray:02X}",
            markersize=rng.uniform(0.8, 2.5), alpha=0.5, zorder=5.1)

# Concrete pour lines
for yline in np.linspace(seg_bottom + 0.8, seg_top - 0.3, 8):
    t = (yline - seg_bottom) / (seg_top - seg_bottom)
    right_at_y = dam_bot_right + t * (dam_top_right - dam_bot_right)
    ax.plot([dam_left, right_at_y], [yline, yline],
            color="#909090", lw=0.5, alpha=0.4, zorder=5.2)

# ── Outlet opening ────────────────────────────────────────────────────
t_out = (outlet_y - seg_bottom) / (seg_top - seg_bottom)
right_at_outlet = dam_bot_right + t_out * (dam_top_right - dam_bot_right)
ax.add_patch(patches.Rectangle(
    (dam_left - 0.02, outlet_y - outlet_half),
    right_at_outlet - dam_left + 0.04, 2 * outlet_half,
    facecolor="#3A3A3A", edgecolor="#222222", linewidth=1.0, zorder=6
))

# ── Thin bed ──────────────────────────────────────────────────────────
bed_h = 0.12
ax.add_patch(patches.Rectangle(
    (seg_left - 0.3, seg_bottom - bed_h),
    (dam_bot_right - seg_left) + 0.65, bed_h,
    facecolor="#8B7D6B", edgecolor="#6B5D4B", linewidth=0.8
))

# ── Curved converging flow arrows ─────────────────────────────────────
def withdrawal_velocity(y, center, zt, zb):
    """Bell-shaped (cosine-squared) velocity profile."""
    if y > zt or y < zb:
        return 0.0
    if y >= center:
        s = (y - center) / (zt - center)
    else:
        s = (center - y) / (center - zb)
    return np.cos(s * np.pi / 2) ** 2

arrow_origin_x = 3.2
target_x = dam_left - 0.10
target_y = outlet_y

y_positions = np.linspace(seg_bottom + layer_h / 2,
                          seg_top - layer_h / 2, n_layers)

for y in y_positions:
    v = withdrawal_velocity(y, outlet_y, zone_top, zone_bot)
    if v < 0.03:
        continue

    dy = y - outlet_y
    rad = 0.15 * (dy / (zone_top - zone_bot)) * 4.0

    ax.add_patch(FancyArrowPatch(
        (arrow_origin_x, y), (target_x, target_y),
        arrowstyle="->,head_width=4,head_length=3",
        connectionstyle=f"arc3,rad={rad}",
        color=arrow_color,
        lw=1.0 + v * 1.6,
        alpha=0.45 + 0.55 * v,
        zorder=4
    ))

# ── Outflow arrow (line + equilateral triangle arrowhead) ─────────────
outflow_x0 = right_at_outlet + 0.02
outflow_x1 = outflow_x0 + 2.646  # longer arrow
# Draw the shaft as a plain line
ax.plot([outflow_x0, outflow_x1], [outlet_y, outlet_y],
        color=arrow_color, lw=2.8, solid_capstyle="butt", zorder=7)
# Equilateral triangle arrowhead
tri_side = 0.225
tri_h = tri_side * np.sqrt(3) / 2
tri_verts = [
    (outflow_x1 + tri_h, outlet_y),            # tip
    (outflow_x1, outlet_y + tri_side / 2),      # upper base
    (outflow_x1, outlet_y - tri_side / 2),      # lower base
]
ax.add_patch(patches.Polygon(
    tri_verts, closed=True,
    facecolor=arrow_color, edgecolor=arrow_color, linewidth=0.5, zorder=7
))

# ── Labels ─────────────────────────────────────────────────────────────
txt_kw = dict(fontsize=11, color=label_color, fontfamily="sans-serif")

ax.text((seg_left + seg_right) / 2, seg_top + 0.55,
        "Model segment next to dam",
        ha="center", va="bottom", fontsize=13.5, fontweight="bold",
        color=label_color, fontfamily="sans-serif")

lbl_x = seg_left - 0.55
lbl_y = (seg_top + seg_bottom) / 2
ax.text(lbl_x, lbl_y, "Vertical\nlayers", ha="center", va="center",
        fontstyle="italic", **txt_kw)

# Flow and Centerline labels: centered above and below the arrow midpoint
arrow_mid_x = (outflow_x0 + outflow_x1 + tri_h) / 2

ax.text(arrow_mid_x, outlet_y + 0.35, "Flow",
        ha="center", va="bottom", fontweight="bold", fontsize=12.5,
        color=arrow_color, fontfamily="sans-serif")

ax.text(arrow_mid_x, outlet_y - 0.35,
        "Centerline of withdrawal",
        ha="center", va="top", fontsize=10.5, color=label_color,
        fontfamily="sans-serif", fontstyle="italic")

# ── Axes ───────────────────────────────────────────────────────────────
ax.set_xlim(-0.2, 9.5)
ax.set_ylim(0.1, 9.8)
ax.set_aspect("equal")
ax.axis("off")

plt.tight_layout()
plt.savefig("/home/claude/selective_withdrawal_schematic.png",
            dpi=200, bbox_inches="tight", facecolor=bg_color)
plt.close()
print("Done.")
