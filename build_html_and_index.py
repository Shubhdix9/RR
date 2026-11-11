import base64
import json

def get_b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

fig1_b64 = get_b64('charts/fig1_pressure_distribution.png')
fig2_b64 = get_b64('charts/fig2_batting_delta_sr.png')
fig3_b64 = get_b64('charts/fig3_bowling_delta_econ.png')
fig4_b64 = get_b64('charts/fig4_rr_auction_matrix.png')

with open('top_players_summary.json', 'r') as f:
    data = json.load(f)

batters = data['batters'][:10]
bowlers = data['bowlers'][:10]

batter_li_html = ''.join([
    f"<li><strong>{b['name']}</strong> (CBI {b['cbi']:.1f} | +{b['delta_sr']:.1f} ΔSR | {b['role'].split('—')[0].strip()})</li>\n"
    for b in batters
])

bowler_li_html = ''.join([
    f"<li><strong>{bw['name']}</strong> (PBI {bw['pbi']:.1f} | {bw['econ_raw']:.2f} HP Econ | {bw['wkts']} HP Wkts)</li>\n"
    for bw in bowlers
])

batter_rows_html = ''
for b in batters:
    rank = b['rank']
    badge_cls = 'badge-top1' if rank==1 else ('badge-top2' if rank==2 else ('badge-top3' if rank==3 else ''))
    delta_cls = 'delta-pos' if b['delta_sr'] >= 0 else 'delta-neg'
    delta_sign = '+' if b['delta_sr'] >= 0 else ''
    batter_rows_html += f'''
        <tr>
          <td><span class="rank-badge {badge_cls}">{rank}</span></td>
          <td><strong>{b['name']}</strong> <span style="font-size:0.75rem; color:#64748B;">({b['team']})</span></td>
          <td><strong style="color:var(--rr-pink);">{b['cbi']:.1f}</strong></td>
          <td>{b['balls']}</td>
          <td>{b['sr_raw']:.1f}</td>
          <td>{b['base_sr']:.1f}</td>
          <td class="{delta_cls}">{delta_sign}{b['delta_sr']:.1f}</td>
          <td>{b['dot_adj']:.1f}%</td>
          <td>{b['bound_adj']:.1f}%</td>
          <td><span class="role-tag">{b['best_phase']}</span></td>
          <td style="font-size:0.82rem; color:#475569;">{b['role']}</td>
        </tr>
    '''

bowler_rows_html = ''
for bw in bowlers:
    rank = bw['rank']
    badge_cls = 'badge-top1' if rank==1 else ('badge-top2' if rank==2 else ('badge-top3' if rank==3 else ''))
    delta_cls = 'delta-pos' if bw['delta_econ'] >= 0 else 'delta-neg'
    delta_sign = '+' if bw['delta_econ'] >= 0 else ''
    bowler_rows_html += f'''
        <tr>
          <td><span class="rank-badge {badge_cls}">{rank}</span></td>
          <td><strong>{bw['name']}</strong> <span style="font-size:0.75rem; color:#64748B;">({bw['team']})</span></td>
          <td><strong style="color:var(--rr-blue);">{bw['pbi']:.1f}</strong></td>
          <td>{bw['balls']}</td>
          <td><strong>{bw['wkts']}</strong></td>
          <td><strong>{bw['econ_raw']:.2f}</strong></td>
          <td>{bw['base_econ']:.2f}</td>
          <td class="{delta_cls}">{delta_sign}{bw['delta_econ']:.2f}</td>
          <td>{bw['dot_adj']:.1f}%</td>
          <td><span class="role-tag">{bw['best_phase']}</span></td>
          <td style="font-size:0.82rem; color:#475569;">{bw['role']}</td>
        </tr>
    '''

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CLUTCH-X | Rajasthan Royals SupeRR Selector Season 2 War Room Dashboard</title>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
  --rr-pink: #EA1A7F;
  --rr-blue: #254AA5;
  --rr-navy: #0B1938;
  --rr-dark: #121F3D;
  --rr-gold: #E5A93C;
  --rr-light: #F8F9FD;
  --card-bg: #FFFFFF;
  --text-primary: #1A202C;
  --text-secondary: #4A5568;
  --border-color: #E2E8F0;
}}

