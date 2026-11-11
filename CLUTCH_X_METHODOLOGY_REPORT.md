# CLUTCH-X v2.0 (War Room Edition)
## Advanced Expected-Value Modeling, Pressure Quantification & Rajasthan Royals IPL 2027 Auction Strategy
**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1  
**Submission Category:** Predictive Analytics & War Room Auction Strategy  
**Dataset Analyzed:** Proprietary Rajasthan Royals Ball-by-Ball Records (2022–2026), 200,999 Deliveries, 883 Matches  

---

## Executive Summary: How Modern IPL War Rooms Actually Scout

Cricket analytics often fails when franchises rely solely on traditional counting stats (Runs, Average, Overall Strike Rate). A batter scoring 60 off 40 balls in a dead rubber chasing 220 when the match is effectively over generates vanity volume but near-zero franchise win-probability equity.

To win the **SupeRR Selector Season 2**, an IPL war-room submission must solve three foundational challenges:
1. **Define Pre-Delivery Pressure Without Outcome Leakage:** Quantify match stress using only the continuous state of the game *before* each ball is bowled (Wickets in hand, Balls Remaining, Required Run Rate vs. Dynamic Par, Innings Leverage, and Playoff Stakes).
2. **Context-Adjusted Expected Value (Runs Above Expected & Prevented):** Measure performance against state-specific baseline expectations ($\mathbb{E}[Runs|State]$, $\mathbb{E}[Wkt|State]$) across 42 discrete match buckets, isolating true execution under stress from pitch inflation.
3. **Realistic Franchise Auction Economics & Role Specificity:** Filter out legally ineligible players (e.g. Pakistani nationals barred from the IPL), untouchable retained mega-stars (Kohli, Rohit, Bumrah, SKY, Pant, Iyer, Gill, Klaasen), **openers/top-order batters** (where RR is already locked with Yashasvi Jaiswal and Vaibhav Sooryavanshi), and **new-ball powerplay pacers** (where RR already deploys Jofra Archer, Sandeep Sharma, and Nandre Burger). 

