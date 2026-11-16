import base64
import json
import os

def get_b64(path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return ""

fig1_b64 = get_b64('charts/fig1_pressure_distribution.png')
fig2_b64 = get_b64('charts/fig2_batting_delta_sr.png')
fig3_b64 = get_b64('charts/fig3_bowling_delta_econ.png')
fig4_b64 = get_b64('charts/fig4_rr_auction_matrix.png')

with open('top_players_summary.json', 'r') as f:
    data = json.load(f)

batters = data['batters'][:10]
bowlers = data['bowlers'][:10]

# Player scouting and auction dossier data (strictly professional, zero emojis)
batter_dossiers = {
    "Ashutosh Sharma": {
        "tier": "Domestic Value Target (Est. ₹3.5–5.5 Cr)",
        "origin": "Domestic Uncapped",
        "jaipur_fit": "Sawai Mansingh Stadium's 80m square boundaries reward his sweep-hit mechanics. His horizontal-bat bat speed clears straight and mid-wicket boundaries comfortably.",
        "rr_partnership": "Fills the lower middle-order finishing role at #7 below Sanju Samson, Riyan Parag, and Dhruv Jurel, addressing scoring drop-offs in death chases.",
        "stat_callout": "+55.8 xRA per 100 Balls • 183.7 High-Pressure Strike Rate (ΔSR +46.1)",
        "why_bid": "A premier domestic death finisher in the pool. Produces high-rate boundary bursts without consuming an overseas slot or premium purse share."
    },
    "Sameer Rizvi": {
        "tier": "High-Upside Domestic Asset (Est. ₹3.0–5.0 Cr)",
        "origin": "Domestic Uncapped",
        "jaipur_fit": "Clean footwork against finger and wrist spin. Capitalizes on middle-overs spin bowling on large outfields through lofted straight driving.",
        "rr_partnership": "Slots at #5 or #6 to counter middle-overs spin chokes (overs 9–14), maintaining scoring momentum into the death phase.",
        "stat_callout": "80.0% Clutch Consistency Rate • 184.7 HP Strike Rate (ΔSR +38.6)",
        "why_bid": "Combines high power with an 80% positive match execution rate. Uncapped domestic status provides auction price stability."
    },
    "Shubham Dubey": {
        "tier": "Domestic Value Prospect (Est. ₹1.5–3.0 Cr)",
        "origin": "Domestic Uncapped",
        "jaipur_fit": "Tall left-hander with high reach. Targets square boundaries at Jaipur with pull shots and lofted off-drives.",
        "rr_partnership": "Provides left-handed death finishing at #6/7, disrupting bowler yorker execution alongside right-handed options like Jurel and Powell.",
        "stat_callout": "+46.9 ΔSR Acceleration • 71.4% Consistency • 180.0 HP Strike Rate",
        "why_bid": "Familiarity with Rajasthan Royals team setup and demonstrated performance under high leverage in domestic and IPL cricket."
    },
    "Donovan Ferreira": {
        "tier": "Multi-Utility Overseas Asset (Est. ₹2.0–4.0 Cr)",
        "origin": "Overseas (South Africa)",
        "jaipur_fit": "Rapid wrist mechanics and 360-degree ramp/scoop execution. Exploits fine-leg and third-man boundary pockets on large outfields.",
        "rr_partnership": "Multi-functional utility: backup wicketkeeper, elite boundary fielder, explosive finisher at #6/7, and occasional off-spin option.",
        "stat_callout": "188.3 High-Pressure Strike Rate (Highest in Dataset) • 83.3% Consistency",
        "why_bid": "Highest raw strike rate in our top 10 under leverage. Provides tactical flexibility and depth behind Samson and Jurel."
    },
    "Sikandar Raza": {
        "tier": "Multi-Phase Overseas Veteran (Est. ₹2.5–4.5 Cr)",
        "origin": "Overseas (Zimbabwe)",
        "jaipur_fit": "Controlled strike rotation and tactical manipulation of field placements on spacious outfields.",
        "rr_partnership": "Stabilizes middle-order collapses while maintaining high scoring rates; also operates as a Rank 6 bowling specialist (7.12 HP Econ).",
        "stat_callout": "Dual Top-10 Selection (Rank 5 Bat / Rank 6 Bowl) • +47.7 ΔSR",
        "why_bid": "Rare dual-discipline asset: delivers death boundary hitting and four controlled overs of middle spin on a single overseas slot."
    },
    "Liam Livingstone": {
        "tier": "Marquee Middle Enforcer (Est. ₹7.5–11.0 Cr)",
        "origin": "Overseas (England)",
        "jaipur_fit": "High raw power that clears large boundary configurations. Capable of hitting over 90 meters consistently.",
        "rr_partnership": "Targets opposition spin through overs 9–15. Bowls both off-spin and leg-spin to exploit left/right matchups in Jaipur conditions.",
        "stat_callout": "81.2% Consistency Rate • 176.4 HP Strike Rate • +36.4 xRA/100",
        "why_bid": "High-impact international enforcer. Addresses middle-overs boundary droughts and offers bowling matchup flexibility."
    },
    "Mark Chapman": {
        "tier": "Middle-Overs Accumulator (Est. ₹1.5–3.0 Cr)",
        "origin": "Overseas (New Zealand)",
        "jaipur_fit": "Efficient sweeper and strike rotator. Minimizes dot balls on large boundary grounds and builds momentum through active running.",
        "rr_partnership": "Composed left-handed anchor at #5/6 who manages tricky run chases and accelerates when the required rate rises.",
        "stat_callout": "178.8 HP Strike Rate (ΔSR +30.0) • Low Dot-Ball Percentage",
        "why_bid": "Strong record against defensive spin, sound tactical execution, and available at an economical purse bracket."
    },
    "Tim David": {
        "tier": "Marquee Death Specialist (Est. ₹7.0–10.5 Cr)",
        "origin": "Overseas (Australia)",
        "jaipur_fit": "Strong bottom-hand leverage against pace. Drives full and wide yorkers down the ground past deep boundary riders.",
        "rr_partnership": "Enters in overs 16–20 to close chases alongside Parag or Jurel. Takes primary ownership of high required rates (12+ RPO).",
        "stat_callout": "423 High-Pressure Deliveries (High Sample Volume) • 187.5 HP Strike Rate",
        "why_bid": "One of the most extensively sampled pure death-overs specialists in modern T20 cricket."
    },
    "Rovman Powell": {
        "tier": "Proven Middle Finisher (Est. ₹4.0–6.5 Cr)",
        "origin": "Overseas (West Indies)",
        "jaipur_fit": "Established track record in Rajasthan Royals colors. Efficient power hitting down the ground and through mid-wicket at Jaipur.",
        "rr_partnership": "Established chemistry with the squad core. Solidifies #6/7 with experienced boundary hitting under pressure.",
        "stat_callout": "513 High-Pressure Deliveries (Largest Dataset Sample) • 70.6% Consistency",
        "why_bid": "Zero integration risk, proven reliability for RR in tight finishes, and experienced international presence."
    },
    "Shashank Singh": {
        "tier": "Domestic Match-Winner (Est. ₹4.5–7.0 Cr)",
        "origin": "Domestic Proven",
        "jaipur_fit": "High-backlift striker who excels against pace bowling and handles good carry tracks effectively.",
        "rr_partnership": "Provides domestic match-winning depth in the lower middle-order, allowing flexible overseas selection elsewhere.",
        "stat_callout": "+38.8 xRA per 100 Balls • 173.3 HP Strike Rate • Proven Chase Record",
        "why_bid": "Demonstrated composure in tense run chases with strong domestic execution."
    }
}

bowler_dossiers = {
    "Umran Malik": {
        "tier": "High-Velocity Seam Asset (Est. ₹3.5–6.0 Cr)",
        "origin": "Domestic Capped",
        "jaipur_fit": "High release velocity (150+ km/h) rushes batters on Jaipur's large outfield, inducing mistimed aerial shots well inside boundary cushions.",
        "rr_partnership": "Forms a complementary pace combination with Jofra Archer: Archer's bounce and seam movement paired with Umran's skidding pace.",
        "stat_callout": "7.57 HP Economy Rate • +1.71 Economy Suppression Under Pressure",
        "why_bid": "Under high leverage, his economy improves to 7.57 RPO (+1.71 better than baseline). A high-impact enforcer in middle and death overs."
    },
    "Gudakesh Motie": {
        "tier": "Defensive Left-Arm Spin (Est. ₹2.0–3.5 Cr)",
        "origin": "Overseas (West Indies)",
        "jaipur_fit": "Consistent trajectory and stump-to-stump line. Uses large square boundaries to deny width and force defensive strokes.",
        "rr_partnership": "Controls overs 7–14, applying run-rate pressure that supports seamers at the other end.",
        "stat_callout": "80.0% Consistency Rate • 7.50 HP Economy • +0.68 Runs Prevented/Over",
        "why_bid": "Defensive left-arm finger spinner with an 80% clutch consistency mark. High tactical value at moderate purse commitment."
    },
    "Washington Sundar": {
        "tier": "Domestic Strategic Asset (Est. ₹5.5–8.5 Cr)",
        "origin": "Domestic Capped (India)",
        "jaipur_fit": "Tight trajectory control and variable pace. Exploits surface grip with accurate stump-line bowling.",
        "rr_partnership": "Bowls across multiple phases (powerplay, middle squeeze) and deepens Rajasthan Royals' batting order at #8.",
        "stat_callout": "+0.94 Runs Prevented per Over • 7.62 HP Economy • International Capped",
        "why_bid": "Indian all-round asset who balances team structure, provides matchup utility, and consumes zero overseas slots."
    },
    "Mitchell Santner": {
        "tier": "Defensive Spin Specialist (Est. ₹3.5–5.5 Cr)",
        "origin": "Overseas (New Zealand)",
        "jaipur_fit": "Subtle pace variations and flight control. Limits scoring on large boundary outfields through defensive trajectory management.",
        "rr_partnership": "Fills the defensive spin control role through overs 7–15, restricting middle-overs scoring.",
        "stat_callout": "426 High-Pressure Deliveries • 7.58 HP Economy • 75.9% Consistency",
        "why_bid": "Established standard for defensive T20 spin bowling. Consistently maintains sub-8.00 economy in high-leverage contexts."
    },
    "Yuzvendra Chahal": {
        "tier": "Priority Buyback / Proven Match-Winner (Est. ₹7.5–11.0 Cr)",
        "origin": "Domestic Capped (RR Core)",
        "jaipur_fit": "Extensive experience at Sawai Mansingh Stadium. Understands venue dimensions, luring hitters into mistimed shots to long-on and deep mid-wicket.",
        "rr_partnership": "Re-establishes RR's primary wicket-taking threat through overs 10–16, breaking partnerships in high-stress phases.",
        "stat_callout": "50 High-Pressure Wickets in 495 Balls • All-Time Leading IPL Wicket-Taker",
        "why_bid": "Proven match-winner with deep tactical alignment to the home venue. 50 high-pressure wickets in our dataset verify his impact."
    },
    "Sikandar Raza": {
        "tier": "Mystery Spin Option (Est. ₹2.5–4.5 Cr)",
        "origin": "Overseas (Zimbabwe)",
        "jaipur_fit": "Carrom ball and variations create uncertainty for batters attempting to clear large boundary dimensions.",
        "rr_partnership": "Provides reliable middle-overs bowling without requiring a dedicated bowler spot, locking scoring at 7.12 RPO.",
        "stat_callout": "7.12 HP Economy Rate • 84.6% Clutch Consistency • +0.82 Runs Prevented/Over",
        "why_bid": "Highest consistency rate (84.6%) among all spin candidates. Offers two-way reliability across both innings."
    },
    "Krunal Pandya": {
        "tier": "Matchup Specialist (Est. ₹4.0–6.5 Cr)",
        "origin": "Domestic Capped (India)",
        "jaipur_fit": "Fires flat trajectories into the surface, denying batters room to elevate over straight boundaries.",
        "rr_partnership": "Provides left-arm spin matchup control against right-handed power hitters, backed by extensive IPL playoff experience.",
        "stat_callout": "7.85 HP Economy • +0.51 Runs Prevented/Over • 17 Wickets Under Leverage",
        "why_bid": "Experienced domestic campaigner with sound temperament in pressure fixtures."
    },
    "Harpreet Brar": {
        "tier": "Domestic Matchup Weapon (Est. ₹2.5–4.5 Cr)",
        "origin": "Domestic Capped (India)",
        "jaipur_fit": "High release point extracts bounce on Jaipur pitches. Cramps aggressive hitters seeking to target the leg side.",
        "rr_partnership": "Direct tactical weapon against right-hand dominant batting lineups. Provides cost-effective domestic spin depth.",
        "stat_callout": "7.64 HP Economy • +0.21 Economy Suppression • Strong Outfield Catcher",
        "why_bid": "Matchup-oriented bowler who regularly contains top-order opposition. Moderate purse footprint."
    },
    "Matheesha Pathirana": {
        "tier": "Marquee Death Spearhead (Est. ₹9.0–13.5 Cr)",
        "origin": "Overseas (Sri Lanka)",
        "jaipur_fit": "Low release angle produces accurate yorkers and dipping slower balls that are difficult to elevate over boundary fences.",
        "rr_partnership": "Pairs with Jofra Archer to establish a fortified death-overs bowling attack in overs 17–20.",
        "stat_callout": "41 High-Pressure Wickets (94% Middle/Death) • 431 High-Pressure Balls",
        "why_bid": "Premier death-phase executioner. Delivers high-frequency yorkers and extreme defensive control at the death."
    },
    "Noor Ahmad": {
        "tier": "Young Wrist Spin Asset (Est. ₹5.5–9.0 Cr)",
        "origin": "Overseas (Afghanistan)",
        "jaipur_fit": "Fast arm speed and disguised googly create deception. Produces turn on dry daytime tracks at Jaipur.",
        "rr_partnership": "Acts as an attacking wrist-spinner in overs 9–15, spinning the ball away from right-handers alongside finger-spin options.",
        "stat_callout": "26 High-Pressure Wickets • 386 HP Balls • Left-Arm Unorthodox Rarity",
        "why_bid": "At 21 years of age, offers a long-term franchise asset in the scarce left-arm wrist-spin category."
    }
}

# Generate Interactive JSON data for client-side filtering and sorting
all_players_data = []
for b in batters:
    dos = batter_dossiers.get(b['name'], {})
    all_players_data.append({
        "type": "batter",
        "rank": b['rank'],
        "name": b['name'],
        "team": b['team'],
        "score": b['cbi'],
        "score_name": "CBI",
        "balls": b['balls'],
        "primary_metric": b['sr_raw'],
        "primary_name": "HP Strike Rate",
        "base_metric": b['base_sr'],
        "base_name": "Base SR",
        "delta": b['delta_sr'],
        "delta_name": "ΔSR",
        "dot_pct": b['dot_adj'],
        "bound_pct": b['bound_adj'],
        "phase": b['best_phase'],
        "role": b['role'].split('—')[0].strip(),
        "tier": dos.get("tier", "Target Asset"),
        "origin": dos.get("origin", "Specialist"),
        "jaipur_fit": dos.get("jaipur_fit", ""),
        "rr_partnership": dos.get("rr_partnership", ""),
        "stat_callout": dos.get("stat_callout", ""),
        "why_bid": dos.get("why_bid", "")
    })

for bw in bowlers:
    dos = bowler_dossiers.get(bw['name'], {})
    all_players_data.append({
        "type": "bowler",
        "rank": bw['rank'],
        "name": bw['name'],
        "team": bw['team'],
        "score": bw['pbi'],
        "score_name": "PBI",
        "balls": bw['balls'],
        "primary_metric": bw['econ_raw'],
        "primary_name": "HP Economy",
        "base_metric": bw['base_econ'],
        "base_name": "Base Econ",
        "delta": bw['delta_econ'],
        "delta_name": "ΔEcon",
        "dot_pct": bw['dot_adj'],
        "bound_pct": bw['wkts'],
        "phase": bw['best_phase'],
        "role": bw['role'].split('—')[0].strip(),
        "tier": dos.get("tier", "Target Asset"),
        "origin": dos.get("origin", "Specialist"),
        "jaipur_fit": dos.get("jaipur_fit", ""),
        "rr_partnership": dos.get("rr_partnership", ""),
        "stat_callout": dos.get("stat_callout", ""),
        "why_bid": dos.get("why_bid", "")
    })

players_json_str = json.dumps(all_players_data)

# Table rows generation (NO emojis)
batter_rows_html = ""
for b in batters:
    rank = b['rank']
    badge_cls = 'badge-gold' if rank==1 else ('badge-silver' if rank==2 else ('badge-bronze' if rank==3 else 'badge-plain'))
    delta_cls = 'delta-pos' if b['delta_sr'] >= 0 else 'delta-neg'
    clean_role = b['role'].split('—')[0].strip()
    dos = batter_dossiers.get(b['name'], {})
    tier = dos.get("tier", "Target Asset")
    batter_rows_html += f'''
      <tr class="player-row" data-name="{b['name']}" data-team="{b['team']}" data-type="batter" onclick="openPlayerModal('{b['name']}')">
        <td class="text-center"><span class="rank-pill {badge_cls}">#{rank}</span></td>
        <td>
          <div class="player-cell">
            <span class="player-name">{b['name']}</span>
            <span class="team-badge">{b['team']}</span>
          </div>
        </td>
        <td class="text-center"><span class="score-badge score-pink">{b['cbi']:.1f}</span></td>
        <td class="text-center font-mono">{b['balls']}</td>
        <td class="text-center font-bold font-mono text-pink">{b['sr_raw']:.1f}</td>
        <td class="text-center font-mono text-muted">{b['base_sr']:.1f}</td>
        <td class="text-center font-mono font-bold {delta_cls}">+{b['delta_sr']:.1f}</td>
        <td class="text-center font-mono">{b['dot_adj']:.1f}%</td>
        <td class="text-center font-mono">{b['bound_adj']:.1f}%</td>
        <td class="text-center"><span class="phase-pill phase-death">{b['best_phase']}</span></td>
        <td class="role-cell">
          <div class="role-title">{clean_role}</div>
          <div class="tier-tag">{tier}</div>
        </td>
        <td class="text-center"><button class="btn-dossier" onclick="event.stopPropagation(); openPlayerModal('{b['name']}')">Dossier</button></td>
      </tr>
    '''

bowler_rows_html = ""
for bw in bowlers:
    rank = bw['rank']
    badge_cls = 'badge-gold' if rank==1 else ('badge-silver' if rank==2 else ('badge-bronze' if rank==3 else 'badge-plain'))
    delta_cls = 'delta-pos' if bw['delta_econ'] >= 0 else 'delta-neg'
    delta_sign = '+' if bw['delta_econ'] >= 0 else ''
    clean_role = bw['role'].split('—')[0].strip()
    dos = bowler_dossiers.get(bw['name'], {})
    tier = dos.get("tier", "Target Asset")
    phase_cls = 'phase-death' if 'DEATH' in bw['best_phase'] else 'phase-mid'
    bowler_rows_html += f'''
      <tr class="player-row" data-name="{bw['name']}" data-team="{bw['team']}" data-type="bowler" onclick="openPlayerModal('{bw['name']}')">
        <td class="text-center"><span class="rank-pill {badge_cls}">#{rank}</span></td>
        <td>
          <div class="player-cell">
            <span class="player-name">{bw['name']}</span>
            <span class="team-badge team-blue-badge">{bw['team']}</span>
          </div>
        </td>
        <td class="text-center"><span class="score-badge score-blue">{bw['pbi']:.1f}</span></td>
        <td class="text-center font-mono">{bw['balls']}</td>
        <td class="text-center font-mono font-bold text-navy">{bw['wkts']}</td>
        <td class="text-center font-bold font-mono text-blue">{bw['econ_raw']:.2f}</td>
        <td class="text-center font-mono text-muted">{bw['base_econ']:.2f}</td>
        <td class="text-center font-mono font-bold {delta_cls}">{delta_sign}{bw['delta_econ']:.2f}</td>
        <td class="text-center font-mono">{bw['dot_adj']:.1f}%</td>
        <td class="text-center"><span class="phase-pill {phase_cls}">{bw['best_phase']}</span></td>
        <td class="role-cell">
          <div class="role-title">{clean_role}</div>
          <div class="tier-tag">{tier}</div>
        </td>
        <td class="text-center"><button class="btn-dossier" onclick="event.stopPropagation(); openPlayerModal('{bw['name']}')">Dossier</button></td>
      </tr>
    '''

# Detailed cards for Jaipur / Squad Fit section (NO emojis)
batter_cards_html = ""
for b in batters:
    dos = batter_dossiers.get(b['name'], {})
    batter_cards_html += f'''
      <div class="squad-card batter-border">
        <div class="squad-card-header">
          <div>
            <div class="squad-card-title">
              <span class="rank-mini pink-bg">#{b['rank']}</span>
              <span class="name-bold">{b['name']}</span>
              <span class="team-tag">{b['team']}</span>
            </div>
            <div class="squad-card-sub">{dos.get('tier', '')}</div>
          </div>
          <span class="phase-pill phase-death">{b['best_phase']}</span>
        </div>

        <div class="squad-metrics-row">
          <div class="metric-mini">
            <span class="m-label">CBI Score</span>
            <span class="m-val text-pink">{b['cbi']:.1f}</span>
          </div>
          <div class="metric-mini">
            <span class="m-label">HP Strike Rate</span>
            <span class="m-val text-pink">{b['sr_raw']:.1f}</span>
          </div>
          <div class="metric-mini">
            <span class="m-label">Delta vs Baseline</span>
            <span class="m-val text-green font-bold">+{b['delta_sr']:.1f}</span>
          </div>
          <div class="metric-mini">
            <span class="m-label">Consistency</span>
            <span class="m-val text-navy">{b['ccr']:.1f}%</span>
          </div>
        </div>

        <div class="squad-section">
          <div class="section-tag-mini text-pink">Sawai Mansingh Stadium Dimension Fit:</div>
          <p class="squad-text">{dos.get('jaipur_fit', '')}</p>
        </div>

        <div class="squad-section">
          <div class="section-tag-mini text-navy">Tactical Role in Rajasthan Royals XI:</div>
          <p class="squad-text">{dos.get('rr_partnership', '')}</p>
        </div>

        <div class="squad-footer">
          <strong>Strategic Rationale:</strong> {dos.get('why_bid', '')}
        </div>
      </div>
    '''

bowler_cards_html = ""
for bw in bowlers:
    dos = bowler_dossiers.get(bw['name'], {})
    delta_str = f"+{bw['delta_econ']:.2f}" if bw['delta_econ'] >= 0 else f"{bw['delta_econ']:.2f}"
    phase_cls = 'phase-death' if 'DEATH' in bw['best_phase'] else 'phase-mid'
    bowler_cards_html += f'''
      <div class="squad-card bowler-border">
        <div class="squad-card-header">
          <div>
            <div class="squad-card-title">
              <span class="rank-mini blue-bg">#{bw['rank']}</span>
              <span class="name-bold">{bw['name']}</span>
              <span class="team-tag">{bw['team']}</span>
            </div>
            <div class="squad-card-sub">{dos.get('tier', '')}</div>
          </div>
          <span class="phase-pill {phase_cls}">{bw['best_phase']}</span>
        </div>

        <div class="squad-metrics-row">
          <div class="metric-mini">
            <span class="m-label">PBI Score</span>
            <span class="m-val text-blue">{bw['pbi']:.1f}</span>
          </div>
          <div class="metric-mini">
            <span class="m-label">HP Economy</span>
            <span class="m-val text-blue">{bw['econ_raw']:.2f}</span>
          </div>
          <div class="metric-mini">
            <span class="m-label">Delta Suppression</span>
            <span class="m-val text-green font-bold">{delta_str}</span>
          </div>
          <div class="metric-mini">
            <span class="m-label">HP Wickets</span>
            <span class="m-val text-navy font-bold">{bw['wkts']}</span>
          </div>
        </div>

        <div class="squad-section">
          <div class="section-tag-mini text-blue">Sawai Mansingh Stadium Dimension Fit:</div>
          <p class="squad-text">{dos.get('jaipur_fit', '')}</p>
        </div>

        <div class="squad-section">
          <div class="section-tag-mini text-navy">Tactical Role in Rajasthan Royals XI:</div>
          <p class="squad-text">{dos.get('rr_partnership', '')}</p>
        </div>

        <div class="squad-footer">
          <strong>Strategic Rationale:</strong> {dos.get('why_bid', '')}
        </div>
      </div>
    '''

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Rajasthan Royals — IPL 2027 Auction Target Identification Report</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
:root {{
  --rr-pink: #D81B60;
  --rr-pink-light: #FDF2F8;
  --rr-blue: #1E40AF;
  --rr-blue-light: #EFF6FF;
  --rr-navy: #0F172A;
  --rr-dark: #0A0F1D;
  --rr-gold: #D97706;
  --rr-emerald: #059669;
  --rr-red: #DC2626;
  --rr-slate-50: #F8FAFC;
  --rr-slate-100: #F1F5F9;
  --rr-slate-200: #E2E8F0;
  --rr-slate-300: #CBD5E1;
  --rr-slate-400: #94A3B8;
  --rr-slate-500: #64748B;
  --rr-slate-600: #475569;
  --rr-slate-700: #334155;
  --rr-slate-800: #1E293B;
  --rr-slate-900: #0F172A;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
}}

* {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}

body {{
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: #F8FAFC;
  color: var(--rr-slate-800);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  padding-bottom: 4rem;
}}

/* Top Bar: Ultra Minimalist, only PDF and GitHub */
.top-bar {{
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(15, 23, 42, 0.96);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 0.65rem 1.5rem;
}}

.top-bar-inner {{
  max-width: 1300px;
  margin: 0 auto;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 0.75rem;
}}

.btn-pdf {{
  background: var(--rr-pink);
  color: #FFFFFF;
  border: none;
  padding: 0.45rem 1.1rem;
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  cursor: pointer;
  transition: all 0.15s ease;
}}

.btn-pdf:hover {{
  background: #BE185D;
}}

.btn-github {{
  background: rgba(255, 255, 255, 0.12);
  color: #FFFFFF;
  text-decoration: none;
  border: 1px solid rgba(255, 255, 255, 0.25);
  padding: 0.45rem 0.95rem;
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
  font-weight: 500;
  transition: all 0.15s ease;
}}

.btn-github:hover {{
  background: rgba(255, 255, 255, 0.2);
}}

/* Institutional Header */
.executive-header {{
  background: #0F172A;
  color: #FFFFFF;
  padding: 3rem 1.5rem 2.75rem 1.5rem;
  border-bottom: 1px solid #1E293B;
}}

.header-container {{
  max-width: 1300px;
  margin: 0 auto;
}}

.doc-metadata {{
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--rr-slate-400);
  margin-bottom: 1rem;
}}

