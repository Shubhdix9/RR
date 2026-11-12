import csv, math, json
from collections import defaultdict

print("=" * 70)
print("CLUTCH-X ADVANCED FINE-TUNING ENGINE (v6.0)")
print("=" * 70)

# 1. Competitions & Match Weights
comp_weights = {}
with open('competitions.csv') as f:
    for r in csv.DictReader(f):
        cid = r['comp_id']
        cname = r['comp_name'].lower()
        if 'ipl' in cname:
            comp_weights[cid] = 1.30  # Premier league quality
        elif 'asia cup' in cname or 'world cup' in cname:
            comp_weights[cid] = 1.20  # Tournament stakes
        elif any(country in cname for country in ['india', 'australia', 'england', 'south africa', 'new zealand', 'west indies', 'pakistan']):
            comp_weights[cid] = 1.05  # Top tier bilateral
        else:
            comp_weights[cid] = 0.90  # Lower tier / associate

match_info = {}
with open('matches.csv') as f:
    for r in csv.DictReader(f):
        mid = int(r['match_id'])
        cid = r['comp_id']
        ko = r['knock_out'].strip() == '1'
        w = comp_weights.get(cid, 1.0)
        if ko:
            w *= 1.15  # Knockout multiplier
        match_info[mid] = {'weight': w, 'knockout': ko, 'comp_id': cid}

# 2. Player Mapping & Eligibility
player_names = {}
with open('competition_team_player_mapping.csv') as f:
    for r in csv.DictReader(f):
        player_names[int(r['player_id'])] = r['player_name'].strip()

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
    'Hardik Pandya','Ravindra Jadeja','Tilak Varma','Namboori Tilak Varma',
    'Axar Patel','Kuldeep Yadav','Mohammed Shami','Rinku Singh','Nitish Reddy',
    'Varun Chakravarthy','Rajat Patidar','Patrick Cummins'
}
RETIRED = {
    'Shikhar Dhawan','Dinesh Karthik','R Ashwin','Mohit Sharma',
    'Ambati Rayudu','Kieron Pollard','Dwayne Bravo','Wriddhiman Saha',
    'Aaron Finch','Chris Gayle','Jason Roy','Eoin Morgan',
    'Mahendra Singh Dhoni','Ravichandran Ashwin'
}

def eligible(name):
    return name not in PAK and name not in RETAINED and name not in RETIRED

# 3. Match 1st Innings Totals
mitt = defaultdict(lambda: defaultdict(int))
with open('ball_by_ball.csv') as f:
    for r in csv.DictReader(f):
        mid = int(r['match_id']); inn = int(r['innings'])
        runs = int(r['runs'])
        et = r.get('extras_type','').strip().lower()
        if et in ('wide','wides'):
            runs += int(r['extras1_runs'])
        mitt[mid][inn] += runs

# 4. State-Level Baselines E[Runs|State] and E[Wkt|State]
# State = (inn, phase_bucket, wkt_bucket)
# phase_bucket: 1-6 (PP), 7-10 (Early Mid), 11-15 (Late Mid), 16-18 (Early Death), 19-20 (Extreme Death)
# wkt_bucket: 0-2, 3-5, 6-9
state_balls = defaultdict(int)
state_runs = defaultdict(int)
state_wkts = defaultdict(int)

def get_phase_bucket(overid):
    if overid <= 6: return 'PP'
    elif overid <= 10: return 'EARLY_MID'
    elif overid <= 15: return 'LATE_MID'
    elif overid <= 18: return 'EARLY_DEATH'
    else: return 'EXTREME_DEATH'

def get_wkt_bucket(w):
    if w <= 2: return 'LOW_WKT'
    elif w <= 5: return 'MED_WKT'
    else: return 'HIGH_WKT'

print("Pass 1: Computing state expected values across 200,999 balls...")
match_state = defaultdict(lambda: {'runs':0, 'wkts':0, 'balls':0})
with open('ball_by_ball.csv') as f:
    for r in csv.DictReader(f):
        mid = int(r['match_id']); inn = int(r['innings'])
        overid = int(r['overid'])
        runs_b = int(r['runs'])
        isW = r['is_wicket'].strip().lower() == 'true'
        et = r.get('extras_type','').strip().lower()
        wide = et in ('wide','wides')
        
        st = match_state[(mid, inn)]
        wkt_b = get_wkt_bucket(st['wkts'])
        ph_b = get_phase_bucket(overid)
        s_key = (inn, ph_b, wkt_b)
        
        if not wide:
            state_balls[s_key] += 1
            state_runs[s_key] += runs_b
            if isW:
                state_wkts[s_key] += 1
                
        st['runs'] += runs_b
        if not wide: st['balls'] += 1
        if isW: st['wkts'] += 1

