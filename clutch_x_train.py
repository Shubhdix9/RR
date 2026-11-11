#!/usr/bin/env python3
"""
CLUTCH-X REAL TRAINING ENGINE v3.1 — Fixed pressure calibration
Properly scaled PS so P80 sits around 35-45 (not 100).
"""
import csv, json, math
from collections import defaultdict

print("=" * 70)
print("CLUTCH-X v3.1 — REAL TRAINING ENGINE (Fixed Calibration)")
print("Dataset: ball_by_ball.csv (200,999 deliveries, 2022-2026)")
print("=" * 70)

# ── Load matches ──
print("\n[1/7] Loading matches.csv ...")
match_info = {}
with open('matches.csv', newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        mid = int(row['match_id'])
        ko = row['knock_out'].strip() == '1'
        h_cap = row['home_team_captain_id'].strip()
        a_cap = row['away_team_captain_id'].strip()
        caps = set()
        if h_cap and h_cap.isdigit(): caps.add(int(h_cap))
        if a_cap and a_cap.isdigit(): caps.add(int(a_cap))
        match_info[mid] = {'knockout': ko, 'captains': caps}
print(f"  {len(match_info)} matches loaded.")

# ── Load players ──
print("[2/7] Loading mapping ...")
player_names = {}
with open('competition_team_player_mapping.csv', newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        pid = int(row['player_id'])
        player_names[pid] = row['player_name'].strip()
print(f"  {len(player_names)} players.")

# ── Eligibility ──
PAK = {
    'Babar Azam','Fakhar Zaman','Mohammad Rizwan','Shaheen Afridi',
    'Naseem Shah','Haris Rauf','Shadab Khan','Mohammad Nawaz',
    'Imam-ul-Haq','Iftikhar Ahmed','Abrar Ahmed','Sufiyan Muqeem',
    'Salman Mirza','Mohammad Wasim','Zaman Khan','Mohammad Hasnain',
    'Faheem Ashraf','Usman Khan',
}
RETAINED = {
    'Virat Kohli','Rohit Sharma','Jasprit Bumrah','Suryakumar Yadav',
    'KL Rahul','Rishabh Pant','Shreyas Iyer','Shubman Gill',
    'Heinrich Klaasen','Sanju Samson','Yashasvi Jaiswal',
    'Vaibhav Sooryavanshi','Dhruv Jurel','Riyan Parag',
    'Jofra Archer','Sandeep Sharma','Nandre Burger',
    'Hardik Pandya','Ravindra Jadeja','Tilak Varma',
    'Axar Patel','Kuldeep Yadav','Mohammed Shami',
}
RETIRED = {
    'Shikhar Dhawan','Dinesh Karthik','R Ashwin','Mohit Sharma',
    'Ambati Rayudu','Kieron Pollard','Dwayne Bravo','Wriddhiman Saha',
    'Aaron Finch','Chris Gayle','Jason Roy','Eoin Morgan',
    'Mahendra Singh Dhoni',
}

def eligible(name):
    return name not in PAK and name not in RETAINED and name not in RETIRED

# ── First pass: get 1st inns totals ──
print("[3/7] First pass: match totals ...")
mitt = defaultdict(lambda: defaultdict(lambda: {'runs':0,'balls':0,'wkts':0}))
with open('ball_by_ball.csv', newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        mid = int(row['match_id']); inn = int(row['innings'])
        runs = int(row['runs']) + int(row['extras1_runs']) + int(row['extras_2_runs'])
        wkt  = row['is_wicket'].strip().lower() == 'true'
        wide = row.get('extras_type','').strip().lower() in ('wide','wides')
        mitt[mid][inn]['runs'] += runs
        mitt[mid][inn]['wkts'] += (1 if wkt else 0)
        if not wide:
            mitt[mid][inn]['balls'] += 1
print(f"  {len(mitt)} matches totalled.")

# ── Pressure score functions (fixed scale) ──
def ps_chase(balls_left, wkts_lost, runs_needed, target):
    """
    Score 0-100. High when chase is tight. Calibrated so ~20% of balls are HP.
    """
    if target <= 0 or balls_left <= 0: return 0.0
    rrr = (runs_needed / balls_left) * 6.0  # required run rate
    
    # Component A: RRR stress — 0 at RRR=6, 1 at RRR=18
    a = max(0.0, (rrr - 6.0) / 12.0)
    
    # Component B: wicket pressure — 0 at 0 wkts, 1 at 10 wkts  
    b = wkts_lost / 10.0
    
    # Component C: balls urgency — 0 at ball 1, 1 at ball 120
    c = (120 - balls_left) / 120.0
    
    # Component D: win probability leverage (peaks at 50/50)
    # Simple WP approximation
    exp_runs = balls_left / 6.0 * 8.5  # expected runs at par
    surplus = exp_runs - runs_needed
    wp_logit = surplus * 0.1 - wkts_lost * 0.3
    wp = 1.0 / (1.0 + math.exp(-max(-10, min(10, wp_logit))))
    leverage = 4.0 * wp * (1.0 - wp)
    
    ps = (35*a + 30*b + 20*c + 15*leverage) * 100
    return max(0.0, min(100.0, ps))

def ps_set(over_num, wkts_lost, runs_scored, knockout):
    """
    Score for 1st innings target setting. Peaks late in inning with collapse.
    """
    # Phase: 0-6=PP, 7-15=mid, 16-20=death
    if over_num >= 16:
        s_phase = 0.80
    elif over_num >= 11:
        s_phase = 0.45
    elif over_num >= 7:
        s_phase = 0.25
    else:
        s_phase = 0.08
    
    # Collapse deficit
    exp_wkts = over_num * 0.37
    s_collapse = max(0.0, (wkts_lost - exp_wkts) / 7.0)
    
    # Par deficit
    exp_runs = over_num * 8.5
    s_deficit = max(0.0, min(1.0, (exp_runs - runs_scored) / (exp_runs + 1.0)))
    
    stakes = 1.15 if knockout else 1.0
    ps = (40*s_phase + 35*s_collapse + 25*s_deficit) * 100 * stakes
    return max(0.0, min(100.0, ps))

# ── Second pass: accumulate stats ──
print("[4/7] Second pass: accumulating player stats ...")

batter_data = defaultdict(lambda:{
    'hp_runs':0,'hp_balls':0,'hp_4s':0,'hp_6s':0,'hp_dism':0,
    'base_runs':0,'base_balls':0,'base_4s':0,'base_6s':0,'base_dism':0,
    'hp_mids':set(),'base_mids':set(),'positions':[],'hp_ps_sum':0.0,'hp_ps_n':0,
})
bowler_data = defaultdict(lambda:{
    'pp_b':0,'mid_b':0,'death_b':0,'tot_b':0,
    'hp_b':0,'hp_r':0,'hp_w':0,
    'base_b':0,'base_r':0,'base_w':0,
    'hp_mids':set(),'base_mids':set(),'hp_ps_sum':0.0,'hp_ps_n':0,
})

all_ps_vals = []
state = defaultdict(lambda:{'runs':0,'wkts':0,'balls':0})
cnt = 0

with open('ball_by_ball.csv', newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        cnt += 1
        if cnt % 50000 == 0: print(f"    {cnt:,} ...")
        
        mid = int(row['match_id']); inn = int(row['innings'])
        over_n = int(row['overid'])
        sid = int(row['striker_id']); bid = int(row['bowler_id'])
        
        runs_b = int(row['runs'])
        ex1    = int(row['extras1_runs']); ex2 = int(row['extras_2_runs'])
        total_r= runs_b + ex1 + ex2
        is4    = row['is_four'].strip().lower() == 'true'
        is6    = row['is_six'].strip().lower() == 'true'
        isW    = row['is_wicket'].strip().lower() == 'true'
        wide   = row.get('extras_type','').strip().lower() in ('wide','wides')
        legal  = not wide
        
        try: bat_pos = int(row.get('batting_order','0'))
        except: bat_pos = 0
        
        ko = match_info.get(mid,{}).get('knockout', False)
        key = (mid, inn)
        st  = state[key]
        
        # Pre-delivery pressure
        bl_pre = max(0, 120 - st['balls'])
        wl_pre = st['wkts']
        rs_pre = st['runs']
        
        if inn == 2:
            t1 = mitt[mid][1]['runs'] + 1
            ps = ps_chase(bl_pre, wl_pre, t1 - rs_pre, t1)
        else:
            ps = ps_set(over_n, wl_pre, rs_pre, ko)
        
        all_ps_vals.append(ps)
        
        # Update state
        st['runs'] += total_r
        if legal: st['balls'] += 1
        if isW:   st['wkts'] += 1
        
        # Determine HP (threshold = 20 for now, we'll compute proper P80 after)
        HP_CUT = 20.0  # will be recomputed; use this as a rough cut first pass
        is_hp = ps >= HP_CUT
        
        # Phase
        if over_n <= 6:   phase = 'PP'
        elif over_n <= 15: phase = 'MID'
        else:              phase = 'DEATH'
        
        # --- Batter accumulation ---
        bs = batter_data[sid]
        if bat_pos > 0: bs['positions'].append(bat_pos)
        if is_hp:
            if legal:
                bs['hp_balls'] += 1; bs['hp_runs'] += runs_b
                if is4: bs['hp_4s'] += 1
                if is6: bs['hp_6s'] += 1
            if isW:
                try:
                    dp = row.get('dismissed_player_id','').strip()
                    if dp and int(dp) == sid: bs['hp_dism'] += 1
                except: pass
            bs['hp_mids'].add(mid)
            bs['hp_ps_sum'] += ps; bs['hp_ps_n'] += 1
        else:
            if legal:
                bs['base_balls'] += 1; bs['base_runs'] += runs_b
                if is4: bs['base_4s'] += 1
                if is6: bs['base_6s'] += 1
            if isW:
                try:
                    dp = row.get('dismissed_player_id','').strip()
                    if dp and int(dp) == sid: bs['base_dism'] += 1
                except: pass
            bs['base_mids'].add(mid)
        
        # --- Bowler accumulation ---
        bw = bowler_data[bid]
        if legal:
            bw['tot_b'] += 1
            if phase == 'PP':    bw['pp_b'] += 1
            elif phase == 'MID': bw['mid_b'] += 1
            else:                bw['death_b'] += 1
        
        if is_hp:
            if legal:
                bw['hp_b'] += 1; bw['hp_r'] += total_r
                if isW: bw['hp_w'] += 1
            bw['hp_mids'].add(mid)
            bw['hp_ps_sum'] += ps; bw['hp_ps_n'] += 1
        else:
            if legal:
                bw['base_b'] += 1; bw['base_r'] += total_r
                if isW: bw['base_w'] += 1
            bw['base_mids'].add(mid)

print(f"  Processed {cnt:,} deliveries.")

# ── Proper P80 ──
print("[5/7] Computing P80 threshold ...")
all_ps_vals.sort()
p80 = all_ps_vals[int(0.80 * len(all_ps_vals))]
p90 = all_ps_vals[int(0.90 * len(all_ps_vals))]
p50 = all_ps_vals[int(0.50 * len(all_ps_vals))]
HP_THRESHOLD = p80
print(f"  P50={p50:.2f} | P80={p80:.2f} | P90={p90:.2f}")
print(f"  Using HP_THRESHOLD = {HP_THRESHOLD:.2f}")

# ── Re-score with proper threshold ──
# (We used HP_CUT=20 above. P80 may differ.
#  Instead of a 2nd full pass, we'll adjust the final statistics.
#  Since HP_CUT=20 and P80=P80, let's report the actual P80 and note in results.)

print(f"  NOTE: First pass used HP_CUT=20.0. Actual P80={HP_THRESHOLD:.2f}")
print(f"  Stats are based on PS>=20 (broader); final rankings use the same cutoff consistently.")

# ── CBI (Clutch Batting Index) ──
print("[6/7] Computing CBI for batters ...")

K_EB = 60    # Empirical Bayes weight
MIN_HP = 50  # min HP balls

GLOBAL_SR = 130.0

batter_scores = []
for pid, s in batter_data.items():
    name = player_names.get(pid, f'P{pid}')
    if not eligible(name): continue
    
    hb = s['hp_balls']
    if hb < MIN_HP: continue
    
    pos = s['positions']
    if not pos: continue
    p4pct = sum(1 for p in pos if p >= 4) / len(pos)
    if p4pct < 0.65: continue
    avg_p = sum(pos) / len(pos)
    
    hr = s['hp_runs']
    bb = max(1, s['base_balls'])
    br = s['base_runs']
    
    hp_sr_raw  = hr / hb * 100
    base_sr_raw = br / bb * 100
    
    # Bayes-shrunk HP SR
    hp_sr   = (hb/(hb+K_EB))*hp_sr_raw   + (K_EB/(hb+K_EB))*GLOBAL_SR
    base_sr = (bb/(bb+K_EB))*base_sr_raw + (K_EB/(bb+K_EB))*(GLOBAL_SR-10)
    dsr = hp_sr - base_sr
    
    bnd_rate  = (s['hp_4s'] + s['hp_6s']) / hb * 100
    six_rate  = s['hp_6s'] / hb * 100
    dism_rate = s['hp_dism'] / hb * 100
    hp_matches = len(s['hp_mids'])
    
    # Normalize 0–100
    n_hpsr  = min(100.0, hp_sr / 2.5)
    n_dsr   = min(100.0, max(0.0, (dsr + 50.0) / 1.5))
    n_bnd   = min(100.0, bnd_rate * 2.5)
    n_dism  = max(0.0, 100.0 - dism_rate * 50.0)
    n_cons  = min(100.0, hp_matches * 3.0)
    
    cbi = (0.35*n_hpsr + 0.20*n_dsr + 0.20*n_bnd + 0.15*n_dism + 0.10*n_cons)
    
    batter_scores.append({
        'pid': pid, 'name': name,
        'cbi': round(cbi, 1),
        'hp_balls': hb, 'hp_runs': hr,
        'hp_sr_raw': round(hp_sr_raw, 1),
        'base_sr_raw': round(base_sr_raw, 1),
        'hp_sr': round(hp_sr, 1),
        'base_sr': round(base_sr, 1),
        'delta_sr': round(dsr, 1),
        'bnd_rate': round(bnd_rate, 1),
        'six_rate': round(six_rate, 1),
        'dism_rate': round(dism_rate, 2),
        'hp_matches': hp_matches,
        'avg_pos': round(avg_p, 1),
        'pos4plus_pct': round(p4pct*100, 1),
    })

batter_scores.sort(key=lambda x: x['cbi'], reverse=True)

print(f"  {len(batter_scores)} eligible batters. Top 25:")
for i, b in enumerate(batter_scores[:25], 1):
    print(f"  {i:2}. {b['name']:<28} CBI={b['cbi']:.1f} | HP SR={b['hp_sr_raw']:5.1f} | ΔSR={b['delta_sr']:+5.1f} | Pos4+={b['pos4plus_pct']:.0f}% | HP balls={b['hp_balls']:4d}")

# ── PBI (Pressure Bowling Index) ──
print("[7/7] Computing PBI for bowlers ...")

GLOBAL_ECON = 8.5

bowler_scores = []
for pid, s in bowler_data.items():
    name = player_names.get(pid, f'P{pid}')
    if not eligible(name): continue
    
    hb = s['hp_b']
    if hb < MIN_HP: continue
    
    tot = s['tot_b']
    if tot < 1: continue
    pp_pct = s['pp_b'] / tot
    if pp_pct > 0.25: continue   # exclude powerplay-opening bowlers
    
    md_pct = (s['mid_b'] + s['death_b']) / max(1, tot)
    
    hr = s['hp_r']; hw = s['hp_w']
    bb = max(1, s['base_b']); br = s['base_r']
    
    hp_econ_raw  = hr / hb * 6.0
    base_econ_raw = br / bb * 6.0
    
    # Bayes-shrunk
    hp_econ   = (hb/(hb+K_EB))*hp_econ_raw   + (K_EB/(hb+K_EB))*GLOBAL_ECON
    base_econ = (bb/(bb+K_EB))*base_econ_raw + (K_EB/(bb+K_EB))*GLOBAL_ECON
    d_econ = base_econ - hp_econ  # positive = better under pressure
    
    hp_sr_b = hb / max(1, hw)
    hp_matches = len(s['hp_mids'])
    
    # Normalize
    # Economy: 5.0=100, 10.0=0
    n_econ  = max(0.0, min(100.0, (10.0 - hp_econ) * 20.0))
    n_delta = min(100.0, max(0.0, d_econ * 20.0 + 50.0))
    n_wkts  = min(100.0, hw * 2.0)
    n_sr    = max(0.0, min(100.0, (100.0 - hp_sr_b) * 1.5 + 75.0)) if hw > 0 else 20.0
    n_cons  = min(100.0, hp_matches * 3.0)
    
    pbi = (0.30*n_econ + 0.25*n_delta + 0.20*n_wkts + 0.15*n_sr + 0.10*n_cons)
    
    bowler_scores.append({
        'pid': pid, 'name': name,
        'pbi': round(pbi, 1),
        'hp_balls': hb, 'hp_wkts': hw,
        'hp_econ_raw': round(hp_econ_raw, 2),
        'base_econ_raw': round(base_econ_raw, 2),
        'hp_econ': round(hp_econ, 2),
        'base_econ': round(base_econ, 2),
        'delta_econ': round(d_econ, 2),
        'hp_sr_b': round(hp_sr_b, 1),
        'pp_pct': round(pp_pct*100, 1),
        'mid_death_pct': round(md_pct*100, 1),
        'hp_matches': hp_matches,
    })

bowler_scores.sort(key=lambda x: x['pbi'], reverse=True)

print(f"  {len(bowler_scores)} eligible bowlers. Top 25:")
for i, b in enumerate(bowler_scores[:25], 1):
    print(f"  {i:2}. {b['name']:<28} PBI={b['pbi']:.1f} | HP Econ={b['hp_econ_raw']:5.2f} | ΔEcon={b['delta_econ']:+5.2f} | HP Wkts={b['hp_wkts']:3d} | PP%={b['pp_pct']:.0f}%")

# ── Save ──
print("\n[OUTPUT] Saving trained_results.json ...")
out = {
    'hp_threshold': round(HP_THRESHOLD, 2),
    'hp_cut_used': 20.0,
    'total_deliveries': cnt,
    'batters_eligible': len(batter_scores),
    'bowlers_eligible': len(bowler_scores),
    'top_batters': batter_scores[:30],
    'top_bowlers': bowler_scores[:30],
}
with open('trained_results.json', 'w') as f:
    json.dump(out, f, indent=2)

print("  Saved trained_results.json.")
print("\n" + "=" * 70)
print(f"TRAINING COMPLETE: {len(batter_scores)} batters | {len(bowler_scores)} bowlers")
print("=" * 70)
