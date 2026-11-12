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

# Individual tactical descriptions for RR Squad Strengthening
rr_batter_reasons = {
    "Ashutosh Sharma": "Solves RR's historic #6/7 scoring dip. Accelerates to 183.7 HP SR with +55.8 xRA/100, providing domestic power hitting at low auction purse impact.",
    "Sameer Rizvi": "Uncapped Indian spin-smasher for overs 11–15 (184.7 HP SR, 80% CCR). Brings elite domestic boundary hitting without consuming an overseas slot.",
    "Shubham Dubey": "Left-hand domestic death enforcer (180.0 HP SR, +46.9 ΔSR). Adds tactical left-hand balance at #6/7 to disrupt death-bowler field placements.",
    "Donovan Ferreira": "Explosive 360° finisher and backup wicketkeeper (188.3 HP SR, 83.3% CCR). Provides dynamic tactical flexibility and insurance for Samson/Jurel.",
    "Sikandar Raza": "Dual-threat crisis recovery specialist (178.9 HP SR, 71.4% CCR). Stabilizes middle-order collapses while maintaining high-efficiency boundary hitting.",
    "Liam Livingstone": "Proven world-class middle-overs destroyer (176.4 HP SR, 81.2% CCR). Dominates spin through overs 7–15 and contributes secondary spin options.",
    "Mark Chapman": "Left-hand anchor against defensive spin (178.8 HP SR, +34.7 xRA/100). Controls middle overs with low dot-ball rates and rapid strike rotation.",
    "Tim David": "High-volume death boundary maximizer (187.5 HP SR, 423 HP balls). Specialist match-winner who converts high required run rates in final 3 overs.",
    "Rovman Powell": "High-experience boundary finisher (513 HP balls, 166.9 HP SR, 70.6% CCR). Offers proven calm leadership in chaotic death chases.",
    "Shashank Singh": "Domestic clutch sensation (173.3 HP SR, +38.8 xRA/100). Proven lower-order boundary striker who thrives in close finishes."
}

rr_bowler_reasons = {
    "Umran Malik": "155+ kmph express pace improves to 7.57 HP Econ (+1.71 suppression). Generates intimidate-and-shatter reverse swing at the death alongside Jofra Archer.",
    "Gudakesh Motie": "Left-arm orthodox precision (7.50 HP Econ, 80% CCR). Exploits Jaipur's 80m boundaries by starving batters of width and inducing mistimed aerial shots.",
    "Washington Sundar": "Powerplay and middle-overs finger-spin control (+0.94 runs prevented/over vs state). Chokes boundary access while lengthening RR's batting depth.",
    "Mitchell Santner": "World-class economy strangulation (7.58 HP Econ, 75.9% CCR). Deceives in flight and pace, suffocating opposition scoring through overs 7–15.",
    "Yuzvendra Chahal": "Proven wicket-taking machine under pressure (50 HP wickets in 495 balls). Master of SMS Stadium conditions who consistently breaks key partnerships.",
    "Sikandar Raza": "High-efficiency off-spin squeeze (7.12 HP Econ, +0.82 xRP/ov, 84.6% CCR). Delivers 4 tight overs under pressure without eating a pure bowler slot.",
    "Krunal Pandya": "Experienced defensive left-arm squeeze (7.85 HP Econ, +0.51 runs prevented/over). Restricts right-handers on large square boundaries.",
    "Harpreet Brar": "High-arm release left-arm spinner (+0.21 economy suppression under pressure). Traps aggressive hitters on large Jaipur boundaries.",
    "Matheesha Pathirana": "Slingy yorker executioner (41 HP wickets, 94% middle/death overs). Locks down overs 18–20 with unhittable yorkers and dipping slower balls.",
    "Noor Ahmad": "Dynamic young left-arm wrist spinner (26 HP wickets, 8.64 HP Econ). Generates sharp turn and variation on dry Jaipur surfaces in overs 11–15."
}

