import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

RR_PINK = '#D81B60'
RR_BLUE = '#1E40AF'
RR_NAVY = '#0F172A'
RR_GOLD = '#D97706'

fig, ax = plt.subplots(figsize=(13.5, 8.2), dpi=300)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, sans-serif'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.9

# 16 Players with exact coordinates
# Format: (name, score, balls, short_role, color, shape, text_pos, ha, va)
players = [
    # Top Left Batters Cluster
    ('Sameer Rizvi', 86.4, 85, 'Spin Enforcer #5/6', RR_PINK, 'circle', (50, 91.2), 'right', 'bottom'),
    ('Shubham Dubey', 85.1, 90, 'Left-Hand Finisher #6/7', RR_PINK, 'circle', (55, 79.5), 'right', 'top'),
    ('Donovan Ferreira', 84.5, 111, '360° Finisher / WK', RR_GOLD, 'circle', (125, 91.0), 'left', 'bottom'),
    
    # Top Middle Batters Cluster
    ('Sikandar Raza (Bat)', 83.8, 223, 'Crisis Recovery #5', RR_GOLD, 'circle', (165, 88.5), 'right', 'bottom'),
    ('Ashutosh Sharma', 88.2, 233, 'Domestic Death Destroyer', RR_PINK, 'circle', (233, 93.0), 'center', 'bottom'),
    ('Liam Livingstone', 82.9, 237, 'Middle-Overs Destroyer', RR_NAVY, 'circle', (185, 75.0), 'right', 'top'),
    ('Shashank Singh', 79.1, 277, 'Clutch Domestic Finisher', RR_PINK, 'circle', (305, 75.0), 'left', 'top'),
    
    # Top Right Batter
    ('Tim David', 81.0, 423, 'Elite Death Boundary Striker', RR_NAVY, 'circle', (440, 85.5), 'left', 'bottom'),
    
    # Bottom Left Bowlers Cluster
    ('Sikandar Raza (Bowl)', 53.9, 67, 'Mystery Spin Squeeze (7.12 RPO)', RR_GOLD, 'square', (40, 47.5), 'right', 'top'),
    ('Washington Sundar', 55.2, 87, 'Powerplay & Middle Control', RR_PINK, 'square', (55, 61.5), 'right', 'bottom'),
    ('Gudakesh Motie', 55.4, 88, 'Left-Arm Finger Spin Squeeze', RR_GOLD, 'square', (115, 47.5), 'left', 'top'),
    ('Umran Malik', 61.6, 126, 'Express Pace (155+ km/h)', RR_BLUE, 'square', (126, 66.8), 'center', 'bottom'),
    ('Mitchell Santner', 54.3, 175, 'Elite Defensive Spin (7.58 RPO)', RR_NAVY, 'square', (195, 60.5), 'left', 'bottom'),
    
    # Bottom Right Bowlers Cluster
    ('Noor Ahmad', 49.8, 386, 'Left-Arm Wrist Spin Mystery', RR_BLUE, 'square', (350, 46.0), 'right', 'top'),
    ('Matheesha Pathirana', 50.5, 431, 'Slingy Yorker Specialist', RR_BLUE, 'square', (400, 56.5), 'right', 'bottom'),
    ('Yuzvendra Chahal', 54.2, 495, 'All-Time Leading Wicket-Taker', RR_PINK, 'square', (495, 60.5), 'center', 'bottom'),
]

# Plot scatter points
for name, score, balls, role, col, shape, (tx, ty), ha, va in players:
    marker = 'o' if shape == 'circle' else 's'
    edge_col = '#0F172A'
    ax.scatter(balls, score, s=150, color=col, edgecolors=edge_col, linewidth=1.4, alpha=0.95, zorder=5, marker=marker)
    
    # Clean pointer arrow and clean box
    ax.annotate(
        f"{name}\n{role}",
        xy=(balls, score),
        xytext=(tx, ty),
        fontsize=8.2,
        fontweight='bold',
        color='#0F172A',
        ha=ha,
        va=va,
        bbox=dict(boxstyle='round,pad=0.32', facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=0.8, alpha=0.96),
        arrowprops=dict(
            arrowstyle='->',
            connectionstyle='arc3,rad=0.08',
            color='#64748B',
            lw=0.9,
            shrinkA=2,
            shrinkB=4
        ),
        zorder=6
    )

