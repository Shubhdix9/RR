import csv
import math
import numpy as np
from collections import defaultdict

# 1. Load matches and competitions
matches = {}
with open('matches.csv', 'r') as f:
    for r in csv.DictReader(f):
        matches[r['match_id']] = r

comps = {}
with open('competitions.csv', 'r') as f:
    for r in csv.DictReader(f):
        comps[r['comp_id']] = r

# 2. Player team mappings across seasons
player_teams = defaultdict(set)
player_comps = defaultdict(set)
with open('competition_team_player_mapping.csv', 'r') as f:
    for r in csv.DictReader(f):
        player_teams[r['player_id']].add(r['team_name'])
        player_comps[r['player_id']].add(r['comp_name'])

# 3. Known retired players from IPL / professional T20 cricket by 2026
retired_players = {
    'Shikhar Dhawan', 'Dinesh Karthik', 'Ravichandran Ashwin', 'Mohit Sharma',
    'Ambati Rayudu', 'Kieron Pollard', 'Dwayne Bravo', 'Eoin Morgan',
    'David Wiese', 'Manoj Tiwary', 'Varun Aaron', 'Amit Mishra', 'Piyush Chawla',
    'Robin Uthappa', 'Suresh Raina', 'Wriddhiman Saha', 'Ishant Sharma',
    'Umesh Yadav', 'Kedar Jadhav', 'Shane Watson', 'AB de Villiers'
}

# 4. Untouchable / Retained Franchise Faces (not realistic auction steals for RR in 2027)
retained_superstars = {
    'Virat Kohli', 'Rohit Sharma', 'Jasprit Bumrah', 'Suryakumar Yadav',
    'Hardik Pandya', 'Ravindra Jadeja', 'Rishabh Pant', 'KL Rahul',
    'Shreyas Iyer', 'Shubman Gill', 'Heinrich Klaasen', 'Sanju Samson',
    'Yashasvi Jaiswal', 'Rinku Singh', 'Ruturaj Gaikwad', 'Axar Patel',
    'Sunil Narine', 'Andre Russell', 'Nicholas Pooran', 'Rashid Khan',
    'Kuldeep Yadav', 'Mohammed Siraj', 'Arshdeep Singh', 'Travis Head',
    'Pat Cummins', 'Mitchell Starc', 'Riyan Parag', 'Dhruv Jurel' # RR's own retained core
}

def is_pakistani(pid):
    for t in player_teams[pid]:
        if 'pakistan' in t.lower():
            return True
    return False

def is_ineligible_or_unavailable(pid, name):
    if is_pakistani(pid):
        return True, "Pakistani (Ineligible)"
    if name in retired_players:
        return True, "Retired"
    if name in retained_superstars:
        return True, "Retained Marquee Core"
    return False, "Eligible"

# 5. First pass: compute expected runs E[Runs | over, wkts, inn] across all 201,000 deliveries
state_runs = defaultdict(list)
state_wkts = defaultdict(list)

# Compute 1st inn totals
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

print("Training delivery-level Expected Value & Leverage Index...")
