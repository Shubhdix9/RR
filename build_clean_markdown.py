import json

with open('top_players_summary.json') as f:
    data = json.load(f)

batters = data['batters'][:10]
bowlers = data['bowlers'][:10]

md_content = """# Rajasthan Royals War Room Player Evaluation & Auction Strategy
## High-Pressure Performance Modeling & IPL 2027 Auction Target Identification
**Analysis Scope:** Proprietary Delivery-Level Match Records (2022–2026), 200,999 Deliveries, 883 Matches (IPL & International T20Is)  
**Live Interactive Dashboard:** [https://shubhdix9.github.io/RR/](https://shubhdix9.github.io/RR/)  
**GitHub Repository:** [https://github.com/Shubhdix9/RR](https://github.com/Shubhdix9/RR)  

---

## Executive Summary: How Modern IPL War Rooms Actually Scout

Cricket analytics often fails when franchises rely solely on traditional counting stats (Runs, Average, Overall Strike Rate). A batter scoring 60 off 40 balls in a dead rubber chasing 220 when the match is effectively over generates vanity volume but near-zero franchise win-probability equity.

To shape Rajasthan Royals' **IPL 2027 Auction Strategy**, an analytics war room must answer three foundational challenges:
1. **Define Pre-Delivery Pressure Without Outcome Leakage:** Quantify match stress using only the continuous state of the game *before* each ball is bowled (Wickets in hand, Balls Remaining, Required Run Rate vs. Dynamic Par, Innings Leverage, and Playoff Stakes).
2. **Context-Adjusted Expected Value (xRA & xRP):** Measure performance against state-specific empirical baseline expectations ($\mathbb{E}[Runs|State]$, $\mathbb{E}[Wkt|State]$) across match phases, isolating true execution under stress from routine accumulation.
3. **Realistic Franchise Auction Economics & Recruitment Feasibility:** Filter out legally ineligible players, untouchable retained mega-stars, established openers, and powerplay-opening pacers to focus strictly on Rajasthan Royals' genuine tactical deficits.

---

## 1. Franchise Auction Feasibility & Eligibility Filters (Exclusion of Star Retentions)

A naive model might rank famous superstars at the top. However, an elite franchise war room operates under strict commercial and tactical constraints. Our model enforces four non-negotiable operational filters:

### 1.1 Exclusion of Franchise Mega-Stars & Retained Faces
Players such as **Virat Kohli, Jasprit Bumrah, Rohit Sharma, Suryakumar Yadav, Heinrich Klaasen, Shubman Gill, Rishabh Pant, and Sanju Samson** command locked multi-year franchise retention contracts at top purse brackets (₹18–25+ Cr) or Right-To-Match (RTM) guarantees. **It is statistically and commercially impossible for these players to enter the open auction pool for Rajasthan Royals in IPL 2027.** Recommending them wastes analytical bandwidth and provides zero actionable recruitment value.

### 1.2 Exclusion of Legally Ineligible Nationals
By BCCI regulatory policy and IPL governance protocols, Pakistani cricketers (e.g., Babar Azam, Mohammad Rizwan, Shaheen Afridi) are barred from registering for the IPL auction. All Pakistani players have been strictly removed to preserve legal compliance.

### 1.3 Exclusion of Top-Order Openers (Batting Positions 1–3)
Rajasthan Royals have already solidified their long-term opening partnership in **Yashasvi Jaiswal and Vaibhav Sooryavanshi**. Allocating auction purse to top-order anchors would cause roster redundancy. Our batting evaluation strictly isolates **Middle-Order Enforcers & Death Finishers (Positions 4, 5, 6, 7)**.

### 1.4 Exclusion of Powerplay Opening Bowlers (>25% PP Overs)
RR's new-ball seam attack is already anchored by Jofra Archer, Sandeep Sharma, and Nandre Burger. The war room's urgent tactical requirement is **Middle-Overs Spin Squeeze (Overs 7–15)** and **Death-Overs Yorker Lockdown (Overs 16–20)**. Bowlers bowling over 25% of their deliveries in the powerplay were filtered out.

---

## 2. In-Depth Empirical Data Breakdown Across 200,999 Deliveries

Across 883 matches (371 IPL matches and 512 International T20Is) from 2022 to 2026, empirical scoring baselines differ dramatically by match phase and resource depletion:

| Match Phase | Delivery Range | Empirical Run Rate (RPO) | Expected Wickets per Ball | Scoring Dynamic |
|:---|:---:|:---:|:---:|:---|
| **Powerplay** | Overs 1–6 | **8.02 RPO** | 0.048 | Fielding restrictions; horizontal boundary exploration |
| **Early Middle** | Overs 7–10 | **7.45 RPO** | 0.049 | Spin consolidation and strike rotation |
| **Late Middle** | Overs 11–15 | **8.04 RPO** | 0.054 | Acceleration phase against boundary sweepers |
| **Early Death** | Overs 16–18 | **9.92 RPO** | 0.071 | Death-overs launch; boundary maximization |
| **Extreme Death** | Overs 19–20 | **11.49 RPO** | 0.089 | Maximum boundary risk; yorker vs swing execution |

### Pre-Delivery Pressure Score Formulation
Every delivery receives a continuous Pressure Score ($PS \in [0, 100]$):
- **Chasing (2nd Innings):**
  $$PS = 35 \cdot S_{RRR} + 30 \cdot S_{Wickets} + 20 \cdot S_{Urgency} + 15 \cdot L_t$$
  where $L_t = 4 \cdot WP \cdot (1 - WP)$ is the Win Probability Leverage Index (peaking on 50-50 matches and approaching zero in blowout contests).
- **Target Setting (1st Innings):**
  $$PS = (40 \cdot S_{Phase} + 35 \cdot S_{Collapse} + 25 \cdot S_{Deficit}) \cdot \text{Stakes}$$
Deliveries with $PS \ge 42.26$ (the exact 80th percentile / P80 cutoff) are classified as **High Pressure**, isolating the top 20.0% highest-leverage deliveries (40,200 balls).

---

## 3. Top 10 Batters Under Pressure: Clutch Batting Index (CBI)

**Target Role:** Middle-Order Power Anchors & Death Finishers (Positions 4, 5, 6, 7).  
*Metrics:* 30% HP Strike Rate, 25% Runs Above Expected (xRA/100), 20% Delta Strike Rate, 15% Boundary Rate, 10% Match Consistency Rate (CCR).

| Rank | Player Name | CBI | HP Balls | HP SR | Base SR | ΔSR | Dot% | Boundary% | Phase | Tactical Role & War Room Fit | Team |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---:|
"""