expected_runs_state = {}
expected_wkt_state = {}
for k in state_balls:
    b = max(1, state_balls[k])
    expected_runs_state[k] = state_runs[k] / b
    expected_wkt_state[k] = state_wkts[k] / b

print("Empirical Expected Runs per ball by phase & wickets:")
for k, v in sorted(expected_runs_state.items()):
    if k[0] == 2: # 2nd innings
        print(f"  Inn 2 | {k[1]:<13} | {k[2]:<8} -> E[Runs]={v:.2f} ({v*6:.2f} RPO), E[Wkt]={expected_wkt_state[k]:.3f}")


# 5. Pressure Scoring Model
def ps_chase_ft(balls_left, wkts_lost, runs_needed, target):
    if target <= 0 or balls_left <= 0: return 0.0
    rrr = max(0.0, (runs_needed / balls_left) * 6.0)
    a = max(0.0, min(1.0, (rrr - 6.0) / 10.0))  # RRR stress
    b = min(1.0, wkts_lost / 10.0)             # Wicket stress
    c = (120 - balls_left) / 120.0             # Urgency
    exp_runs = (balls_left / 6.0) * 8.5
    surplus = exp_runs - max(0.0, runs_needed)
    wp_logit = max(-10.0, min(10.0, surplus * 0.08 - wkts_lost * 0.25))
    wp = 1.0 / (1.0 + math.exp(-wp_logit))
    lev = 4.0 * wp * (1.0 - wp)                # Leverage index
    return max(0.0, min(100.0, 35.0*a + 30.0*b + 20.0*c + 15.0*lev))

def ps_set_ft(over_num, wkts_lost, runs_scored, knockout):
    if over_num >= 19:   a = 1.00
    elif over_num >= 16: a = 0.85
    elif over_num >= 11: a = 0.55
    elif over_num >= 7:  a = 0.30
    else:                a = 0.12
    exp_wkts = over_num * 0.38
    b = max(0.0, min(1.0, (wkts_lost - exp_wkts) / 6.5))
    exp_runs = over_num * 8.6
    c = max(0.0, min(1.0, (exp_runs - runs_scored) / (exp_runs * 1.1))) if exp_runs > 0 else 0.0
    stakes = 1.15 if knockout else 1.0
    return max(0.0, min(100.0, (40.0*a + 35.0*b + 25.0*c) * stakes))

# Pass 2: Accumulate ball-level xRA, xRP and pressure stats
batter_ft = defaultdict(lambda: {
    'hp_balls': 0, 'hp_runs': 0, 'hp_4s': 0, 'hp_6s': 0, 'hp_dism': 0, 'hp_xra': 0.0,
    'base_balls': 0, 'base_runs': 0, 'base_4s': 0, 'base_6s': 0, 'base_dism': 0, 'base_xra': 0.0,
    'match_hp_xra': defaultdict(float), 'match_hp_balls': defaultdict(int),
    'positions': [], 'teams': set()
})

bowler_ft = defaultdict(lambda: {
    'pp_b': 0, 'mid_b': 0, 'death_b': 0, 'tot_b': 0,
    'hp_b': 0, 'hp_r': 0, 'hp_w': 0, 'hp_xrp': 0.0, 'hp_xwa': 0.0,
    'base_b': 0, 'base_r': 0, 'base_w': 0, 'base_xrp': 0.0,
    'match_hp_xrp': defaultdict(float), 'match_hp_balls': defaultdict(int),
    'teams': set()
})

all_ps = []
player_teams = defaultdict(set)
with open('competition_team_player_mapping.csv') as f:
    for r in csv.DictReader(f):
        player_teams[int(r['player_id'])].add(r['team_name'].strip())

match_state = defaultdict(lambda: {'runs':0, 'wkts':0, 'balls':0})
deliveries = []