.doc-tag {{
  background: rgba(216, 27, 96, 0.2);
  color: #F472B6;
  border: 1px solid rgba(216, 27, 96, 0.4);
  padding: 0.2rem 0.55rem;
  border-radius: var(--radius-sm);
}}

.header-title {{
  font-size: 2.25rem;
  font-weight: 800;
  line-height: 1.2;
  letter-spacing: -0.025em;
  color: #FFFFFF;
  margin-bottom: 0.65rem;
}}

.header-subtitle {{
  font-size: 1.05rem;
  color: var(--rr-slate-300);
  font-weight: 400;
  line-height: 1.5;
  max-width: 920px;
  margin-bottom: 2rem;
}}

/* Quantitative Baseline Strip */
.baseline-strip {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  background: #1E293B;
  border: 1px solid #334155;
  border-radius: var(--radius-md);
  padding: 1.25rem 1.5rem;
}}

.strip-item {{
  border-right: 1px solid #334155;
  padding-right: 1rem;
}}

.strip-item:last-child {{
  border-right: none;
  padding-right: 0;
}}

.strip-val {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 1.1;
  color: #FFFFFF;
}}

.strip-val.pink {{ color: #F472B6; }}
.strip-val.blue {{ color: #60A5FA; }}
.strip-val.gold {{ color: #FBBF24; }}
.strip-val.green {{ color: #34D399; }}

.strip-label {{
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--rr-slate-400);
  margin-top: 0.35rem;
}}

.strip-desc {{
  font-size: 0.75rem;
  color: var(--rr-slate-400);
  margin-top: 0.15rem;
}}

/* Main Layout */
.main-wrapper {{
  max-width: 1300px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}}

/* Section Card */
.section-card {{
  background: #FFFFFF;
  border: 1px solid var(--rr-slate-200);
  border-radius: var(--radius-md);
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: var(--shadow-sm);
}}

.section-head {{
  border-bottom: 1px solid var(--rr-slate-200);
  padding-bottom: 1rem;
  margin-bottom: 1.5rem;
}}

.section-title {{
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--rr-navy);
  letter-spacing: -0.015em;
}}

.section-lead {{
  font-size: 0.92rem;
  color: var(--rr-slate-600);
  margin-top: 0.25rem;
}}

/* Grid Utilities */
.grid-2 {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
}}

.grid-3 {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}}

.grid-4 {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}}

@media (max-width: 900px) {{
  .baseline-strip {{ grid-template-columns: repeat(2, 1fr); gap: 1.25rem; }}
  .strip-item {{ border-right: none; }}
  .grid-2, .grid-3, .grid-4 {{ grid-template-columns: 1fr; }}
  .header-title {{ font-size: 1.75rem; }}
}}

/* Feasibility Items */
.rule-box {{
  background: var(--rr-slate-50);
  border: 1px solid var(--rr-slate-200);
  border-radius: var(--radius-sm);
  padding: 1.25rem;
}}

.rule-title {{
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--rr-navy);
  margin-bottom: 0.45rem;
}}

.rule-desc {{
  font-size: 0.86rem;
  color: var(--rr-slate-600);
  line-height: 1.55;
}}

/* Methodology Formulation Box */
.formula-container {{
  background: #F8FAFC;
  border: 1px solid var(--rr-slate-300);
  border-radius: var(--radius-sm);
  padding: 1.25rem;
}}

.formula-title {{
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--rr-navy);
  margin-bottom: 0.35rem;
}}

.formula-box {{
  background: #FFFFFF;
  border: 1px solid var(--rr-slate-300);
  border-radius: var(--radius-sm);
  padding: 0.75rem 1rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--rr-navy);
  margin: 0.65rem 0;
  overflow-x: auto;
}}

