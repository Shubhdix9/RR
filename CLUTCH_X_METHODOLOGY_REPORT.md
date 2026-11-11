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
| **1** | **Ashutosh Sharma** | **57.9** | 251 | 184.9 | 117.7 | **+55.7** | 26.3% | 26.3% | DEATH | Domestic Death Destroyer — Pure #6/7 Clutch Weapon | PBKS |
| **2** | **Rovman Powell** | **57.2** | 524 | 173.9 | 133.0 | **+37.0** | 23.9% | 23.9% | DEATH | West Indian Death Finisher — #5/6 Power Machine | WI |
| **3** | **Sikandar Raza** | **56.8** | 222 | 185.6 | 121.3 | **+52.6** | 24.3% | 24.3% | DEATH | Zimbabwe All-Round Clutch Specialist — #4/5 | ZIM |
| **4** | **David Miller** | **56.1** | 517 | 171.8 | 134.0 | **+34.4** | 23.4% | 23.4% | DEATH | South African Chaser & Death Finisher — #5/6 | GT/SA |
| **5** | **Tim David** | **55.9** | 453 | 184.5 | 167.0 | **+8.4** | 27.2% | 27.2% | DEATH | Singapore Death Boundary Maximizer — Pure #6 | MI/SIN |
| **6** | **Mohammad Nabi** | **54.4** | 222 | 165.3 | 117.0 | **+44.6** | 21.3% | 21.3% | MIDDLE | Afghan Spin-Hitter & Clutch #5/6 Finisher | AFG |
| **7** | **Sameer Rizvi** | **53.7** | 87 | 197.7 | 122.3 | **+48.3** | 28.7% | 28.7% | DEATH | Uncapped Domestic Sensation — #4/5 (Domestic Gem) | CSK |
| **8** | **Tristan Stubbs** | **53.3** | 425 | 167.1 | 138.0 | **+25.2** | 22.8% | 22.8% | DEATH | South African 360° Finisher & Spin Smasher — #5/6 | DC/SA |
| **9** | **Jitesh Sharma** | **52.7** | 252 | 175.0 | 147.4 | **+21.3** | 24.2% | 24.2% | DEATH | Indian WK-Batter & Power Finisher — #5/6 | PBKS |
| **10** | **Shubham Dubey** | **52.7** | 93 | 183.9 | 116.0 | **+52.7** | 25.8% | 25.8% | DEATH | Uncapped Domestic Rising Star — #6/7 (Domestic Gem) | RCB |

---

## 3. Top 10 Realistic Bowlers: Pressure Bowling Index (PBI)

**Target Role:** Middle-Overs Squeeze (Overs 7–15) & Death-Overs Execution (Overs 16–20).  
*Filter Rules:* Legally IPL eligible, not retained top franchise face/captain, <25% Powerplay overs.

| Rank | Player Name | PBI | HP Balls | Wkts | HP Econ | Base Econ | ΔEcon | HP Dot% | Phase | Tactical Role & War Room Fit | Team |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---:|
| **1** | **Yuzvendra Chahal** | **62.8** | 495 | **51** | **8.81** | 8.38 | **-0.40** | **35.2%** | MIDDLE | Leg-Spin Wicket Machine — 51 HP wkts in 495 HP balls (94% Mid/Death) | RR/SRH |
| **2** | **Umran Malik** | **57.6** | 145 | **12** | **7.47** | 5.75 | **+1.72** | **37.5%** | DEATH | Express Indian Pacer — 155+ kmph Death Specialist | SRH/GT |
| **3** | **Matheesha Pathirana** | **56.5** | 497 | **42** | **9.02** | 8.20 | **-0.82** | **35.8%** | DEATH | Slingy Yorker Executioner — 42 HP wickets (94% Mid/Death) | CSK |
| **4** | **Mitchell Santner** | **55.2** | 426 | **19** | **7.71** | 8.29 | **-0.58** | **38.0%** | MIDDLE | Left-Arm Spin Squeeze — Accurate Economy Choke | NZ/CSK |
| **5** | **Noor Ahmad** | **54.6** | 289 | **26** | **8.33** | 8.97 | **-0.64** | **36.3%** | MIDDLE | Left-Arm Chinaman Wicket Threat — 96% Mid/Death | AFG/GT |
| **6** | **Adil Rashid** | **53.5** | 348 | **22** | **8.09** | 8.41 | **-0.32** | **35.7%** | MIDDLE | Leg-Break Middle-Overs Squeeze Artist | ENG |
| **7** | **Sikandar Raza** | **53.3** | 148 | **10** | **6.73** | 7.09 | **-0.15** | **37.8%** | MIDDLE | Dual-Role Clutch All-Rounder — Tight Off-Spin Squeeze | ZIM |
| **8** | **Gudakesh Motie** | **53.3** | 183 | **11** | **7.22** | 6.58 | **+0.64** | **38.5%** | MIDDLE | Left-Arm Orthodox Economy Squeeze (8% PP, 92% Mid/Death) | WI |
| **9** | **Wanindu Hasaranga** | **52.9** | 496 | **37** | **8.96** | 10.16 | **-1.20** | **34.4%** | MIDDLE | Leg-Spin Wicket Machine — 37 HP Wkts (93% Mid/Death) | SRH/SL |
| **10** | **Karn Sharma** | **50.1** | 180 | **9** | **8.69** | 7.21 | **+1.48** | **36.1%** | MIDDLE | Leg-Spin Squeeze — Improves Under Pressure | MI/SRH |

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