Instead, the **CLUTCH-X Engine** targets **pure middle-order/death finishers (#4–7)** and **middle-overs squeeze / death-overs executioners (Overs 7–20)**.

### The Final 20 Selected Players for Unstop Dropdowns

| Rank | Top 10 Batters (CBI) | CBI | Tactical Role | Top 10 Bowlers (PBI) | PBI | Tactical Role |
|:---:|:---|:---:|:---|:---|:---:|:---|
| **1** | Glenn Maxwell | 92.4 | Middle Spin Destroyer / #4-5 | Vipraj Nigam (Domestic Gem) | 87.7 | Uncapped Wrist-Spin Squeeze |
| **2** | Shashank Singh | 84.4 | Domestic Clutch Finisher / #6-7 | Noor Ahmad | 87.1 | Left-Arm Wrist Spin Wickets |
| **3** | Romario Shepherd | 84.0 | Pace All-Rounder & Finisher / #7 | Matheesha Pathirana | 85.0 | Slingy Yorker Death Specialist |
| **4** | Marcus Stoinis | 83.6 | Heavy-Ball Finisher / #5-6 | Kartik Tyagi | 82.2 | Express Indian Death Pacer |
| **5** | Abdul Samad | 82.3 | Domestic Death Striker / #6-7 | Qais Ahmad | 79.5 | Attacking Wrist-Spin Squeeze |
| **6** | Tim David | 82.2 | Pure Death Boundary Maximizer | Moeen Ali | 77.1 | Off-Spin Middle-Overs Squeeze |
| **7** | Liam Livingstone | 81.6 | Middle Power Enforcer / #4-5 | Wanindu Hasaranga | 74.8 | Leg-Spin Wicket Machine |
| **8** | Najibullah Zadran | 81.5 | Spin Destroyer & Finisher / #5-6 | Chamika Karunaratne | 73.7 | Seam Change-Up & Death |
| **9** | Donovan Ferreira | 81.3 | Explosive Finisher / WK / #6-7 | Harshal Patel | 73.6 | Death Dipping Slower Balls |
| **10** | Tristan Stubbs | 76.1 | 360° Finisher & Spin Smasher | Krunal Pandya | 73.5 | Left-Arm Defensive Squeeze |

> **The Next Vignesh Puthur:** In Bowlers Rank 1, our model unearths uncapped Indian leg-spinner **Vipraj Nigam** (Delhi Capitals in dataset). Nigam's regular baseline economy of 9.29 drops to an astonishing **5.64 RPO under pressure (+3.65 economy suppression)** with a **39.9% dot-ball rate**, representing a low-cost, high-upside steal ideally suited to the massive 80m+ boundaries at the Sawai Mansingh Stadium (Jaipur).

---

## 1. Advanced Machine Learning Framework: Expected Value & Leverage Index

### Mathematical Definitions

#### 1. Win Probability & Leverage Index ($L_t$)
Following Tom Tango's win-probability framework adapted for 20-over cricket, every delivery possesses a swing potential:
$$WP_t = \sigma\left(eta_0 + eta_1 \cdot RRR_t + eta_2 \cdot WktsLost_t + eta_3 \cdot BallsRemaining_tight)$$
$$L_t = 4 \cdot WP_t \cdot (1 - WP_t)$$
$L_t \in [0, 1]$ peaks when $WP = 0.50$ (50-50 contest) and approaches zero when a match is already decided.

#### 2. Pre-Delivery Pressure Score ($PS \in [0, 100]$)
For chases (2nd Innings):
$$PS_t = 	ext{clip}\left(30 \cdot rac{RRR_t - 6.0}{6.0} + 35 \cdot e^{0.18 \cdot (WktsLost_t - 3)} + 20 \cdot rac{120 - BallsLeft_t}{120} + 15 \cdot L_t, 0, 100ight)$$
For target-setting (1st Innings):
$$PS_t = 	ext{clip}\left(40 \cdot S_{phase} + 30 \cdot S_{collapse} + 20 \cdot S_{deficit} + 10 \cdot 	ext{Stakes}, 0, 100ight)$$
Deliveries with $PS \ge 38.00$ (80th percentile) are classified as **High Pressure (HP)**.

#### 3. Runs Above Expected ($xRA$) & Runs Prevented ($xRP$)
For each of the 42 match states $S = (Phase, WktsLost, RunRateBracket)$:
$$xRA_i = RunsScored_i - \mathbb{E}[Runs | S_i]$$
$$xRP_i = \mathbb{E}[Runs | S_i] - RunsConceded_i$$

#### 4. Empirical Bayes Shrinkage
To avoid small-sample bias:
$$	heta_{EB} = rac{N}{N + K} \cdot ar{X}_{sample} + rac{K}{N + K} \cdot \mu_{prior}$$
with prior confidence weight $K = 60$ balls.

---

## 2. Top 10 Realistic Batters: Clutch Batting Index (CBI)

**Target Role:** Middle-Order Power Anchors & Death Finishers (Positions 4, 5, 6, 7).  
*Filter Rules:* Legally IPL eligible, not retained top franchise face/captain, position 4+ execution.

| Rank | Player Name | CBI | HP Balls | HP SR | Base SR | ΔSR | HP Dot% | HP Bnd% | Tactical Role & War Room Fit | Team |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---:|
| **1** | **Glenn Maxwell** | **92.4** | 183 | 212.0 | 161.0 | **+51.1** | 24.9% | 28.5% | Middle-Overs Game Changer (#4/5) | RCB |
| **2** | **Shashank Singh** | **84.4** | 193 | 186.5 | 161.6 | **+24.9** | 24.3% | 26.2% | Domestic Clutch Finisher Sensation (#6/7) | PBKS |
| **3** | **Romario Shepherd** | **84.0** | 247 | 191.1 | 154.1 | **+36.9** | 27.2% | 25.9% | Pace All-Rounder & Death Finisher (#7) | RCB |
| **4** | **Marcus Stoinis** | **83.6** | 359 | 181.6 | 153.6 | **+28.0** | 27.6% | 24.2% | Seam All-Rounder & Finisher (#5/6) | LSG |
| **5** | **Abdul Samad** | **82.3** | 164 | 185.4 | 149.8 | **+35.6** | 26.6% | 25.0% | Domestic Death Boundary Striker (#6/7) | LSG |
| **6** | **Tim David** | **82.2** | 448 | 200.9 | 177.7 | **+23.2** | 28.8% | 27.4% | Death Boundary Maximizer (#6) | MI |
| **7** | **Liam Livingstone** | **81.6** | 270 | 178.9 | 153.9 | **+25.0** | 26.5% | 24.8% | Middle-Overs Power Enforcer (#4/5) | PBKS |
| **8** | **Najibullah Zadran** | **81.5** | 94 | 176.6 | 138.6 | **+38.0** | 25.7% | 21.7% | Middle Spin Destroyer & Finisher (#5/6) | AFG |
| **9** | **Donovan Ferreira** | **81.3** | 152 | 187.5 | 163.8 | **+23.7** | 28.6% | 27.0% | Explosive Finisher / WK Utility (#6/7) | RR |
| **10** | **Tristan Stubbs** | **76.1** | 369 | 164.8 | 149.9 | **+14.9** | 23.7% | 23.4% | Dynamic 360° Finisher / Spin Smasher (#5/6) | DC |

### Analytical Highlights for Top Batters:
- **Glenn Maxwell (Rank 1):** Unbelievable acceleration under severe pressure (+51.1 ΔSR to 212.0 HP SR). Decimates spin through overs 7–15 and finishes at death.
- **Shashank Singh (Rank 2):** The breakout domestic clutch sensation. 100% middle/death innings with a 186.5 HP SR and microscopic 24.3% dot-ball rate.
- **Romario Shepherd (Rank 3):** Ideal #7 finisher and seam all-rounder. 191.1 HP SR (+36.9 ΔSR) with explosive boundary production (25.9%).
- **Marcus Stoinis (Rank 4):** Heavy ball hitter who anchors collapses and finishes at 181.6 HP SR.
- **Abdul Samad (Rank 5):** High-impact domestic death boundary striker (185.4 HP SR).

---

## 3. Top 10 Realistic Bowlers: Pressure Bowling Index (PBI)

**Target Role:** Middle-Overs Squeeze (Overs 7–15) & Death-Overs Execution (Overs 16–20).  
*Filter Rules:* Legally IPL eligible, not retained top franchise face/captain, <25% Powerplay overs.

| Rank | Player Name | PBI | HP Balls | Wkts | HP Econ | Base Econ | ΔEcon | HP Dot% | Tactical Role & War Room Fit | Team |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---:|
| **1** | **Vipraj Nigam** | **87.7** | 50 | 3 | **5.64** | 9.29 | **+3.65** | **39.9%** | Uncapped Indian Domestic Diamond (Jaipur Fit) | DC |
| **2** | **Noor Ahmad** | **87.1** | 258 | 23 | **7.16** | 7.61 | **+0.45** | **39.3%** | Left-Arm Wrist Spin Wicket Machine (96% Mid/Death) | GT |
| **3** | **Matheesha Pathirana** | **85.0** | 394 | 33 | **7.77** | 7.79 | **+0.02** | **35.2%** | Slingy Death Yorker Specialist (94% Mid/Death) | CSK |
| **4** | **Kartik Tyagi** | **82.2** | 107 | 10 | **8.47** | 9.79 | **+1.32** | **37.7%** | Express Indian Pacer / Death Specialist (Former RR) | GT/KKR |
| **5** | **Qais Ahmad** | **79.5** | 74 | 4 | **6.41** | 7.50 | **+1.09** | **35.7%** | Attacking Wrist-Spin Squeeze (100% Mid/Death) | AFG |
| **6** | **Moeen Ali** | **77.1** | 100 | 5 | **6.18** | 8.08 | **+1.90** | **38.0%** | Middle-Overs Off-Spin Squeeze (78% Mid/Death) | CSK |
| **7** | **Wanindu Hasaranga** | **74.8** | 390 | 31 | **7.77** | 7.87 | **+0.10** | **34.4%** | Middle-Overs Leg-Spin Weapon (93% Mid/Death) | SRH/RCB |
| **8** | **Chamika Karunaratne** | **73.7** | 56 | 4 | **7.61** | 8.41 | **+0.80** | **36.5%** | Seam Change-Up & Middle/Death Bowler | KKR |
| **9** | **Harshal Patel** | **73.6** | 470 | 44 | **8.66** | 8.77 | **+0.11** | **35.8%** | Death-Overs Slower Ball & Dip Master (90% Mid/Death) | PBKS |
| **10** | **Krunal Pandya** | **73.5** | 174 | 10 | **7.17** | 7.63 | **+0.46** | **37.2%** | Middle-Overs Defensive Squeeze (80% Mid/Death) | LSG |

### Analytical Highlights for Top Bowlers:
- **Vipraj Nigam (Rank 1):** The undiscovered domestic prodigy. Drops his economy by an unprecedented +3.65 runs to 5.64 in high pressure with a 39.9% dot-ball rate. 
- **Noor Ahmad (Rank 2):** 258 pressure balls, 23 wickets, 7.16 HP Econ. Elite left-arm wrist spin squeeze through overs 7–15.
- **Matheesha Pathirana (Rank 3):** The premier death-overs weapon. 33 pressure wickets and 7.77 HP Econ with an unhittable slingy yorker trajectory.
- **Kartik Tyagi (Rank 4):** Former RR pacer with 145+ kmph express pace and reverse swing at the death (8.47 HP Econ, +1.32 ΔEcon).
- **Qais Ahmad & Moeen Ali (Ranks 5–6):** Masterful middle-overs squeeze bowlers who choke scoring under 6.5 RPO.

---

## 4. Rajasthan Royals War Room Strategy: IPL 2027 Auction Blueprint

### Squad Context & Tactical Gaps at Sawai Mansingh Stadium (Jaipur)

The Rajasthan Royals entered IPL 2026 with a powerful core:
- **Top Order:** Yashasvi Jaiswal & Vaibhav Sooryavanshi (Openers locked).
- **Middle Core:** Riyan Parag & Dhruv Jurel.
- **Opening Seam:** Jofra Archer, Sandeep Sharma, Nandre Burger.
- **Historical Anchor:** In Season 1, RR signed domestic prodigy **Vignesh Puthur** (Player ID 48557).

#### The 4 Critical Gaps to Solve at the IPL 2027 Auction:
1. **The Domestic Scouting Masterstroke: Vipraj Nigam (Rank 1 Bowler)**  
   *Why RR Must Bid:* Vipraj Nigam embodies the exact scouting philosophy that brought Vignesh Puthur to RR in Season 1. At SMS Stadium (Jaipur), square boundaries measure 80+ meters. Leg-spinners who force aerial miscues are lethal. Nigam's 5.64 HP Economy and 39.9% dot-ball rate offer multi-crore value at a base-price/domestic discount.
2. **The #7 Power Finisher Gap: Romario Shepherd & Shashank Singh**  
   *Why RR Must Bid:* When Samson, Parag, or Jurel depart, RR has historically suffered from lower-order scoring stalls. Romario Shepherd (191.1 HP SR, 25.9% boundary rate) and Shashank Singh (186.5 HP SR) provide match-winning firepower without taking up top-order overs.
3. **The Middle-Overs Spin Choke: Noor Ahmad & Wanindu Hasaranga**  
   *Why RR Must Bid:* Following the transition of senior spinners, RR needs a dynamic wicket-taker through overs 7–15. Noor Ahmad (23 HP wickets, 7.16 HP Econ) is the premier left-arm mystery spinner in the competition.
4. **Death-Overs Lockdown: Matheesha Pathirana & Kartik Tyagi**  
   *Why RR Must Bid:* Complementing Archer and Sandeep Sharma at the death, Pathirana (33 HP wickets, 7.77 Econ) guarantees unhittable yorkers in overs 18–20.

---

## 5. Official Submission Checklist for Unstop

- [x] **Top 10 Batsmen Dropdowns Selected:** Glenn Maxwell, Shashank Singh, Romario Shepherd, Marcus Stoinis, Abdul Samad, Tim David, Liam Livingstone, Najibullah Zadran, Donovan Ferreira, Tristan Stubbs.
- [x] **Top 10 Bowlers Dropdowns Selected:** Vipraj Nigam, Noor Ahmad, Matheesha Pathirana, Kartik Tyagi, Qais Ahmad, Moeen Ali, Wanindu Hasaranga, Chamika Karunaratne, Harshal Patel, Krunal Pandya.
- [x] **Methodology Report Uploaded:** `RR_WAR_ROOM_REPORT.pdf` generated from `RR_WAR_ROOM_REPORT.html` via Cmd+P.
- [x] **Share Your Journey (Under 500 Chars):** Prepared and validated.
