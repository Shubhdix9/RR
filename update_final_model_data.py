import json

batters = [
    {"rank": 1, "name": "Glenn Maxwell", "cbi": 92.4, "balls": 183, "sr_raw": 212.0, "base_sr": 161.0, "delta_sr": 51.1, "dot_adj": 24.9, "bound_adj": 28.5, "best_phase": "DEATH", "role": "Middle-Overs Game Changer (#4/5)", "team": "RCB"},
    {"rank": 2, "name": "Shashank Singh", "cbi": 84.4, "balls": 193, "sr_raw": 186.5, "base_sr": 161.6, "delta_sr": 24.9, "dot_adj": 24.3, "bound_adj": 26.2, "best_phase": "DEATH", "role": "Domestic Clutch Finisher Sensation (#6/7)", "team": "PBKS"},
    {"rank": 3, "name": "Romario Shepherd", "cbi": 84.0, "balls": 247, "sr_raw": 191.1, "base_sr": 154.1, "delta_sr": 36.9, "dot_adj": 27.2, "bound_adj": 25.9, "best_phase": "DEATH", "role": "Pace All-Rounder & Death Finisher (#7)", "team": "RCB"},
    {"rank": 4, "name": "Marcus Stoinis", "cbi": 83.6, "balls": 359, "sr_raw": 181.6, "base_sr": 153.6, "delta_sr": 28.0, "dot_adj": 27.6, "bound_adj": 24.2, "best_phase": "DEATH", "role": "Seam All-Rounder & Finisher (#5/6)", "team": "LSG"},
    {"rank": 5, "name": "Abdul Samad", "cbi": 82.3, "balls": 164, "sr_raw": 185.4, "base_sr": 149.8, "delta_sr": 35.6, "dot_adj": 26.6, "bound_adj": 25.0, "best_phase": "DEATH", "role": "Domestic Death Boundary Striker (#6/7)", "team": "LSG"},
    {"rank": 6, "name": "Tim David", "cbi": 82.2, "balls": 448, "sr_raw": 200.9, "base_sr": 177.7, "delta_sr": 23.2, "dot_adj": 28.8, "bound_adj": 27.4, "best_phase": "DEATH", "role": "Death Boundary Maximizer (#6)", "team": "MI"},
    {"rank": 7, "name": "Liam Livingstone", "cbi": 81.6, "balls": 270, "sr_raw": 178.9, "base_sr": 153.9, "delta_sr": 25.0, "dot_adj": 26.5, "bound_adj": 24.8, "best_phase": "DEATH", "role": "Middle-Overs Power Enforcer (#4/5)", "team": "PBKS"},
    {"rank": 8, "name": "Najibullah Zadran", "cbi": 81.5, "balls": 94, "sr_raw": 176.6, "base_sr": 138.6, "delta_sr": 38.0, "dot_adj": 25.7, "bound_adj": 21.7, "best_phase": "DEATH", "role": "Middle Spin Destroyer & Finisher (#5/6)", "team": "AFG"},
    {"rank": 9, "name": "Donovan Ferreira", "cbi": 81.3, "balls": 152, "sr_raw": 187.5, "base_sr": 163.8, "delta_sr": 23.7, "dot_adj": 28.6, "bound_adj": 27.0, "best_phase": "DEATH", "role": "Explosive Finisher / WK Utility (#6/7)", "team": "RR"},
    {"rank": 10, "name": "Tristan Stubbs", "cbi": 76.1, "balls": 369, "sr_raw": 164.8, "base_sr": 149.9, "delta_sr": 14.9, "dot_adj": 23.7, "bound_adj": 23.4, "best_phase": "DEATH", "role": "Dynamic 360° Finisher / Spin Smasher (#5/6)", "team": "DC"}
]

