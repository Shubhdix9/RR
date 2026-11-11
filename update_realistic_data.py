import json

batters = [
    {"rank": 1, "name": "Tom Banton", "cbi": 89.5, "balls": 55, "sr_raw": 190.9, "base_sr": 159.5, "delta_sr": 31.4, "dot_adj": 24.8, "bound_adj": 24.7, "best_phase": "DEATH", "role": "Overseas WK / Finisher"},
    {"rank": 2, "name": "Najibullah Zadran", "cbi": 85.5, "balls": 94, "sr_raw": 176.6, "base_sr": 138.6, "delta_sr": 38.0, "dot_adj": 25.7, "bound_adj": 21.7, "best_phase": "DEATH", "role": "Middle-Overs Enforcer"},
    {"rank": 3, "name": "Sai Sudharsan", "cbi": 81.9, "balls": 195, "sr_raw": 187.2, "base_sr": 149.2, "delta_sr": 38.0, "dot_adj": 20.6, "bound_adj": 24.9, "best_phase": "DEATH", "role": "Indian Clutch Anchor"},
    {"rank": 4, "name": "Romario Shepherd", "cbi": 81.7, "balls": 247, "sr_raw": 191.1, "base_sr": 154.1, "delta_sr": 36.9, "dot_adj": 27.2, "bound_adj": 25.9, "best_phase": "DEATH", "role": "Pace All-Rounder Finisher"},
    {"rank": 5, "name": "Glenn Maxwell", "cbi": 81.6, "balls": 183, "sr_raw": 212.0, "base_sr": 161.0, "delta_sr": 51.1, "dot_adj": 24.9, "bound_adj": 28.5, "best_phase": "DEATH", "role": "Dynamic Match-Winner"},
    {"rank": 6, "name": "Marcus Stoinis", "cbi": 80.7, "balls": 359, "sr_raw": 181.6, "base_sr": 153.6, "delta_sr": 28.0, "dot_adj": 27.6, "bound_adj": 24.2, "best_phase": "DEATH", "role": "Pace All-Rounder Finisher"},
    {"rank": 7, "name": "Harry Tector", "cbi": 80.7, "balls": 157, "sr_raw": 160.5, "base_sr": 122.6, "delta_sr": 37.9, "dot_adj": 18.2, "bound_adj": 20.1, "best_phase": "DEATH", "role": "Low-Dot Middle Anchor"},
    {"rank": 8, "name": "Shashank Singh", "cbi": 80.0, "balls": 193, "sr_raw": 186.5, "base_sr": 161.6, "delta_sr": 24.9, "dot_adj": 24.3, "bound_adj": 26.2, "best_phase": "DEATH", "role": "Domestic Clutch Finisher"},
    {"rank": 9, "name": "Naman Dhir", "cbi": 78.1, "balls": 117, "sr_raw": 206.8, "base_sr": 168.4, "delta_sr": 38.4, "dot_adj": 26.3, "bound_adj": 29.1, "best_phase": "DEATH", "role": "Domestic Power-Hitter"},
    {"rank": 10, "name": "Tim David", "cbi": 77.8, "balls": 448, "sr_raw": 200.9, "base_sr": 177.7, "delta_sr": 23.2, "dot_adj": 28.8, "bound_adj": 27.4, "best_phase": "DEATH", "role": "Death Power Enforcer"}
]

bowlers = [
    {"rank": 1, "name": "Kane Richardson", "pbi": 88.6, "balls": 73, "wkts": 8, "econ_raw": 6.58, "base_econ": 9.12, "delta_econ": 2.55, "dot_adj": 38.3, "best_phase": "DEATH", "role": "Death Yorker Specialist"},
    {"rank": 2, "name": "Craig Young", "pbi": 87.0, "balls": 86, "wkts": 10, "econ_raw": 7.67, "base_econ": 8.64, "delta_econ": 0.97, "dot_adj": 37.6, "best_phase": "DEATH", "role": "Hit-the-Deck Seamer"},
    {"rank": 3, "name": "Hasan Mahmud", "pbi": 85.8, "balls": 91, "wkts": 7, "econ_raw": 6.92, "base_econ": 7.80, "delta_econ": 0.88, "dot_adj": 38.3, "best_phase": "MIDDLE", "role": "Pace & Death Yorker"},
    {"rank": 4, "name": "Mujeeb Ur Rahman", "pbi": 84.6, "balls": 84, "wkts": 6, "econ_raw": 6.00, "base_econ": 7.00, "delta_econ": 1.00, "dot_adj": 38.1, "best_phase": "MIDDLE", "role": "Mystery Spin Squeeze"},
    {"rank": 5, "name": "Noor Ahmad", "pbi": 83.3, "balls": 258, "wkts": 23, "econ_raw": 7.72, "base_econ": 7.93, "delta_econ": 0.21, "dot_adj": 39.3, "best_phase": "MIDDLE", "role": "Left-Arm Wrist Spin"},
    {"rank": 6, "name": "Vipraj Nigam", "pbi": 82.0, "balls": 50, "wkts": 3, "econ_raw": 5.88, "base_econ": 9.75, "delta_econ": 3.87, "dot_adj": 39.9, "best_phase": "DEATH", "role": "Domestic Leg-Spin Diamond"},
    {"rank": 7, "name": "Kartik Tyagi", "pbi": 78.5, "balls": 107, "wkts": 10, "econ_raw": 8.69, "base_econ": 10.18, "delta_econ": 1.48, "dot_adj": 37.7, "best_phase": "DEATH", "role": "Indian Express Pacer"},
    {"rank": 8, "name": "Wanindu Hasaranga", "pbi": 77.0, "balls": 390, "wkts": 31, "econ_raw": 7.85, "base_econ": 7.92, "delta_econ": 0.08, "dot_adj": 34.4, "best_phase": "MIDDLE", "role": "Wicket-Taking Leg Spinner"},
    {"rank": 9, "name": "Akeal Hosein", "pbi": 76.6, "balls": 179, "wkts": 12, "econ_raw": 7.47, "base_econ": 7.72, "delta_econ": 0.25, "dot_adj": 38.4, "best_phase": "MIDDLE", "role": "PP / Middle Spin Squeeze"},
    {"rank": 10, "name": "Matheesha Pathirana", "pbi": 76.4, "balls": 394, "wkts": 33, "econ_raw": 8.51, "base_econ": 8.60, "delta_econ": 0.09, "dot_adj": 35.2, "best_phase": "DEATH", "role": "Slingy Death Executioner"}
]

with open('top_players_summary.json', 'w') as f:
    json.dump({'batters': batters, 'bowlers': bowlers}, f, indent=2)

print('Updated top_players_summary.json with Realistic Auction Targets!')
