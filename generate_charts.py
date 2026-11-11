import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('charts', exist_ok=True)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, sans-serif'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# Color palette: Rajasthan Royals Pink and Royal Blue
RR_PINK = '#EA1A7F'
RR_BLUE = '#254AA5'
RR_NAVY = '#10224D'
RR_GOLD = '#E5A93C'
RR_LIGHT_BG = '#F8F9FA'

# 1. Figure 1: Pressure Score Distribution & P80 Cutoff
print("Generating Figure 1: Pressure Distribution...")
from clutch_x_master import ps_vals, p75, p80, p85

fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
num_bins = 50
vmin, vmax = 0.0, 100.0
bin_width = (vmax - vmin) / num_bins
counts = [0] * num_bins
for v in ps_vals:
    idx = int((v - vmin) / bin_width)
    if idx < 0: idx = 0
    elif idx >= num_bins: idx = num_bins - 1
    counts[idx] += 1
bin_centers = [vmin + (i + 0.5) * bin_width for i in range(num_bins)]

# Bar plot
for i in range(num_bins):
    col = RR_PINK if bin_centers[i] >= p80 else RR_BLUE
    alpha = 0.85 if bin_centers[i] >= p80 else 0.7
    ax.bar(bin_centers[i], counts[i], width=bin_width*0.88, color=col, alpha=alpha, edgecolor='white', linewidth=0.5)

ax.axvline(p80, color=RR_NAVY, linestyle='--', linewidth=2, label=f'P80 Cutoff ({p80:.1f}) - Top 20% Pressure')
ax.axvline(p75, color='#888888', linestyle=':', linewidth=1.5, label=f'P75 Sensitivity ({p75:.1f}) - Top 25%')
ax.axvline(p85, color=RR_GOLD, linestyle=':', linewidth=1.5, label=f'P85 Sensitivity ({p85:.1f}) - Top 15%')

ax.set_title('CLUTCH-X: Distribution of Pre-Delivery Match Pressure Scores (N=200,999)', fontsize=13, fontweight='bold', pad=15, color=RR_NAVY)
ax.set_xlabel('Continuous Pressure Score (0 - 100)', fontsize=11, fontweight='bold')
ax.set_ylabel('Number of Deliveries', fontsize=11, fontweight='bold')
ax.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=10)

