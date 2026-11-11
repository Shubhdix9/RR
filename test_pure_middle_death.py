import csv
from collections import defaultdict

# 1. Load candidates from clutch_x_advanced_engine
from clutch_x_advanced_engine import (
    bat_candidates, bowl_candidates, player_names, player_teams,
    retired_set, retained_superstars, is_pakistani
)

# 2. IPL 2025 and 2026 captains
ipl_captains = {
    'Ajinkya Rahane', 'Suryakumar Yadav', 'Jasprit Bumrah', 'Riyan Parag',
    'Rishabh Pant', 'Patrick Cummins', 'Faf du Plessis', 'Shreyas Iyer',
    'Ruturaj Gaikwad', 'Yashasvi Jaiswal', 'Mahendra Singh Dhoni', 'Sanju Samson',
    'Rashid Khan', 'Shubman Gill', 'Jitesh Sharma', 'Hardik Pandya', 'KL Rahul',
    'Axar Patel', 'Sam Curran', 'Rajat Patidar', 'Sai Sudharsan', 'Aiden Markram'
}

# 3. Check exact batting order distribution
batter_pos = defaultdict(lambda: Counter())
bowler_phases = defaultdict(lambda: {'pp': 0, 'mid': 0, 'death': 0})
from collections import Counter

with open('ball_by_ball.csv', 'r') as f:
    for r in csv.DictReader(f):
        sid = r['striker_id']
        bid = r['bowler_id']
        bo = r['batting_order']
        ov = int(r['overid'])
        ext = r['extras_type']
        
        if bo and bo.isdigit():
            batter_pos[sid][int(bo)] += 1
            
        if ext not in ['wide', 'Overstep']:
            if ov <= 6: bowler_phases[bid]['pp'] += 1
            elif ov <= 15: bowler_phases[bid]['mid'] += 1
            else: bowler_phases[bid]['death'] += 1

print("=== PURE MIDDLE-ORDER & DEATH FINISHERS (BATTERS 4-7) ===")
# Exclude: Openers / Top 3 (>40% balls in pos 1-3), Captains, Retained stars, Pakistani, Retired
pure_finishers = []
for b in bat_candidates:
    name = b['name']
    sid = b['id']
    if name in ipl_captains or sid in ipl_captains:
        continue
    pos = batter_pos[sid]
    tot = sum(pos.values())
    if tot == 0: continue
    
    top3_balls = pos[1] + pos[2] + pos[3]
    top3_pct = (top3_balls / tot) * 100
    mid_death_balls = sum(pos[i] for i in range(4, 12))
    mid_death_pct = (mid_death_balls / tot) * 100
    
    # Must be overwhelmingly middle/death (positions 4+)
    if top3_pct > 25.0: # If more than 25% balls in top 3, exclude as opener/top-order!
        continue
        
    pure_finishers.append((b, mid_death_pct, pos))

for i, (b, md_pct, pos) in enumerate(pure_finishers[:15], 1):
    pos_summary = ", ".join([f"#{k}:{v}" for k, v in sorted(pos.items()) if v > 10])
    print(f"{i:2d}. {b['name']:20s} | CBI={b['cbi']:4.1f} | HP_Balls={b['balls']:3d} | HP_SR={b['sr_raw']:5.1f} | ΔSR={b['delta_sr']:+5.1f} | Dot%={b['dot_adj']:4.1f}% | Pos4+={md_pct:.0f}% ({pos_summary})")

print("\n=== PURE MIDDLE-OVERS & DEATH SPECIALISTS (BOWLERS 7-20) ===")
# Exclude: Start/Opening bowlers (>30% balls in Powerplay), Captains, Retained stars, Pakistani, Retired
pure_middle_death_bowlers = []
for bw in bowl_candidates:
    name = bw['name']
    bid = bw['id']
    if name in ipl_captains:
        continue
    ph = bowler_phases[bid]
    tot = sum(ph.values())
    if tot == 0: continue
    
    pp_pct = (ph['pp'] / tot) * 100
    mid_pct = (ph['mid'] / tot) * 100
    death_pct = (ph['death'] / tot) * 100
    
    # Must NOT be a start / powerplay bowler (Powerplay < 25%)
    if pp_pct > 25.0:
        continue
        
    pure_middle_death_bowlers.append((bw, pp_pct, mid_pct, death_pct))

for i, (bw, pp_pct, mid_pct, death_pct) in enumerate(pure_middle_death_bowlers[:15], 1):
    print(f"{i:2d}. {bw['name']:20s} | PBI={bw['pbi']:4.1f} | HP_Balls={bw['balls']:3d} | Wkts={bw['wkts']:2d} | HP_Econ={bw['econ_raw']:5.2f} | ΔEcon={bw['delta_econ']:+5.2f} | PP={pp_pct:.0f}% | Mid={mid_pct:.0f}% | Death={death_pct:.0f}%")