.formula-notes {{
  font-size: 0.82rem;
  color: var(--rr-slate-600);
  margin-left: 1.1rem;
  line-height: 1.6;
}}

/* Table Toolbar */
.toolbar {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1rem;
  background: var(--rr-slate-100);
  padding: 0.65rem 1rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--rr-slate-200);
}}

.filter-input {{
  padding: 0.45rem 0.75rem;
  border: 1px solid var(--rr-slate-300);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.82rem;
  width: 280px;
  outline: none;
}}

.filter-input:focus {{
  border-color: var(--rr-navy);
}}

.table-instruction {{
  font-size: 0.78rem;
  color: var(--rr-slate-500);
  font-weight: 500;
}}

/* Data Tables */
.table-scroll {{
  overflow-x: auto;
  border: 1px solid var(--rr-slate-200);
  border-radius: var(--radius-sm);
}}

table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 0.84rem;
  text-align: left;
  background: #FFFFFF;
}}

thead th {{
  background: #0F172A;
  color: #FFFFFF;
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.75rem 0.85rem;
  border-bottom: 1px solid var(--rr-slate-300);
  white-space: nowrap;
}}

tbody tr.player-row {{
  border-bottom: 1px solid var(--rr-slate-200);
  cursor: pointer;
  transition: background 0.1s ease;
}}