batter_rows_html = ''
for b in batters:
    rank = b['rank']
    badge_cls = 'badge-top1' if rank==1 else ('badge-top2' if rank==2 else ('badge-top3' if rank==3 else ''))
    delta_cls = 'delta-pos' if b['delta_sr'] >= 0 else 'delta-neg'
    delta_sign = '+' if b['delta_sr'] >= 0 else ''
    clean_role = b['role'].split('—')[0].strip() if '—' in b['role'] else b['role']
    batter_rows_html += f'''
        <tr>
          <td><span class="rank-badge {badge_cls}">{rank}</span></td>
          <td><strong>{b['name']}</strong> <span class="team-tag">{b['team']}</span></td>
          <td><strong style="color:var(--rr-pink); font-size:1rem;">{b['cbi']:.1f}</strong></td>
          <td>{b['balls']}</td>
          <td>{b['sr_raw']:.1f}</td>
          <td>{b['base_sr']:.1f}</td>
          <td class="{delta_cls}">{delta_sign}{b['delta_sr']:.1f}</td>
          <td>{b['dot_adj']:.1f}%</td>
          <td>{b['bound_adj']:.1f}%</td>
          <td><span class="role-tag">{b['best_phase']}</span></td>
          <td style="font-size:0.83rem; color:#334155;">{clean_role}</td>
        </tr>
    '''

bowler_rows_html = ''
for bw in bowlers:
    rank = bw['rank']
    badge_cls = 'badge-top1' if rank==1 else ('badge-top2' if rank==2 else ('badge-top3' if rank==3 else ''))
    delta_cls = 'delta-pos' if bw['delta_econ'] >= 0 else 'delta-neg'
    delta_sign = '+' if bw['delta_econ'] >= 0 else ''
    clean_role = bw['role'].split('—')[0].strip() if '—' in bw['role'] else bw['role']
    bowler_rows_html += f'''
        <tr>
          <td><span class="rank-badge {badge_cls}">{rank}</span></td>
          <td><strong>{bw['name']}</strong> <span class="team-tag">{bw['team']}</span></td>
          <td><strong style="color:var(--rr-blue); font-size:1rem;">{bw['pbi']:.1f}</strong></td>
          <td>{bw['balls']}</td>
          <td><strong>{bw['wkts']}</strong></td>
          <td><strong>{bw['econ_raw']:.2f}</strong></td>
          <td>{bw['base_econ']:.2f}</td>
          <td class="{delta_cls}">{delta_sign}{bw['delta_econ']:.2f}</td>
          <td>{bw['dot_adj']:.1f}%</td>
          <td><span class="role-tag">{bw['best_phase']}</span></td>
          <td style="font-size:0.83rem; color:#334155;">{clean_role}</td>
        </tr>
    '''

# Build 10 Batter Cards for RR Squad Fit
batter_fit_cards_html = ''
for b in batters:
    reason = rr_batter_reasons.get(b['name'], b['role'])
    batter_fit_cards_html += f'''
      <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:1.15rem; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
          <div style="font-weight:800; color:var(--rr-navy); font-size:1.02rem;">
            <span style="color:var(--rr-pink);">#{b['rank']}</span> {b['name']} <span style="font-size:0.75rem; color:#64748B; font-weight:600;">({b['team']})</span>
          </div>
          <span class="role-tag">{b['best_phase']}</span>
        </div>
        <div style="font-size:0.82rem; color:#475569; margin-bottom:0.5rem; font-weight:600;">
          HP SR: <strong style="color:var(--rr-pink);">{b['sr_raw']:.1f}</strong> (ΔSR: +{b['delta_sr']:.1f}) • Dot%: {b['dot_adj']:.1f}% • CBI: {b['cbi']:.1f}
        </div>
        <p style="font-size:0.86rem; color:#1E293B; line-height:1.5;">
          <strong>Why RR Must Bid:</strong> {reason}
        </p>
      </div>
    '''