for b in batters:
    clean_role = b['role'].split('—')[0].strip() if '—' in b['role'] else b['role']
    md_content += f"| **{b['rank']}** | **{b['name']}** | **{b['cbi']:.1f}** | {b['balls']} | {b['sr_raw']:.1f} | {b['base_sr']:.1f} | **+{b['delta_sr']:.1f}** | {b['dot_adj']:.1f}% | {b['bound_adj']:.1f}% | {b['best_phase']} | {clean_role} | {b['team']} |\n"

md_content += """
---

## 4. Top 10 Bowlers Under Pressure: Pressure Bowling Index (PBI)

**Target Role:** Middle-Overs Squeeze (Overs 7–15) & Death-Overs Execution (Overs 16–20).  
*Metrics:* 30% Runs Prevented vs State (xRP/over), 25% Economy Suppression, 20% Wicket Production, 15% Delta Economy, 10% Spell Consistency.

| Rank | Player Name | PBI | HP Balls | Wkts | HP Econ | Base Econ | ΔEcon | Dot% | Phase | Tactical Role & War Room Fit | Team |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---:|
"""

for bw in bowlers:
    clean_role = bw['role'].split('—')[0].strip() if '—' in bw['role'] else bw['role']
    md_content += f"| **{bw['rank']}** | **{bw['name']}** | **{bw['pbi']:.1f}** | {bw['balls']} | **{bw['wkts']}** | **{bw['econ_raw']:.2f}** | {bw['base_econ']:.2f} | **{'+' if bw['delta_econ']>=0 else ''}{bw['delta_econ']:.2f}** | {bw['dot_adj']:.1f}% | {bw['best_phase']} | {clean_role} | {bw['team']} |\n"

md_content += """
---

## 5. Rajasthan Royals War Room Strategy: IPL 2027 Auction Blueprint

### Tactical Gaps Solved at Sawai Mansingh Stadium (Jaipur)
The Sawai Mansingh Stadium features long 80-meter square boundaries and true bounce. Navigating death chases and defending totals at Jaipur requires specialized lower-order execution:

1. **The Domestic Death Destroyer: Ashutosh Sharma (Rank 1 Batter)**  
   *Why RR Must Bid:* Across 233 high-pressure deliveries, Ashutosh accelerates to 183.7 HP SR (+46.1 ΔSR) with +55.8 Runs Above Expected per 100 balls. He directly solves RR's historic #6/7 scoring dip after the middle-order foundation.
2. **High-Upside Indian Spin Hitters: Sameer Rizvi & Shubham Dubey**  
   *Why RR Must Bid:* Uncapped domestic power hitters with 80.0% and 71.4% match consistency. Their entry at #4/5 disrupts opposition spin strangulation in overs 11–15.
3. **155+ kmph Death Execution: Umran Malik & Matheesha Pathirana**  
   *Why RR Must Bid:* Umran Malik's raw pace suppresses high-pressure economy to 7.57 RPO (+1.71 ΔEcon). Pathirana's slingy yorker trajectory (41 HP wickets) locks down overs 18–20 alongside Jofra Archer.
4. **Middle-Overs Spin Squeeze: Gudakesh Motie, Washington Sundar & Mitchell Santner**  
   *Why RR Must Bid:* These finger-spin artists prevent scoring (+0.68 to +0.94 runs prevented per over) on large Jaipur boundaries while maintaining match consistency above 75%.
"""

with open('CLUTCH_X_METHODOLOGY_REPORT.md', 'w', encoding='utf-8') as f:
    f.write(md_content)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(md_content)

print("Successfully updated CLUTCH_X_METHODOLOGY_REPORT.md and README.md!")
