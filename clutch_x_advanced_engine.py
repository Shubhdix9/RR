import csv
import math
import numpy as np
from collections import defaultdict

print("=== STARTING CLUTCH-X ADVANCED ENGINE (WAR ROOM EDITION) ===")

# 1. Load matches and metadata
matches = {}
with open('matches.csv', 'r') as f:
    for r in csv.DictReader(f):
        matches[r['match_id']] = r

comps = {}
with open('competitions.csv', 'r') as f:
    for r in csv.DictReader(f):
        comps[r['comp_id']] = r

player_teams = defaultdict(set)
with open('competition_team_player_mapping.csv', 'r') as f:
    for r in csv.DictReader(f):
        player_teams[r['player_id']].add(r['team_name'])

# Known retired players
retired_set = {
    'Shikhar Dhawan', 'Dinesh Karthik', 'Ravichandran Ashwin', 'Mohit Sharma',
    'Ambati Rayudu', 'Kieron Pollard', 'Dwayne Bravo', 'Eoin Morgan',
    'David Wiese', 'Manoj Tiwary', 'Varun Aaron', 'Amit Mishra', 'Piyush Chawla',
    'Robin Uthappa', 'Suresh Raina', 'Wriddhiman Saha', 'Ishant Sharma',
    'Umesh Yadav', 'Kedar Jadhav', 'Shane Watson', 'AB de Villiers', 'Mandeep Singh'
}

# Retained Marquee Superstars (Untouchable at Auction)
retained_superstars = {
    'Virat Kohli', 'Rohit Sharma', 'Jasprit Bumrah', 'Suryakumar Yadav',
    'Hardik Pandya', 'Ravindra Jadeja', 'Rishabh Pant', 'KL Rahul',
    'Shreyas Iyer', 'Shubman Gill', 'Heinrich Klaasen', 'Sanju Samson',
    'Yashasvi Jaiswal', 'Rinku Singh', 'Ruturaj Gaikwad', 'Axar Patel',
    'Sunil Narine', 'Andre Russell', 'Nicholas Pooran', 'Rashid Khan',
    'Kuldeep Yadav', 'Mohammed Siraj', 'Arshdeep Singh', 'Travis Head',
    'Pat Cummins', 'Mitchell Starc', 'Riyan Parag', 'Dhruv Jurel',
    'Ravi Bishnoi', 'Jofra Archer', 'Sam Curran' # RR's own retained core in IPL 2026
}

def is_pakistani(pid):
    for t in player_teams[pid]:
        if 'pakistan' in t.lower():
            return True
    return False

# 2. First pass: compute 1st innings total runs per match
inn1_totals = defaultdict(int)
with open('ball_by_ball.csv', 'r') as f:
    for r in csv.DictReader(f):
        if r['innings'] == '1':
            mid = r['match_id']
            runs = int(r['runs'])
            ext = r['extras_type']
            ext2 = int(r['extras_2_runs'] if r['extras_2_runs'] else 0)
            extra_runs = (1 + ext2) if ext in ['wide', 'legbyes', 'byes', 'Overstep', 'other'] else 0
            inn1_totals[mid] += runs + extra_runs

def estimate_win_prob(runs_req, balls_rem, wkts_hand):
    if runs_req <= 0: return 1.0
    if balls_rem <= 0 or wkts_hand <= 0: return 0.0
    rrr = (runs_req / balls_rem) * 6.0
    z = 0.55 * wkts_hand + 0.15 * (balls_rem / 6.0) - 0.48 * rrr - 0.8
    wp = 1.0 / (1.0 + math.exp(-max(-6.0, min(6.0, z))))
    return wp

# 3. Deliveries pass: compute expected runs E[Runs | state] and score deliveries
print("Pass 1: Reconstructing match states and calculating E[Runs] & E[Wkts] matrix...")
state_runs_list = defaultdict(list)
state_wkt_list = defaultdict(list)