# Build 10 Bowler Cards for RR Squad Fit
bowler_fit_cards_html = ''
for bw in bowlers:
    reason = rr_bowler_reasons.get(bw['name'], bw['role'])
    delta_str = f"+{bw['delta_econ']:.2f}" if bw['delta_econ'] >= 0 else f"{bw['delta_econ']:.2f}"
    bowler_fit_cards_html += f'''
      <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:8px; padding:1.15rem; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
          <div style="font-weight:800; color:var(--rr-navy); font-size:1.02rem;">
            <span style="color:var(--rr-blue);">#{bw['rank']}</span> {bw['name']} <span style="font-size:0.75rem; color:#64748B; font-weight:600;">({bw['team']})</span>
          </div>
          <span class="role-tag">{bw['best_phase']}</span>
        </div>
        <div style="font-size:0.82rem; color:#475569; margin-bottom:0.5rem; font-weight:600;">
          HP Econ: <strong style="color:var(--rr-blue);">{bw['econ_raw']:.2f}</strong> (ΔEcon: {delta_str}) • HP Wkts: {bw['wkts']} • PBI: {bw['pbi']:.1f}
        </div>
        <p style="font-size:0.86rem; color:#1E293B; line-height:1.5;">
          <strong>Why RR Must Bid:</strong> {reason}
        </p>
      </div>
    '''

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Rajasthan Royals War Room Player Evaluation & Auction Strategy</title>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
  --rr-pink: #EA1A7F;
  --rr-blue: #254AA5;
  --rr-navy: #0B1938;
  --rr-dark: #121F3D;
  --rr-gold: #E5A93C;
  --rr-light: #F8F9FD;
  --card-bg: #FFFFFF;
  --text-primary: #1E293B;
  --text-secondary: #475569;
  --border-color: #E2E8F0;
}}

* {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}

body {{
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: var(--rr-light);
  color: var(--text-primary);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}}

header {{
  background: linear-gradient(135deg, var(--rr-navy) 0%, var(--rr-blue) 60%, var(--rr-pink) 120%);
  color: white;
  padding: 2.2rem 2rem 2rem 2rem;
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
  font-size: 2.1rem;
  font-weight: 900;
  letter-spacing: -0.02em;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}}

.subtitle {{
  font-size: 1.02rem;
  opacity: 0.95;
  max-width: 780px;
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
  font-size: 1.35rem;
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

.grid-3 {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
}}

.grid-4 {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}}

@media (max-width: 900px) {{
  .grid-2 {{ grid-template-columns: 1fr; }}
  .grid-3 {{ grid-template-columns: 1fr; }}
  .grid-4 {{ grid-template-columns: 1fr 1fr; }}
}}

.stat-box {{
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  padding: 1.25rem;
  text-align: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
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
  font-weight: 600;
}}

table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 0.88rem;
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

.team-tag {{
  display: inline-block;
  background: #F1F5F9;
  color: #475569;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-left: 0.35rem;
}}

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

.metric-list {{
  list-style: none;
  font-size: 0.92rem;
  margin-top: 0.5rem;
}}

.metric-list li {{
  padding: 0.45rem 0;
  border-bottom: 1px dashed #E2E8F0;
}}

.metric-list li:last-child {{
  border-bottom: none;
}}

.weight-tag {{
  display: inline-block;
  background: #E2E8F0;
  color: #334155;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  margin-left: 0.35rem;
}}

.feasibility-box {{
  background: #F1F5F9;
  border-left: 4px solid var(--rr-navy);
  padding: 1.25rem;
  border-radius: 0 8px 8px 0;
  margin: 0.75rem 0;
}}

.feasibility-box h4 {{
  color: var(--rr-navy);
  font-size: 0.98rem;
  font-weight: 700;
  margin-bottom: 0.35rem;
}}