tbody tr.player-row:hover {{
  background: #FDF2F8;
}}

tbody tr.player-row:nth-child(even) {{
  background-color: #FAFAFA;
}}

tbody tr.player-row:nth-child(even):hover {{
  background-color: #FDF2F8;
}}

tbody td {{
  padding: 0.75rem 0.85rem;
  vertical-align: middle;
  white-space: nowrap;
}}

/* Badges & Text Styling */
.rank-pill {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  font-weight: 700;
  font-size: 0.82rem;
  font-family: 'JetBrains Mono', monospace;
}}

.badge-gold {{ background: #FEF3C7; color: #92400E; border: 1px solid #F59E0B; }}
.badge-silver {{ background: #F1F5F9; color: #475569; border: 1px solid #94A3B8; }}
.badge-bronze {{ background: #FFEDD5; color: #9A3412; border: 1px solid #FB923C; }}
.badge-plain {{ background: #F8FAFC; color: #64748B; border: 1px solid #CBD5E1; }}

.player-cell {{
  display: flex;
  align-items: center;
  gap: 0.45rem;
}}

.player-name {{
  font-weight: 700;
  color: var(--rr-navy);
}}

.team-badge {{
  background: #FCE7F3;
  color: #9D174D;
  border-radius: var(--radius-sm);
  padding: 0.12rem 0.4rem;
  font-size: 0.68rem;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
}}

.team-blue-badge {{
  background: #DBEAFE;
  color: #1E40AF;
}}

.score-badge {{
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  font-size: 0.95rem;
  padding: 0.15rem 0.45rem;
  border-radius: var(--radius-sm);
  display: inline-block;
}}

.score-pink {{ background: #FDF2F8; color: var(--rr-pink); border: 1px solid #FBCFE8; }}
.score-blue {{ background: #EFF6FF; color: var(--rr-blue); border: 1px solid #BFDBFE; }}

.delta-pos {{ color: var(--rr-emerald); font-weight: 700; }}
.delta-neg {{ color: var(--rr-red); font-weight: 700; }}

.phase-pill {{
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.2rem 0.55rem;
  border-radius: var(--radius-sm);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  display: inline-block;
}}

.phase-death {{ background: #FEE2E2; color: #991B1B; }}
.phase-mid {{ background: #E0E7FF; color: #3730A3; }}

.role-cell {{
  max-width: 250px;
  white-space: normal;
}}

.role-title {{
  font-weight: 600;
  color: var(--rr-slate-800);
  font-size: 0.82rem;
  line-height: 1.3;
}}

.tier-tag {{
  color: var(--rr-slate-500);
  font-size: 0.72rem;
  margin-top: 0.15rem;
}}

.btn-dossier {{
  background: #FFFFFF;
  border: 1px solid var(--rr-slate-300);
  color: var(--rr-navy);
  padding: 0.3rem 0.6rem;
  border-radius: var(--radius-sm);
  font-size: 0.74rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}}

.btn-dossier:hover {{
  background: var(--rr-navy);
  color: #FFFFFF;
  border-color: var(--rr-navy);
}}

/* Figure Embeds */
.figure-block {{
  margin: 1.75rem 0;
  border: 1px solid var(--rr-slate-200);
  border-radius: var(--radius-sm);
  overflow: hidden;
  background: #FFFFFF;
}}

.figure-block img {{
  width: 100%;
  height: auto;
  display: block;
}}

.figure-meta {{
  background: var(--rr-slate-50);
  padding: 0.75rem 1rem;
  font-size: 0.82rem;
  color: var(--rr-slate-600);
  border-top: 1px solid var(--rr-slate-200);
}}

/* Squad Cards */
.squad-card {{
  background: #FFFFFF;
  border-radius: var(--radius-sm);
  padding: 1.35rem;
  border: 1px solid var(--rr-slate-200);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}

.batter-border {{ border-top: 3px solid var(--rr-pink); }}
.bowler-border {{ border-top: 3px solid var(--rr-blue); }}

.squad-card-header {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.85rem;
}}

.squad-card-title {{
  display: flex;
  align-items: center;
  gap: 0.45rem;
}}

.rank-mini {{
  width: 22px;
  height: 22px;
  border-radius: 50%;
  color: #FFFFFF;
  font-weight: 700;
  font-size: 0.75rem;
  font-family: 'JetBrains Mono', monospace;
  display: flex;
  align-items: center;
  justify-content: center;
}}

.pink-bg {{ background: var(--rr-pink); }}
.blue-bg {{ background: var(--rr-blue); }}

.name-bold {{
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--rr-navy);
}}

.team-tag {{
  background: var(--rr-slate-100);
  color: var(--rr-slate-600);
  padding: 0.12rem 0.4rem;
  border-radius: var(--radius-sm);
  font-size: 0.7rem;
  font-weight: 600;
}}

.squad-card-sub {{
  color: var(--rr-slate-500);
  font-size: 0.75rem;
  margin-top: 0.15rem;
}}

.squad-metrics-row {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.5rem;
  background: var(--rr-slate-50);
  padding: 0.65rem;
  border-radius: var(--radius-sm);
  margin-bottom: 0.85rem;
  border: 1px solid var(--rr-slate-200);
}}

.metric-mini {{
  display: flex;
  flex-direction: column;
  text-align: center;
}}

.m-label {{
  font-size: 0.65rem;
  color: var(--rr-slate-500);
  font-weight: 600;
  text-transform: uppercase;
}}

.m-val {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.88rem;
  font-weight: 700;
  margin-top: 0.1rem;
}}

.squad-section {{
  margin-bottom: 0.75rem;
}}

.section-tag-mini {{
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 0.2rem;
}}

.squad-text {{
  font-size: 0.84rem;
  color: var(--rr-slate-600);
  line-height: 1.5;
}}

.squad-footer {{
  background: #FFFBEB;
  border-left: 2px solid var(--rr-gold);
  padding: 0.55rem 0.75rem;
  font-size: 0.8rem;
  color: #92400E;
  line-height: 1.45;
  margin-top: 0.4rem;
}}

/* Modal Scouting Drawer */
.modal-overlay {{
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(4px);
  z-index: 999;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}}

.modal-content {{
  background: #FFFFFF;
  border-radius: var(--radius-md);
  max-width: 640px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--rr-slate-300);
}}

.modal-header {{
  background: #0F172A;
  color: #FFFFFF;
  padding: 1.5rem 1.75rem;
  position: relative;
}}

.modal-close {{
  position: absolute;
  top: 1rem;
  right: 1.25rem;
  background: transparent;
  border: none;
  color: var(--rr-slate-300);
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0.25rem;
}}

.modal-close:hover {{
  color: #FFFFFF;
}}

.modal-body {{
  padding: 1.75rem;
}}

/* Utility Classes */
.text-pink {{ color: var(--rr-pink); }}
.text-blue {{ color: var(--rr-blue); }}
.text-navy {{ color: var(--rr-navy); }}
.text-green {{ color: var(--rr-emerald); }}
.text-muted {{ color: var(--rr-slate-400); }}
.text-center {{ text-align: center; }}
.font-mono {{ font-family: 'JetBrains Mono', monospace; }}
.font-bold {{ font-weight: 700; }}

/* Footer */
footer {{
  background: #0F172A;
  color: var(--rr-slate-400);
  text-align: center;
  padding: 2.5rem 1.5rem;
  border-top: 1px solid #1E293B;
  margin-top: 3rem;
}}

footer a {{
  color: #F472B6;
  text-decoration: none;
}}

footer a:hover {{
  text-decoration: underline;
}}

/* Print Optimization */
@media print {{
  .top-bar, .toolbar, .btn-dossier, footer {{
    display: none !important;
  }}
  body {{
    background: #FFFFFF;
    color: #000000;
    padding: 0;
  }}
  .executive-header {{
    background: #0F172A !important;
    color: #FFFFFF !important;
    padding: 1.75rem 1rem !important;
  }}
  .section-card {{
    box-shadow: none !important;
    border: 1px solid #CCCCCC !important;
    page-break-inside: avoid;
    margin-bottom: 1.5rem !important;
    padding: 1.25rem !important;
  }}
  table {{
    font-size: 0.72rem !important;
  }}
  thead th {{
    background: #0F172A !important;
    color: #FFFFFF !important;
    padding: 0.35rem !important;
  }}
  tbody td {{
    padding: 0.3rem !important;
  }}
  .squad-card {{
    page-break-inside: avoid;
    margin-bottom: 0.75rem !important;
  }}
}}
</style>
</head>
<body>

<!-- TOP BAR: Ultra clean, only PDF and GitHub -->
<div class="top-bar">
  <div class="top-bar-inner">
    <button class="btn-pdf" onclick="window.print()">Save as PDF</button>
    <a href="https://github.com/Shubhdix9/RR" target="_blank" class="btn-github">GitHub</a>
  </div>
</div>

<!-- EXECUTIVE HEADER -->
<header class="executive-header">
  <div class="header-container">
    <div class="doc-metadata">
      <span class="doc-tag">Rajasthan Royals War Room</span>
      <span>IPL 2027 Auction Recruitment Dossier</span>
    </div>

    <h1 class="header-title">
      Target Identification Under High Match Leverage
    </h1>
    <p class="header-subtitle">
      Pre-delivery state evaluation across 200,999 deliveries (2022–2026) isolating high-leverage middle-order finishers and middle-to-death bowlers for Sawai Mansingh Stadium conditions.
    </p>

    <!-- QUANTITATIVE BASELINE STRIP -->
    <div class="baseline-strip">
      <div class="strip-item">
        <div class="strip-val pink">200,999</div>
        <div class="strip-label">Deliveries Evaluated</div>
        <div class="strip-desc">Ball-by-ball empirical database</div>
      </div>
      <div class="strip-item">
        <div class="strip-val blue">883</div>
        <div class="strip-label">Match Sample</div>
        <div class="strip-desc">371 IPL and 512 T20I fixtures</div>
      </div>
      <div class="strip-item">
        <div class="strip-val gold">42.26</div>
        <div class="strip-label">P80 Leverage Threshold</div>
        <div class="strip-desc">Calibrated 80th percentile cutoff</div>
      </div>
      <div class="strip-item">
        <div class="strip-val green">20.0%</div>
        <div class="strip-label">High-Pressure Deliveries</div>
        <div class="strip-desc">Isolating top 20% critical game states</div>
      </div>
    </div>
  </div>
</header>

<main class="main-wrapper">

  <!-- SECTION 1: RECRUITMENT CONSTRAINTS & FEASIBILITY -->
  <section class=section-card>
    <div class=section-head>
      <h2 class=section-title>1. Operational Constraints &amp; Auction Scenario Modeling</h2>
      <p class=section-lead>Establishing objective boundary conditions and strategic scenario parameters for recruitment planning</p>
    </div>

    <!-- METHODOLOGICAL NOTICE & DISCLAIMER -->
    <div style="background:#F8FAFC; border:1px solid #CBD5E1; border-left:4px solid var(--rr-navy); padding:1rem 1.25rem; margin-bottom:1.5rem; border-radius:var(--radius-sm);">
      <div style="font-size:0.78rem; font-weight:700; color:var(--rr-navy); text-transform:uppercase; letter-spacing:0.04em; margin-bottom:0.25rem;">
        Analytical Architecture: Separation of Performance Ranking vs. Auction Shortlist
      </div>
      <p style="font-size:0.84rem; color:var(--rr-slate-600); line-height:1.55;">
        To ensure methodological clarity, this dossier maintains a strict separation between <strong>(A) Objective On-Field Performance Rankings</strong> (derived exclusively from mathematical modeling across 200,999 deliveries) and <strong>(B) Operational Auction Strategy Shortlists</strong>. All auction valuations, purse allocations, and availability profiles represent theoretical simulation models developed for strategic planning based on historical mega-auction distributions. They do not constitute official, confirmed retention, release, or contractual statements by Rajasthan Royals, rival franchises, or the IPL Governing Council.
      </p>
    </div>

    <div class="grid-2">
      <div class="rule-box">
        <div class="rule-title text-pink">1. Strategic Scenario: Marquee Retention Constraints</div>
        <p class="rule-desc">
          For simulation integrity, franchise cornerstones commanding top-bracket retention commitments (e.g. ₹18–25+ Cr) are modeled as statistically unavailable in the open auction pool. Modeling these players as actionable targets creates severe budget distortion; our war room engine therefore focuses analytical capital on high-value, contested market assets.
        </p>
      </div>

      <div class="rule-box">
        <div class="rule-title text-navy">2. Regulatory Eligibility Scope</div>
        <p class="rule-desc">
          Pursuant to BCCI governance policies and IPL player registration directives, players not registered in the active BCCI auction pool are excluded from candidate recruitment simulations to preserve operational feasibility.
        </p>
      </div>

      <div class="rule-box">
        <div class="rule-title text-blue">3. Squad Gap Alignment: Pure #4–7 Finishers</div>
        <p class="rule-desc">
          Rajasthan Royals have solidified their core top-order foundation in Yashasvi Jaiswal, Vaibhav Sooryavanshi, and Sanju Samson. Allocating auction purse to top-order anchors creates roster redundancy. Batting evaluations strictly isolate middle-order enforcers and death finishers (Batting Positions 4, 5, 6, 7).
        </p>
      </div>

      <div class="rule-box">
        <div class="rule-title text-green">4. Phase Specialization: Middle &amp; Death Overs (7–20)</div>
        <p class="rule-desc">
          RR's new-ball seam attack is established with Jofra Archer, Sandeep Sharma, and Nandre Burger. The war room's urgent tactical requirements are middle-overs spin restriction (Overs 7–15) and death-overs yorker execution (Overs 16–20). Bowlers delivering &gt;25% of balls in the powerplay are filtered out.
        </p>
      </div>
    </div>
  </section>

  <!-- SECTION 2: MATHEMATICAL MODEL -->
  <section class="section-card">
    <div class="section-head">
      <h2 class="section-title">2. Pre-Delivery Leverage Framework &amp; Methodology</h2>
      <p class="section-lead">Quantifying pressure strictly on the pre-delivery match state across 200,999 balls to prevent outcome leakage</p>
    </div>

    <div class="grid-2">
      <div class="formula-container">
        <div class="formula-title text-pink">Second Innings: Chasing Leverage Model</div>
        <p style="font-size:0.84rem; color:var(--rr-slate-600);">Evaluates required run rate stress, wicket depletion, and time decay:</p>
        <div class="formula-box">
          PS = 0.35 × S_RRR + 0.30 × S_wkt + 0.20 × S_urgency + 0.15 × S_leverage
        </div>
        <ul class="formula-notes">
          <li><strong>S_RRR (35%):</strong> min[100, (RRR / 8.50)^2.2 × 28] — non-linear acceleration when RRR exceeds par.</li>
          <li><strong>S_wkt (30%):</strong> (Wickets Down / 9)^1.8 × 100 — compounding resource scarcity.</li>
          <li><strong>S_urgency (20%):</strong> [1 - (Balls Left / 120)]^1.5 × 100 — exponential death-overs urgency.</li>
          <li><strong>S_leverage (15%):</strong> 100 × [4 × WP × (1 - WP)] — normalized win probability leverage index [0, 100].</li>
        </ul>
        <div style="margin-top:0.65rem; font-size:0.78rem; color:#475569; background:#FFFFFF; padding:0.5rem 0.75rem; border-radius:var(--radius-sm); border:1px solid #CBD5E1;">
          <strong>Mathematical Normalization Note:</strong> To ensure dimensional parity, the win-probability leverage metric is normalized to a [0, 100] scale as S_leverage = 100 × [4 · WP · (1 - WP)]. This brings all four terms to an identical 0–100 scale, with weights summing strictly to 1.00 (PS ∈ [0, 100]).
        </div>
      </div>

      <div class="formula-container">
        <div class="formula-title text-blue">First Innings: Target-Setting Leverage Model</div>
        <p style="font-size:0.84rem; color:var(--rr-slate-600);">Evaluates phase scoring variance, top-order collapse, and par score deficit:</p>
        <div class="formula-box">
          PS = [40 × S_phase + 35 × S_collapse + 25 × S_deficit] × Knockout_Multiplier
        </div>
        <ul class="formula-notes">
          <li><strong>S_phase (40%):</strong> Overs 16–20 carry maximum scoring variance (10.48 RPO baseline par).</li>
          <li><strong>S_collapse (35%):</strong> Evaluates crisis recovery when wickets fall ahead of expected curve.</li>
          <li><strong>S_deficit (25%):</strong> Pressure when cumulative scoring lags behind the 8.50 RPO par total.</li>
          <li><strong>Knockout Multiplier:</strong> 1.15× multiplier applied for playoffs, qualifiers, and finals.</li>
        </ul>
      </div>
    </div>

    <!-- EMPIRICAL BENCHMARKS -->
    <div style="margin-top:1.25rem; background:var(--rr-slate-50); border:1px solid var(--rr-slate-200); border-radius:var(--radius-sm); padding:1.25rem;">
      <div style="font-size:0.88rem; font-weight:700; color:var(--rr-navy); margin-bottom:0.75rem;">
        Empirical Phase Benchmarks from 200,999 Deliveries
      </div>
      <div class="grid-3">
        <div style="background:#FFFFFF; padding:0.85rem; border-radius:var(--radius-sm); text-align:center; border:1px solid var(--rr-slate-200);">
          <div style="font-size:0.72rem; font-weight:700; color:var(--rr-blue); text-transform:uppercase;">Powerplay (Overs 1–6)</div>
          <div style="font-size:1.35rem; font-weight:700; color:var(--rr-navy); font-family:'JetBrains Mono',monospace;">8.02 RPO</div>
          <div style="font-size:0.72rem; color:var(--rr-slate-500);">Expected Wickets: 0.048 / ball</div>
        </div>
        <div style="background:#FFFFFF; padding:0.85rem; border-radius:var(--radius-sm); text-align:center; border:1px solid var(--rr-slate-200);">
          <div style="font-size:0.72rem; font-weight:700; color:var(--rr-navy); text-transform:uppercase;">Middle Overs (Overs 7–15)</div>
          <div style="font-size:1.35rem; font-weight:700; color:var(--rr-navy); font-family:'JetBrains Mono',monospace;">7.74 RPO</div>
          <div style="font-size:0.72rem; color:var(--rr-slate-500);">Expected Wickets: 0.051 / ball</div>
        </div>
        <div style="background:#FFFFFF; padding:0.85rem; border-radius:var(--radius-sm); text-align:center; border:1px solid var(--rr-slate-200);">
          <div style="font-size:0.72rem; font-weight:700; color:var(--rr-pink); text-transform:uppercase;">Death Overs (Overs 16–20)</div>
          <div style="font-size:1.35rem; font-weight:700; color:var(--rr-pink); font-family:'JetBrains Mono',monospace;">10.48 RPO</div>
          <div style="font-size:0.72rem; color:var(--rr-slate-500);">Overs 19–20: 11.49 RPO (0.089 wkt/ball)</div>
        </div>
      </div>
    </div>

    <!-- FIGURE 1 -->
    <div class="figure-block">
      <img src="data:image/png;base64,{fig1_b64}" alt="Figure 1: Pre-Delivery Pressure Score Distribution">
      <div class="figure-meta">
        <strong>Figure 1:</strong> Pre-delivery pressure score distribution across 200,999 deliveries, establishing the P80 cutoff (42.26) isolating the top 20% highest-leverage game situations.
      </div>
    </div>
  </section>

  <!-- SECTION 3: TOP 10 BATTERS -->
  <section class="section-card">
    <div class="section-head">
      <h2 class="section-title">3. Top 10 Middle-Order &amp; Death Batters (Positions 4–7)</h2>
      <p class="section-lead">Ranked by Clutch Batting Index (CBI): 30% HP SR, 25% xRA, 20% ΔSR, 15% Boundaries, 10% Consistency</p>
    <div style="background:#FDF2F8; border:1px solid #FBCFE8; border-left:4px solid var(--rr-pink); padding:0.75rem 1rem; margin-top:0.75rem; border-radius:var(--radius-sm);">
      <div style="font-size:0.76rem; font-weight:700; color:var(--rr-pink); text-transform:uppercase; margin-bottom:0.15rem;">
        Scoring Rule Reconciliation: Composite Batting Index (CBI)
      </div>
      <p style="font-size:0.82rem; color:#831843; line-height:1.5;">
        Rankings strictly follow the final reconciled <strong>Composite Batting Index (CBI)</strong>, integrating Bayesian sample reliability W(N) = N / (N + 30). High-volume sample execution (e.g. Ashutosh Sharma: 233 balls, +55.8 xRA/100) receives superior confidence scoring (88.2) ahead of lower-sample bursts, ensuring monotonic alignment between displayed score and rank order.
      </p>
    </div>
    </div>

    <div class="toolbar">
      <input type="text" class="filter-input" id="batterSearch" placeholder="Filter by player name or team..." onkeyup="filterTable('batter')">
      <span class="table-instruction">Click any player for detailed scouting notes</span>
    </div>

    <div class="table-scroll">
      <table id="batterTable">
        <thead>
          <tr>
            <th class="text-center">Rank</th>
            <th>Player Name</th>
            <th class="text-center">CBI Score</th>
            <th class="text-center">HP Balls</th>
            <th class="text-center">HP Strike Rate</th>
            <th class="text-center">Base SR</th>
            <th class="text-center">ΔSR Jump</th>
            <th class="text-center">Dot%</th>
            <th class="text-center">Boundary%</th>
            <th class="text-center">Phase</th>
            <th>Tactical Role</th>
            <th class="text-center">Dossier</th>
          </tr>
        </thead>
        <tbody>
{batter_rows_html}
        </tbody>
      </table>
    </div>

    <!-- FIGURE 2 -->
    <div class="figure-block">
      <img src="data:image/png;base64,{fig2_b64}" alt="Figure 2: Batting Delta Strike Rate">
      <div class="figure-meta">
        <strong>Figure 2:</strong> Career baseline strike rate vs high-pressure strike rate (ΔSR) across top 10 finishers, highlighting major strike rate increases under pressure from Ashutosh Sharma (+46.1) and Shubham Dubey (+46.9).
      </div>
    </div>
  </section>

  <!-- SECTION 4: TOP 10 BOWLERS -->
  <section class="section-card">
    <div class="section-head">
      <h2 class="section-title">4. Top 10 Middle-Overs &amp; Death Bowlers (Overs 7–20)</h2>
      <p class="section-lead">Ranked by Pressure Bowling Index (PBI): 30% xRP, 25% Econ Suppression, 20% Wickets, 15% ΔEcon, 10% Consistency</p>
    </div>

    <div class="toolbar">
      <input type="text" class="filter-input" id="bowlerSearch" placeholder="Filter by player name or team..." onkeyup="filterTable('bowler')">
      <span class="table-instruction">Click any player for detailed scouting notes</span>
    </div>

    <div class="table-scroll">
      <table id="bowlerTable">
        <thead>
          <tr>
            <th class="text-center">Rank</th>
            <th>Player Name</th>
            <th class="text-center">PBI Score</th>
            <th class="text-center">HP Balls</th>
            <th class="text-center">HP Wkts</th>
            <th class="text-center">HP Economy</th>
            <th class="text-center">Base Econ</th>
            <th class="text-center">ΔEcon Suppression</th>
            <th class="text-center">Dot%</th>
            <th class="text-center">Phase</th>
            <th>Tactical Role</th>
            <th class="text-center">Dossier</th>
          </tr>
        </thead>
        <tbody>
{bowler_rows_html}
        </tbody>
      </table>
    </div>

    <!-- FIGURE 3 -->
    <div class="figure-block">
      <img src="data:image/png;base64,{fig3_b64}" alt="Figure 3: Bowling Delta Economy">
      <div class="figure-meta">
        <strong>Figure 3:</strong> Baseline vs high-pressure economy rate (ΔEcon). Positive deltas demonstrate bowlers who restrict scoring under leverage (e.g. Umran Malik +1.71 suppression, Gudakesh Motie +0.36).
      </div>
    </div>
  </section>

  <!-- SECTION 5: SQUAD FIT & JAIPUR CONDITIONS -->
  <section class="section-card">
    <div class="section-head">
      <h2 class="section-title">5. Rajasthan Royals Squad Fit &amp; Sawai Mansingh Stadium Strategy</h2>
      <p class="section-lead">Aligning statistical reliability with venue dimensions and roster construction for the IPL 2027 auction</p>
    </div>

    <div style="background:#FFFBEB; border:1px solid #FCD34D; border-radius:var(--radius-sm); padding:1.15rem; margin-bottom:1.75rem;">
      <div style="font-weight:700; font-size:0.95rem; color:#92400E; margin-bottom:0.25rem;">
        Sawai Mansingh Stadium (Jaipur) Venue Blueprint
      </div>
      <p style="font-size:0.85rem; color:#78350F; line-height:1.55;">
        SMS Stadium features large <strong>75–82 meter straight and square boundaries</strong>. Unlike smaller outfields where mistimed edges carry over the ropes, Jaipur penalizes false shots while rewarding batters with genuine 360-degree boundary clearance and spinners who deceive in flight. Our recruitment targets directly address RR's two structural gaps: <strong>explosive #6/7 boundary execution</strong> and <strong>middle-overs spin control</strong>.
      </p>
    </div>

    <!-- BATTERS SQUAD FIT CARDS -->
    <h3 style="font-size:1.1rem; font-weight:700; color:var(--rr-pink); margin-bottom:0.85rem; border-bottom:2px solid var(--rr-pink); padding-bottom:0.35rem;">
      Batting Targets (#4–7 Finishers): Tactical Fit for All 10 Players
    </h3>
    <div class="grid-2" style="margin-bottom:2rem;">
{batter_cards_html}
    </div>

    <!-- BOWLERS SQUAD FIT CARDS -->
    <h3 style="font-size:1.1rem; font-weight:700; color:var(--rr-blue); margin-bottom:0.85rem; border-bottom:2px solid var(--rr-blue); padding-bottom:0.35rem;">
      Bowling Targets (Overs 7–20 Specialists): Tactical Fit for All 10 Players
    </h3>
    <div class="grid-2">
{bowler_cards_html}
    </div>

    <!-- FIGURE 4 -->
    <div class="figure-block" style="margin-top:2rem;">
      <img src="data:image/png;base64,{fig4_b64}" alt="Figure 4: RR Auction Target Matrix">
      <div class="figure-meta">
        <strong>Figure 4:</strong> Rajasthan Royals IPL 2027 Auction Target Portfolio: Performance Index vs Experience Sample Volume, illustrating the balance between proven high-volume assets and domestic value prospects.
      </div>
    </div>
  </section>


  <!-- SECTION 6: VALUE ECONOMICS, RISK ADJUSTMENT & AUCTION CONTINGENCY -->
  <section class="section-card">
    <div class="section-head">
      <h2 class="section-title">6. Value Economics, Risk Modeling &amp; Auction Contingency</h2>
      <p class="section-lead">Incorporating role scarcity premiums, multi-factor risk discounting, and bidding sensitivity scenarios</p>
    </div>

    <!-- 1. ROLE SCARCITY MATRIX -->
    <div style="margin-bottom:1.75rem;">
      <h3 style="font-size:1.05rem; font-weight:700; color:var(--rr-navy); margin-bottom:0.65rem;">
        6.1 Role Scarcity Multipliers (Indian Market Premium)
      </h3>
      <p style="font-size:0.86rem; color:var(--rr-slate-600); margin-bottom:0.75rem; line-height:1.55;">
        In the IPL auction dynamic, Indian domestic specialists command significant market scarcity premiums because the playing XI is restricted to four overseas players. A scarcity multiplier is applied to prioritize high-leverage Indian assets:
      </p>
      
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th>Role Archetype</th>
              <th class="text-center">Scarcity Multiplier</th>
              <th>Market Dynamics &amp; War Room Justification</th>
              <th>RR Target Alignment</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Indian Death Finisher (#6/7)</strong></td>
              <td class="text-center font-mono font-bold text-pink">1.40×</td>
              <td style="font-size:0.82rem; color:var(--rr-slate-700);">Extreme market scarcity; few Indian domestic batters possess 180+ strike rates under death leverage.</td>
              <td><span class="player-name">Ashutosh Sharma</span>, <span class="player-name">Shubham Dubey</span></td>
            </tr>
            <tr>
              <td><strong>Indian Express Pacer (150+ km/h)</strong></td>
              <td class="text-center font-mono font-bold text-blue">1.35×</td>
              <td style="font-size:0.82rem; color:var(--rr-slate-700);">High barrier to entry; forces opposition mistakes on large outfields without utilizing an overseas slot.</td>
              <td><span class="player-name">Umran Malik</span></td>
            </tr>
            <tr>
              <td><strong>Indian Wrist Spinner</strong></td>
              <td class="text-center font-mono font-bold text-blue">1.35×</td>
              <td style="font-size:0.82rem; color:var(--rr-slate-700);">High-value partnership breaker in overs 10–16; historically dominant at Sawai Mansingh Stadium.</td>
              <td><span class="player-name">Yuzvendra Chahal</span></td>
            </tr>
            <tr>
              <td><strong>Indian Middle Spin Enforcer</strong></td>
              <td class="text-center font-mono font-bold text-navy">1.25×</td>
              <td style="font-size:0.82rem; color:var(--rr-slate-700);">Controls run rate against spin bowling in overs 9–14; balances lineup flexibility.</td>
              <td><span class="player-name">Sameer Rizvi</span>, <span class="player-name">Washington Sundar</span></td>
            </tr>
            <tr>
              <td><strong>Overseas Specialist Finisher / Pacer</strong></td>
              <td class="text-center font-mono font-bold text-muted">1.00×</td>
              <td style="font-size:0.82rem; color:var(--rr-slate-700);">Higher global supply across international leagues; constrained strictly by 4-overseas limit.</td>
              <td><span class="player-name">Tim David</span>, <span class="player-name">Matheesha Pathirana</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 2. RISK ADJUSTMENT FRAMEWORK -->
    <div style="margin-bottom:1.75rem;">
      <h3 style="font-size:1.05rem; font-weight:700; color:var(--rr-navy); margin-bottom:0.65rem;">
        6.2 Multi-Factor Risk Adjustment Framework
      </h3>
      <p style="font-size:0.86rem; color:var(--rr-slate-600); margin-bottom:0.75rem; line-height:1.55;">
        Every target is evaluated through a composite risk deduction ($r_i$) to prevent over-investing in injury-prone, volatile, or calendar-conflicted assets:
      </p>
      
      <div class="formula-box" style="margin-bottom:0.85rem;">
        Composite Risk (r_i) = 0.35 × Injury_Risk + 0.30 × Availability_Risk + 0.20 × Volatility_Risk + 0.15 × Age_Risk
      </div>

      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th>Target Player</th>
              <th>Role Profile</th>
              <th class="text-center">Injury Risk (35%)</th>
              <th class="text-center">Availability (30%)</th>
              <th class="text-center">Volatility (20%)</th>
              <th class="text-center">Age Risk (15%)</th>
              <th class="text-center">Total Risk (r_i)</th>
              <th class="text-center">Risk Rating</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Ashutosh Sharma</strong></td>
              <td>Domestic Death Finisher</td>
              <td class="text-center font-mono">0.05</td>
              <td class="text-center font-mono">0.00</td>
              <td class="text-center font-mono">0.12</td>
              <td class="text-center font-mono">0.05</td>
              <td class="text-center font-mono font-bold text-green">0.059</td>
              <td class="text-center"><span class="phase-pill" style="background:#ECFDF5; color:#065F46;">Very Low</span></td>
            </tr>
            <tr>
              <td><strong>Sameer Rizvi</strong></td>
              <td>Domestic Spin Smasher</td>
              <td class="text-center font-mono">0.05</td>
              <td class="text-center font-mono">0.00</td>
              <td class="text-center font-mono">0.10</td>
              <td class="text-center font-mono">0.00</td>
              <td class="text-center font-mono font-bold text-green">0.038</td>
              <td class="text-center"><span class="phase-pill" style="background:#ECFDF5; color:#065F46;">Very Low</span></td>
            </tr>
            <tr>
              <td><strong>Umran Malik</strong></td>
              <td>Express Pace Bowler</td>
              <td class="text-center font-mono">0.15</td>
              <td class="text-center font-mono">0.00</td>
              <td class="text-center font-mono">0.18</td>
              <td class="text-center font-mono">0.05</td>
              <td class="text-center font-mono font-bold text-blue">0.096</td>
              <td class="text-center"><span class="phase-pill" style="background:#EFF6FF; color:#1E40AF;">Low</span></td>
            </tr>
            <tr>
              <td><strong>Gudakesh Motie</strong></td>
              <td>Left-Arm Finger Spin</td>
              <td class="text-center font-mono">0.08</td>
              <td class="text-center font-mono">0.15</td>
              <td class="text-center font-mono">0.10</td>
              <td class="text-center font-mono">0.10</td>
              <td class="text-center font-mono font-bold text-blue">0.108</td>
              <td class="text-center"><span class="phase-pill" style="background:#EFF6FF; color:#1E40AF;">Low</span></td>
            </tr>
            <tr>
              <td><strong>Washington Sundar</strong></td>
              <td>Domestic Finger Spin AR</td>
              <td class="text-center font-mono">0.20</td>
              <td class="text-center font-mono">0.00</td>
              <td class="text-center font-mono">0.10</td>
              <td class="text-center font-mono">0.05</td>
              <td class="text-center font-mono font-bold text-navy">0.098</td>
              <td class="text-center"><span class="phase-pill" style="background:#EFF6FF; color:#1E40AF;">Low</span></td>
            </tr>
            <tr>
              <td><strong>Yuzvendra Chahal</strong></td>
              <td>Leg-Spin Specialist</td>
              <td class="text-center font-mono">0.05</td>
              <td class="text-center font-mono">0.00</td>
              <td class="text-center font-mono">0.10</td>
              <td class="text-center font-mono">0.28</td>
              <td class="text-center font-mono font-bold text-gold">0.080</td>
              <td class="text-center"><span class="phase-pill" style="background:#FEF3C7; color:#92400E;">Moderate (Age)</span></td>
            </tr>
            <tr>
              <td><strong>Liam Livingstone</strong></td>
              <td>Overseas Power Enforcer</td>
              <td class="text-center font-mono">0.18</td>
              <td class="text-center font-mono">0.20</td>
              <td class="text-center font-mono">0.22</td>
              <td class="text-center font-mono">0.15</td>
              <td class="text-center font-mono font-bold text-gold">0.189</td>
              <td class="text-center"><span class="phase-pill" style="background:#FEF3C7; color:#92400E;">Moderate (ECB/Inj)</span></td>
            </tr>
            <tr>
              <td><strong>Matheesha Pathirana</strong></td>
              <td>Slingy Death Pacer</td>
              <td class="text-center font-mono">0.22</td>
              <td class="text-center font-mono">0.10</td>
              <td class="text-center font-mono">0.12</td>
              <td class="text-center font-mono">0.00</td>
              <td class="text-center font-mono font-bold text-gold">0.131</td>
              <td class="text-center"><span class="phase-pill" style="background:#FEF3C7; color:#92400E;">Moderate (Hamstring)</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 3. PROJECTED SQUAD IMPACT: BEFORE VS AFTER -->
    <div style="margin-bottom:1.75rem;">
      <h3 style="font-size:1.05rem; font-weight:700; color:var(--rr-navy); margin-bottom:0.65rem;">
        6.3 Projected Rajasthan Royals Squad Impact (Before vs. After Model Execution)
      </h3>
      <p style="font-size:0.86rem; color:var(--rr-slate-600); margin-bottom:0.75rem; line-height:1.55;">
        Comparing Rajasthan Royals' historical baseline phase outputs (2024–2025) against projected performance after integrating our top-ranked high-leverage specialists:
      </p>

      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th>Match Phase</th>
              <th>Critical Performance Metric</th>
              <th class="text-center">Historical Baseline</th>
              <th class="text-center">Projected Output</th>
              <th class="text-center">Net Change</th>
              <th>Key Target Contributors</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Death Batting (Overs 16–20)</strong></td>
              <td>Death Strike Rate</td>
              <td class="text-center font-mono">144.6 SR</td>
              <td class="text-center font-mono font-bold text-pink">181.2 SR</td>
              <td class="text-center font-mono font-bold text-green">+25.3%</td>
              <td>Ashutosh Sharma (+46.1 ΔSR), Shubham Dubey, Sameer Rizvi</td>
            </tr>
            <tr>
              <td><strong>Death Batting (Overs 16–20)</strong></td>
              <td>Boundary Ball Percentage</td>
              <td class="text-center font-mono">16.8%</td>
              <td class="text-center font-mono font-bold text-pink">24.5%</td>
              <td class="text-center font-mono font-bold text-green">+45.8%</td>
              <td>Donovan Ferreira (27.0%), Tim David (26.5%)</td>
            </tr>
            <tr>
              <td><strong>Middle Bowling (Overs 7–15)</strong></td>
              <td>Middle Overs Economy Rate</td>
              <td class="text-center font-mono">8.65 RPO</td>
              <td class="text-center font-mono font-bold text-blue">7.48 RPO</td>
              <td class="text-center font-mono font-bold text-green">-1.17 RPO</td>
              <td>Gudakesh Motie (7.50 RPO), Mitchell Santner (7.58 RPO)</td>
            </tr>
            <tr>
              <td><strong>Middle Bowling (Overs 7–15)</strong></td>
              <td>Average Wickets Taken / Match</td>
              <td class="text-center font-mono">2.2 Wkts</td>
              <td class="text-center font-mono font-bold text-blue">3.1 Wkts</td>
              <td class="text-center font-mono font-bold text-green">+40.9%</td>
              <td>Yuzvendra Chahal (50 HP wkts), Noor Ahmad (26 HP wkts)</td>
            </tr>
            <tr>
              <td><strong>Death Bowling (Overs 16–20)</strong></td>
              <td>Death Overs Economy Rate</td>
              <td class="text-center font-mono">10.92 RPO</td>
              <td class="text-center font-mono font-bold text-navy">9.22 RPO</td>
              <td class="text-center font-mono font-bold text-green">-15.6%</td>
              <td>Umran Malik (+1.71 suppression), Matheesha Pathirana (41 wkts)</td>
            </tr>
            <tr>
              <td><strong>Tactical Auction Purse</strong></td>
              <td>Purse Allocation Efficiency</td>
              <td class="text-center font-mono">Top-Heavy Star Drain</td>
              <td class="text-center font-mono font-bold text-navy">Value-Optimized</td>
              <td class="text-center font-mono font-bold text-green">₹18–25 Cr Saved</td>
              <td>Targeting domestic uncapped steals over inflated superstar contracts</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 4. BIDDING STRATEGY & SENSITIVITY CONTINGENCY -->
    <div>
      <h3 style="font-size:1.05rem; font-weight:700; color:var(--rr-navy); margin-bottom:0.65rem;">
        6.4 Bidding Priority Tiers &amp; Sensitivity Contingency Scenarios (Plan B)
      </h3>
      <p style="font-size:0.86rem; color:var(--rr-slate-600); margin-bottom:0.75rem; line-height:1.55;">
        Live auctions create sudden bidding spikes. Below is Rajasthan Royals' structured tier priority and contingency pivot matrix:
      </p>

      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th>Priority Tier</th>
              <th>Primary Targets</th>
              <th class="text-center">Ceiling Bid</th>
              <th>Strategic Role in XI</th>
              <th>Contingency Pivot Plan (If Price Surpasses Ceiling)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="rank-pill badge-gold">Tier 1</span> <strong>Must-Have</strong></td>
              <td><strong>Ashutosh Sharma</strong>, <strong>Umran Malik</strong></td>
              <td class="text-center font-mono font-bold">₹5.5 Cr</td>
              <td>Solves #7 death finishing and 150+ km/h middle/death pace tandem with Archer.</td>
              <td style="font-size:0.82rem; color:var(--rr-slate-700);">If Ashutosh exceeds ₹5.5 Cr, pivot purse immediately to <strong>Shubham Dubey</strong> (Est. ₹2.5 Cr) or <strong>Shashank Singh</strong>.</td>
            </tr>
            <tr>
              <td><span class="rank-pill badge-silver">Tier 2</span> <strong>High Priority</strong></td>
              <td><strong>Sameer Rizvi</strong>, <strong>Gudakesh Motie</strong></td>
              <td class="text-center font-mono font-bold">₹4.5 Cr</td>
              <td>Neutralizes opposition spin in middle overs and delivers 7.50 RPO defensive squeeze.</td>
              <td style="font-size:0.82rem; color:var(--rr-slate-700);">If Motie becomes contested, pivot to <strong>Mitchell Santner</strong> (Est. ₹3.5 Cr) or <strong>Sikandar Raza</strong> (dual asset).</td>
            </tr>
            <tr>
              <td><span class="rank-pill badge-bronze">Tier 3</span> <strong>Tactical Value</strong></td>
              <td><strong>Shubham Dubey</strong>, <strong>Donovan Ferreira</strong></td>
              <td class="text-center font-mono font-bold">₹3.0 Cr</td>
              <td>Left-hand death hitting and dynamic multi-utility wicketkeeping depth.</td>
              <td style="font-size:0.82rem; color:var(--rr-slate-700);">If Ferreira inflates, lock in <strong>Mark Chapman</strong> (Est. ₹2.0 Cr) for left-handed middle stability.</td>
            </tr>
            <tr>
              <td><span class="rank-pill badge-plain">Tier 4</span> <strong>Marquee Impact</strong></td>
              <td><strong>Yuzvendra Chahal</strong>, <strong>Matheesha Pathirana</strong></td>
              <td class="text-center font-mono font-bold">₹10.5 Cr</td>
              <td>Game-breaking IPL all-time wicket taker or generational slingy death spearhead.</td>
              <td style="font-size:0.82rem; color:var(--rr-slate-700);">If Chahal enters bidding war >₹11 Cr, pivot immediately to <strong>Noor Ahmad</strong> (Est. ₹6.5 Cr) + <strong>Washington Sundar</strong>.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- SECTION 7: STATISTICAL RIGOR & LIMITATIONS -->
  <section class="section-card">
    <div class="section-head">
      <h2 class="section-title">7. Statistical Rigor, Bayesian Shrinkage &amp; Model Limitations</h2>
      <p class="section-lead">Validation techniques, sample adjustments, and documented model scope</p>
    </div>

    <div class="grid-2">
      <div style="background:var(--rr-slate-50); border:1px solid var(--rr-slate-200); border-radius:var(--radius-sm); padding:1.25rem;">
        <div style="font-weight:700; font-size:0.92rem; color:var(--rr-navy); margin-bottom:0.5rem;">
          Sample Corrections &amp; Consistency
        </div>
        <ul style="font-size:0.84rem; color:var(--rr-slate-600); line-height:1.65; margin-left:1.1rem;">
          <li><strong>Empirical Bayes Shrinkage:</strong> Regresses small samples toward league priors (K=50 balls for batting, K=60 for bowling) to reduce small-sample distortion.</li>
          <li><strong>Clutch Consistency Rate (CCR):</strong> Measures the percentage of high-pressure matches where a player delivered net-positive contributions (xRA &gt; 0 or xRP &gt; 0).</li>
          <li><strong>Competition Weighting:</strong> IPL fixtures weighted at 1.30×; ICC T20 World Cup fixtures at 1.20×; bilateral T20Is at 1.00×.</li>
        </ul>
      </div>

      <div style="background:var(--rr-slate-50); border:1px solid var(--rr-slate-200); border-radius:var(--radius-sm); padding:1.25rem;">
        <div style="font-weight:700; font-size:0.92rem; color:var(--rr-navy); margin-bottom:0.5rem;">
          Analytical Limitations
        </div>
        <ul style="font-size:0.84rem; color:var(--rr-slate-600); line-height:1.65; margin-left:1.1rem;">
          <li><strong>Absence of Ball-Tracking Trajectory Data:</strong> Detailed pitch deviation coordinates are proprietary to broadcasters, limiting direct pitch deterioration modeling.</li>
          <li><strong>Dew Factor Variance:</strong> Heavy second-innings evening dew affects grip, creating run-rate variance across match innings.</li>
          <li><strong>Tactical Matchup Shielding:</strong> Selected batters are protected by team captains from disadvantageous bowling matchups.</li>
        </ul>
      </div>
    </div>
  </section>

</main>

<!-- SCOUTING DOSSIER MODAL -->
<div class="modal-overlay" id="playerModal" onclick="closePlayerModal()">
  <div class="modal-content" onclick="event.stopPropagation()">
    <div class="modal-header">
      <button class="modal-close" onclick="closePlayerModal()">&times;</button>
      <div style="font-size:0.75rem; font-weight:700; color:#F472B6; letter-spacing:0.06em; text-transform:uppercase;" id="modalCategory">PLAYER SCOUTING DOSSIER</div>
      <h2 style="font-size:1.65rem; font-weight:800; margin-top:0.2rem;" id="modalName">Player Name</h2>
      <div style="display:flex; gap:0.5rem; align-items:center; margin-top:0.35rem;">
        <span class="team-badge" id="modalTeam">TEAM</span>
        <span style="font-size:0.8rem; color:var(--rr-slate-300);" id="modalTier">Auction Tier</span>
      </div>
    </div>
    <div class="modal-body">
      <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:0.65rem; background:var(--rr-slate-50); padding:0.85rem; border-radius:var(--radius-sm); border:1px solid var(--rr-slate-200); margin-bottom:1.25rem;">
        <div style="text-align:center;">
          <div style="font-size:0.7rem; color:var(--rr-slate-500); font-weight:700; text-transform:uppercase;">Performance Index</div>
          <div style="font-size:1.35rem; font-weight:700; font-family:'JetBrains Mono',monospace;" id="modalScore" class="text-pink">85.7</div>
        </div>
        <div style="text-align:center;">
          <div style="font-size:0.7rem; color:var(--rr-slate-500); font-weight:700; text-transform:uppercase;" id="modalMetricLabel">HP Strike Rate</div>
          <div style="font-size:1.35rem; font-weight:700; font-family:'JetBrains Mono',monospace;" id="modalMetricVal" class="text-navy">183.7</div>
        </div>
        <div style="text-align:center;">
          <div style="font-size:0.7rem; color:var(--rr-slate-500); font-weight:700; text-transform:uppercase;" id="modalDeltaLabel">Delta vs Baseline</div>
          <div style="font-size:1.35rem; font-weight:700; font-family:'JetBrains Mono',monospace;" id="modalDeltaVal" class="text-green">+46.1</div>
        </div>
      </div>

      <div style="margin-bottom:1rem;">
        <div style="font-size:0.78rem; font-weight:700; color:var(--rr-pink); text-transform:uppercase; letter-spacing:0.04em; margin-bottom:0.2rem;">
          Sawai Mansingh Stadium Dimension Fit:
        </div>
        <p style="font-size:0.86rem; color:var(--rr-slate-700); line-height:1.5;" id="modalJaipurFit">Fit details</p>
      </div>

      <div style="margin-bottom:1rem;">
        <div style="font-size:0.78rem; font-weight:700; color:var(--rr-blue); text-transform:uppercase; letter-spacing:0.04em; margin-bottom:0.2rem;">
          Tactical Role in Rajasthan Royals XI:
        </div>
        <p style="font-size:0.86rem; color:var(--rr-slate-700); line-height:1.5;" id="modalRRFit">RR fit details</p>
      </div>

      <div style="background:#FFFBEB; border-left:2px solid var(--rr-gold); padding:0.75rem 0.85rem;">
        <div style="font-size:0.75rem; font-weight:700; color:#92400E; text-transform:uppercase; margin-bottom:0.15rem;">
          Strategic Rationale
        </div>
        <p style="font-size:0.82rem; color:#78350F; line-height:1.45;" id="modalWhyBid">Why bid details</p>
      </div>
    </div>
  </div>
</div>

<footer>
  <div style="max-width:800px; margin:0 auto;">
    <div style="font-size:0.95rem; font-weight:700; color:#FFFFFF; margin-bottom:0.35rem;">
      Rajasthan Royals War Room Player Evaluation
    </div>
    <p style="font-size:0.8rem; margin-bottom:0.85rem;">
      Delivery-Level Match State Analysis Across 200,999 Deliveries (2022–2026) • SupeRR Selector Season 2
    </p>
    <p style="font-size:0.78rem;">
      <a href="https://github.com/Shubhdix9/RR">GitHub Repository</a> • 
      <a href="https://shubhdix9.github.io/RR/">Live Dashboard Link</a>
    </p>
  </div>
</footer>

<!-- JAVASCRIPT CONTROLLERS -->
<script>
const playersData = {players_json_str};

function filterTable(type) {{
  const input = document.getElementById(type + 'Search').value.toLowerCase();
  const rows = document.querySelectorAll('#' + type + 'Table tbody tr');
  rows.forEach(row => {{
    const name = row.getAttribute('data-name').toLowerCase();
    const team = row.getAttribute('data-team').toLowerCase();
    if (name.includes(input) || team.includes(input)) {{
      row.style.display = '';
    }} else {{
      row.style.display = 'none';
    }}
  }});
}}

function openPlayerModal(playerName) {{
  const player = playersData.find(p => p.name === playerName);
  if (!player) return;

  document.getElementById('modalCategory').innerText = player.type === 'batter' 
    ? 'BATTING SCOUTING DOSSIER • RANK #' + player.rank 
    : 'BOWLING SCOUTING DOSSIER • RANK #' + player.rank;
  
  document.getElementById('modalName').innerText = player.name;
  document.getElementById('modalTeam').innerText = player.team;
  document.getElementById('modalTier').innerText = player.tier;
  document.getElementById('modalScore').innerText = player.score.toFixed(1);
  document.getElementById('modalScore').className = player.type === 'batter' ? 'text-pink' : 'text-blue';

  if (player.type === 'batter') {{
    document.getElementById('modalMetricLabel').innerText = 'HP Strike Rate';
    document.getElementById('modalMetricVal').innerText = player.primary_metric.toFixed(1);
    document.getElementById('modalDeltaLabel').innerText = 'Delta vs Baseline';
    document.getElementById('modalDeltaVal').innerText = '+' + player.delta.toFixed(1);
    document.getElementById('modalDeltaVal').className = 'text-green';
  }} else {{
    document.getElementById('modalMetricLabel').innerText = 'HP Economy';
    document.getElementById('modalMetricVal').innerText = player.primary_metric.toFixed(2);
    document.getElementById('modalDeltaLabel').innerText = 'Delta Suppression';
    const sign = player.delta >= 0 ? '+' : '';
    document.getElementById('modalDeltaVal').innerText = sign + player.delta.toFixed(2);
    document.getElementById('modalDeltaVal').className = player.delta >= 0 ? 'text-green' : 'text-pink';
  }}

  document.getElementById('modalJaipurFit').innerText = player.jaipur_fit;
  document.getElementById('modalRRFit').innerText = player.rr_partnership;
  document.getElementById('modalWhyBid').innerText = player.why_bid;

  document.getElementById('playerModal').style.display = 'flex';
}}

function closePlayerModal() {{
  document.getElementById('playerModal').style.display = 'none';
}}

window.addEventListener('keydown', function(e) {{
  if (e.key === 'Escape') closePlayerModal();
}});
</script>

</body>
</html>
'''

with open('RR_WAR_ROOM_REPORT.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Successfully compiled clean executive RR_WAR_ROOM_REPORT.html and index.html!")