# Annotation for regions
ax.text(18, max(counts)*0.75, 'Normal Match Context\n(80% of Deliveries)', color=RR_BLUE, fontweight='bold', ha='center', fontsize=10)
ax.text(55, max(counts)*0.45, 'CLUTCH ZONE\n(Top 20% High Pressure)', color=RR_PINK, fontweight='bold', ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('charts/fig1_pressure_distribution.png')
plt.close()

# 2. Figure 2: Top 10 Batters - Baseline vs Pressure Strike Rate (Delta SR)
print("Generating Figure 2: Batting Delta SR...")
from clutch_x_master import bat_p80

top10_b = bat_p80[:10]
names = [b['name'] for b in top10_b][::-1]
base_srs = [b['base_sr'] for b in top10_b][::-1]
hp_srs = [b['sr_raw'] for b in top10_b][::-1]
delta_srs = [b['delta_sr'] for b in top10_b][::-1]

y_pos = np.arange(len(names))
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

height = 0.38
rects1 = ax.barh(y_pos + height/2, base_srs, height, label='Baseline Strike Rate', color=RR_BLUE, alpha=0.75)
rects2 = ax.barh(y_pos - height/2, hp_srs, height, label='Pressure Strike Rate (CLUTCH-X)', color=RR_PINK, alpha=0.9)

ax.set_yticks(y_pos)
ax.set_yticklabels(names, fontsize=10, fontweight='bold')
ax.set_xlabel('Strike Rate (Runs per 100 Balls)', fontsize=11, fontweight='bold')
ax.set_title('Top 10 Batters: Normal Baseline vs. High-Pressure Strike Rate (ΔSR)', fontsize=13, fontweight='bold', pad=15, color=RR_NAVY)
ax.set_xlim(100, 225)
ax.legend(loc='lower right', frameon=True, facecolor='white', fontsize=10)

# Add Delta labels
for i, d in enumerate(delta_srs):
    ax.text(hp_srs[i] + 2, y_pos[i] - height/2, f"Δ: {d:+4.1f}", va='center', fontweight='bold', color=RR_PINK, fontsize=9)

plt.tight_layout()
plt.savefig('charts/fig2_batting_delta_sr.png')
plt.close()

# 3. Figure 3: Top 10 Bowlers - Baseline vs Pressure Economy (Delta Econ)
print("Generating Figure 3: Bowling Delta Econ...")
from clutch_x_master import bowl_p80

top10_bw = bowl_p80[:10]
bw_names = [b['name'] for b in top10_bw][::-1]
bw_base_econ = [b['base_econ'] for b in top10_bw][::-1]
bw_hp_econ = [b['econ_raw'] for b in top10_bw][::-1]
bw_delta_econ = [b['delta_econ'] for b in top10_bw][::-1]

y_pos = np.arange(len(bw_names))
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

rects1 = ax.barh(y_pos + height/2, bw_base_econ, height, label='Baseline Economy', color='#888888', alpha=0.6)
rects2 = ax.barh(y_pos - height/2, bw_hp_econ, height, label='Pressure Economy (CLUTCH-X)', color=RR_BLUE, alpha=0.9)

ax.set_yticks(y_pos)
ax.set_yticklabels(bw_names, fontsize=10, fontweight='bold')
ax.set_xlabel('Economy Rate (Runs per Over - Lower is Better)', fontsize=11, fontweight='bold')
ax.set_title('Top 10 Bowlers: Baseline vs. High-Pressure Economy Suppression (ΔEcon)', fontsize=13, fontweight='bold', pad=15, color=RR_NAVY)
ax.set_xlim(2, 11)
ax.legend(loc='lower right', frameon=True, facecolor='white', fontsize=10)

for i, d in enumerate(bw_delta_econ):
    ax.text(bw_hp_econ[i] - 0.2, y_pos[i] - height/2, f"Δ: {d:+4.2f}", va='center', ha='right', fontweight='bold', color=RR_BLUE, fontsize=9)

plt.tight_layout()
plt.savefig('charts/fig3_bowling_delta_econ.png')
plt.close()

# 4. Figure 4: Rajasthan Royals 2027 Auction Strategic Matrix
print("Generating Figure 4: RR Auction Matrix...")
fig, ax = plt.subplots(figsize=(9, 6), dpi=300)

# Quadrant plot: Experience / Sample Size (Balls) vs Clutch Index
# Highlight domestic / emerging diamonds vs established stars
targets = [
    ('Tom Banton', 89.5, 55, 'Overseas Finisher / WK', RR_PINK),
    ('Heinrich Klaasen', 84.7, 469, 'Overseas Spin Enforcer', RR_NAVY),
    ('Shreyas Iyer', 89.1, 326, 'Indian Core Anchor', RR_NAVY),
    ('Sai Sudharsan', 81.9, 195, 'Indian Top-Order Clutch', RR_NAVY),
    ('Romario Shepherd', 81.7, 247, 'Pace All-Rounder Finisher', RR_PINK),
    ('Vipraj Nigam', 82.0, 50, 'Domestic Wrist-Spin Diamond', RR_GOLD),
    ('Kane Richardson', 88.6, 73, 'Overseas Death Yorker', RR_BLUE),
    ('Craig Young', 87.0, 86, 'Associate/Overseas Seam', RR_BLUE),
    ('Noor Ahmad', 83.3, 258, 'Elite Wrist-Spin Squeeze', RR_BLUE),
    ('Sufiyan Muqeem', 97.6, 101, 'Global Benchmark Spinner', '#888888'),
]

for name, c_idx, balls, role, col in targets:
    ax.scatter(balls, c_idx, s=180, color=col, edgecolors='black', linewidth=1, alpha=0.9, zorder=5)
    offset_y = 1.0 if c_idx < 95 else -1.5
    offset_x = 10 if balls < 300 else -30
    ax.annotate(f"{name}\n({role})", (balls, c_idx), textcoords="offset points", xytext=(offset_x, offset_y),
                fontsize=8.5, fontweight='bold', color=RR_NAVY, bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#ddd", alpha=0.85))

ax.axhline(80.0, color='gray', linestyle='--', alpha=0.5)
ax.axvline(150, color='gray', linestyle='--', alpha=0.5)

ax.text(20, 96, 'High Impact / Emerging Gems\n(Value Auction Buys)', color=RR_PINK, fontweight='bold', fontsize=9.5)
ax.text(320, 96, 'Proven High-Volume Masters\n(Core Marquee Targets)', color=RR_NAVY, fontweight='bold', fontsize=9.5)

ax.set_title('RR War Room: IPL 2027 Auction Target Portfolio (Reliability vs Volume)', fontsize=13, fontweight='bold', pad=15, color=RR_NAVY)
ax.set_xlabel('Pressure Sample Size (High-Pressure Deliveries Faced / Bowled)', fontsize=11, fontweight='bold')
ax.set_ylabel('Clutch Performance Index (CBI / PBI)', fontsize=11, fontweight='bold')
ax.set_ylim(75, 100)
ax.set_xlim(20, 520)

plt.tight_layout()
plt.savefig('charts/fig4_rr_auction_matrix.png')
plt.close()

print("All charts successfully generated in charts/ directory!")