# Axis limits & grid
ax.set_xlim(15, 545)
ax.set_ylim(44, 96)
ax.set_xlabel('High-Pressure Deliveries Faced / Bowled (Sample Reliability & Experience)', fontsize=11, fontweight='bold', color=RR_NAVY, labelpad=10)
ax.set_ylabel('High-Pressure Performance Index (CBI / PBI Scale)', fontsize=11, fontweight='bold', color=RR_NAVY, labelpad=10)
ax.set_title('Rajasthan Royals IPL 2027 Auction Target Portfolio: Performance Index vs Sample Volume', fontsize=13, fontweight='bold', pad=18, color=RR_NAVY)

# Dividing Lines
ax.axhline(68, color='#94A3B8', linestyle='--', linewidth=1.2, alpha=0.6, zorder=2)
ax.axvline(200, color='#94A3B8', linestyle='--', linewidth=1.2, alpha=0.6, zorder=2)

# Quadrant Banner Tags (Positioned away from data points)
ax.text(105, 94.8, 'HIGH-CEILING VALUE TARGETS\nElite Rate Execution • Favorable Purse Impact', 
        ha='center', va='top', fontsize=8.5, fontweight='bold', color='#B45309',
        bbox=dict(boxstyle='square,pad=0.35', facecolor='#FEF3C7', edgecolor='#F59E0B', alpha=0.85, linewidth=0.8))

ax.text(420, 94.8, 'PROVEN HIGH-LEVERAGE ASSETS\nVerified Sample Volume • Direct Walk-in XI', 
        ha='center', va='top', fontsize=8.5, fontweight='bold', color='#BE185D',
        bbox=dict(boxstyle='square,pad=0.35', facecolor='#FDF2F8', edgecolor='#F472B6', alpha=0.85, linewidth=0.8))

ax.text(105, 44.5, 'TACTICAL MATCHUP OPERATORS\nPhase Specialists • Economy Squeeze', 
        ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#1E40AF',
        bbox=dict(boxstyle='square,pad=0.35', facecolor='#EFF6FF', edgecolor='#93C5FD', alpha=0.85, linewidth=0.8))

ax.text(420, 44.5, 'VETERAN SPECIALISTS & MARQUEE ASSETS\nProven Track Record Under Severe Match Stress', 
        ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#0F172A',
        bbox=dict(boxstyle='square,pad=0.35', facecolor='#F1F5F9', edgecolor='#CBD5E1', alpha=0.85, linewidth=0.8))

# Clean Legend in empty center-right whitespace (x=330, y=69)
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Target Batters (#4–7 Finishers)', markerfacecolor=RR_PINK, markersize=9, markeredgecolor='#0F172A', markeredgewidth=1.2),
    Line2D([0], [0], marker='s', color='w', label='Target Bowlers (Overs 7–20)', markerfacecolor=RR_BLUE, markersize=9, markeredgecolor='#0F172A', markeredgewidth=1.2),
    Line2D([0], [0], marker='o', color='w', label='High-Utility All-Rounders', markerfacecolor=RR_GOLD, markersize=9, markeredgecolor='#0F172A', markeredgewidth=1.2),
]
leg = ax.legend(handles=legend_elements, loc='center', bbox_to_anchor=(0.68, 0.52), frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', framealpha=0.95, fontsize=8.8)
leg.get_frame().set_linewidth(0.8)

plt.tight_layout()
plt.savefig('charts/fig4_rr_auction_matrix.png', dpi=300)
plt.close()
print("Clean non-overlapping Figure 4 generated successfully!")