# We group state by (innings, over_group, wkts_lost_group)
# over_group: 1-6 (PP), 7-10, 11-15, 16-18, 19-20
# wkts_group: 0-1, 2-3, 4-5, 6+
def get_state_key(inn, over, wkts):
    if over <= 6: og = 'PP'
    elif over <= 10: og = 'MID_EARLY'
    elif over <= 15: og = 'MID_LATE'
    elif over <= 18: og = 'DEATH_EARLY'
    else: og = 'DEATH_LATE'
    
    if wkts <= 1: wg = 'W0_1'
    elif wkts <= 3: wg = 'W2_3'
    elif wkts <= 5: wg = 'W4_5'
    else: wg = 'W6_PLUS'
    
    return (inn, og, wg)

raw_balls = []
with open('ball_by_ball.csv', 'r') as f:
    reader = csv.DictReader(f)
    curr_mid, curr_inn = None, None
    cum_runs, cum_wkts, legal_balls = 0, 0, 0
    target, total_balls, is_ko = 0, 120, False
    
    for r in reader:
        mid = r['match_id']
        inn = r['innings']
        
        if mid != curr_mid or inn != curr_inn:
            curr_mid = mid
            curr_inn = inn
            cum_runs = 0
            cum_wkts = 0
            legal_balls = 0
            m_meta = matches.get(mid, {})
            is_ko = (m_meta.get('knock_out', '0') == '1')
            
            if inn == '1':
                rev_ov = m_meta.get('first_inn_revised_overs', '')
                total_balls = int(rev_ov) if rev_ov else 120
                target = None
            else:
                rev_ov = m_meta.get('second_inn_revised_overs', '')
                total_balls = int(rev_ov) if rev_ov else 120
                rev_t = m_meta.get('revised_target', '')
                target = int(rev_t) if rev_t else (inn1_totals.get(mid, 160) + 1)
                
        over_id = int(r['overid'])
        wkts_lost = cum_wkts
        st_key = get_state_key(inn, over_id, wkts_lost)
        
        runs = int(r['runs'])
        ext = r['extras_type']
        ext2 = int(r['extras_2_runs'] if r['extras_2_runs'] else 0)
        is_legal = (ext not in ['wide', 'Overstep'])
        bowler_runs = runs + ((1 + ext2) if ext in ['wide', 'Overstep'] else 0)
        is_wkt = (r['is_wicket'].lower() == 'true')
        
        state_runs_list[st_key].append(bowler_runs)
        state_wkt_list[st_key].append(1 if is_wkt else 0)
        
        raw_balls.append({
            'mid': mid, 'inn': inn, 'overid': over_id,
            'st_key': st_key,
            'cum_runs': cum_runs, 'cum_wkts': cum_wkts, 'legal_balls': legal_balls,
            'target': target, 'total_balls': total_balls, 'is_ko': is_ko,
            'striker_id': r['striker_id'], 'striker_name': r['striker_name'],
            'bowler_id': r['bowler_id'], 'bowler_name': r['bowler_name'],
            'runs': runs, 'bowler_runs': bowler_runs,
            'is_four': r['is_four'].lower() == 'true',
            'is_six': r['is_six'].lower() == 'true',
            'is_wkt': is_wkt, 'd_type': r['dismissal_type'],
            'dismissed_id': r['dismissed_player_id'],
            'ext_type': ext, 'is_legal': is_legal
        })
        
        extra_runs = (1 + ext2) if ext in ['wide', 'legbyes', 'byes', 'Overstep', 'other'] else 0
        cum_runs += runs + extra_runs
        if is_legal: legal_balls += 1
        if is_wkt: cum_wkts += 1

# Expected value lookup table
exp_runs = {}
exp_wkts = {}
for k in state_runs_list:
    exp_runs[k] = float(np.mean(state_runs_list[k]))
    exp_wkts[k] = float(np.mean(state_wkt_list[k]))

print(f"Calculated state benchmark across {len(exp_runs)} match state buckets.")