bowlers = [
    {"rank": 1, "name": "Vipraj Nigam", "pbi": 87.7, "balls": 50, "wkts": 3, "econ_raw": 5.64, "base_econ": 9.29, "delta_econ": 3.65, "dot_adj": 39.9, "best_phase": "MIDDLE", "role": "Uncapped Indian Domestic Diamond (Jaipur Fit)", "team": "DC"},
    {"rank": 2, "name": "Noor Ahmad", "pbi": 87.1, "balls": 258, "wkts": 23, "econ_raw": 7.16, "base_econ": 7.61, "delta_econ": 0.45, "dot_adj": 39.3, "best_phase": "MIDDLE", "role": "Left-Arm Wrist Spin Wicket Machine (96% Mid/Death)", "team": "GT"},
    {"rank": 3, "name": "Matheesha Pathirana", "pbi": 85.0, "balls": 394, "wkts": 33, "econ_raw": 7.77, "base_econ": 7.79, "delta_econ": 0.02, "dot_adj": 35.2, "best_phase": "DEATH", "role": "Slingy Death Yorker Specialist (94% Mid/Death)", "team": "CSK"},
    {"rank": 4, "name": "Kartik Tyagi", "pbi": 82.2, "balls": 107, "wkts": 10, "econ_raw": 8.47, "base_econ": 9.79, "delta_econ": 1.32, "dot_adj": 37.7, "best_phase": "DEATH", "role": "Express Indian Pacer / Death Specialist (Former RR)", "team": "GT/KKR"},
    {"rank": 5, "name": "Qais Ahmad", "pbi": 79.5, "balls": 74, "wkts": 4, "econ_raw": 6.41, "base_econ": 7.50, "delta_econ": 1.09, "dot_adj": 35.7, "best_phase": "MIDDLE", "role": "Attacking Wrist-Spin Squeeze (100% Mid/Death)", "team": "AFG"},
    {"rank": 6, "name": "Moeen Ali", "pbi": 77.1, "balls": 100, "wkts": 5, "econ_raw": 6.18, "base_econ": 8.08, "delta_econ": 1.90, "dot_adj": 38.0, "best_phase": "MIDDLE", "role": "Middle-Overs Off-Spin Squeeze (78% Mid/Death)", "team": "CSK"},
    {"rank": 7, "name": "Wanindu Hasaranga", "pbi": 74.8, "balls": 390, "wkts": 31, "econ_raw": 7.77, "base_econ": 7.87, "delta_econ": 0.10, "dot_adj": 34.4, "best_phase": "MIDDLE", "role": "Middle-Overs Leg-Spin Weapon (93% Mid/Death)", "team": "SRH/RCB"},
    {"rank": 8, "name": "Chamika Karunaratne", "pbi": 73.7, "balls": 56, "wkts": 4, "econ_raw": 7.61, "base_econ": 8.41, "delta_econ": 0.80, "dot_adj": 36.5, "best_phase": "MIDDLE", "role": "Seam Change-Up & Middle/Death Bowler", "team": "KKR"},
    {"rank": 9, "name": "Harshal Patel", "pbi": 73.6, "balls": 470, "wkts": 44, "econ_raw": 8.66, "base_econ": 8.77, "delta_econ": 0.11, "dot_adj": 35.8, "best_phase": "DEATH", "role": "Death-Overs Slower Ball & Dip Master (90% Mid/Death)", "team": "PBKS"},
    {"rank": 10, "name": "Krunal Pandya", "pbi": 73.5, "balls": 174, "wkts": 10, "econ_raw": 7.17, "base_econ": 7.63, "delta_econ": 0.46, "dot_adj": 37.2, "best_phase": "MIDDLE", "role": "Middle-Overs Defensive Squeeze (80% Mid/Death)", "team": "LSG"}
]

with open('top_players_summary.json', 'w') as f:
    json.dump({'batters': batters, 'bowlers': bowlers}, f, indent=2)

print('Saved top_players_summary.json successfully with pure specialist middle/death players!')
