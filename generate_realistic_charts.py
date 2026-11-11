import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import json
import os

os.makedirs('charts', exist_ok=True)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, sans-serif'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

RR_PINK = '#EA1A7F'
RR_BLUE = '#254AA5'
RR_NAVY = '#10224D'
RR_GOLD = '#E5A93C'

with open('top_players_summary.json', 'r') as f:
    data = json.load(f)

batters = data['batters'][:10]
bowlers = data['bowlers'][:10]

# 1. Figure 2: Pure Finishers Batting Delta SR
print("Generating Specialist Batting Delta SR...")
names = [b['name'] for b in batters][::-1]
base_srs = [b['base_sr'] for b in batters][::-1]
hp_srs = [b['sr_raw'] for b in batters][::-1]
delta_srs = [b['delta_sr'] for b in batters][::-1]

y_pos = np.arange(len(names))
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
height = 0.38

rects1 = ax.barh(y_pos + height/2, base_srs, height, label='Career Baseline Strike Rate', color=RR_BLUE, alpha=0.75)
rects2 = ax.barh(y_pos - height/2, hp_srs, height, label='High-Pressure Strike Rate (CLUTCH-X)', color=RR_PINK, alpha=0.9)

ax.set_yticks(y_pos)
ax.set_yticklabels(names, fontsize=10, fontweight='bold')
ax.set_xlabel('Strike Rate (Runs per 100 Balls)', fontsize=11, fontweight='bold')
ax.set_title('RR Auction Targets: Top 10 Middle-Order & Death Finishers (ΔSR)', fontsize=13, fontweight='bold', pad=15, color=RR_NAVY)
ax.set_xlim(125, 230)
ax.legend(loc='lower right', frameon=True, facecolor='white', fontsize=10)

for i, d in enumerate(delta_srs):
    ax.text(hp_srs[i] + 2, y_pos[i] - height/2, f"Δ: +{d:.1f}", va='center', fontweight='bold', color=RR_PINK, fontsize=9)

plt.tight_layout()
plt.savefig('charts/fig2_batting_delta_sr.png')
plt.close()

# 2. Figure 3: Pure Middle & Death Bowling Delta Econ
print("Generating Specialist Bowling Delta Econ...")
bw_names = [b['name'] for b in bowlers][::-1]
bw_base_econ = [b['base_econ'] for b in bowlers][::-1]
bw_hp_econ = [b['econ_raw'] for b in bowlers][::-1]
bw_delta_econ = [b['delta_econ'] for b in bowlers][::-1]

y_pos = np.arange(len(bw_names))
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)

rects1 = ax.barh(y_pos + height/2, bw_base_econ, height, label='Career Baseline Economy', color='#888888', alpha=0.6)
rects2 = ax.barh(y_pos - height/2, bw_hp_econ, height, label='High-Pressure Economy (CLUTCH-X)', color=RR_BLUE, alpha=0.9)

ax.set_yticks(y_pos)
ax.set_yticklabels(bw_names, fontsize=10, fontweight='bold')
ax.set_xlabel('Economy Rate (Runs per Over - Lower is Better)', fontsize=11, fontweight='bold')
ax.set_title('RR Auction Targets: Top 10 Middle & Death-Overs Bowlers (ΔEcon)', fontsize=13, fontweight='bold', pad=15, color=RR_NAVY)
ax.set_xlim(3.5, 11.5)
ax.legend(loc='lower right', frameon=True, facecolor='white', fontsize=10)

for i, d in enumerate(bw_delta_econ):
    ax.text(bw_hp_econ[i] - 0.25, y_pos[i] - height/2, f"Δ: +{d:.2f}", va='center', ha='right', fontweight='bold', color=RR_BLUE, fontsize=9)

plt.tight_layout()
plt.savefig('charts/fig3_bowling_delta_econ.png')
plt.close()

# 3. Figure 4: RR Specialist Auction Matrix
print("Generating Figure 4: Specialist Auction Target Matrix...")
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)

targets = [
    ('Glenn Maxwell', 92.4, 183, 'Middle-Overs Game Changer', RR_PINK),
    ('Shashank Singh', 84.4, 193, 'Domestic Clutch Finisher', RR_GOLD),
    ('Romario Shepherd', 84.0, 247, '#7 Pace All-Rounder', RR_PINK),
    ('Marcus Stoinis', 83.6, 359, 'Seam All-Rounder Finisher', RR_NAVY),
    ('Abdul Samad', 82.3, 164, 'Domestic Death Striker', RR_GOLD),
    ('Tim David', 82.2, 448, 'Death Boundary Maximizer', RR_PINK),
    ('Liam Livingstone', 81.6, 270, 'Middle-Overs Power Enforcer', RR_NAVY),
    ('Vipraj Nigam', 87.7, 50, 'Domestic Leg-Spin Diamond', RR_GOLD),
    ('Noor Ahmad', 87.1, 258, 'Left-Arm Wrist Spin', RR_BLUE),
    ('Matheesha Pathirana', 85.0, 394, 'Slingy Death Yorker Specialist', RR_BLUE),
    ('Kartik Tyagi', 82.2, 107, 'Express Pace / Reverse Yorker', RR_NAVY),
    ('Harshal Patel', 73.6, 470, 'Death Slower Ball Specialist', RR_BLUE),
]

for name, c_idx, balls, role, col in targets:
    ax.scatter(balls, c_idx, s=190, color=col, edgecolors='black', linewidth=1.2, alpha=0.9, zorder=5)
    offset_y = 1.0 if c_idx < 88 else -1.5
    offset_x = 10 if balls < 200 else -25
    ax.annotate(f"{name}\n({role})", (balls, c_idx), textcoords="offset points", xytext=(offset_x, offset_y),
                fontsize=8.5, fontweight='bold', color=RR_NAVY, bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#ddd", alpha=0.9))

ax.axhline(80.0, color='gray', linestyle='--', alpha=0.5)
ax.axvline(200, color='gray', linestyle='--', alpha=0.5)

ax.text(30, 93.5, 'HIGH-IMPACT / DOMESTIC GEMS\n(Target for Steals / Budget Arbitrage)', color=RR_PINK, fontweight='bold', fontsize=9.5)
ax.text(260, 93.5, 'PROVEN HIGH-VOLUME WEAPONS\n(Target for Core Starting XI Roles)', color=RR_NAVY, fontweight='bold', fontsize=9.5)

ax.set_title('Rajasthan Royals War Room: Middle-Order & Death Specialists Portfolio', fontsize=13, fontweight='bold', pad=15, color=RR_NAVY)
ax.set_xlabel('Sample Size (High-Pressure Deliveries Faced / Bowled)', fontsize=11, fontweight='bold')
ax.set_ylabel('Clutch Performance Index (CBI / PBI)', fontsize=11, fontweight='bold')
ax.set_ylim(70, 96)
ax.set_xlim(20, 500)

plt.tight_layout()
plt.savefig('charts/fig4_rr_auction_matrix.png')
plt.close()

print("All specialist charts successfully updated in charts/!")