# 4. Score deliveries with Pressure Score, Leverage, and xRA / xRP
print("Pass 2: Calculating Pre-Delivery Pressure, Leverage Index, and Runs Above Expected...")
deliveries = []
for b in raw_balls:
    inn = b['inn']
    target = b['target']
    cum_runs = b['cum_runs']
    cum_wkts = b['cum_wkts']
    legal_balls = b['legal_balls']
    total_balls = b['total_balls']
    is_ko = b['is_ko']
    
    wkts_hand = max(0, 10 - cum_wkts)
    balls_rem = max(1, total_balls - legal_balls)
    
    if inn == '2' and target is not None:
        runs_req = max(1, target - cum_runs)
        rrr = (runs_req / balls_rem) * 6.0
        s_rrr = min(1.5, max(0.0, (rrr - 6.0) / 10.0))
        s_wkt = 1.0 - (wkts_hand / 10.0) ** 1.2
        s_urgency = min(1.0, max(0.0, 1.0 - (balls_rem / total_balls)))
        wp = estimate_win_prob(runs_req, balls_rem, wkts_hand)
        leverage = 4.0 * wp * (1.0 - wp)
        raw_p = 100.0 * (0.35 * s_rrr + 0.35 * s_wkt + 0.30 * s_urgency) * (0.25 + 0.75 * leverage)
    else:
        over_num = legal_balls // 6 + 1
        exp_w_lost = 10.0 * ((legal_balls / 120.0) ** 1.3)
        collapse_stress = min(1.0, max(0.0, (cum_wkts - exp_w_lost) / max(1, wkts_hand)))
        if over_num <= 6:
            phase_stress = 0.35 if cum_wkts >= 2 else 0.20
        elif over_num <= 15:
            phase_stress = 0.40 if cum_wkts >= 4 else 0.25
        else:
            phase_stress = 0.75 + 0.25 * ((over_num - 15) / 5.0)
        par_runs = (legal_balls / 6.0) * 8.5
        deficit_stress = min(1.0, max(0.0, (par_runs - cum_runs) / 30.0))
        raw_p = 100.0 * (0.45 * phase_stress + 0.35 * collapse_stress + 0.20 * deficit_stress)
        leverage = 0.5 + 0.5 * phase_stress
        
    ps = min(100.0, raw_p * (1.15 if is_ko else 1.0))
    
    e_r = exp_runs.get(b['st_key'], 1.30)
    e_w = exp_wkts.get(b['st_key'], 0.05)
    
    # Batter Runs Above Expected (xRA)
    xra_bat = b['runs'] - e_r
    # Bowler Runs Prevented Below Expected (xRP)
    xrp_bowl = e_r - b['bowler_runs']
    
    b['ps'] = ps
    b['leverage'] = leverage
    b['xra'] = xra_bat
    b['xrp'] = xrp_bowl
    deliveries.append(b)

ps_vals = np.array([d['ps'] for d in deliveries])
p80 = float(np.percentile(ps_vals, 80))
print(f"Total scored: {len(deliveries)} | P80 Cutoff: {p80:.2f}")

# 5. Aggregate Players
player_names = {}
bat_all = defaultdict(lambda: {'balls': 0, 'runs': 0, 'xra': 0.0, 'dots': 0, 'fours': 0, 'sixes': 0, 'dismissals': 0, 'matches': set()})
bat_hp = defaultdict(lambda: {'balls': 0, 'runs': 0, 'xra': 0.0, 'dots': 0, 'fours': 0, 'sixes': 0, 'dismissals': 0, 'matches': set(), 'phases': defaultdict(lambda: [0, 0])})
bat_match = defaultdict(lambda: defaultdict(lambda: [0, 0]))

bowl_all = defaultdict(lambda: {'balls': 0, 'runs': 0, 'xrp': 0.0, 'dots': 0, 'bounds': 0, 'wkts': 0, 'matches': set()})
bowl_hp = defaultdict(lambda: {'balls': 0, 'runs': 0, 'xrp': 0.0, 'dots': 0, 'bounds': 0, 'wkts': 0, 'matches': set(), 'phases': defaultdict(lambda: [0, 0, 0])})
bowl_match = defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))

