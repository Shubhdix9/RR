import csv
from collections import defaultdict
import numpy as np

# Load our CLUTCH-X advanced engine data
from clutch_x_advanced_engine import (
    bat_candidates, bowl_candidates, player_names, player_teams,
    retired_set, retained_superstars, is_pakistani, p80, deliveries
)

# 1. Identify Captains
captains = set()
with open('matches.csv', 'r') as f:
    for r in csv.DictReader(f):
        if r['home_team_captain_id']: captains.add(r['home_team_captain_id'])
        if r['away_team_captain_id']: captains.add(r['away_team_captain_id'])

with open('playing_eleven.csv', 'r') as f:
    for r in csv.DictReader(f):
        if r['is_captain'] == '1':
            captains.add(r['player_id'])

# Known captains / team leaders to exclude
known_captains = {
    'Rajat Patidar', 'Sai Sudharsan', 'Aiden Markram', 'Temba Bavuma',
    'Dasun Shanaka', 'Charith Asalanka', 'Sikandar Raza', 'Kusal Mendis',
    'Hardik Pandya', 'Rishabh Pant', 'Shreyas Iyer', 'KL Rahul', 'Sanju Samson',
    'Shubman Gill', 'Ruturaj Gaikwad', 'David Warner', 'Kane Williamson'
}

# 2. Check position distribution
batter_pos = defaultdict(lambda: {'top': 0, 'middle_death': 0})
bowler_phases = defaultdict(lambda: {'pp': 0, 'mid_death': 0, 'death': 0})

with open('ball_by_ball.csv', 'r') as f:
    for r in csv.DictReader(f):
        sid = r['striker_id']
        bid = r['bowler_id']
        bo = r['batting_order']
        ov = int(r['overid'])
        ext = r['extras_type']
        
        if bo and bo.isdigit():
            if int(bo) <= 3:
                batter_pos[sid]['top'] += 1
            else:
                batter_pos[sid]['middle_death'] += 1
                
        if ext not in ['wide', 'Overstep']:
            if ov <= 6:
                bowler_phases[bid]['pp'] += 1
            else:
                bowler_phases[bid]['mid_death'] += 1
                if ov >= 16:
                    bowler_phases[bid]['death'] += 1

print("--- FILTERING FOR PURE MIDDLE-ORDER / DEATH FINISHERS (POSITIONS 4-7) ---")
specialist_finishers = []
for b in bat_candidates:
    sid = b['id']
    name = b['name']
    
    # Exclude captains
    if sid in captains or name in known_captains:
        continue
        
    pos = batter_pos[sid]
    total_balls = pos['top'] + pos['middle_death']
    if total_balls == 0: continue
    
    # Exclude openers: must play majority or substantial in middle/death (positions 4+)
    # or specifically known as middle/lower finisher
    mid_death_ratio = pos['middle_death'] / total_balls
    if mid_death_ratio < 0.45:
        # predominantly opener/top 3
        continue
        
    specialist_finishers.append(b)

for i, b in enumerate(specialist_finishers[:15], 1):
    pos = batter_pos[b['id']]
    tot = pos['top'] + pos['middle_death']
    md_pct = (pos['middle_death'] / tot) * 100
    print(f"{i:2d}. {b['name']:20s} | CBI={b['cbi']:4.1f} | HP_Balls={b['balls']:3d} | HP_SR={b['sr_raw']:5.1f} | ΔSR={b['delta_sr']:+5.1f} | Dot%={b['dot_adj']:4.1f}% | Pos4+={md_pct:.0f}%")

print("\n--- FILTERING FOR MIDDLE & DEATH BOWLERS (EXCLUDE POWERPLAY OPENERS) ---")
specialist_bowlers = []
for bw in bowl_candidates:
    bid = bw['id']
    name = bw['name']
    
    # Exclude captains
    if bid in captains or name in known_captains:
        continue
        
    ph = bowler_phases[bid]
    total_legal = ph['pp'] + ph['mid_death']
    if total_legal == 0: continue
    
    # Exclude new-ball powerplay openers: pp ratio must NOT be dominant (>50% in PP)
    pp_ratio = ph['pp'] / total_legal
    if pp_ratio > 0.48:
        # Start/Opening bowler (New ball)
        continue
        
    specialist_bowlers.append(bw)

for i, bw in enumerate(specialist_bowlers[:15], 1):
    ph = bowler_phases[bw['id']]
    tot = ph['pp'] + ph['mid_death']
    d_pct = (ph['death'] / tot) * 100
    mid_pct = ((ph['mid_death'] - ph['death']) / tot) * 100
    print(f"{i:2d}. {bw['name']:20s} | PBI={bw['pbi']:4.1f} | HP_Balls={bw['balls']:3d} | Wkts={bw['wkts']:2d} | HP_Econ={bw['econ_raw']:5.2f} | ΔEcon={bw['delta_econ']:+5.2f} | Mid={mid_pct:.0f}% | Death={d_pct:.0f}%")

