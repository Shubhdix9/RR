import csv
import math
from collections import defaultdict

# 1. Load Match metadata
matches = {}
with open('matches.csv', 'r') as f:
    for r in csv.DictReader(f):
        matches[r['match_id']] = r

# 2. First pass: compute 1st innings total runs per match
inn1_totals = defaultdict(int)
with open('ball_by_ball.csv', 'r') as f:
    for r in csv.DictReader(f):
        if r['innings'] == '1':
            mid = r['match_id']
            runs = int(r['runs'])
            ext = r['extras_type']
            ext2 = int(r['extras_2_runs'] if r['extras_2_runs'] else 0)
            extra_runs = 0
            if ext in ['wide', 'legbyes', 'byes', 'Overstep', 'other']:
                extra_runs = 1 + ext2
            inn1_totals[mid] += runs + extra_runs

print(f"Computed 1st innings totals for {len(inn1_totals)} matches.")

# 3. Model delivery-by-delivery pressure
def estimate_win_prob(runs_req, balls_rem, wkts_hand):
    if runs_req <= 0:
        return 1.0
    if balls_rem <= 0:
        return 0.0
    if wkts_hand <= 0:
        return 0.0
    
    rrr = (runs_req / balls_rem) * 6.0
    # Empirical logit proxy: positive when in control, negative when behind
    # Benchmark: RRR 8.5 with 7 wkts in hand at 60 balls rem -> z ~ 0 (50/50)
    # Resources: wkts_hand (weight ~0.55), balls_rem/20 (weight ~0.3)
    # Demand: rrr (weight ~0.45)
    z = 0.55 * wkts_hand + 0.15 * (balls_rem / 6.0) - 0.48 * rrr - 0.8
    wp = 1.0 / (1.0 + math.exp(-max(-6.0, min(6.0, z))))
    return wp

pressure_scores = []
sample_high_p = []

with open('ball_by_ball.csv', 'r') as f:
    reader = csv.DictReader(f)
    curr_mid = None
    curr_inn = None
    cum_runs = 0
    cum_wkts = 0
    legal_balls = 0
    target = 0
    total_balls = 120
    is_ko = False
    
    for r in reader:
        mid = r['match_id']
        inn = r['innings']
        
        # Reset state on new innings or match
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
                if rev_t:
                    target = int(rev_t)
                else:
                    target = inn1_totals.get(mid, 160) + 1
        
        # State BEFORE the delivery
        wkts_hand = max(0, 10 - cum_wkts)
        balls_rem = max(1, total_balls - legal_balls)
        
        if inn == '2' and target is not None:
            runs_req = max(1, target - cum_runs)
            rrr = (runs_req / balls_rem) * 6.0
            
            # S_rrr: stress from required run rate
            s_rrr = min(1.5, max(0.0, (rrr - 6.0) / 10.0))
            # S_wkt: wicket loss stress
            s_wkt = 1.0 - (wkts_hand / 10.0) ** 1.2
            # S_urgency: balls running out
            s_urgency = min(1.0, max(0.0, 1.0 - (balls_rem / total_balls)))
            
            # Win probability & leverage
            wp = estimate_win_prob(runs_req, balls_rem, wkts_hand)
            # Leverage index: peaks at WP=0.5, dampens garbage time
            leverage = 4.0 * wp * (1.0 - wp)
            
            raw_p = 100.0 * (0.35 * s_rrr + 0.35 * s_wkt + 0.30 * s_urgency) * (0.25 + 0.75 * leverage)
        else:
            # Innings 1
            over_num = legal_balls // 6 + 1
            # Expected wickets lost by over
            exp_wkts = 10.0 * ((legal_balls / 120.0) ** 1.3)
            collapse_stress = min(1.0, max(0.0, (cum_wkts - exp_wkts) / max(1, wkts_hand)))
            
            # Phase stress
            if over_num <= 6:
                phase_stress = 0.35 if cum_wkts >= 2 else 0.20
            elif over_num <= 15:
                phase_stress = 0.40 if cum_wkts >= 4 else 0.25
            else: # Death overs 16-20
                phase_stress = 0.75 + 0.25 * ((over_num - 15) / 5.0)
            
            # Par deficit (assuming modern par ~8.5 RPO)
            par_runs = (legal_balls / 6.0) * 8.5
            deficit_stress = min(1.0, max(0.0, (par_runs - cum_runs) / 30.0))
            
            raw_p = 100.0 * (0.45 * phase_stress + 0.35 * collapse_stress + 0.20 * deficit_stress)
            
        if is_ko:
            ps = min(100.0, raw_p * 1.15)
        else:
            ps = min(100.0, raw_p)
            
        pressure_scores.append(ps)
        
        # State update AFTER the delivery
        ext = r['extras_type']
        ext2 = int(r['extras_2_runs'] if r['extras_2_runs'] else 0)
        runs = int(r['runs'])
        extra_runs = (1 + ext2) if ext in ['wide', 'legbyes', 'byes', 'Overstep', 'other'] else 0
        cum_runs += runs + extra_runs
        if ext not in ['wide', 'Overstep']:
            legal_balls += 1
        if r['is_wicket'].lower() == 'true':
            cum_wkts += 1

import numpy as np
ps_arr = np.array(pressure_scores)
p50 = np.percentile(ps_arr, 50)
p75 = np.percentile(ps_arr, 75)
p80 = np.percentile(ps_arr, 80)
p85 = np.percentile(ps_arr, 85)
p90 = np.percentile(ps_arr, 90)

print(f"Total deliveries scored: {len(ps_arr)}")
print(f"Pressure Distribution: Min={ps_arr.min():.1f}, P50={p50:.1f}, P75={p75:.1f}, P80={p80:.1f}, P85={p85:.1f}, P90={p90:.1f}, Max={ps_arr.max():.1f}")