for d in deliveries:
    sid, sname = d['striker_id'], d['striker_name']
    bid, bname = d['bowler_id'], d['bowler_name']
    player_names[sid] = sname
    player_names[bid] = bname
    mid = d['mid']
    
    is_hp = (d['ps'] >= p80)
    over_id = d['overid']
    phase = 'PP' if over_id <= 6 else ('MIDDLE' if over_id <= 15 else 'DEATH')
    
    # Batting
    if d['ext_type'] != 'wide':
        runs = d['runs']
        is_dot = (runs == 0 and d['ext_type'] == 'None')
        is_wkt = (d['is_wkt'] and d['dismissed_id'] == sid)
        
        ba = bat_all[sid]
        ba['balls'] += 1
        ba['runs'] += runs
        ba['xra'] += d['xra']
        if is_dot: ba['dots'] += 1
        if d['is_four']: ba['fours'] += 1
        if d['is_six']: ba['sixes'] += 1
        if is_wkt: ba['dismissals'] += 1
        ba['matches'].add(mid)
        
        if is_hp:
            bhp = bat_hp[sid]
            bhp['balls'] += 1
            bhp['runs'] += runs
            bhp['xra'] += d['xra']
            if is_dot: bhp['dots'] += 1
            if d['is_four']: bhp['fours'] += 1
            if d['is_six']: bhp['sixes'] += 1
            if is_wkt: bhp['dismissals'] += 1
            bhp['matches'].add(mid)
            bhp['phases'][phase][0] += 1
            bhp['phases'][phase][1] += runs
            
            bat_match[sid][mid][0] += 1
            bat_match[sid][mid][1] += runs
            
    # Bowling
    if d['is_legal']:
        b_runs = d['bowler_runs']
        is_dot = (b_runs == 0)
        is_bound = (d['is_four'] or d['is_six'])
        is_bw_wkt = (d['is_wkt'] and d['d_type'] not in ['RunOut', 'Retire Out', 'Obstracting the field', 'Obstructing the field', ''])
        
        bwa = bowl_all[bid]
        bwa['balls'] += 1
        bwa['runs'] += b_runs
        bwa['xrp'] += d['xrp']
        if is_dot: bwa['dots'] += 1
        if is_bound: bwa['bounds'] += 1
        if is_bw_wkt: bwa['wkts'] += 1
        bwa['matches'].add(mid)
        
        if is_hp:
            bwh = bowl_hp[bid]
            bwh['balls'] += 1
            bwh['runs'] += b_runs
            bwh['xrp'] += d['xrp']
            if is_dot: bwh['dots'] += 1
            if is_bound: bwh['bounds'] += 1
            if is_bw_wkt:
                bwh['wkts'] += 1
                bwh['phases'][phase][2] += 1
            bwh['matches'].add(mid)
            bwh['phases'][phase][0] += 1
            bwh['phases'][phase][1] += b_runs
            
            bowl_match[bid][mid][0] += 1
            bowl_match[bid][mid][1] += b_runs
            if is_bw_wkt: bowl_match[bid][mid][2] += 1

def calc_pcts(values, reverse=False):
    n = len(values)
    order = np.argsort(values)
    ranks = np.empty(n, dtype=float)
    ranks[order] = np.arange(1, n + 1, dtype=float)
    pcts = 100.0 * (ranks - 0.5) / n
    return (100.0 - pcts) if reverse else pcts

# 6. Evaluate Realistic Eligible Batters
K = 60.0
pop_b_balls = sum(b['balls'] for b in bat_hp.values())
pop_b_runs = sum(b['runs'] for b in bat_hp.values())
pop_b_xra = sum(b['xra'] for b in bat_hp.values())
pop_b_dots = sum(b['dots'] for b in bat_hp.values())
pop_b_bounds = sum(b['fours'] + b['sixes'] for b in bat_hp.values())

pop_sr = (pop_b_runs / pop_b_balls) * 100.0
pop_xra_rate = pop_b_xra / pop_b_balls
pop_dot_pct = (pop_b_dots / pop_b_balls) * 100.0
pop_bound_pct = (pop_b_bounds / pop_b_balls) * 100.0

