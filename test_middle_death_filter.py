import csv
from collections import defaultdict

# 1. Check captains in matches and playing_eleven
captains = set()
with open('matches.csv', 'r') as f:
    for r in csv.DictReader(f):
        if r['home_team_captain_id']: captains.add(r['home_team_captain_id'])
        if r['away_team_captain_id']: captains.add(r['away_team_captain_id'])

with open('playing_eleven.csv', 'r') as f:
    for r in csv.DictReader(f):
        if r['is_captain'] == '1':
            captains.add(r['player_id'])

print(f"Total identified captains in dataset: {len(captains)}")

# 2. Check batting order distribution per player in ball_by_ball
batter_orders = defaultdict(lambda: defaultdict(int))
bowler_overs = defaultdict(lambda: defaultdict(int))

with open('ball_by_ball.csv', 'r') as f:
    for r in csv.DictReader(f):
        sid = r['striker_id']
        bid = r['bowler_id']
        bo = r['batting_order']
        if bo and bo.isdigit():
            batter_orders[sid][int(bo)] += 1
            
        ov = int(r['overid'])
        if ov <= 6:
            bowler_overs[bid]['PP'] += 1
        elif ov <= 15:
            bowler_overs[bid]['MID'] += 1
        else:
            bowler_overs[bid]['DEATH'] += 1

print("Calculated phase and batting position profiles.")