* {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}

body {{
  font-family: 'Inter', sans-serif;
  background-color: var(--rr-light);
  color: var(--text-primary);
  line-height: 1.6;
}}

header {{
  background: linear-gradient(135deg, var(--rr-navy) 0%, var(--rr-blue) 60%, var(--rr-pink) 120%);
  color: white;
  padding: 2.5rem 2rem 2rem 2rem;
  box-shadow: 0 4px 20px rgba(11, 25, 56, 0.15);
}}

.header-container {{
  max-width: 1250px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.5rem;
}}

.title-badge {{
  display: inline-block;
  background: rgba(234, 26, 127, 0.25);
  border: 1px solid var(--rr-pink);
  color: #FFF;
  padding: 0.35rem 0.85rem;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 0.75rem;
}}

h1 {{
  font-family: 'Montserrat', sans-serif;
  font-size: 2.2rem;
  font-weight: 900;
  letter-spacing: -0.02em;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}}

.subtitle {{
  font-size: 1.05rem;
  opacity: 0.95;
  max-width: 750px;
  font-weight: 400;
}}

.header-actions {{
  display: flex;
  gap: 0.75rem;
}}

.print-btn {{
  background: var(--rr-pink);
  color: white;
  border: none;
  padding: 0.85rem 1.6rem;
  font-family: 'Montserrat', sans-serif;
  font-size: 0.95rem;
  font-weight: 700;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 12px rgba(234, 26, 127, 0.4);
}}

.print-btn:hover {{
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(234, 26, 127, 0.6);
}}

.github-btn {{
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 0.85rem 1.4rem;
  font-family: 'Montserrat', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  border-radius: 8px;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}}

.github-btn:hover {{
  background: rgba(255, 255, 255, 0.25);
}}

main {{
  max-width: 1250px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}}

.card {{
  background: var(--card-bg);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
}}

h2 {{
  font-family: 'Montserrat', sans-serif;
  font-size: 1.45rem;
  font-weight: 800;
  color: var(--rr-navy);
  margin-bottom: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border-bottom: 2px solid #EDF2F7;
  padding-bottom: 0.75rem;
}}

h2 .num {{
  background: var(--rr-blue);
  color: white;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 0.9rem;
  font-weight: 700;
}}

.grid-2 {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}}

.grid-4 {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}}

@media (max-width: 900px) {{
  .grid-2 {{ grid-template-columns: 1fr; }}
  .grid-4 {{ grid-template-columns: 1fr 1fr; }}
}}

.stat-box {{
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  padding: 1.25rem;
  text-align: center;
}}

.stat-val {{
  font-size: 1.75rem;
  font-weight: 900;
  font-family: 'Montserrat', sans-serif;
  color: var(--rr-navy);
}}

.stat-label {{
  font-size: 0.8rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: 0.25rem;
}}

.unstop-box {{
  background: #EFF6FF;
  border: 1.5px solid #93C5FD;
  border-radius: 10px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}}

.unstop-box h3 {{
  color: var(--rr-blue);
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
}}

table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
  margin-top: 1rem;
}}

th {{
  background: #F1F5F9;
  color: var(--rr-navy);
  font-weight: 700;
  text-align: left;
  padding: 0.75rem 0.85rem;
  border-bottom: 2px solid #CBD5E1;
}}

td {{
  padding: 0.75rem 0.85rem;
  border-bottom: 1px solid #E2E8F0;
}}

tr:hover td {{
  background: #F8FAFC;
}}

