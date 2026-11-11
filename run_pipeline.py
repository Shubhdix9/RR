import csv
import math
import numpy as np
from collections import defaultdict

# 1. Load matches
matches = {}
with open('matches.csv', 'r') as f:
    for r in csv.DictReader(f):
        matches[r['match_id']] = r

# 2. Competitions mapping
comps = {}
with open('competitions.csv', 'r') as f:
    for r in csv.DictReader(f):
        comps[r['comp_id']] = r

# 3. First pass: compute 1st innings total runs per match
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

# 4. Score all deliveries and collect stats
print("Scoring all deliveries...")
deliveries = []
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
            exp_wkts = 10.0 * ((legal_balls / 120.0) ** 1.3)
            collapse_stress = min(1.0, max(0.0, (cum_wkts - exp_wkts) / max(1, wkts_hand)))
            if over_num <= 6:
                phase_stress = 0.35 if cum_wkts >= 2 else 0.20
            elif over_num <= 15:
                phase_stress = 0.40 if cum_wkts >= 4 else 0.25
            else:
                phase_stress = 0.75 + 0.25 * ((over_num - 15) / 5.0)
            par_runs = (legal_balls / 6.0) * 8.5
            deficit_stress = min(1.0, max(0.0, (par_runs - cum_runs) / 30.0))
            raw_p = 100.0 * (0.45 * phase_stress + 0.35 * collapse_stress + 0.20 * deficit_stress)
            
        ps = min(100.0, raw_p * (1.15 if is_ko else 1.0))
        
        deliveries.append({
            'mid': mid,
            'inn': inn,
            'ps': ps,
            'striker_id': r['striker_id'],
            'striker_name': r['striker_name'],
            'bowler_id': r['bowler_id'],
            'bowler_name': r['bowler_name'],
            'runs': int(r['runs']),
            'is_four': r['is_four'].lower() == 'true',
            'is_six': r['is_six'].lower() == 'true',
            'is_wkt': r['is_wicket'].lower() == 'true',
            'd_type': r['dismissal_type'],
            'dismissed_id': r['dismissed_player_id'],
            'ext_type': r['extras_type'],
            'ext_2': int(r['extras_2_runs'] if r['extras_2_runs'] else 0)
        })
        
        # State update after ball
        ext = r['extras_type']
        ext2 = int(r['extras_2_runs'] if r['extras_2_runs'] else 0)
        extra_runs = (1 + ext2) if ext in ['wide', 'legbyes', 'byes', 'Overstep', 'other'] else 0
        cum_runs += int(r['runs']) + extra_runs
        if ext not in ['wide', 'Overstep']:
            legal_balls += 1
        if r['is_wicket'].lower() == 'true':
            cum_wkts += 1

ps_vals = [d['ps'] for d in deliveries]
p80 = float(np.percentile(ps_vals, 80))
p85 = float(np.percentile(ps_vals, 85))
p75 = float(np.percentile(ps_vals, 75))
print(f"P75={p75:.2f}, P80 (Primary Cutoff)={p80:.2f}, P85={p85:.2f}")

# Save deliveries metadata for further analysis

# 5. Batting Aggregation
print("Aggregating Batting Performance...")
batter_all = defaultdict(lambda: {'balls': 0, 'runs': 0, 'dots': 0, 'fours': 0, 'sixes': 0, 'dismissals': 0, 'matches': set()})
batter_hp = defaultdict(lambda: {'balls': 0, 'runs': 0, 'dots': 0, 'fours': 0, 'sixes': 0, 'dismissals': 0, 'matches': set()})
batter_hp_match = defaultdict(lambda: defaultdict(lambda: {'balls': 0, 'runs': 0, 'dots': 0, 'wkts': 0}))

player_names = {}

for d in deliveries:
    sid = d['striker_id']
    sname = d['striker_name']
    player_names[sid] = sname
    
    # Batters face all balls except wides
    if d['ext_type'] != 'wide':
        mid = d['mid']
        runs = d['runs']
        is_dot = (runs == 0 and d['ext_type'] == 'None')
        is_wkt = (d['is_wkt'] and d['dismissed_id'] == sid)
        
        b_all = batter_all[sid]
        b_all['balls'] += 1
        b_all['runs'] += runs
        if is_dot: b_all['dots'] += 1
        if d['is_four']: b_all['fours'] += 1
        if d['is_six']: b_all['sixes'] += 1
        if is_wkt: b_all['dismissals'] += 1
        b_all['matches'].add(mid)
        
        if d['ps'] >= p80:
            b_hp = batter_hp[sid]
            b_hp['balls'] += 1
            b_hp['runs'] += runs
            if is_dot: b_hp['dots'] += 1
            if d['is_four']: b_hp['fours'] += 1
            if d['is_six']: b_hp['sixes'] += 1
            if is_wkt: b_hp['dismissals'] += 1
            b_hp['matches'].add(mid)
            
            m_stat = batter_hp_match[sid][mid]
            m_stat['balls'] += 1
            m_stat['runs'] += runs
            if is_dot: m_stat['dots'] += 1
            if is_wkt: m_stat['wkts'] += 1