bat_candidates = []
for sid, hp in bat_hp.items():
    sname = player_names[sid]
    n = hp['balls']
    m = len(hp['matches'])
    if n < 40 or m < 5:
        continue
    
    # Filter retired, Pakistani, and retained superstars
    if is_pakistani(sid) or sname in retired_set or sname in retained_superstars:
        continue
        
    ba = bat_all[sid]
    sr_raw = (hp['runs'] / n) * 100.0
    base_sr = (ba['runs'] / ba['balls']) * 100.0
    delta_sr = sr_raw - base_sr
    xra_per_ball = hp['xra'] / n
    
    # Bayesian shrinkage
    w = n / (n + K)
    sr_adj = w * sr_raw + (1.0 - w) * pop_sr
    xra_adj = w * xra_per_ball + (1.0 - w) * pop_xra_rate
    dot_adj = w * ((hp['dots'] / n) * 100.0) + (1.0 - w) * pop_dot_pct
    bound_adj = w * (((hp['fours'] + hp['sixes']) / n) * 100.0) + (1.0 - w) * pop_bound_pct
    
    # Match consistency
    m_srs = [(v[1]/v[0])*100.0 for v in bat_match[sid].values() if v[0] >= 4]
    consistency = max(0.0, 100.0 - float(np.std(m_srs)/2.0)) if len(m_srs) >= 3 else 50.0
    
    # Best phase
    best_phase = max(hp['phases'].keys(), key=lambda p: (hp['phases'][p][1]/max(1, hp['phases'][p][0])) if hp['phases'][p][0]>=10 else 0)
    
    bat_candidates.append({
        'id': sid, 'name': sname, 'balls': n, 'matches': m,
        'runs': hp['runs'], 'sr_raw': sr_raw, 'base_sr': base_sr, 'delta_sr': delta_sr,
        'xra_adj': xra_adj, 'sr_adj': sr_adj, 'dot_adj': dot_adj, 'bound_adj': bound_adj,
        'consistency': consistency, 'best_phase': best_phase,
        'teams': list(player_teams[sid])
    })

p_sr = calc_pcts([b['sr_adj'] for b in bat_candidates])
p_xra = calc_pcts([b['xra_adj'] for b in bat_candidates])
p_dot = calc_pcts([b['dot_adj'] for b in bat_candidates], reverse=True)
p_bnd = calc_pcts([b['bound_adj'] for b in bat_candidates])
p_delta = calc_pcts([b['delta_sr'] for b in bat_candidates])
p_const = calc_pcts([b['consistency'] for b in bat_candidates])

for i, b in enumerate(bat_candidates):
    b['cbi'] = (
        0.25 * p_sr[i] +
        0.25 * p_xra[i] +
        0.15 * p_dot[i] +
        0.15 * p_bnd[i] +
        0.10 * p_delta[i] +
        0.10 * p_const[i]
    )

bat_candidates.sort(key=lambda x: x['cbi'], reverse=True)

# 7. Evaluate Realistic Eligible Bowlers
pop_bw_balls = sum(b['balls'] for b in bowl_hp.values())
pop_bw_runs = sum(b['runs'] for b in bowl_hp.values())
pop_bw_xrp = sum(b['xrp'] for b in bowl_hp.values())
pop_bw_dots = sum(b['dots'] for b in bowl_hp.values())
pop_bw_bounds = sum(b['bounds'] for b in bowl_hp.values())
pop_bw_wkts = sum(b['wkts'] for b in bowl_hp.values())

pop_econ = (pop_bw_runs / pop_bw_balls) * 6.0
pop_xrp_rate = pop_bw_xrp / pop_bw_balls
pop_bw_dot = (pop_bw_dots / pop_bw_balls) * 100.0
pop_bw_bound = (pop_bw_bounds / pop_bw_balls) * 100.0
pop_wkt_rate = (pop_bw_wkts / pop_bw_balls) * 100.0

