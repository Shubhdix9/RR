import csv
import math
import numpy as np
from collections import defaultdict

print("=== STARTING CLUTCH-X MASTER PIPELINE ===")

# 1. Load Match metadata
matches = {}
with open('matches.csv', 'r') as f:
    for r in csv.DictReader(f):
        matches[r['match_id']] = r

comps = {}
with open('competitions.csv', 'r') as f:
    for r in csv.DictReader(f):
        comps[r['comp_id']] = r

# 2. Compute 1st innings totals per match
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

# 3. Score all deliveries
deliveries = []
print("Scoring 201,000 deliveries with pre-delivery match state...")
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
        
        over_id = int(r['overid'])
        phase = 'PP' if over_id <= 6 else ('MIDDLE' if over_id <= 15 else 'DEATH')
        
        deliveries.append({
            'mid': mid,
            'inn': inn,
            'overid': over_id,
            'phase': phase,
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

ps_vals = np.array([d['ps'] for d in deliveries])
p75 = float(np.percentile(ps_vals, 75))
p80 = float(np.percentile(ps_vals, 80))
p85 = float(np.percentile(ps_vals, 85))

print(f"Scored {len(deliveries)} deliveries.")
print(f"Thresholds: P75 (Top 25%) = {p75:.2f} | P80 (Top 20% Primary) = {p80:.2f} | P85 (Top 15%) = {p85:.2f}")

def calc_percentile_ranks(values, reverse=False):
    n = len(values)
    order = np.argsort(values)
    ranks = np.empty(n, dtype=float)
    ranks[order] = np.arange(1, n + 1, dtype=float)
    pcts = 100.0 * (ranks - 0.5) / n
    return (100.0 - pcts) if reverse else pcts

# 4. Analyze function for any given threshold
def evaluate_players(threshold, min_bat_balls=40, min_bowl_balls=50, min_matches=5):
    player_names = {}
    
    # BATTING
    b_all = defaultdict(lambda: {'balls': 0, 'runs': 0, 'dots': 0, 'fours': 0, 'sixes': 0, 'dismissals': 0, 'matches': set()})
    b_hp = defaultdict(lambda: {'balls': 0, 'runs': 0, 'dots': 0, 'fours': 0, 'sixes': 0, 'dismissals': 0, 'matches': set(), 'phases': defaultdict(lambda: [0, 0])}) # [balls, runs]
    b_match = defaultdict(lambda: defaultdict(lambda: [0, 0])) # mid: [balls, runs]
    
    # BOWLING
    bw_all = defaultdict(lambda: {'balls': 0, 'runs': 0, 'dots': 0, 'bounds': 0, 'wkts': 0, 'matches': set()})
    bw_hp = defaultdict(lambda: {'balls': 0, 'runs': 0, 'dots': 0, 'bounds': 0, 'wkts': 0, 'matches': set(), 'phases': defaultdict(lambda: [0, 0, 0])}) # [balls, runs, wkts]
    bw_match = defaultdict(lambda: defaultdict(lambda: [0, 0, 0])) # mid: [balls, runs, wkts]
    
    for d in deliveries:
        sid, sname = d['striker_id'], d['striker_name']
        bid, bname = d['bowler_id'], d['bowler_name']
        player_names[sid] = sname
        player_names[bid] = bname
        
        mid = d['mid']
        runs = d['runs']
        ext = d['ext_type']
        ext2 = d['ext_2']
        is_hp = (d['ps'] >= threshold)
        phase = d['phase']
        
        # --- Batting stats ---
        if ext != 'wide':
            is_dot = (runs == 0 and ext == 'None')
            is_wkt = (d['is_wkt'] and d['dismissed_id'] == sid)
            
            ba = b_all[sid]
            ba['balls'] += 1
            ba['runs'] += runs
            if is_dot: ba['dots'] += 1
            if d['is_four']: ba['fours'] += 1
            if d['is_six']: ba['sixes'] += 1
            if is_wkt: ba['dismissals'] += 1
            ba['matches'].add(mid)
            
            if is_hp:
                bhp = b_hp[sid]
                bhp['balls'] += 1
                bhp['runs'] += runs
                if is_dot: bhp['dots'] += 1
                if d['is_four']: bhp['fours'] += 1
                if d['is_six']: bhp['sixes'] += 1
                if is_wkt: bhp['dismissals'] += 1
                bhp['matches'].add(mid)
                bhp['phases'][phase][0] += 1
                bhp['phases'][phase][1] += runs
                
                b_match[sid][mid][0] += 1
                b_match[sid][mid][1] += runs
                
        # --- Bowling stats ---
        is_legal = (ext not in ['wide', 'Overstep'])
        b_conceded = runs + ((1 + ext2) if ext in ['wide', 'Overstep'] else 0)
        is_bw_wkt = (d['is_wkt'] and d['d_type'] not in ['RunOut', 'Retire Out', 'Obstracting the field', 'Obstructing the field', ''])
        is_bound = (d['is_four'] or d['is_six'])
        
        bwa = bw_all[bid]
        if is_legal:
            bwa['balls'] += 1
            if b_conceded == 0: bwa['dots'] += 1
        bwa['runs'] += b_conceded
        if is_bound: bwa['bounds'] += 1
        if is_bw_wkt: bwa['wkts'] += 1
        bwa['matches'].add(mid)
        
        if is_hp:
            bwh = bw_hp[bid]
            if is_legal:
                bwh['balls'] += 1
                if b_conceded == 0: bwh['dots'] += 1
                bwh['phases'][phase][0] += 1
            bwh['runs'] += b_conceded
            if is_bound: bwh['bounds'] += 1
            if is_bw_wkt:
                bwh['wkts'] += 1
                bwh['phases'][phase][2] += 1
            bwh['matches'].add(mid)
            bwh['phases'][phase][1] += b_conceded
            
            if is_legal: bw_match[bid][mid][0] += 1
            bw_match[bid][mid][1] += b_conceded
            if is_bw_wkt: bw_match[bid][mid][2] += 1

    # --- Batting Ranking ---
    pop_b_balls = sum(b['balls'] for b in b_hp.values())
    pop_b_runs = sum(b['runs'] for b in b_hp.values())
    pop_b_dots = sum(b['dots'] for b in b_hp.values())
    pop_b_bounds = sum(b['fours'] + b['sixes'] for b in b_hp.values())
    pop_b_d = sum(b['dismissals'] for b in b_hp.values())
    
    pop_sr = (pop_b_runs / max(1, pop_b_balls)) * 100.0
    pop_dot = (pop_b_dots / max(1, pop_b_balls)) * 100.0
    pop_bound = (pop_b_bounds / max(1, pop_b_balls)) * 100.0
    pop_d = (pop_b_d / max(1, pop_b_balls)) * 100.0
    
    K = 60.0
    bat_list = []
    for sid, bhp in b_hp.items():
        n = bhp['balls']
        m = len(bhp['matches'])
        if n < min_bat_balls or m < min_matches:
            continue
        ba = b_all[sid]
        sr_raw = (bhp['runs'] / n) * 100.0
        base_sr = (ba['runs'] / ba['balls']) * 100.0
        delta_sr = sr_raw - base_sr
        
        w = n / (n + K)
        sr_adj = w * sr_raw + (1.0 - w) * pop_sr
        dot_adj = w * ((bhp['dots'] / n) * 100.0) + (1.0 - w) * pop_dot
        bound_adj = w * (((bhp['fours'] + bhp['sixes']) / n) * 100.0) + (1.0 - w) * pop_bound
        d_adj = w * ((bhp['dismissals'] / n) * 100.0) + (1.0 - w) * pop_d
        
        # Consistency
        m_srs = [ (v[1]/v[0])*100.0 for v in b_match[sid].values() if v[0] >= 4 ]
        consistency = max(0.0, 100.0 - float(np.std(m_srs)/2.0)) if len(m_srs) >= 3 else 50.0
        
        # Best phase
        best_phase = max(bhp['phases'].keys(), key=lambda p: (bhp['phases'][p][1]/max(1, bhp['phases'][p][0])) if bhp['phases'][p][0]>=10 else 0)
        
        bat_list.append({
            'id': sid, 'name': player_names[sid], 'balls': n, 'matches': m,
            'runs': bhp['runs'], 'sr_raw': sr_raw, 'base_sr': base_sr, 'delta_sr': delta_sr,
            'sr_adj': sr_adj, 'dot_adj': dot_adj, 'bound_adj': bound_adj, 'd_adj': d_adj,
            'consistency': consistency, 'best_phase': best_phase,
            'dismissals': bhp['dismissals'], 'dots': bhp['dots'], 'bounds': bhp['fours'] + bhp['sixes']
        })
        
    sr_p = calc_percentile_ranks([b['sr_adj'] for b in bat_list])
    dot_p = calc_percentile_ranks([b['dot_adj'] for b in bat_list], reverse=True)
    bound_p = calc_percentile_ranks([b['bound_adj'] for b in bat_list])
    d_p = calc_percentile_ranks([b['d_adj'] for b in bat_list], reverse=True)
    delta_p = calc_percentile_ranks([b['delta_sr'] for b in bat_list])
    const_p = calc_percentile_ranks([b['consistency'] for b in bat_list])
    
    for i, b in enumerate(bat_list):
        b['cbi'] = (
            0.30 * sr_p[i] +
            0.20 * dot_p[i] +
            0.15 * d_p[i] +
            0.15 * bound_p[i] +
            0.10 * delta_p[i] +
            0.10 * const_p[i]
        )
    bat_list.sort(key=lambda x: x['cbi'], reverse=True)
    
    # --- Bowling Ranking ---
    pop_bw_balls = sum(b['balls'] for b in bw_hp.values())
    pop_bw_runs = sum(b['runs'] for b in bw_hp.values())
    pop_bw_dots = sum(b['dots'] for b in bw_hp.values())
    pop_bw_bounds = sum(b['bounds'] for b in bw_hp.values())
    pop_bw_wkts = sum(b['wkts'] for b in bw_hp.values())
    
    pop_econ = (pop_bw_runs / max(1, pop_bw_balls)) * 6.0
    pop_bw_dot = (pop_bw_dots / max(1, pop_bw_balls)) * 100.0
    pop_bw_bound = (pop_bw_bounds / max(1, pop_bw_balls)) * 100.0
    pop_wkt_rate = (pop_bw_wkts / max(1, pop_bw_balls)) * 100.0
    
    bowl_list = []
    for bid, bwh in bw_hp.items():
        n = bwh['balls']
        m = len(bwh['matches'])
        if n < min_bowl_balls or m < min_matches:
            continue
        bwa = bw_all[bid]
        econ_raw = (bwh['runs'] / n) * 6.0
        base_econ = (bwa['runs'] / bwa['balls']) * 6.0
        delta_econ = base_econ - econ_raw # Positive means more economical under pressure
        
        w = n / (n + K)
        econ_adj = w * econ_raw + (1.0 - w) * pop_econ
        wkt_adj = w * ((bwh['wkts'] / n) * 100.0) + (1.0 - w) * pop_wkt_rate
        dot_adj = w * ((bwh['dots'] / n) * 100.0) + (1.0 - w) * pop_bw_dot
        bound_adj = w * ((bwh['bounds'] / n) * 100.0) + (1.0 - w) * pop_bw_bound
        
        # Consistency
        m_econs = [ (v[1]/v[0])*6.0 for v in bw_match[bid].values() if v[0] >= 6 ]
        consistency = max(0.0, 100.0 - float(np.std(m_econs)*5.0)) if len(m_econs) >= 3 else 50.0
        
        best_phase = min(bwh['phases'].keys(), key=lambda p: (bwh['phases'][p][1]/max(1, bwh['phases'][p][0])*6.0) if bwh['phases'][p][0]>=12 else 99.0)
        
        bowl_list.append({
            'id': bid, 'name': player_names[bid], 'balls': n, 'matches': m,
            'runs': bwh['runs'], 'wkts': bwh['wkts'], 'econ_raw': econ_raw, 'base_econ': base_econ, 'delta_econ': delta_econ,
            'econ_adj': econ_adj, 'wkt_adj': wkt_adj, 'dot_adj': dot_adj, 'bound_adj': bound_adj,
            'consistency': consistency, 'best_phase': best_phase,
            'dots': bwh['dots'], 'bounds': bwh['bounds']
        })
        
    econ_p = calc_percentile_ranks([b['econ_adj'] for b in bowl_list], reverse=True)
    wkt_p = calc_percentile_ranks([b['wkt_adj'] for b in bowl_list])
    dot_p = calc_percentile_ranks([b['dot_adj'] for b in bowl_list])
    bound_p = calc_percentile_ranks([b['bound_adj'] for b in bowl_list], reverse=True)
    delta_p = calc_percentile_ranks([b['delta_econ'] for b in bowl_list])
    const_p = calc_percentile_ranks([b['consistency'] for b in bowl_list])
    
    for i, b in enumerate(bowl_list):
        b['pbi'] = (
            0.30 * econ_p[i] +
            0.25 * wkt_p[i] +
            0.15 * dot_p[i] +
            0.10 * bound_p[i] +
            0.10 * delta_p[i] +
            0.10 * const_p[i]
        )
    bowl_list.sort(key=lambda x: x['pbi'], reverse=True)
    
    return bat_list, bowl_list

# Run primary evaluation (P80)
print("\n--- Running Evaluation at P80 (Top 20% Pressure) ---")
bat_p80, bowl_p80 = evaluate_players(p80)

print(f"Qualified Batters: {len(bat_p80)} | Qualified Bowlers: {len(bowl_p80)}")

print("\n================== TOP 10 BATTERS (CLUTCH BATTING INDEX) ==================")
print(f"{'Rank':4s} | {'Player Name':22s} | {'CBI':5s} | {'HP Balls':8s} | {'HP SR':6s} | {'Base SR':7s} | {'ΔSR':6s} | {'Dot%':5s} | {'Bnd%':5s} | {'Best Phase'}")
print("-" * 95)
for i, b in enumerate(bat_p80[:10], 1):
    print(f"{i:4d} | {b['name']:22s} | {b['cbi']:5.1f} | {b['balls']:8d} | {b['sr_raw']:6.1f} | {b['base_sr']:7.1f} | {b['delta_sr']:+6.1f} | {b['dot_adj']:4.1f}% | {b['bound_adj']:4.1f}% | {b['best_phase']}")

print("\n================== TOP 10 BOWLERS (PRESSURE BOWLING INDEX) ==================")
print(f"{'Rank':4s} | {'Player Name':22s} | {'PBI':5s} | {'HP Balls':8s} | {'Wkts':4s} | {'HP Econ':7s} | {'Base Econ':9s} | {'ΔEcon':6s} | {'Dot%':5s} | {'Best Phase'}")
print("-" * 95)
for i, b in enumerate(bowl_p80[:10], 1):
    print(f"{i:4d} | {b['name']:22s} | {b['pbi']:5.1f} | {b['balls']:8d} | {b['wkts']:4d} | {b['econ_raw']:7.2f} | {b['base_econ']:9.2f} | {b['delta_econ']:+6.2f} | {b['dot_adj']:4.1f}% | {b['best_phase']}")

# Run sensitivity checks at P75 and P85
print("\n--- Sensitivity Stability Check (Top 25% vs Top 20% vs Top 15%) ---")
bat_p75, bowl_p75 = evaluate_players(p75)
bat_p85, bowl_p85 = evaluate_players(p85)

top10_bat_names = [b['name'] for b in bat_p80[:10]]
top10_bowl_names = [b['name'] for b in bowl_p80[:10]]

names_p75_bat = [b['name'] for b in bat_p75[:15]]
names_p85_bat = [b['name'] for b in bat_p85[:15]]
names_p75_bowl = [b['name'] for b in bowl_p75[:15]]
names_p85_bowl = [b['name'] for b in bowl_p85[:15]]

bat_overlap_75 = sum(1 for name in top10_bat_names if name in names_p75_bat)
bat_overlap_85 = sum(1 for name in top10_bat_names if name in names_p85_bat)
bowl_overlap_75 = sum(1 for name in top10_bowl_names if name in names_p75_bowl)
bowl_overlap_85 = sum(1 for name in top10_bowl_names if name in names_p85_bowl)

print(f"Batting Stability: Top-10 overlap with P75 top 15 = {bat_overlap_75}/10, with P85 top 15 = {bat_overlap_85}/10")
print(f"Bowling Stability: Top-10 overlap with P75 top 15 = {bowl_overlap_75}/10, with P85 top 15 = {bowl_overlap_85}/10")

