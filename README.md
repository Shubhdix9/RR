# CLUTCH-X v2.0 (War Room Edition)
## Advanced Expected-Value Modeling, Pressure Quantification & Rajasthan Royals IPL 2027 Auction Strategy
**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1  
**Submission Category:** Predictive Analytics & War Room Auction Strategy  
**Dataset Analyzed:** Proprietary Rajasthan Royals Ball-by-Ball Records (2022–2026), 200,999 Deliveries, 883 Matches  
**Live Dashboard:** [https://shubhdix9.github.io/RR/](https://shubhdix9.github.io/RR/)  
**GitHub Repository:** [https://github.com/Shubhdix9/RR](https://github.com/Shubhdix9/RR)  

---

## Executive Summary: How Modern IPL War Rooms Actually Scout

Cricket analytics often fails when franchises rely solely on traditional counting stats (Runs, Average, Overall Strike Rate). A batter scoring 60 off 40 balls in a dead rubber chasing 220 when the match is effectively over generates vanity volume but near-zero franchise win-probability equity.

To win the **SupeRR Selector Season 2**, an IPL war-room submission must solve three foundational challenges:
1. **Define Pre-Delivery Pressure Without Outcome Leakage:** Quantify match stress using only the continuous state of the game *before* each ball is bowled (Wickets in hand, Balls Remaining, Required Run Rate vs. Dynamic Par, Innings Leverage, and Playoff Stakes).
2. **Context-Adjusted Expected Value:** Measure performance against state-specific baseline expectations across match buckets, isolating true execution under stress from routine accumulation.
3. **Realistic Franchise Auction Economics & Role Specificity:** Filter out legally ineligible players (Pakistani nationals barred from the IPL), untouchable retained mega-stars (Kohli, Rohit, Bumrah, SKY, Pant, Iyer, Gill, Klaasen), **openers/top-order batters** (where RR is already locked with Yashasvi Jaiswal and Vaibhav Sooryavanshi), and **new-ball powerplay pacers** (where RR already deploys Jofra Archer, Sandeep Sharma, and Nandre Burger). 

Instead, the **CLUTCH-X Engine** targets **pure middle-order/death finishers (#4–7)** and **middle-overs squeeze / death-overs executioners (Overs 7–20)**.

### The Final 20 Selected Players for Unstop Dropdowns

| Rank | Top 10 Batters (CBI) | CBI | Tactical Role | Top 10 Bowlers (PBI) | PBI | Tactical Role |
|:---:|:---|:---:|:---|:---|:---:|:---|
| **1** | Ashutosh Sharma | 57.9 | Domestic Death Destroyer (#6/7) | Yuzvendra Chahal | 62.8 | King of Middle Wickets (51 HP Wkts) |
| **2** | Rovman Powell | 57.2 | Boundary Enforcer & Finisher (#5/6) | Umran Malik | 57.6 | 155+ kmph Express Death Pacer |
| **3** | Sikandar Raza | 56.8 | Clutch All-Rounder (#4/5) | Matheesha Pathirana | 56.5 | Slingy Yorker Death Specialist (42 Wkts) |
| **4** | David Miller | 56.1 | Proven Chase Finisher (#5/6) | Mitchell Santner | 55.2 | Left-Arm Spin Economy Squeeze |
| **5** | Tim David | 55.9 | Death Boundary Maximizer (#6) | Noor Ahmad | 54.6 | Left-Arm Wrist Spin Weapon (26 Wkts) |
| **6** | Mohammad Nabi | 54.4 | Spin Hitter & Death Finisher (#5/6) | Adil Rashid | 53.5 | Leg-Break Middle Squeeze |
| **7** | Sameer Rizvi | 53.7 | Uncapped Spin Destroyer (#4/5) | Sikandar Raza | 53.3 | Dual-Role Tight Off-Spin Squeeze |
| **8** | Tristan Stubbs | 53.3 | 360° Finisher & Spin Smasher (#5/6) | Gudakesh Motie | 53.3 | Left-Arm Orthodox Squeeze |
| **9** | Jitesh Sharma | 52.7 | Indian WK Power Finisher (#5/6) | Wanindu Hasaranga | 52.9 | Middle Leg-Spin Weapon (37 Wkts) |
| **10** | Shubham Dubey | 52.7 | Uncapped Domestic Power Gem (#6/7) | Karn Sharma | 50.1 | Leg-Spin Squeeze Under Pressure |

---

## 1. Advanced Machine Learning Framework: Expected Value & Leverage Index

### Mathematical Definitions

#### 1. Win Probability & Leverage Index ($L_t$)
Following win-probability modeling adapted for 20-over cricket:
$$WP_t = \sigma\left(\beta_0 + \beta_1 \cdot RRR_t + \beta_2 \cdot WktsLost_t + \beta_3 \cdot BallsRemaining_t\right)$$
$$L_t = 4 \cdot WP_t \cdot (1 - WP_t)$$
$L_t \in [0, 1]$ peaks when $WP = 0.50$ (50-50 contest) and approaches zero when a match is decided.

#### 2. Pre-Delivery Pressure Score ($PS \in [0, 100]$)
For chases (2nd Innings):
$$PS_t = 35 \cdot \text{clip}\left(\frac{RRR_t - 6.0}{12.0}, 0, 1\right) + 30 \cdot \frac{WktsLost_t}{10} + 20 \cdot \frac{120 - BallsLeft_t}{120} + 15 \cdot L_t$$
For target-setting (1st Innings):
$$PS_t = (40 \cdot S_{phase} + 35 \cdot S_{collapse} + 25 \cdot S_{deficit}) \cdot \text{Stakes}$$
Deliveries with $PS \ge 42.26$ (80th percentile / P80 cutoff) are classified as **High Pressure (HP)**, isolating exactly 20.0% of all deliveries.

#### 3. Empirical Bayes Shrinkage
To eliminate sample size noise:
$$\theta_{EB} = \frac{N}{N + K} \cdot \bar{X}_{sample} + \frac{K}{N + K} \cdot \mu_{prior}$$
with prior confidence weight $K = 60$ balls.

---

## 2. Top 10 Realistic Batters: Clutch Batting Index (CBI)

**Target Role:** Middle-Order Power Anchors & Death Finishers (Positions 4, 5, 6, 7).  
*Filter Rules:* Legally IPL eligible, not retained top franchise face/captain, position 4+ execution.

| Rank | Player Name | CBI | HP Balls | HP SR | Base SR | ΔSR | HP Dot% | HP Bnd% | Phase | Tactical Role & War Room Fit | Team |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---:|
| **1** | **Ashutosh Sharma** | **85.7** | 233 | 183.7 | 137.6 | **+46.1** | 25.3% | 26.2% | DEATH | Domestic Death Destroyer — Pure #6/7 Clutch Gem (+55.8 xRA/100) | PBKS |
| **2** | **Sameer Rizvi** | **86.7** | 85 | 184.7 | 146.1 | **+38.6** | 24.7% | 27.1% | DEATH | Uncapped Indian Spin Smasher — High Upside #4/5 (80% Consistency) | CSK |
| **3** | **Shubham Dubey** | **85.2** | 90 | 180.0 | 133.1 | **+46.9** | 25.6% | 25.6% | DEATH | Uncapped Domestic Power Gem — #6/7 Left-Hand Finisher | RR/RCB |
| **4** | **Donovan Ferreira** | **85.0** | 111 | 188.3 | 163.9 | **+24.4** | 26.1% | 27.9% | DEATH | Explosive 360° Finisher & Backup WK — 83.3% Match Consistency | RR |
| **5** | **Sikandar Raza** | **84.2** | 223 | 178.9 | 131.2 | **+47.7** | 24.2% | 24.7% | DEATH | Dual-Threat Clutch All-Rounder — Crisis Recovery #5/6 Anchor | PBKS/ZIM |
| **6** | **Liam Livingstone** | **82.1** | 237 | 176.4 | 152.8 | **+23.6** | 26.6% | 25.3% | DEATH | Middle-Overs Power Enforcer — 81.2% Match Consistency | PBKS/ENG |
| **7** | **Mark Chapman** | **82.2** | 137 | 178.8 | 148.8 | **+30.0** | 24.8% | 24.1% | MIDDLE | High-Efficiency Middle Spin Destroyer — #4/5 Left-Hand Anchor | NZ |
| **8** | **Tim David** | **81.0** | 423 | 187.5 | 175.3 | **+12.2** | 27.9% | 27.2% | DEATH | High-Volume Death Boundary Maximizer — Pure #6 Finisher | MI |
| **9** | **Rovman Powell** | **79.4** | 513 | 166.9 | 139.2 | **+27.7** | 24.0% | 23.8% | DEATH | Proven Match-Winning Finisher — 513 HP Deliveries Tested | RR/WI |
| **10** | **Shashank Singh** | **79.1** | 277 | 173.3 | 152.3 | **+21.0** | 24.2% | 25.6% | DEATH | Domestic Clutch Sensation — Reliable Lower-Order Hitter (#6/7) | PBKS |

---

## 3. Top 10 Realistic Bowlers: Pressure Bowling Index (PBI)

**Target Role:** Middle-Overs Squeeze (Overs 7–15) & Death-Overs Execution (Overs 16–20).  
*Filter Rules:* Legally IPL eligible, not retained top franchise face/captain, <25% Powerplay overs.

| Rank | Player Name | PBI | HP Balls | Wkts | HP Econ | Base Econ | ΔEcon | HP Dot% | Phase | Tactical Role & War Room Fit | Team |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---:|
| **1** | **Umran Malik** | **61.6** | 132 | **16** | **7.57** | 9.28 | **+1.71** | **38.2%** | DEATH | 155+ kmph Express Death Bowler — +1.71 Economy Suppression Under Pressure | SRH/GT |
| **2** | **Gudakesh Motie** | **55.4** | 168 | **11** | **7.50** | 7.86 | **+0.36** | **38.5%** | MIDDLE | Left-Arm Orthodox Squeeze — 80.0% Match Consistency (92% Mid/Death) | WI |
| **3** | **Washington Sundar** | **55.4** | 181 | **11** | **7.62** | 7.90 | **+0.28** | **38.7%** | MIDDLE | Finger Spin Precision Choke — +0.94 Runs Prevented per Over vs State | SRH/IND |
| **4** | **Mitchell Santner** | **54.3** | 426 | **22** | **7.58** | 7.16 | **-0.42** | **38.0%** | MIDDLE | World-Class Middle Spin Squeeze — 75.9% Match Consistency | CSK/NZ |
| **5** | **Yuzvendra Chahal** | **54.2** | 495 | **50** | **8.73** | 8.41 | **-0.32** | **35.4%** | MIDDLE | King of High-Pressure Wickets — 50 HP Wickets in 495 Deliveries | RR/SRH |
| **6** | **Sikandar Raza** | **53.9** | 144 | **8** | **7.12** | 6.59 | **-0.53** | **37.8%** | MIDDLE | Dual-Role Finger Spin Lockdown — 84.6% Match Consistency (+0.82 xRP/ov) | PBKS/ZIM |
| **7** | **Krunal Pandya** | **51.9** | 234 | **17** | **7.85** | 7.59 | **-0.26** | **37.2%** | MIDDLE | Middle-Overs Defensive Squeeze — +0.51 Runs Prevented per Over | LSG |
| **8** | **Harpreet Brar** | **50.7** | 133 | **9** | **7.64** | 7.85 | **+0.21** | **37.6%** | MIDDLE | High-Trajectory Left-Arm Squeeze — +0.21 Economy Suppression | PBKS |
| **9** | **Matheesha Pathirana** | **50.5** | 431 | **41** | **9.48** | 8.66 | **-0.82** | **35.8%** | DEATH | Slingy Yorker Death Executioner — 41 HP Wickets (94% Mid/Death) | CSK |
| **10** | **Noor Ahmad** | **49.8** | 386 | **26** | **8.64** | 8.00 | **-0.64** | **36.5%** | MIDDLE | Young Left-Arm Wrist Spin Weapon — 26 HP Wickets (96% Mid/Death) | GT/CSK |

---

## 4. Rajasthan Royals War Room Strategy: IPL 2027 Auction Blueprint

### Squad Context & Tactical Gaps at Sawai Mansingh Stadium (Jaipur)

The Rajasthan Royals enter IPL 2027 planning with a clear structural framework:
- **Top Order:** Yashasvi Jaiswal & Vaibhav Sooryavanshi (Openers locked).
- **Core Leaders:** Sanju Samson, Riyan Parag, Dhruv Jurel.
- **Pace Foundation:** Jofra Archer, Sandeep Sharma, Nandre Burger.

#### The 4 Critical Gaps Solved:
1. **The Domestic Scouting Masterstroke: Ashutosh Sharma (Rank 1 Batter)**  
   *Why RR Must Bid:* Across 251 high-pressure balls, Ashutosh accelerates to 184.9 HP SR (+55.7 ΔSR) with a 26.3% boundary rate. He solves RR's historic #6/7 late-overs scoring drop-off.
2. **Dual-Threat Overseas Power: Rovman Powell & Sikandar Raza**  
   *Why RR Must Bid:* Proven match-winners who do not eat top-order overs. Raza provides simultaneous top-tier spin economy (6.73 HP Econ) and batting violence (185.6 HP SR).
3. **Middle-Overs Spin Lockdown: Yuzvendra Chahal & Noor Ahmad**  
   *Why RR Must Bid:* Chahal dominates high-leverage situations with 51 HP wickets in 495 pressure balls. Paired with Noor Ahmad's left-arm wrist spin, RR creates an unbreachable middle-overs squeeze.
4. **Extreme Pace & Death Yorker Execution: Umran Malik & Matheesha Pathirana**  
   *Why RR Must Bid:* Complements Archer at the death. Malik's 155+ kmph pace drops to 7.47 HP Econ under pressure, while Pathirana's slingy yorker trajectory (42 HP wkts) locks down overs 18–20.

---

## 5. Official Submission Checklist for Unstop

- [x] **Top 10 Batsmen Dropdowns Selected:** Ashutosh Sharma, Rovman Powell, Sikandar Raza, David Miller, Tim David, Mohammad Nabi, Sameer Rizvi, Tristan Stubbs, Jitesh Sharma, Shubham Dubey.
- [x] **Top 10 Bowlers Dropdowns Selected:** Yuzvendra Chahal, Umran Malik, Matheesha Pathirana, Mitchell Santner, Noor Ahmad, Adil Rashid, Sikandar Raza, Gudakesh Motie, Wanindu Hasaranga, Karn Sharma.
- [x] **Methodology Report Uploaded:** `RR_WAR_ROOM_REPORT.pdf` generated from `RR_WAR_ROOM_REPORT.html` via Save as PDF.
- [x] **Dashboard Link Shared:** `https://shubhdix9.github.io/RR/`
- [x] **Share Your Journey (Under 500 Chars):** Prepared and validated.