bowl_candidates = []
for bid, hp in bowl_hp.items():
    bname = player_names[bid]
    n = hp['balls']
    m = len(hp['matches'])
    if n < 50 or m < 5:
        continue
        
    if is_pakistani(bid) or bname in retired_set or bname in retained_superstars:
        continue
        
    bwa = bowl_all[bid]
    econ_raw = (hp['runs'] / n) * 6.0
    base_econ = (bwa['runs'] / bwa['balls']) * 6.0
    delta_econ = base_econ - econ_raw
    xrp_per_ball = hp['xrp'] / n
    
    w = n / (n + K)
    econ_adj = w * econ_raw + (1.0 - w) * pop_econ
    xrp_adj = w * xrp_per_ball + (1.0 - w) * pop_xrp_rate
    wkt_adj = w * ((hp['wkts'] / n) * 100.0) + (1.0 - w) * pop_wkt_rate
    dot_adj = w * ((hp['dots'] / n) * 100.0) + (1.0 - w) * pop_bw_dot
    bound_adj = w * ((hp['bounds'] / n) * 100.0) + (1.0 - w) * pop_bw_bound
    
    m_econs = [(v[1]/v[0])*6.0 for v in bowl_match[bid].values() if v[0] >= 6]
    consistency = max(0.0, 100.0 - float(np.std(m_econs)*5.0)) if len(m_econs) >= 3 else 50.0
    best_phase = min(hp['phases'].keys(), key=lambda p: (hp['phases'][p][1]/max(1, hp['phases'][p][0])*6.0) if hp['phases'][p][0]>=12 else 99.0)
    
    bowl_candidates.append({
        'id': bid, 'name': bname, 'balls': n, 'matches': m,
        'runs': hp['runs'], 'wkts': hp['wkts'], 'econ_raw': econ_raw, 'base_econ': base_econ, 'delta_econ': delta_econ,
        'xrp_adj': xrp_adj, 'econ_adj': econ_adj, 'wkt_adj': wkt_adj, 'dot_adj': dot_adj, 'bound_adj': bound_adj,
        'consistency': consistency, 'best_phase': best_phase,
        'teams': list(player_teams[bid])
    })

p_ec = calc_pcts([b['econ_adj'] for b in bowl_candidates], reverse=True)
p_xrp = calc_pcts([b['xrp_adj'] for b in bowl_candidates])
p_wkt = calc_pcts([b['wkt_adj'] for b in bowl_candidates])
p_dot_b = calc_pcts([b['dot_adj'] for b in bowl_candidates])
p_bnd_b = calc_pcts([b['bound_adj'] for b in bowl_candidates], reverse=True)
p_dec = calc_pcts([b['delta_econ'] for b in bowl_candidates])
p_cst_b = calc_pcts([b['consistency'] for b in bowl_candidates])

for i, b in enumerate(bowl_candidates):
    b['pbi'] = (
        0.25 * p_ec[i] +
        0.25 * p_xrp[i] +
        0.20 * p_wkt[i] +
        0.10 * p_dot_b[i] +
        0.10 * p_dec[i] +
        0.10 * p_cst_b[i]
    )

bowl_candidates.sort(key=lambda x: x['pbi'], reverse=True)

print("\n================== TOP 15 REALISTIC AUCTION BATTERS (WAR ROOM) ==================")
for i, b in enumerate(bat_candidates[:15], 1):
    ipl_t = [t for t in b['teams'] if 'ipl' in t.lower() or t in ['Gujarat Titans', 'Mumbai Indians', 'Chennai Super Kings', 'Royal Challengers Bengaluru', 'Delhi Capitals', 'Kolkata Knight Riders', 'Sunrisers Hyderabad', 'Lucknow Super Giants', 'Punjab Kings']]
    print(f"{i:2d}. {b['name']:20s} | CBI={b['cbi']:4.1f} | HP_Balls={b['balls']:3d} | HP_SR={b['sr_raw']:5.1f} | ΔSR={b['delta_sr']:+5.1f} | Dot%={b['dot_adj']:4.1f}% | Team={ipl_t[:1] or b['teams'][:1]}")

print("\n================== TOP 15 REALISTIC AUCTION BOWLERS (WAR ROOM) ==================")
for i, b in enumerate(bowl_candidates[:15], 1):
    ipl_t = [t for t in b['teams'] if 'ipl' in t.lower() or t in ['Gujarat Titans', 'Mumbai Indians', 'Chennai Super Kings', 'Royal Challengers Bengaluru', 'Delhi Capitals', 'Kolkata Knight Riders', 'Sunrisers Hyderabad', 'Lucknow Super Giants', 'Punjab Kings']]
    print(f"{i:2d}. {b['name']:20s} | PBI={b['pbi']:4.1f} | HP_Balls={b['balls']:3d} | Wkts={b['wkts']:2d} | HP_Econ={b['econ_raw']:5.2f} | ΔEcon={b['delta_econ']:+5.2f} | Team={ipl_t[:1] or b['teams'][:1]}")

