# Rajasthan Royals War Room Player Evaluation & Auction Strategy
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
  $$PS = (40 \cdot S_{Phase} + 35 \cdot S_{Collapse} + 25 \cdot S_{Deficit}) \cdot 	ext{Stakes}$$
Deliveries with $PS \ge 42.26$ (the exact 80th percentile / P80 cutoff) are classified as **High Pressure**, isolating the top 20.0% highest-leverage deliveries (40,200 balls).

---

## 3. Top 10 Batters Under Pressure: Clutch Batting Index (CBI)

**Target Role:** Middle-Order Power Anchors & Death Finishers (Positions 4, 5, 6, 7).  
*Metrics:* 30% HP Strike Rate, 25% Runs Above Expected (xRA/100), 20% Delta Strike Rate, 15% Boundary Rate, 10% Match Consistency Rate (CCR).

| Rank | Player Name | CBI | HP Balls | HP SR | Base SR | ΔSR | Dot% | Boundary% | Phase | Tactical Role & War Room Fit | Team |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---:|
| **1** | **Ashutosh Sharma** | **85.7** | 233 | 183.7 | 137.6 | **+46.1** | 25.3% | 26.2% | DEATH | Domestic Death Destroyer | PBKS |
| **2** | **Sameer Rizvi** | **86.7** | 85 | 184.7 | 146.1 | **+38.6** | 24.7% | 27.1% | DEATH | Uncapped Indian Spin Smasher | CSK |
| **3** | **Shubham Dubey** | **85.2** | 90 | 180.0 | 133.1 | **+46.9** | 25.6% | 25.6% | DEATH | Uncapped Domestic Power Gem | RR/RCB |
| **4** | **Donovan Ferreira** | **85.0** | 111 | 188.3 | 163.9 | **+24.4** | 26.1% | 27.9% | DEATH | Explosive 360° Finisher & Backup WK | RR |
| **5** | **Sikandar Raza** | **84.2** | 223 | 178.9 | 131.2 | **+47.7** | 24.2% | 24.7% | DEATH | Dual-Threat Clutch All-Rounder | PBKS/ZIM |
| **6** | **Liam Livingstone** | **82.1** | 237 | 176.4 | 152.8 | **+23.6** | 26.6% | 25.3% | DEATH | Middle-Overs Power Enforcer | PBKS/ENG |
| **7** | **Mark Chapman** | **82.2** | 137 | 178.8 | 148.8 | **+30.0** | 24.8% | 24.1% | MIDDLE | High-Efficiency Middle Spin Destroyer | NZ |
| **8** | **Tim David** | **81.0** | 423 | 187.5 | 175.3 | **+12.2** | 27.9% | 27.2% | DEATH | High-Volume Death Boundary Maximizer | MI |
| **9** | **Rovman Powell** | **79.4** | 513 | 166.9 | 139.2 | **+27.7** | 24.0% | 23.8% | DEATH | Proven Match-Winning Finisher | RR/WI |
| **10** | **Shashank Singh** | **79.1** | 277 | 173.3 | 152.3 | **+21.0** | 24.2% | 25.6% | DEATH | Domestic Clutch Sensation | PBKS |

---

## 4. Top 10 Bowlers Under Pressure: Pressure Bowling Index (PBI)

**Target Role:** Middle-Overs Squeeze (Overs 7–15) & Death-Overs Execution (Overs 16–20).  
*Metrics:* 30% Runs Prevented vs State (xRP/over), 25% Economy Suppression, 20% Wicket Production, 15% Delta Economy, 10% Spell Consistency.

| Rank | Player Name | PBI | HP Balls | Wkts | HP Econ | Base Econ | ΔEcon | Dot% | Phase | Tactical Role & War Room Fit | Team |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---:|
| **1** | **Umran Malik** | **61.6** | 132 | **16** | **7.57** | 9.28 | **+1.71** | 38.2% | DEATH | 155+ kmph Express Death Bowler | SRH/GT |
| **2** | **Gudakesh Motie** | **55.4** | 168 | **11** | **7.50** | 7.86 | **+0.36** | 38.5% | MIDDLE | Left-Arm Orthodox Squeeze | WI |
| **3** | **Washington Sundar** | **55.4** | 181 | **11** | **7.62** | 7.90 | **+0.28** | 38.7% | MIDDLE | Finger Spin Precision Choke | SRH/IND |
| **4** | **Mitchell Santner** | **54.3** | 426 | **22** | **7.58** | 7.16 | **-0.42** | 38.0% | MIDDLE | World-Class Middle Spin Squeeze | CSK/NZ |
| **5** | **Yuzvendra Chahal** | **54.2** | 495 | **50** | **8.73** | 8.41 | **-0.32** | 35.4% | MIDDLE | King of High-Pressure Wickets | RR/SRH |
| **6** | **Sikandar Raza** | **53.9** | 144 | **8** | **7.12** | 6.59 | **-0.53** | 37.8% | MIDDLE | Dual-Role Finger Spin Lockdown | PBKS/ZIM |
| **7** | **Krunal Pandya** | **51.9** | 234 | **17** | **7.85** | 7.59 | **-0.26** | 37.2% | MIDDLE | Middle-Overs Defensive Squeeze | LSG |
| **8** | **Harpreet Brar** | **50.7** | 133 | **9** | **7.64** | 7.85 | **+0.21** | 37.6% | MIDDLE | High-Trajectory Left-Arm Squeeze | PBKS |
| **9** | **Matheesha Pathirana** | **50.5** | 431 | **41** | **9.48** | 8.66 | **-0.82** | 35.8% | DEATH | Slingy Yorker Death Executioner | CSK |
| **10** | **Noor Ahmad** | **49.8** | 386 | **26** | **8.64** | 8.00 | **-0.64** | 36.5% | MIDDLE | Young Left-Arm Wrist Spin Weapon | GT/CSK |

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