# Population averages for Bayesian prior
pop_hp_balls = sum(b['balls'] for b in batter_hp.values())
pop_hp_runs = sum(b['runs'] for b in batter_hp.values())
pop_hp_dots = sum(b['dots'] for b in batter_hp.values())
pop_hp_bounds = sum(b['fours'] + b['sixes'] for b in batter_hp.values())
pop_hp_dismissals = sum(b['dismissals'] for b in batter_hp.values())

pop_sr = (pop_hp_runs / max(1, pop_hp_balls)) * 100.0
pop_dot_pct = (pop_hp_dots / max(1, pop_hp_balls)) * 100.0
pop_bound_pct = (pop_hp_bounds / max(1, pop_hp_balls)) * 100.0
pop_d_rate = (pop_hp_dismissals / max(1, pop_hp_balls)) * 100.0

print(f"Batting HP Population: SR={pop_sr:.2f}, Dot%={pop_dot_pct:.2f}, Bound%={pop_bound_pct:.2f}, Dismissal%={pop_d_rate:.2f}")

# Batting consistency & CBI calculation
# Minimum threshold: min 40 pressure balls across at least 5 matches
K = 60.0
qualified_batters = []

for sid, hp in batter_hp.items():
    n_balls = hp['balls']
    n_matches = len(hp['matches'])
    if n_balls < 40 or n_matches < 5:
        continue
    
    b_all = batter_all[sid]
    sr_raw = (hp['runs'] / n_balls) * 100.0
    dot_pct_raw = (hp['dots'] / n_balls) * 100.0
    bound_pct_raw = ((hp['fours'] + hp['sixes']) / n_balls) * 100.0
    d_rate_raw = (hp['dismissals'] / n_balls) * 100.0
    
    # Baseline
    base_sr = (b_all['runs'] / b_all['balls']) * 100.0
    delta_sr = sr_raw - base_sr
    
    # Bayesian shrinkage
    w = n_balls / (n_balls + K)
    sr_adj = w * sr_raw + (1.0 - w) * pop_sr
    dot_pct_adj = w * dot_pct_raw + (1.0 - w) * pop_dot_pct
    bound_pct_adj = w * bound_pct_raw + (1.0 - w) * pop_bound_pct
    d_rate_adj = w * d_rate_raw + (1.0 - w) * pop_d_rate
    
    # Match consistency: standard deviation of match SR (clamped)
    match_srs = []
    for mid, mstat in batter_hp_match[sid].items():
        if mstat['balls'] >= 4:
            match_srs.append((mstat['runs'] / mstat['balls']) * 100.0)
    
    if len(match_srs) >= 3:
        sr_std = float(np.std(match_srs))
        # Consistency score: higher is better, penalize high variance
        consistency = max(0.0, 100.0 - (sr_std / 2.0))
    else:
        consistency = 50.0 # Prior
        
    qualified_batters.append({
        'id': sid,
        'name': player_names[sid],
        'balls': n_balls,
        'matches': n_matches,
        'runs': hp['runs'],
        'sr_raw': sr_raw,
        'base_sr': base_sr,
        'delta_sr': delta_sr,
        'sr_adj': sr_adj,
        'dot_pct_adj': dot_pct_adj,
        'bound_pct_adj': bound_pct_adj,
        'd_rate_adj': d_rate_adj,
        'consistency': consistency
    })

print(f"Qualified Batters (>=40 balls, >=5 matches): {len(qualified_batters)}")

# Calculate CBI using percentile ranks
from scipy import stats

def get_percentile_ranks(values, reverse=False):
    # reverse=True means lower value gets higher percentile (e.g. dot%, dismissals, economy)
    ranks = stats.rankdata(values)
    pcts = 100.0 * (ranks - 0.5) / len(values)
    if reverse:
        pcts = 100.0 - pcts
    return pcts

sr_pct = get_percentile_ranks([b['sr_adj'] for b in qualified_batters])
dot_pct = get_percentile_ranks([b['dot_pct_adj'] for b in qualified_batters], reverse=True)
bound_pct = get_percentile_ranks([b['bound_pct_adj'] for b in qualified_batters])
d_rate_pct = get_percentile_ranks([b['d_rate_adj'] for b in qualified_batters], reverse=True)
delta_sr_pct = get_percentile_ranks([b['delta_sr'] for b in qualified_batters])
const_pct = get_percentile_ranks([b['consistency'] for b in qualified_batters])

for i, b in enumerate(qualified_batters):
    # CBI weights: 30% SR, 20% Dot avoidance, 15% Dismissal avoidance, 15% Boundary, 10% Delta SR, 10% Consistency
    cbi = (
        0.30 * sr_pct[i] +
        0.20 * dot_pct[i] +
        0.15 * d_rate_pct[i] +
        0.15 * bound_pct[i] +
        0.10 * delta_sr_pct[i] +
        0.10 * const_pct[i]
    )
    b['cbi'] = cbi

qualified_batters.sort(key=lambda x: x['cbi'], reverse=True)

print("\n=== TOP 15 BATTERS BY CBI ===")
for i, b in enumerate(qualified_batters[:15], 1):
    print(f"{i:2d}. {b['name']:22s} | CBI={b['cbi']:.2f} | HP_Balls={b['balls']:3d} | Match={b['matches']:2d} | HP_SR={b['sr_raw']:.1f} | Base_SR={b['base_sr']:.1f} | ΔSR={b['delta_sr']:+5.1f} | Dot%={b['dot_pct_adj']:.1f}%")
