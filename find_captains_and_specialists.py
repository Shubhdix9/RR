import csv
from collections import defaultdict

# 1. Identify all captains in IPL 2025 and IPL 2026
ipl_comps = set()
with open('competitions.csv', 'r') as f:
    for r in csv.DictReader(f):
        if r['season'] in ['2025', '2026'] and 'ipl' in r['comp_name'].lower():
            ipl_comps.add(r['comp_id'])

print(f"IPL 2025 and 2026 comp_ids: {ipl_comps}")

ipl_matches = set()
ipl_captains = set()

with open('matches.csv', 'r') as f:
    for r in csv.DictReader(f):
        if r['comp_id'] in ipl_comps:
            ipl_matches.add(r['match_id'])
            if r['home_team_captain_id']: ipl_captains.add(r['home_team_captain_id'])
            if r['away_team_captain_id']: ipl_captains.add(r['away_team_captain_id'])

with open('playing_eleven.csv', 'r') as f:
    for r in csv.DictReader(f):
        if r['match_id'] in ipl_matches and r['is_captain'] == '1':
            ipl_captains.add(r['player_id'])

# Map player_id to names
player_names = {}
with open('competition_team_player_mapping.csv', 'r') as f:
    for r in csv.DictReader(f):
        player_names[r['player_id']] = r['player_name']

print(f"Total IPL 2025-2026 captains found: {len(ipl_captains)}")
print("Sample IPL Captains:")
for cid in list(ipl_captains)[:15]:
    print(f"  {cid}: {player_names.get(cid, 'Unknown')}")