print("Pass 2: Evaluating 200,999 balls with pre-delivery leverage & competition weight...")
with open('ball_by_ball.csv') as f:
    for r in csv.DictReader(f):
        mid = int(r['match_id']); inn = int(r['innings'])
        overid = int(r['overid'])
        sid = int(r['striker_id']); bid = int(r['bowler_id'])
        runs_b = int(r['runs'])
        is4 = r['is_four'].strip().lower() == 'true'
        is6 = r['is_six'].strip().lower() == 'true'
        isW = r['is_wicket'].strip().lower() == 'true'
        et = r.get('extras_type','').strip().lower()
        wide = et in ('wide','wides')
        noball = et in ('overstep','no ball','no-ball','noball')
        penalty = int(r['extras1_runs']) if (wide or noball) else 0
        legal = not wide
        bowler_runs = runs_b + penalty
        
        try: bat_pos = int(r.get('batting_order','0'))
        except: bat_pos = 0

        minfo = match_info.get(mid, {'weight':1.0, 'knockout':False})
        ko = minfo['knockout']
        m_weight = minfo['weight']

        st = match_state[(mid, inn)]
        bl = max(0, 120 - st['balls'])
        wl = st['wkts']
        rs = st['runs']

        # Pre-delivery pressure
        if inn == 2:
            t1 = mitt[mid][1] + 1
            ps = ps_chase_ft(bl, wl, t1 - rs, t1)
        else:
            ps = ps_set_ft(overid, wl, rs, ko)

        all_ps.append(ps)
        
        # Phase bucket & expected value
        ph_b = get_phase_bucket(overid)
        wkt_b = get_wkt_bucket(wl)
        s_key = (inn, ph_b, wkt_b)
        e_runs = expected_runs_state.get(s_key, 1.35)
        e_wkt = expected_wkt_state.get(s_key, 0.05)
        
        # Runs Above Expected
        xra_val = (runs_b - e_runs) * m_weight
        xrp_val = (e_runs - bowler_runs) * m_weight
        xwa_val = ((1.0 if isW else 0.0) - e_wkt) * m_weight

        # Update state
        st['runs'] += runs_b + penalty
        if legal: st['balls'] += 1
        if isW: st['wkts'] += 1

        # Phase for bowler
        if overid <= 6: phase = 'PP'
        elif overid <= 15: phase = 'MID'
        else: phase = 'DEATH'

        deliveries.append((sid, bid, ps, runs_b, bowler_runs, is4, is6, isW, legal, bat_pos, phase, mid, xra_val, xrp_val, xwa_val, r.get('dismissed_player_id','').strip()))

# Calculate exact P80
all_ps_sorted = sorted(all_ps)
HP_P80 = all_ps_sorted[int(0.80 * len(all_ps_sorted))]
print(f"Fine-tuned High-Pressure Threshold (P80) = {HP_P80:.2f}")

print("Pass 3: Aggregating advanced metrics for all players...")
for d in deliveries:
    sid, bid, ps, runs_b, bowler_runs, is4, is6, isW, legal, bat_pos, phase, mid, xra, xrp, xwa, dism_id = d
    is_hp = ps >= HP_P80
    
    # Batter aggregation
    bs = batter_ft[sid]
    if bat_pos > 0: bs['positions'].append(bat_pos)
    if is_hp:
        if legal:
            bs['hp_balls'] += 1
            bs['hp_runs'] += runs_b
            if is4: bs['hp_4s'] += 1
            if is6: bs['hp_6s'] += 1
            bs['hp_xra'] += xra
            bs['match_hp_xra'][mid] += xra
            bs['match_hp_balls'][mid] += 1
        if isW and dism_id.isdigit() and int(dism_id) == sid:
            bs['hp_dism'] += 1
    else:
        if legal:
            bs['base_balls'] += 1
            bs['base_runs'] += runs_b
            if is4: bs['base_4s'] += 1
            if is6: bs['base_6s'] += 1
            bs['base_xra'] += xra
        if isW and dism_id.isdigit() and int(dism_id) == sid:
            bs['base_dism'] += 1

    # Bowler aggregation
    bw = bowler_ft[bid]
    if legal:
        bw['tot_b'] += 1
        if phase == 'PP': bw['pp_b'] += 1
        elif phase == 'MID': bw['mid_b'] += 1
        else: bw['death_b'] += 1
    
    if is_hp:
        if legal:
            bw['hp_b'] += 1
            bw['hp_r'] += bowler_runs
            if isW: bw['hp_w'] += 1
            bw['hp_xrp'] += xrp
            bw['hp_xwa'] += xwa
            bw['match_hp_xrp'][mid] += xrp
            bw['match_hp_balls'][mid] += 1
        elif bowler_runs > 0: # wide/noball runs
            bw['hp_r'] += bowler_runs
            bw['hp_xrp'] += (0 - bowler_runs)
    else:
        if legal:
            bw['base_b'] += 1
            bw['base_r'] += bowler_runs
            if isW: bw['base_w'] += 1
            bw['base_xrp'] += xrp

