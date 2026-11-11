import json
import csv
from collections import defaultdict
from clutch_x_master import bat_p80, bowl_p80, comps

# Map player_id to all teams they played for
player_teams = defaultdict(set)
with open('competition_team_player_mapping.csv', 'r') as f:
    for r in csv.DictReader(f):
        player_teams[r['player_id']].add(r['team_name'])

# Pakistani team names or indicators
pak_indicators = {'Pakistan', 'Pakistan A', 'Lahore Qalandars', 'Karachi Kings', 'Peshawar Zalmi', 'Islamabad United', 'Multan Sultans', 'Quetta Gladiators'}

# Known IPL untouchable / retained franchise superstars (not realistic auction steals for RR)
retained_marquee = {
    'Virat Kohli', 'Rohit Sharma', 'Jasprit Bumrah', 'Suryakumar Yadav', 
    'Hardik Pandya', 'Ravindra Jadeja', 'Rishabh Pant', 'KL Rahul', 
    'Shreyas Iyer', 'Shubman Gill', 'Heinrich Klaasen', 'Sanju Samson', 
    'Yashasvi Jaiswal', 'Rinku Singh', 'Ruturaj Gaikwad', 'Axar Patel',
    'Sunil Narine', 'Andre Russell', 'Nicholas Pooran', 'Rashid Khan',
    'Kuldeep Yadav', 'Mohammed Siraj', 'Arshdeep Singh'
}

def is_pakistani(pid, name):
    teams = player_teams[pid]
    for t in teams:
        if any(pi.lower() in t.lower() for pi in ['pakistan']):
            return True
    return False

def is_marquee(name):
    return name in retained_marquee

print("=== REALISTIC AUCTION-ELIGIBLE BATTERS UNDER PRESSURE (CBI) ===")
eligible_batters = []
for b in bat_p80:
    name = b['name']
    pid = b['id']
    if is_pakistani(pid, name):
        continue
    if is_marquee(name):
        continue
    teams = list(player_teams[pid])
    eligible_batters.append((b, teams))

for i, (b, teams) in enumerate(eligible_batters[:20], 1):
    ipl_teams = [t for t in teams if 'ipl' in t.lower() or t in ['Rajasthan Royals', 'Mumbai Indians', 'Chennai Super Kings', 'Royal Challengers Bengaluru', 'Delhi Capitals', 'Kolkata Knight Riders', 'Sunrisers Hyderabad', 'Gujarat Titans', 'Lucknow Super Giants', 'Punjab Kings']]
    print(f"{i:2d}. {b['name']:20s} | CBI={b['cbi']:4.1f} | HP_Balls={b['balls']:3d} | HP_SR={b['sr_raw']:5.1f} | ΔSR={b['delta_sr']:+5.1f} | Dot%={b['dot_adj']:4.1f}% | Teams={ipl_teams[:2] or teams[:1]}")

print("\n=== REALISTIC AUCTION-ELIGIBLE BOWLERS UNDER PRESSURE (PBI) ===")
eligible_bowlers = []
for bw in bowl_p80:
    name = bw['name']
    pid = bw['id']
    if is_pakistani(pid, name):
        continue
    if is_marquee(name):
        continue
    teams = list(player_teams[pid])
    eligible_bowlers.append((bw, teams))

for i, (bw, teams) in enumerate(eligible_bowlers[:20], 1):
    ipl_teams = [t for t in teams if 'ipl' in t.lower() or t in ['Rajasthan Royals', 'Mumbai Indians', 'Chennai Super Kings', 'Royal Challengers Bengaluru', 'Delhi Capitals', 'Kolkata Knight Riders', 'Sunrisers Hyderabad', 'Gujarat Titans', 'Lucknow Super Giants', 'Punjab Kings']]
    print(f"{i:2d}. {bw['name']:20s} | PBI={bw['pbi']:4.1f} | HP_Balls={bw['balls']:3d} | Wkts={bw['wkts']:2d} | HP_Econ={bw['econ_raw']:5.2f} | ΔEcon={bw['delta_econ']:+5.2f} | Teams={ipl_teams[:2] or teams[:1]}")

