#!/usr/bin/env python3
"""
CLUTCH-X REAL TRAINING ENGINE v5.0 — FINAL CORRECT VERSION
Schema fixed:
  - 'runs' column = all runs scored on that delivery (batter + extras like byes)
  - 'extras1_runs' for extras_type=None is ALWAYS 6 (artifact = balls per over), IGNORE IT
  - 'extras1_runs' for wide/no-ball = penalty runs (1 for no-ball, 1-2 for wide)
  - For bowler economy: runs scored off the bat + wide/no-ball penalty (not legbyes/byes)
  - For batter scoring: 'runs' column directly (includes batter's runs)
  
Pressure Model (properly calibrated, all components in [0,1]):
  - Chase: 35*RRR_stress + 30*wicket_dep + 20*urgency + 15*leverage = 0-100
  - 1st inns: 40*phase + 35*collapse + 25*par_deficit = 0-100
  - HP threshold = P80 of all deliveries
"""
import csv, json, math
from collections import defaultdict

print("=" * 70)
print("CLUTCH-X v5.0 — FINAL REAL TRAINING")
print("=" * 70)

# ── Load matches ──
match_info = {}
with open('matches.csv', newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        mid = int(row['match_id'])
        ko = row['knock_out'].strip() == '1'
        h = row['home_team_captain_id'].strip()
        a = row['away_team_captain_id'].strip()
        caps = set()
        if h and h.isdigit(): caps.add(int(h))
        if a and a.isdigit(): caps.add(int(a))
        match_info[mid] = {'knockout': ko, 'captains': caps}
print(f"[1] {len(match_info)} matches")

# ── Load players ──
player_names = {}
with open('competition_team_player_mapping.csv', newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        pid = int(row['player_id'])
        player_names[pid] = row['player_name'].strip()
print(f"[2] {len(player_names)} players")

# ── Eligibility ──
PAK = {
    'Babar Azam','Fakhar Zaman','Mohammad Rizwan','Shaheen Afridi',
    'Naseem Shah','Haris Rauf','Shadab Khan','Mohammad Nawaz',
    'Imam-ul-Haq','Iftikhar Ahmed','Abrar Ahmed','Sufiyan Muqeem',
    'Salman Mirza','Mohammad Wasim','Zaman Khan','Mohammad Hasnain',
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

# ── 1st-pass: 1st innings total USING RUNS COLUMN ONLY ──
print("[3] First pass: inning totals ...")
mitt = defaultdict(lambda: defaultdict(lambda: {'runs': 0, 'balls': 0}))
with open('ball_by_ball.csv', newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        mid = int(row['match_id']); inn = int(row['innings'])
        runs = int(row['runs'])   # ONLY the runs column
        wide = row.get('extras_type','').strip().lower() in ('wide','wides')
        # Add wide penalty for total score (wides still count toward target)
        if wide:
            penalty = int(row['extras1_runs'])   # 1-2 for wide
            runs += penalty
        mitt[mid][inn]['runs'] += runs
        if not wide:
            mitt[mid][inn]['balls'] += 1
print(f"   {len(mitt)} matches")

# ── PS functions ──
def ps_chase(balls_left, wkts_lost, runs_needed, target):
    if target <= 0 or balls_left <= 0: return 0.0
    rrr = max(0.0, (runs_needed / balls_left) * 6.0)
    a = max(0.0, min(1.0, (rrr - 6.0) / 12.0))   # 0 at rrr=6, 1 at rrr=18
    b = min(1.0, wkts_lost / 10.0)
    c = (120 - balls_left) / 120.0
    exp_runs = (balls_left / 6.0) * 8.5
    surplus  = exp_runs - max(0.0, runs_needed)
    wp_logit = max(-10.0, min(10.0, surplus * 0.08 - wkts_lost * 0.25))
    wp  = 1.0 / (1.0 + math.exp(-wp_logit))
    lev = 4.0 * wp * (1.0 - wp)
    return max(0.0, min(100.0, 35.0*a + 30.0*b + 20.0*c + 15.0*lev))

def ps_set(over_num, wkts_lost, runs_scored, knockout):
    if over_num >= 16:   a = 1.00
    elif over_num >= 11: a = 0.56
    elif over_num >= 7:  a = 0.31
    else:                a = 0.10
    exp_wkts = over_num * 0.37
    b = max(0.0, min(1.0, (wkts_lost - exp_wkts) / 7.0))
    exp_runs = over_num * 8.5
    c = max(0.0, min(1.0, (exp_runs - runs_scored) / (exp_runs * 1.2))) if exp_runs > 0 else 0.0
    stakes = 1.15 if knockout else 1.0
    return max(0.0, min(100.0, (40.0*a + 35.0*b + 25.0*c) * stakes))

# ── 2nd-pass: accumulate ──
print("[4] Second pass: computing pressure & stats ...")

batter_data = defaultdict(lambda: {
    'hp_runs':0,'hp_balls':0,'hp_4s':0,'hp_6s':0,'hp_dism':0,
    'base_runs':0,'base_balls':0,'base_4s':0,'base_6s':0,'base_dism':0,
    'hp_mids':set(),'base_mids':set(),'positions':[],'all_ps':[],
})
bowler_data = defaultdict(lambda: {
    'pp_b':0,'mid_b':0,'death_b':0,'tot_b':0,
    'hp_b':0,'hp_r':0,'hp_w':0,
    'base_b':0,'base_r':0,'base_w':0,
    'hp_mids':set(),'base_mids':set(),'all_ps':[],
})

all_ps = []
state  = defaultdict(lambda: {'runs':0,'wkts':0,'balls':0})
cnt    = 0

with open('ball_by_ball.csv', newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        cnt += 1
        if cnt % 50000 == 0: print(f"   {cnt:,} ...")

        mid   = int(row['match_id']); inn = int(row['innings'])
        over_n= int(row['overid'])
        sid   = int(row['striker_id']); bid = int(row['bowler_id'])

        batter_runs = int(row['runs'])   # runs scored off the bat (0,1,2,3,4,6)
        is4  = row['is_four'].strip().lower() == 'true'
        is6  = row['is_six'].strip().lower() == 'true'
        isW  = row['is_wicket'].strip().lower() == 'true'

        et   = row.get('extras_type','').strip().lower()
        wide = et in ('wide','wides')
        noball = et in ('overstep','no ball','no-ball','noball')
        # Penalty runs for wide/noball (counted against bowler)
        if wide or noball:
            penalty = int(row['extras1_runs'])  # 1-2 for wide, 1 for no-ball
        else:
            penalty = 0
        legal = not wide  # wides don't count as a legal delivery

        # Runs for bowler's economy: batter_runs + wide/noball penalty
        # (legbyes/byes don't count against bowler)
        bowler_runs = batter_runs + penalty

        try: bat_pos = int(row.get('batting_order','0'))
        except: bat_pos = 0

        ko  = match_info.get(mid, {}).get('knockout', False)
        key = (mid, inn)
        st  = state[key]

        bl = max(0, 120 - st['balls'])
        wl = st['wkts']
        rs = st['runs']

        # PS (pre-delivery state)
        if inn == 2:
            t1 = mitt[mid][1]['runs'] + 1
            ps = ps_chase(bl, wl, t1 - rs, t1)
        else:
            ps = ps_set(over_n, wl, rs, ko)

        all_ps.append(ps)

        # Update state (post-delivery)
        st['runs'] += batter_runs + penalty   # all runs added to inning total
        if legal: st['balls'] += 1
        if isW:   st['wkts'] += 1

        # Phase
        if over_n <= 6:    phase = 'PP'
        elif over_n <= 15: phase = 'MID'
        else:              phase = 'DEATH'

        # We'll assign HP after computing P80 — store ps per delivery per player
        bs = batter_data[sid]
        if bat_pos > 0: bs['positions'].append(bat_pos)
        bs['all_ps'].append((ps, batter_runs, is4, is6, isW, mid, row.get('dismissed_player_id','').strip(), legal))

        bw = bowler_data[bid]
        bw['all_ps'].append((ps, bowler_runs, isW, wide, legal, phase, mid))

print(f"   {cnt:,} deliveries")

# ── Compute P80 ──
all_ps_s = sorted(all_ps)
n = len(all_ps_s)
P80 = all_ps_s[int(0.80 * n)]
P90 = all_ps_s[int(0.90 * n)]
P50 = all_ps_s[int(0.50 * n)]
print(f"[5] PS: P50={P50:.2f} | P80={P80:.2f} | P90={P90:.2f}")
print(f"   HP threshold = P80 = {P80:.2f}")
HP = P80

# ── Aggregate per player using correct HP threshold ──
print("[6] Aggregating with real HP threshold ...")
for pid, s in batter_data.items():
    for (ps, runs_b, is4, is6, isW, mid, dism_id, legal) in s['all_ps']:
        if ps >= HP:
            if legal:
                s['hp_balls'] += 1; s['hp_runs'] += runs_b
                if is4: s['hp_4s'] += 1
                if is6: s['hp_6s'] += 1
            if isW and dism_id.isdigit() and int(dism_id) == pid:
                s['hp_dism'] += 1
            s['hp_mids'].add(mid)
        else:
            if legal:
                s['base_balls'] += 1; s['base_runs'] += runs_b
                if is4: s['base_4s'] += 1
                if is6: s['base_6s'] += 1
            if isW and dism_id.isdigit() and int(dism_id) == pid:
                s['base_dism'] += 1
            s['base_mids'].add(mid)

for pid, s in bowler_data.items():
    for (ps, bowler_r, isW, wide, legal, phase, mid) in s['all_ps']:
        if legal:
            s['tot_b'] += 1
            if phase == 'PP':    s['pp_b'] += 1
            elif phase == 'MID': s['mid_b'] += 1
            else:                s['death_b'] += 1
        if ps >= HP:
            if legal:
                s['hp_b'] += 1; s['hp_r'] += bowler_r
                if isW: s['hp_w'] += 1
            elif wide:  # wides count in HP
                s['hp_b'] += 0  # don't add to ball count, do add runs
                s['hp_r'] += bowler_r
            s['hp_mids'].add(mid)
        else:
            if legal:
                s['base_b'] += 1; s['base_r'] += bowler_r
                if isW: s['base_w'] += 1
            s['base_mids'].add(mid)

# ── CBI ──
print("[7] CBI: ranking batters ...")
K = 60; MIN_HP = 40; GLOBAL_SR = 130.0

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

    hr = s['hp_runs']; bb = max(1, s['base_balls']); br = s['base_runs']
    hp_sr_raw   = hr / hb * 100
    base_sr_raw = br / bb * 100
    hp_sr   = (hb/(hb+K))*hp_sr_raw   + (K/(hb+K))*GLOBAL_SR
    base_sr = (bb/(bb+K))*base_sr_raw + (K/(bb+K))*(GLOBAL_SR - 10)
    dsr = hp_sr - base_sr

    bnd_rate  = (s['hp_4s'] + s['hp_6s']) / hb * 100
    six_rate  = s['hp_6s'] / hb * 100
    dism_rate = s['hp_dism'] / max(1, hb) * 100
    hp_matches = len(s['hp_mids'])

    n_hpsr = min(100.0, hp_sr / 2.5)
    n_dsr  = min(100.0, max(0.0, (dsr + 50.0) / 1.5))
    n_bnd  = min(100.0, bnd_rate * 2.5)
    n_dism = max(0.0, 100.0 - dism_rate * 50.0)
    n_cons = min(100.0, hp_matches * 3.0)
    cbi    = 0.35*n_hpsr + 0.20*n_dsr + 0.20*n_bnd + 0.15*n_dism + 0.10*n_cons

    batter_scores.append({
        'pid': pid, 'name': name, 'cbi': round(cbi,1),
        'hp_balls': hb, 'hp_runs': hr,
        'hp_sr_raw': round(hp_sr_raw,1),
        'base_sr_raw': round(base_sr_raw,1),
        'hp_sr': round(hp_sr,1), 'base_sr': round(base_sr,1),
        'delta_sr': round(dsr,1),
        'bnd_rate': round(bnd_rate,1), 'six_rate': round(six_rate,1),
        'dism_rate': round(dism_rate,2), 'hp_matches': hp_matches,
        'avg_pos': round(avg_p,1), 'pos4plus_pct': round(p4pct*100,1),
    })

batter_scores.sort(key=lambda x: x['cbi'], reverse=True)
print(f"   {len(batter_scores)} eligible. Top 25:")
for i, b in enumerate(batter_scores[:25], 1):
    print(f"  {i:2}. {b['name']:<28} CBI={b['cbi']:.1f} | HP SR={b['hp_sr_raw']:5.1f}"
          f" | ΔSR={b['delta_sr']:+5.1f} | Pos4+={b['pos4plus_pct']:.0f}%"
          f" | HP balls={b['hp_balls']:4d}")

# ── PBI ──
print("\n[8] PBI: ranking bowlers ...")
GLOBAL_ECON = 8.5

bowler_scores = []
for pid, s in bowler_data.items():
    name = player_names.get(pid, f'P{pid}')
    if not eligible(name): continue
    hb = s['hp_b']
    if hb < MIN_HP: continue
    tot = max(1, s['tot_b'])
    pp_pct = s['pp_b'] / tot
    if pp_pct > 0.25: continue
    md_pct = (s['mid_b'] + s['death_b']) / tot

    hr = s['hp_r']; hw = s['hp_w']
    bb = max(1, s['base_b']); br = s['base_r']

    # Economy (runs per over = runs/balls * 6)
    hp_econ_raw   = hr / hb * 6.0
    base_econ_raw = br / bb * 6.0
    hp_econ   = (hb/(hb+K))*hp_econ_raw   + (K/(hb+K))*GLOBAL_ECON
    base_econ = (bb/(bb+K))*base_econ_raw + (K/(bb+K))*GLOBAL_ECON
    d_econ = base_econ - hp_econ   # positive = tighter under pressure

    hp_sr_b    = hb / max(1, hw)
    hp_matches = len(s['hp_mids'])

    n_econ  = max(0.0, min(100.0, (10.0 - hp_econ) * 20.0))
    n_delta = min(100.0, max(0.0, d_econ * 20.0 + 50.0))
    n_wkts  = min(100.0, hw * 2.0)
    n_sr    = max(0.0, min(100.0, (100.0 - hp_sr_b)*1.5 + 75.0)) if hw > 0 else 20.0
    n_cons  = min(100.0, hp_matches * 3.0)
    pbi     = 0.30*n_econ + 0.25*n_delta + 0.20*n_wkts + 0.15*n_sr + 0.10*n_cons

    bowler_scores.append({
        'pid': pid, 'name': name, 'pbi': round(pbi,1),
        'hp_balls': hb, 'hp_wkts': hw,
        'hp_econ_raw': round(hp_econ_raw,2),
        'base_econ_raw': round(base_econ_raw,2),
        'hp_econ': round(hp_econ,2), 'base_econ': round(base_econ,2),
        'delta_econ': round(d_econ,2), 'hp_sr_b': round(hp_sr_b,1),
        'pp_pct': round(pp_pct*100,1), 'mid_death_pct': round(md_pct*100,1),
        'hp_matches': hp_matches,
    })

bowler_scores.sort(key=lambda x: x['pbi'], reverse=True)
print(f"   {len(bowler_scores)} eligible. Top 25:")
for i, b in enumerate(bowler_scores[:25], 1):
    print(f"  {i:2}. {b['name']:<28} PBI={b['pbi']:.1f}"
          f" | HP Econ={b['hp_econ_raw']:4.2f}"
          f" | ΔEcon={b['delta_econ']:+4.2f}"
          f" | HP Wkts={b['hp_wkts']:3d}"
          f" | PP%={b['pp_pct']:.0f}%")

# ── Save ──
print("\n[OUTPUT] Saving trained_results.json ...")
out = {
    'hp_threshold': round(HP, 2),
    'ps_p50': round(P50,2), 'ps_p80': round(P80,2), 'ps_p90': round(P90,2),
    'hp_fraction': round(sum(1 for x in all_ps if x >= HP)/n, 3),
    'total_deliveries': cnt,
    'batters_eligible': len(batter_scores),
    'bowlers_eligible': len(bowler_scores),
    'top_batters': batter_scores[:30],
    'top_bowlers': bowler_scores[:30],
}
with open('trained_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"   Saved. HP fraction = {out['hp_fraction']:.1%}")
print("=" * 70)
print("TRAINING COMPLETE")
print("=" * 70)