print("Pass 4: Scoring with Bayesian Shrinkage, Expected Value & Clutch Consistency...")

# Batter Fine-Tuned Scoring (CBI-v6)
ranked_batters = []
for pid, bs in batter_ft.items():
    name = player_names.get(pid, f'Player_{pid}')
    if not eligible(name): continue
    hb = bs['hp_balls']
    if hb < 45: continue  # Sample threshold
    pos = bs['positions']
    if not pos: continue
    pos4plus = sum(1 for p in pos if p >= 4) / len(pos)
    if pos4plus < 0.65: continue  # Pure middle-order & death finisher
    
    bb = max(1, bs['base_balls'])
    hr = bs['hp_runs']; br = bs['base_runs']
    
    hp_sr_raw = (hr / hb) * 100
    base_sr_raw = (br / bb) * 100
    
    # Bayesian shrinkage
    K = 50.0
    hp_sr_shrunk = (hb / (hb + K)) * hp_sr_raw + (K / (hb + K)) * 135.0
    base_sr_shrunk = (bb / (bb + K)) * base_sr_raw + (K / (bb + K)) * 125.0
    delta_sr = hp_sr_shrunk - base_sr_shrunk
    
    # Runs Above Expected per 100 balls under pressure
    xra_per_100 = (bs['hp_xra'] / hb) * 100
    
    # Boundary and dismissal rates
    bnd_rate = (bs['hp_4s'] + bs['hp_6s']) / hb * 100
    dism_rate = bs['hp_dism'] / hb * 100
    
    # Clutch Consistency Rate (CCR): % of HP matches with positive xRA (where player faced >= 6 balls)
    valid_matches = [m for m, b_count in bs['match_hp_balls'].items() if b_count >= 5]
    if valid_matches:
        pos_matches = sum(1 for m in valid_matches if bs['match_hp_xra'][m] > 0)
        ccr = (pos_matches / len(valid_matches)) * 100
    else:
        ccr = 50.0

    # Composite CBI Score (0-100 scale)
    # Weights: 30% HP SR, 25% xRA, 20% Delta SR, 15% Boundary Rate, 10% Consistency
    n_sr = min(100.0, hp_sr_shrunk / 2.2)
    n_xra = min(100.0, max(0.0, (xra_per_100 + 30.0) * 1.5))
    n_dsr = min(100.0, max(0.0, (delta_sr + 40.0) * 1.25))
    n_bnd = min(100.0, bnd_rate * 2.8)
    n_ccr = min(100.0, ccr)
    
    cbi = 0.30 * n_sr + 0.25 * n_xra + 0.20 * n_dsr + 0.15 * n_bnd + 0.10 * n_ccr
    
    teams = player_teams.get(pid, {'T20'})
    t_str = '/'.join(list(teams)[:2])

    ranked_batters.append({
        'pid': pid, 'name': name, 'cbi': round(cbi, 1),
        'hp_balls': hb, 'hp_runs': hr, 'hp_sr_raw': round(hp_sr_raw, 1),
        'base_sr_raw': round(base_sr_raw, 1), 'delta_sr': round(delta_sr, 1),
        'xra_100': round(xra_per_100, 1), 'bnd_rate': round(bnd_rate, 1),
        'dot_rate': round((hb - bs['hp_4s'] - bs['hp_6s'] - (hr - bs['hp_4s']*4 - bs['hp_6s']*6)) / hb * 100, 1),
        'ccr': round(ccr, 1), 'pos4plus': round(pos4plus * 100, 1),
        'team': t_str
    })

ranked_batters.sort(key=lambda x: x['cbi'], reverse=True)