.rank-badge {{
  display: inline-block;
  width: 26px;
  height: 26px;
  background: var(--rr-navy);
  color: white;
  border-radius: 50%;
  text-align: center;
  line-height: 26px;
  font-weight: 700;
  font-size: 0.85rem;
}}

.badge-top1 {{ background: #E5A93C; }}
.badge-top2 {{ background: #94A3B8; }}
.badge-top3 {{ background: #B45309; }}

.delta-pos {{
  color: #16A34A;
  font-weight: 700;
}}

.delta-neg {{
  color: #DC2626;
  font-weight: 700;
}}

.role-tag {{
  display: inline-block;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  background: #E0E7FF;
  color: #3730A3;
}}

.figure-box {{
  margin: 1.5rem 0;
  text-align: center;
  background: #FFFFFF;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1rem;
}}

.figure-box img {{
  max-width: 100%;
  height: auto;
  border-radius: 6px;
}}

.figure-caption {{
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-top: 0.75rem;
  font-style: italic;
}}

.callout {{
  background: #FFFBEB;
  border-left: 4px solid var(--rr-gold);
  padding: 1.25rem;
  border-radius: 0 8px 8px 0;
  margin: 1.25rem 0;
}}

.callout-title {{
  font-weight: 700;
  color: #92400E;
  margin-bottom: 0.25rem;
}}

@media print {{
  header {{ padding: 1.5rem 1rem; }}
  .header-actions {{ display: none; }}
  body {{ background: white; }}
  .card {{ box-shadow: none; border: 1px solid #CCC; page-break-inside: avoid; margin-bottom: 1.5rem; }}
  table {{ font-size: 0.78rem; }}
  th, td {{ padding: 0.35rem 0.45rem; }}
}}
</style>
</head>
<body>

<header>
  <div class="header-container">
    <div>
      <span class="title-badge">Rajasthan Royals War Room Analytics</span>
      <h1>CLUTCH-X: High-Pressure Reliability Engine</h1>
      <p class="subtitle">IPL 2027 Auction Target Identification: Pre-Delivery Leverage Modeling Trained on 200,999 Deliveries (2022–2026)</p>
    </div>
    <div class="header-actions">
      <button class="print-btn" onclick="window.print()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
        Save as PDF
      </button>
      <a href="https://github.com/Shubhdix9/RR" target="_blank" class="github-btn">
        GitHub Repo
      </a>
    </div>
  </div>
</header>

<main>

  <!-- KPI SUMMARY -->
  <div class="grid-4">
    <div class="stat-box">
      <div class="stat-val" style="color:var(--rr-pink);">200,999</div>
      <div class="stat-label">Deliveries Analyzed</div>
    </div>
    <div class="stat-box">
      <div class="stat-val" style="color:var(--rr-blue);">883</div>
      <div class="stat-label">Matches (2022–2026)</div>
    </div>
    <div class="stat-box">
      <div class="stat-val" style="color:var(--rr-gold);">42.26</div>
      <div class="stat-label">P80 Pressure Cutoff</div>
    </div>
    <div class="stat-box">
      <div class="stat-val" style="color:#16A34A;">20.0%</div>
      <div class="stat-label">High-Pressure Balls</div>
    </div>
  </div>

  <!-- UNSTOP QUICK SELECTIONS -->
  <div class="card">
    <h2><span class="num">★</span> Unstop Submission Guide: Official Dropdown Selections</h2>
    <div class="unstop-box">
      <h3>Selections for Unstop Form Dropdowns (In Exact Rank Order)</h3>
      <p>Select the following players in order (Rank 1 through Rank 10) in the <strong>Batsman 1-10</strong> and <strong>Bowler 1-10</strong> dropdown fields:</p>
      
      <div class="grid-2" style="margin-top: 1rem;">
        <div>
          <h4 style="color: var(--rr-navy); margin-bottom: 0.5rem; border-bottom: 2px solid var(--rr-pink); padding-bottom: 0.25rem;">TOP 10 BATSMEN (CBI) — Pure #4–7 Finishers</h4>
          <ol style="margin-left: 1.25rem; font-weight: 600; line-height: 1.8;">
{batter_li_html}          </ol>
        </div>
        <div>
          <h4 style="color: var(--rr-navy); margin-bottom: 0.5rem; border-bottom: 2px solid var(--rr-blue); padding-bottom: 0.25rem;">TOP 10 BOWLERS (PBI) — Overs 7–20 Specialists</h4>
          <ol style="margin-left: 1.25rem; font-weight: 600; line-height: 1.8;">
{bowler_li_html}          </ol>
        </div>
      </div>
    </div>
  </div>

  <!-- SECTION 1: PRESSURE DEFINITION -->
  <div class="card">
    <h2><span class="num">1</span> What Counts as Pressure? The Pre-Delivery Mathematical Framework</h2>
    <p>Cricket analytics often errs by defining pressure simply as "the death overs". In reality, a team needing 85 off 12 balls with 9 wickets down is in the 19th over, but the contest is dead (zero leverage). Conversely, 30/3 in over 5 generates immense stress.</p>
    <p style="margin-top: 0.5rem;"><strong>CLUTCH-X</strong> evaluates pressure strictly on the <strong>pre-delivery match state</strong> across all 200,999 balls (IPL & T20I, 2022–2026), preventing outcome leakage:</p>
    
    <div class="grid-2" style="margin-top: 1rem;">
      <div style="background: #F8FAFC; padding: 1.25rem; border-radius: 8px; border: 1px solid #E2E8F0;">
        <h4 style="color: var(--rr-pink); margin-bottom: 0.5rem;">2nd Innings (Chasing Context)</h4>
        <ul style="font-size: 0.9rem; margin-left: 1rem;">
          <li><strong>Required Run Rate Stress (35%):</strong> Scaled from RRR 6.0 to 18.0+.</li>
          <li><strong>Wicket Depletion (30%):</strong> Linear pressure scaling as wickets fall (0 to 10).</li>
          <li><strong>Innings Urgency (20%):</strong> Scaled with balls elapsed (0 to 120).</li>
          <li><strong>Win Prob. Leverage Index (15%):</strong> $4 \cdot WP \cdot (1 - WP)$ maximizing on 50-50 contests.</li>
        </ul>
      </div>
      <div style="background: #F8FAFC; padding: 1.25rem; border-radius: 8px; border: 1px solid #E2E8F0;">
        <h4 style="color: var(--rr-blue); margin-bottom: 0.5rem;">1st Innings (Target Setting Context)</h4>
        <ul style="font-size: 0.9rem; margin-left: 1rem;">
          <li><strong>Phase Leverage (40%):</strong> Death overs 16–20 carry maximum swing potential.</li>
          <li><strong>Collapse Deficit (35%):</strong> Excess wickets lost vs. expected run-of-play.</li>
          <li><strong>Par Deficit (25%):</strong> Lagging behind 8.50 RPO baseline par score.</li>
          <li><strong>Knockout Stakes:</strong> $1.15\times$ multiplier for playoff and final fixtures.</li>
        </ul>
      </div>
    </div>

    <div class="figure-box">
      <img src="data:image/png;base64,{fig1_b64}" alt="Figure 1: Pressure Score Distribution">
      <div class="figure-caption">Figure 1: Continuous Pressure Score Distribution across 200,999 balls, establishing the P80 Cutoff (42.26) isolating high pressure from routine play.</div>
    </div>
  </div>

  <!-- SECTION 2: BATTING (CBI) -->
  <div class="card">
    <h2><span class="num">2</span> Top 10 Batters Under Pressure: Clutch Batting Index (CBI)</h2>
    <p>The Clutch Batting Index (CBI) synthesizes: <strong>35% High-Pressure Strike Rate</strong>, <strong>20% Delta vs Baseline SR</strong>, <strong>20% Boundary Production Rate</strong>, <strong>15% Dismissal Avoidance</strong>, and <strong>10% Match Consistency</strong> with Empirical Bayes shrinkage ($K=60$ balls).</p>
    <p style="font-size: 0.85rem; color: #4A5568; margin-top: 0.25rem;"><em>Squad Fit Filter: Excludes top-order openers and franchise captains to focus on Rajasthan Royals' war room need for dedicated middle-order power and death finishers (#4–7).</em></p>

    <div style="overflow-x:auto;">
    <table>
      <thead>
        <tr>
          <th>Rank</th>
          <th>Player Name</th>
          <th>CBI</th>
          <th>HP Balls</th>
          <th>HP SR</th>
          <th>Base SR</th>
          <th>ΔSR</th>
          <th>HP Dot%</th>
          <th>HP Bnd%</th>
          <th>Phase</th>
          <th>War Room Tactical Profile</th>
        </tr>
      </thead>
      <tbody>
{batter_rows_html}      </tbody>
    </table>
    </div>

    <div class="figure-box">
      <img src="data:image/png;base64,{fig2_b64}" alt="Figure 2: Batting Delta SR">
      <div class="figure-caption">Figure 2: Normal Baseline vs. High-Pressure Strike Rate (ΔSR) for Top 10 Batters from the real data model.</div>
    </div>
  </div>

  <!-- SECTION 3: BOWLING (PBI) -->
  <div class="card">
    <h2><span class="num">3</span> Top 10 Bowlers Under Pressure: Pressure Bowling Index (PBI)</h2>
    <p>The Pressure Bowling Index (PBI) synthesizes: <strong>30% Economy Suppression</strong>, <strong>25% Delta Economy</strong>, <strong>20% Wicket Production</strong>, <strong>15% Strike Rate</strong>, and <strong>10% Spell Consistency</strong> with Empirical Bayes shrinkage.</p>
    <p style="font-size: 0.85rem; color: #4A5568; margin-top: 0.25rem;"><em>Squad Fit Filter: Excludes new-ball powerplay openers (&lt;25% PP overs) to identify middle-overs squeeze bowlers (overs 7–15) and death-overs yorker executioners (overs 16–20).</em></p>

    <div style="overflow-x:auto;">
    <table>
      <thead>
        <tr>
          <th>Rank</th>
          <th>Player Name</th>
          <th>PBI</th>
          <th>HP Balls</th>
          <th>Wkts</th>
          <th>HP Econ</th>
          <th>Base Econ</th>
          <th>ΔEcon</th>
          <th>HP Dot%</th>
          <th>Phase</th>
          <th>War Room Tactical Profile</th>
        </tr>
      </thead>
      <tbody>
{bowler_rows_html}      </tbody>
    </table>
    </div>

    <div class="figure-box">
      <img src="data:image/png;base64,{fig3_b64}" alt="Figure 3: Bowling Delta Econ">
      <div class="figure-caption">Figure 3: Baseline vs. High-Pressure Economy (ΔEcon) for Top 10 Bowlers.</div>
    </div>
  </div>

  <!-- SECTION 4: RR AUCTION STRATEGY -->
  <div class="card">
    <h2><span class="num">4</span> Rajasthan Royals IPL 2027 Auction Strategy & Squad Fit</h2>
    <p>Translating analytical reliability under pressure into actionable auction strategy for Rajasthan Royals at the Sawai Mansingh Stadium (Jaipur):</p>

    <div class="callout">
      <div class="callout-title">The Breakout Domestic Clutch Weapon: Ashutosh Sharma (Rank 1 Batter | CBI 57.9)</div>
      <p>Ashutosh Sharma emerges as the #1 pressure finisher in the competition. Across 251 high-pressure balls, his strike rate surges from a baseline of 117.7 to an extraordinary <strong>184.9 HP SR (+55.7 ΔSR)</strong> with a 26.3% boundary rate. For RR, who retain Jaiswal and Samson but lack dedicated lower-order boundary hitters at #6/7, Ashutosh represents an unmatched talent acquisition.</p>
    </div>

    <div class="grid-2">
      <div style="background: #F8FAFC; padding: 1.25rem; border-radius: 8px; border: 1px solid #E2E8F0;">
        <h4 style="color: var(--rr-navy); margin-bottom: 0.5rem;">Key Batting Fits for RR 2027 (#4–7)</h4>
        <ul style="font-size: 0.9rem; margin-left: 1rem; line-height: 1.7;">
          <li><strong>Ashutosh Sharma (Rank 1):</strong> Pure #6/7 death destroyer (184.9 HP SR, +55.7 ΔSR).</li>
          <li><strong>Rovman Powell (Rank 2):</strong> Proven boundary enforcer (524 HP balls, 173.9 HP SR).</li>
          <li><strong>Sikandar Raza (Rank 3):</strong> Dual-threat all-rounder (185.6 HP SR & 6.73 HP Econ).</li>
          <li><strong>Sameer Rizvi (Rank 7):</strong> High-upside domestic spin-destroyer (197.7 HP SR).</li>
          <li><strong>Shubham Dubey (Rank 10):</strong> Uncapped domestic prodigy (183.9 HP SR, +52.7 ΔSR).</li>
        </ul>
      </div>
      <div style="background: #F8FAFC; padding: 1.25rem; border-radius: 8px; border: 1px solid #E2E8F0;">
        <h4 style="color: var(--rr-navy); margin-bottom: 0.5rem;">Key Bowling Fits for RR 2027 (Overs 7–20)</h4>
        <ul style="font-size: 0.9rem; margin-left: 1rem; line-height: 1.7;">
          <li><strong>Yuzvendra Chahal (Rank 1):</strong> Proven king of middle-overs wickets (51 HP wkts, 495 HP balls).</li>
          <li><strong>Umran Malik (Rank 2):</strong> 155+ kmph express pacer who tightens to 7.47 HP Econ (+1.72 ΔEcon).</li>
          <li><strong>Matheesha Pathirana (Rank 3):</strong> Unhittable slingy death yorker specialist (42 HP wkts).</li>
          <li><strong>Mitchell Santner (Rank 4):</strong> Left-arm orthodox economy choke (7.71 HP Econ).</li>
          <li><strong>Noor Ahmad (Rank 5):</strong> Young left-arm wrist-spinner (26 HP wkts, 8.33 HP Econ).</li>
        </ul>
      </div>
    </div>

    <div class="figure-box">
      <img src="data:image/png;base64,{fig4_b64}" alt="Figure 4: RR Auction Target Portfolio">
      <div class="figure-caption">Figure 4: Rajasthan Royals 2027 Auction Target Portfolio: Pressure Performance Index vs. Experience Sample Size.</div>
    </div>
  </div>

</main>

<footer style="text-align: center; padding: 2rem; color: var(--text-secondary); font-size: 0.85rem; border-top: 1px solid #E2E8F0; background: white;">
  <p><strong>SupeRR Selector Season 2 — Round 1 Submission</strong> • Proprietary Rajasthan Royals Data Analysis (2022–2026)</p>
  <p style="margin-top: 0.35rem;">Model: CLUTCH-X (Cricket Leverage & Utility Tracking for Critical High-pressure eXecution)</p>
  <p style="margin-top: 0.35rem;"><a href="https://github.com/Shubhdix9/RR" style="color:var(--rr-blue);">GitHub: Shubhdix9/RR</a> • <a href="https://shubhdix9.github.io/RR/" style="color:var(--rr-pink);">Live Dashboard: shubhdix9.github.io/RR/</a></p>
</footer>

</body>
</html>
'''

with open('RR_WAR_ROOM_REPORT.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Successfully generated BOTH RR_WAR_ROOM_REPORT.html AND index.html!")