@media print {{
  header {{ padding: 1.5rem 1rem; }}
  .header-actions {{ display: none; }}
  body {{ background: white; }}
  .card {{ box-shadow: none; border: 1px solid #CCC; page-break-inside: avoid; margin-bottom: 1.5rem; }}
  table {{ font-size: 0.76rem; }}
  th, td {{ padding: 0.35rem 0.45rem; }}
}}
</style>
</head>
<body>

<header>
  <div class="header-container">
    <div>
      <span class="title-badge">Rajasthan Royals War Room Analytics</span>
      <h1>High-Pressure Performance & Auction Intelligence Model</h1>
      <p class="subtitle">IPL 2027 Auction Target Identification: Evaluating Pre-Delivery Leverage Across 200,999 Deliveries (2022–2026)</p>
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
      <div class="stat-label">High-Pressure Deliveries</div>
    </div>
  </div>

  <!-- RUBRIC PILLAR: AUCTION FEASIBILITY -->
  <div class="card">
    <h2><span class="num">★</span> Auction Feasibility Framework: Exclusion of Star Retentions & Ineligible Profiles</h2>
    <p>A fatal flaw in naive sports analytics is ranking players purely by raw prestige or overall stats without evaluating <strong>auction feasibility</strong>. To ensure actionable utility for Rajasthan Royals in the IPL 2027 Auction, our recruitment engine enforces four non-negotiable operational filters:</p>
    
    <div class="grid-2" style="margin-top: 1rem;">
      <div class="feasibility-box">
        <h4>1. Exclusion of Franchise Mega-Stars & Retained Faces</h4>
        <p style="font-size: 0.88rem; color: #334155;">
          Players such as <strong>Virat Kohli, Jasprit Bumrah, Rohit Sharma, Suryakumar Yadav, Heinrich Klaasen, Shubman Gill, Rishabh Pant, and Sanju Samson</strong> command locked multi-year franchise retention contracts at maximum purse brackets (₹18–25+ Cr) or Right-To-Match (RTM) guarantees. <strong>It is statistically and commercially impossible for these players to enter the open auction pool for Rajasthan Royals in 2027.</strong> Recommending them wastes analytical bandwidth and provides zero actionable recruitment strategy.
        </p>
      </div>

      <div class="feasibility-box">
        <h4>2. Exclusion of Legally Ineligible Nationals</h4>
        <p style="font-size: 0.88rem; color: #334155;">
          By BCCI regulatory policy and IPL governance protocols, Pakistani cricketers (e.g., Babar Azam, Mohammad Rizwan, Shaheen Afridi) are barred from registering for the IPL auction. All Pakistani players have been strictly removed from candidate pools to preserve legal compliance.
        </p>
      </div>

      <div class="feasibility-box">
        <h4>3. Exclusion of Top-Order Openers (Batting Positions 1–3)</h4>
        <p style="font-size: 0.88rem; color: #334155;">
          Rajasthan Royals have already solidified their long-term opening partnership in <strong>Yashasvi Jaiswal and Vaibhav Sooryavanshi</strong>. Allocating auction capital to top-order anchors would cause roster redundancy. Our batting evaluation strictly isolates <strong>Middle-Order Enforcers & Death Finishers (Positions 4, 5, 6, 7)</strong>.
        </p>
      </div>

      <div class="feasibility-box">
        <h4>4. Exclusion of Powerplay Opening Bowlers (&gt;25% PP Overs)</h4>
        <p style="font-size: 0.88rem; color: #334155;">
          RR's new-ball seam attack is already anchored by Jofra Archer, Sandeep Sharma, and Nandre Burger. The war room's urgent tactical requirement is <strong>Middle-Overs Spin Squeeze (Overs 7–15)</strong> and <strong>Death-Overs Yorker Lockdown (Overs 16–20)</strong>. Bowlers bowling over 25% of their deliveries in the powerplay were filtered out.
        </p>
      </div>
    </div>
  </div>

  <!-- RUBRIC PILLAR 1: PRESSURE DEFINITION -->
  <div class="card">
    <h2><span class="num">1</span> Pressure Definition: The Pre-Delivery Mathematical Framework</h2>
    <p>Cricket analytics often errs by defining pressure simply as "the death overs". In reality, a team needing 85 off 12 balls with 9 wickets down is in the 19th over, but the contest is dead (zero leverage). Conversely, 30/3 in over 5 generates immense stress.</p>
    <p style="margin-top: 0.5rem;">Our analytical framework evaluates pressure strictly on the <strong>pre-delivery match state</strong> across all 200,999 balls (IPL and T20I, 2022–2026), preventing outcome leakage:</p>
    
    <div class="grid-2" style="margin-top: 1rem;">
      <div style="background: #F8FAFC; padding: 1.25rem; border-radius: 8px; border: 1px solid #E2E8F0;">
        <h4 style="color: var(--rr-pink); margin-bottom: 0.5rem; font-family:'Montserrat',sans-serif;">2nd Innings (Chasing Context)</h4>
        <ul class="metric-list">
          <li><strong>Required Run Rate Stress <span class="weight-tag">35% Weight</span>:</strong> Measures scoring acceleration required relative to contemporary T20 par rates (scaled from 6.0 to 18.0+ RPO).</li>
          <li><strong>Wickets in Hand <span class="weight-tag">30% Weight</span>:</strong> Quantifies exponential resource depletion as wickets fall (0 to 10 wickets down).</li>
          <li><strong>Innings Urgency <span class="weight-tag">20% Weight</span>:</strong> Compounding time penalty as remaining deliveries tick down (0 to 120 balls).</li>
          <li><strong>Win Probability Leverage Index <span class="weight-tag">15% Weight</span>:</strong> Mathematical swing potential, peaking in 50-50 high-stakes situations [Formula: 4 × WP × (1 - WP)].</li>
        </ul>
      </div>
      <div style="background: #F8FAFC; padding: 1.25rem; border-radius: 8px; border: 1px solid #E2E8F0;">
        <h4 style="color: var(--rr-blue); margin-bottom: 0.5rem; font-family:'Montserrat',sans-serif;">1st Innings (Target Setting Context)</h4>
        <ul class="metric-list">
          <li><strong>Phase Leverage <span class="weight-tag">40% Weight</span>:</strong> Overs 16–20 carry maximum scoring variance and match-winning swing potential.</li>
          <li><strong>Collapse Recovery <span class="weight-tag">35% Weight</span>:</strong> Evaluates performance when batting under top-order collapse (excess wickets lost vs expected).</li>
          <li><strong>Par Deficit Pressure <span class="weight-tag">25% Weight</span>:</strong> Urgency created when the team runs behind the 8.50 RPO baseline par total.</li>
          <li><strong>Tournament Stakes:</strong> 1.15× multiplier applied for knockout, playoff, and final fixtures.</li>
        </ul>
      </div>
    </div>

    <!-- EMPIRICAL DATA BREAKDOWN -->
    <div style="margin-top: 1.5rem; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1.25rem;">
      <h4 style="color: var(--rr-navy); margin-bottom: 0.5rem; font-family:'Montserrat',sans-serif;">Empirical Baseline Scoring Rates Across 200,999 Deliveries</h4>
      <p style="font-size: 0.88rem; color: #475569; margin-bottom: 0.75rem;">To avoid phase bias, every delivery is evaluated against the empirical expectation of its discrete match state (Phase × Wickets Lost):</p>
      <div class="grid-3">
        <div style="background: #F8FAFC; padding: 0.85rem; border-radius: 6px; text-align: center; border: 1px solid #E2E8F0;">
          <div style="font-weight: 700; color: var(--rr-blue);">Powerplay (Overs 1–6)</div>
          <div style="font-size: 1.15rem; font-weight: 800; color: #1E293B; margin-top: 0.2rem;">8.02 RPO</div>
          <div style="font-size: 0.75rem; color: #64748B;">Expected Wickets: 0.048/ball</div>
        </div>
        <div style="background: #F8FAFC; padding: 0.85rem; border-radius: 6px; text-align: center; border: 1px solid #E2E8F0;">
          <div style="font-weight: 700; color: var(--rr-navy);">Middle Overs (Overs 7–15)</div>
          <div style="font-size: 1.15rem; font-weight: 800; color: #1E293B; margin-top: 0.2rem;">7.74 RPO</div>
          <div style="font-size: 0.75rem; color: #64748B;">Expected Wickets: 0.051/ball</div>
        </div>
        <div style="background: #F8FAFC; padding: 0.85rem; border-radius: 6px; text-align: center; border: 1px solid #E2E8F0;">
          <div style="font-weight: 700; color: var(--rr-pink);">Death Overs (Overs 16–20)</div>
          <div style="font-size: 1.15rem; font-weight: 800; color: #1E293B; margin-top: 0.2rem;">10.48 RPO</div>
          <div style="font-size: 0.75rem; color: #64748B;">Overs 19–20: 11.49 RPO (0.089 wkts/ball)</div>
        </div>
      </div>
    </div>

    <div class="figure-box">
      <img src="data:image/png;base64,{fig1_b64}" alt="Figure 1: Pressure Score Distribution">
      <div class="figure-caption">Figure 1: Distribution of continuous Pressure Scores across 200,999 balls, establishing the P80 Cutoff (42.26) separating high pressure from routine play.</div>
    </div>
  </div>

  <!-- RUBRIC PILLAR 2 & 4: TOP 10 BATTERS UNDER PRESSURE -->
  <div class="card">
    <h2><span class="num">2</span> Performance Evidence: Top 10 Batters Under Pressure (CBI)</h2>
    <p>The Clutch Batting Index (CBI) synthesizes: <strong>30% High-Pressure Strike Rate</strong>, <strong>25% Runs Above Expected (xRA)</strong>, <strong>20% Delta vs Baseline Strike Rate</strong>, <strong>15% Boundary Production Rate</strong>, and <strong>10% Match Consistency Rate (CCR)</strong> with Empirical Bayes shrinkage (prior confidence: 50 balls).</p>
    <p style="font-size: 0.85rem; color: #4A5568; margin-top: 0.25rem;"><em>Applied Filter: Strictly pure middle-order enforcers and death finishers (Batting Positions 4–7). Openers and retained captains excluded.</em></p>

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
          <th>Dot%</th>
          <th>Boundary%</th>
          <th>Phase</th>
          <th>Tactical Profile & Role</th>
        </tr>
      </thead>
      <tbody>
{batter_rows_html}      </tbody>
    </table>
    </div>

    <div class="figure-box">
      <img src="data:image/png;base64,{fig2_b64}" alt="Figure 2: Batting Delta SR">
      <div class="figure-caption">Figure 2: Normal Baseline vs. High-Pressure Strike Rate (ΔSR) for Top 10 Batters, illustrating massive acceleration under severe match leverage.</div>
    </div>
  </div>

  <!-- RUBRIC PILLAR 2 & 4: TOP 10 BOWLERS UNDER PRESSURE -->
  <div class="card">
    <h2><span class="num">3</span> Performance Evidence: Top 10 Bowlers Under Pressure (PBI)</h2>
    <p>The Pressure Bowling Index (PBI) synthesizes: <strong>30% Runs Prevented vs State (xRP)</strong>, <strong>25% Economy Suppression</strong>, <strong>20% Wicket Production</strong>, <strong>15% Delta Economy</strong>, and <strong>10% Spell Consistency</strong> with Empirical Bayes shrinkage.</p>
    <p style="font-size: 0.85rem; color: #4A5568; margin-top: 0.25rem;"><em>Applied Filter: Strictly middle-overs squeeze and death specialists (&lt;25% Powerplay deliveries). New-ball openers excluded.</em></p>

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
          <th>Dot%</th>
          <th>Phase</th>
          <th>Tactical Profile & Role</th>
        </tr>
      </thead>
      <tbody>
{bowler_rows_html}      </tbody>
    </table>
    </div>

    <div class="figure-box">
      <img src="data:image/png;base64,{fig3_b64}" alt="Figure 3: Bowling Delta Econ">
      <div class="figure-caption">Figure 3: Baseline vs. High-Pressure Economy (ΔEcon). Positive values demonstrate bowlers who strangle scoring rates under pressure.</div>
    </div>
  </div>

  <!-- RUBRIC PILLAR 5: RELIABILITY & LIMITATIONS -->
  <div class="card">
    <h2><span class="num">4</span> Model Reliability, Consistency & Analytical Limitations</h2>
    <div class="grid-2">
      <div style="background:#F8FAFC; padding:1.25rem; border-radius:8px; border:1px solid #E2E8F0;">
        <h4 style="color:var(--rr-navy); margin-bottom:0.5rem; font-family:'Montserrat',sans-serif;">Reliability & Consistency Verification</h4>
        <ul style="font-size:0.88rem; color:#334155; line-height:1.7; margin-left:1.1rem;">
          <li><strong>Clutch Consistency Rate (CCR):</strong> Evaluates the percentage of high-pressure match appearances where the player generated net-positive execution (xRA &gt; 0 or xRP &gt; 0). Penalizes volatile one-hit wonders.</li>
          <li><strong>Empirical Bayes Shrinkage:</strong> Players with lower sample sizes are shrunk toward league baseline priors (K = 50 for batters, K = 60 for bowlers) to prevent small-sample distortion.</li>
          <li><strong>Pre-Delivery Independence:</strong> Leverage metrics are strictly computed before the ball is bowled, guaranteeing zero outcome contamination.</li>
        </ul>
      </div>

      <div style="background:#F8FAFC; padding:1.25rem; border-radius:8px; border:1px solid #E2E8F0;">
        <h4 style="color:var(--rr-navy); margin-bottom:0.5rem; font-family:'Montserrat',sans-serif;">Analytical Limitations & Uncertainty</h4>
        <ul style="font-size:0.88rem; color:#334155; line-height:1.7; margin-left:1.1rem;">
          <li><strong>Impact of Pitch Degradation:</strong> Pitch-level turn and grip variance cannot be fully isolated without optical tracking (Hawkeye) data, occasionally elevating spinners on extreme dust-bowls.</li>
          <li><strong>Small Sample Volatility:</strong> Uncapped domestic talents (e.g., Sameer Rizvi, Shubham Dubey) possess smaller sample sizes (80–90 HP balls); while their Bayesian-shrunk numbers are exceptional, their variance bounds are wider.</li>
          <li><strong>Matchup Tactical Shielding:</strong> Some middle-overs batters are shielded by captains against negative matchups (e.g., off-spin vs left-handers).</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- RUBRIC PILLAR 6: HOW EACH PLAYER STRENGTHENS RR -->
  <div class="card">
    <h2><span class="num">5</span> Rajasthan Royals Squad Strengthening: Why RR Must Back Each Player in IPL 2027</h2>
    <p>Translating analytical reliability into actionable auction acquisitions for the Sawai Mansingh Stadium (Jaipur). Below is the detailed tactical rationale for <strong>all 10 Batters and all 10 Bowlers</strong>:</p>

    <h3 style="color:var(--rr-pink); margin:1.5rem 0 1rem 0; font-family:'Montserrat',sans-serif; font-size:1.15rem; border-bottom:2px solid var(--rr-pink); padding-bottom:0.35rem;">
      🏏 Batters: How Each Pick Strengthens Rajasthan Royals (#4–7)
    </h3>
    <div class="grid-2">
      {batter_fit_cards_html}
    </div>

    <h3 style="color:var(--rr-blue); margin:2rem 0 1rem 0; font-family:'Montserrat',sans-serif; font-size:1.15rem; border-bottom:2px solid var(--rr-blue); padding-bottom:0.35rem;">
      🎯 Bowlers: How Each Pick Strengthens Rajasthan Royals (Overs 7–20)
    </h3>
    <div class="grid-2">
      {bowler_fit_cards_html}
    </div>

    <div class="figure-box" style="margin-top:2rem;">
      <img src="data:image/png;base64,{fig4_b64}" alt="Figure 4: RR Auction Target Portfolio">
      <div class="figure-caption">Figure 4: Rajasthan Royals 2027 Auction Target Portfolio: Pressure Performance Index vs. Experience Sample Size.</div>
    </div>
  </div>

</main>

<footer style="text-align: center; padding: 2rem; color: var(--text-secondary); font-size: 0.85rem; border-top: 1px solid #E2E8F0; background: white;">
  <p><strong>Rajasthan Royals War Room Player Evaluation</strong></p>
  <p style="margin-top: 0.35rem;">Proprietary Delivery-Level Analysis (2022–2026) • Advanced Expected Value & Leverage Modeling</p>
  <p style="margin-top: 0.35rem;"><a href="https://github.com/Shubhdix9/RR" style="color:var(--rr-blue);">GitHub Repository</a> • <a href="https://shubhdix9.github.io/RR/" style="color:var(--rr-pink);">Live Interactive Dashboard</a></p>
</footer>

</body>
</html>
'''

with open('RR_WAR_ROOM_REPORT.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Successfully generated perfect RR_WAR_ROOM_REPORT.html and index.html!")