# Bowler Fine-Tuned Scoring (PBI-v6)
ranked_bowlers = []
for pid, bw in bowler_ft.items():
    name = player_names.get(pid, f'Player_{pid}')
    if not eligible(name): continue
    hb = bw['hp_b']
    if hb < 45: continue
    tot = max(1, bw['tot_b'])
    pp_pct = bw['pp_b'] / tot
    if pp_pct > 0.25: continue  # Overs 7-20 specialists
    
    bb = max(1, bw['base_b'])
    hr = bw['hp_r']; hw = bw['hp_w']
    br = bw['base_r']
    
    hp_econ_raw = (hr / hb) * 6.0
    base_econ_raw = (br / bb) * 6.0
    
    K = 60.0
    hp_econ_shrunk = (hb / (hb + K)) * hp_econ_raw + (K / (hb + K)) * 8.6
    base_econ_shrunk = (bb / (bb + K)) * base_econ_raw + (K / (bb + K)) * 8.4
    delta_econ = base_econ_shrunk - hp_econ_shrunk
    
    # Runs Prevented per 6 balls under pressure
    xrp_per_over = (bw['hp_xrp'] / hb) * 6.0
    
    # Wickets Above Expected
    wkt_rate = (hw / hb) * 100
    
    # Clutch Consistency Rate (CCR): % of HP matches with positive xRP
    valid_matches = [m for m, b_count in bw['match_hp_balls'].items() if b_count >= 6]
    if valid_matches:
        pos_matches = sum(1 for m in valid_matches if bw['match_hp_xrp'][m] > 0)
        ccr = (pos_matches / len(valid_matches)) * 100
    else:
        ccr = 50.0

    # Composite PBI Score (0-100 scale)
    # Weights: 30% xRP (Runs Prevented vs State), 25% Economy Suppression, 20% Wicket Production, 15% Delta Econ, 10% Consistency
    n_xrp = min(100.0, max(0.0, (xrp_per_over + 2.0) * 25.0))
    n_econ = max(0.0, min(100.0, (11.0 - hp_econ_shrunk) * 18.0))
    n_wkt = min(100.0, hw * 2.0)
    n_decon = min(100.0, max(0.0, (delta_econ + 2.0) * 25.0))
    n_ccr = min(100.0, ccr)
    
    pbi = 0.30 * n_xrp + 0.25 * n_econ + 0.20 * n_wkt + 0.15 * n_decon + 0.10 * n_ccr
    
    teams = player_teams.get(pid, {'T20'})
    t_str = '/'.join(list(teams)[:2])

    ranked_bowlers.append({
        'pid': pid, 'name': name, 'pbi': round(pbi, 1),
        'hp_balls': hb, 'hp_wkts': hw, 'hp_econ_raw': round(hp_econ_raw, 2),
        'base_econ_raw': round(base_econ_raw, 2), 'delta_econ': round(delta_econ, 2),
        'xrp_over': round(xrp_per_over, 2), 'wkt_rate': round(wkt_rate, 1),
        'ccr': round(ccr, 1), 'pp_pct': round(pp_pct * 100, 1),
        'team': t_str
    })

ranked_bowlers.sort(key=lambda x: x['pbi'], reverse=True)

print("\n" + "=" * 80)
print("FINE-TUNED TOP 15 BATTERS (#4-7 Finishers with State xRA & Consistency):")
print("=" * 80)
for i, b in enumerate(ranked_batters[:15], 1):
    print(f"{i:2d}. {b['name']:<24} | CBI: {b['cbi']:.1f} | HP SR: {b['hp_sr_raw']:5.1f} | ΔSR: {b['delta_sr']:+5.1f} | xRA/100: {b['xra_100']:+5.1f} | CCR: {b['ccr']:4.1f}% | Balls: {b['hp_balls']:3d}")

print("\n" + "=" * 80)
print("FINE-TUNED TOP 15 BOWLERS (Overs 7-20 Specialists with State xRP & Consistency):")
print("=" * 80)
for i, bw in enumerate(ranked_bowlers[:15], 1):
    print(f"{i:2d}. {bw['name']:<24} | PBI: {bw['pbi']:.1f} | HP Econ: {bw['hp_econ_raw']:4.2f} | ΔEcon: {bw['delta_econ']:+4.2f} | xRP/ov: {bw['xrp_over']:+4.2f} | Wkts: {bw['hp_wkts']:2d} | CCR: {bw['ccr']:4.1f}%")
