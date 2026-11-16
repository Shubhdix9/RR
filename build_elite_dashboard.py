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

# Enriched scouting and auction dossier data for all 20 players
batter_dossiers = {
    "Ashutosh Sharma": {
        "tier": "Domestic Value Target (₹3.5–5.5 Cr)",
        "origin": "Domestic Uncapped",
        "jaipur_fit": "Jaipur's 80m square boundaries reward his 360° sweep-hit arc. His flat-bat muscular bat swing easily clears SMS stadium straight and mid-wicket fences.",
        "rr_partnership": "Slots directly at #7 below Sanju Samson, Riyan Parag, and Dhruv Jurel, solving RR's historic death-overs run leakage and boundary drought in tight chases.",
        "stat_callout": "+55.8 xRA per 100 Balls • 183.7 High-Pressure Strike Rate (ΔSR +46.1)",
        "why_bid": "The single most destructive domestic death finisher available. Generates match-winning boundary bursts without exhausting overseas purse or foreign player slots."
    },
    "Sameer Rizvi": {
        "tier": "High-Upside Domestic Diamond (₹3.0–5.0 Cr)",
        "origin": "Domestic Uncapped",
        "jaipur_fit": "Exceptional footwork against finger and wrist spin. SMS Stadium's afternoon grip offers opposition spinners no respite against his straight lofted boundary strokeplay.",
        "rr_partnership": "Positions at #5 or #6 to counter opposition middle-overs spin chokes (overs 9–14), taking pressure off Samson and anchoring transition into the death overs.",
        "stat_callout": "80.0% Clutch Consistency Rate • 184.7 HP Strike Rate (ΔSR +38.6)",
        "why_bid": "Combines raw power with supreme consistency (80% positive match execution). Uncapped domestic profile keeps auction inflation controlled."
    },
    "Shubham Dubey": {
        "tier": "Budget Domestic Steal (₹1.5–3.0 Cr)",
        "origin": "Domestic Uncapped",
        "jaipur_fit": "Tall left-hander with high reach. Dissects the larger off-side and leg-side boundaries at SMS Stadium with powerful pull and lofted drive shots.",
        "rr_partnership": "Provides vital left-handed death enforcer balance at #6/7, disrupting bowler yorker lines alongside right-handed finishers like Jurel and Powell.",
        "stat_callout": "+46.9 ΔSR Under Leverage • 71.4% Consistency • 180.0 HP Strike Rate",
        "why_bid": "Familiar with RR team culture, highly coachable, and demonstrated elite acceleration under maximum leverage in domestic and IPL action."
    },
    "Donovan Ferreira": {
        "tier": "High-Utility Overseas Asset (₹2.0–4.0 Cr)",
        "origin": "Overseas (South Africa)",
        "jaipur_fit": "Phenomenal wrist speed and 360° ramp/scoop execution. Exploits fine-leg and third-man fielding gaps on Jaipur's vast outfield.",
        "rr_partnership": "Versatile multi-tool asset: backup wicketkeeper, gun boundary fielder, dynamic floater at #6/7, and occasional off-spin option.",
        "stat_callout": "188.3 High-Pressure Strike Rate (Highest in Dataset) • 83.3% Consistency",
        "why_bid": "Highest raw strike rate in our top 10 under leverage. Provides premium insurance for Samson/Jurel while adding explosive firepower."
    },
    "Sikandar Raza": {
        "tier": "Tactical Multi-Phase Veteran (₹2.5–4.5 Cr)",
        "origin": "Overseas (Zimbabwe)",
        "jaipur_fit": "Tactical master of large grounds. Rotates strike effortlessly at 135+ and uses clever manipulation of gaps to punish boundary boundary fielders.",
        "rr_partnership": "The ultimate crisis-recovery asset. Prevents collapses when RR top-order fails early, and doubles as an elite Rank 6 bowler (7.12 HP Econ).",
        "stat_callout": "Dual Top-10 Rank (Rank 5 Bat / Rank 6 Bowl) • +47.7 ΔSR Acceleration",
        "why_bid": "Rare two-in-one commodity: gives RR top-tier death boundary finishing and 4 overs of middle-overs spin strangulation on a single overseas slot."
    },
    "Liam Livingstone": {
        "tier": "Marquee Match-Winner (₹7.5–11.0 Cr)",
        "origin": "Overseas (England)",
        "jaipur_fit": "Immense 110-meter raw power that completely takes stadium boundary sizes out of the equation. Can clear any ground in the world with ease.",
        "rr_partnership": "Destroys opposition spin bowling through overs 9–15. Bowls both off-spin and leg-spin to exploit left/right matchups in Jaipur conditions.",
        "stat_callout": "81.2% Clutch Consistency Rate • 176.4 HP SR • +36.4 xRA/100",
        "why_bid": "A proven global game-changer. Solves RR's middle-overs boundary drought and offers game-breaking all-round flexibility."
    },
    "Mark Chapman": {
        "tier": "High-Value Accumulator & Finisher (₹1.5–3.0 Cr)",
        "origin": "Overseas (New Zealand)",
        "jaipur_fit": "Calculated sweeper and strike manipulator. Minimizes dot balls on large boundaries and converts ones into twos through supreme fitness.",
        "rr_partnership": "Calm left-handed anchor at #5/6 who stabilizes tricky chases and accelerates to 178.8 SR when the required run rate spikes.",
        "stat_callout": "178.8 HP Strike Rate (ΔSR +30.0) • Low Dot-Ball Frequency",
        "why_bid": "High cricket IQ, exceptional against defensive spin, and available at a highly cost-efficient auction price bracket."
    },
    "Tim David": {
        "tier": "Marquee Death Specialist (₹7.0–10.5 Cr)",
        "origin": "Overseas (Australia)",
        "jaipur_fit": "Elite muscle mass and bottom-hand leverage. Punishes full and wide yorkers straight down the ground, easily clearing Jaipur's 78m sightscreen.",
        "rr_partnership": "Walks in at over 16 to finish chases alongside Parag or Jurel. Takes total ownership of high required rates (12–15 RPO).",
        "stat_callout": "423 High-Pressure Deliveries (Proven Sample Volume) • 187.5 HP Strike Rate",
        "why_bid": "Statistically the most tested and verified pure death-overs finisher in high-pressure T20 cricket over massive sample volumes."
    },
    "Rovman Powell": {
        "tier": "Core Power Leader (₹4.0–6.5 Cr)",
        "origin": "Overseas (West Indies)",
        "jaipur_fit": "Proven track record in Rajasthan Royals colors. Master of high-pressure straight hitting down the V and cow corner at SMS Stadium.",
        "rr_partnership": "Trusted war room asset with established dressing-room chemistry. Solidifies #6/7 with intimidating physical presence and tactical calm.",
        "stat_callout": "513 High-Pressure Deliveries (Largest Dataset Volume) • 70.6% Consistency",
        "why_bid": "Zero integration risk, proven reliability for RR in tight finishes, and an established international leader."
    },
    "Shashank Singh": {
        "tier": "Domestic Match-Winner (₹4.5–7.0 Cr)",
        "origin": "Domestic Capped/Proven",
        "jaipur_fit": "High-backlift power striker who thrives under high required rates. Punishes pace bowlers who miss lengths on good bounce tracks.",
        "rr_partnership": "Provides domestic match-winning insurance in the lower middle-order, allowing RR to field a lethal top 7 without over-relying on foreign batters.",
        "stat_callout": "+38.8 xRA per 100 Balls • 173.3 HP Strike Rate • Proven Chase Record",
        "why_bid": "Demonstrated cold-blooded composure in close IPL run chases; perfect cultural and tactical fit for Rajasthan Royals' fighting ethos."
    }
}

bowler_dossiers = {
    "Umran Malik": {
        "tier": "High-Ceiling Express Pacer (₹3.5–6.0 Cr)",
        "origin": "Domestic Capped",
        "jaipur_fit": "155+ km/h thunderbolts force false shots on Jaipur's large outfield. Batters rushing pulls get caught well inside the 80m boundary cushions.",
        "rr_partnership": "Forms a terrifying pace tandem with Jofra Archer: Archer's steep bounce and seam movement paired with Umran's blistering through-the-air velocity.",
        "stat_callout": "7.57 HP Economy Rate • +1.71 Economy Suppression Under Pressure",
        "why_bid": "Under high leverage, his economy actually drops to 7.57 RPO (+1.71 better than baseline). A game-breaking enforcer at the middle and death."
    },
    "Gudakesh Motie": {
        "tier": "Tactical Left-Arm Squeeze (₹2.0–3.5 Cr)",
        "origin": "Overseas (West Indies)",
        "jaipur_fit": "Subtle changes of pace and tight stump-to-stump line. Uses the big square boundaries at SMS Stadium to starve right-handers of room.",
        "rr_partnership": "Controls overs 7–14 from the South Pavilion End, creating pressure that enables Archer and Sandeep Sharma to harvest wickets at the other end.",
        "stat_callout": "80.0% Consistency Rate • 7.50 HP Economy • +0.68 Runs Prevented/Over",
        "why_bid": "Elite modern white-ball finger-spinner with an 80% clutch consistency record. High value at moderate auction investment."
    },
    "Washington Sundar": {
        "tier": "Domestic Strategic Asset (₹5.5–8.5 Cr)",
        "origin": "Domestic Capped (India)",
        "jaipur_fit": "Flies through overs with immaculate control. Exploits Jaipur's daytime surface grip with subtle arm-balls and skidding deliveries.",
        "rr_partnership": "Can bowl anywhere: 1 over in the powerplay, 2 in the middle, 1 in the squeeze overs. Also significantly deepens RR's batting at #8.",
        "stat_callout": "+0.94 Runs Prevented per Over • 7.62 HP Economy • International Pedigree",
        "why_bid": "Top-tier Indian all-round commodity. Solves team balance issues, provides tactical match-up control, and costs zero foreign player slots."
    },
    "Mitchell Santner": {
        "tier": "Master Defensive Spin Enforcer (₹3.5–5.5 Cr)",
        "origin": "Overseas (New Zealand)",
        "jaipur_fit": "World-class trajectory control and side-spin. Traps aggressive hitters on large boundary outfields with clever dips and subtle speed variations.",
        "rr_partnership": "Replaces the tactical void left by Ravichandran Ashwin in controlling run flow through overs 7–15 with pinpoint economy.",
        "stat_callout": "426 High-Pressure Deliveries • 7.58 HP Economy • 75.9% Consistency",
        "why_bid": "The benchmark for T20 defensive spin. Never gets flustered in high-pressure chases and provides valuable lower-order batting cameos."
    },
    "Yuzvendra Chahal": {
        "tier": "Iconic Priority Buyback (₹7.5–11.0 Cr)",
        "origin": "Domestic Capped (RR Legend)",
        "jaipur_fit": "Undisputed king of Sawai Mansingh Stadium. Knows every millimeter of the Jaipur pitch, baiting batters into mistimed lofted shots toward long-on.",
        "rr_partnership": "Reunites with the Royals family as the primary wicket-taking weapon in overs 10–17, breaking dangerous opposition partnerships at will.",
        "stat_callout": "50 High-Pressure Wickets in 495 Balls • IPL All-Time Leading Wicket-Taker",
        "why_bid": "Proven match-winner with emotional and strategic synergy with the franchise. 50 high-pressure wickets in our dataset prove his unmatched value."
    },
    "Sikandar Raza": {
        "tier": "Mystery Spin Squeeze (₹2.5–4.5 Cr)",
        "origin": "Overseas (Zimbabwe)",
        "jaipur_fit": "Carrom ball and disguised knuckle-delivery deceive batters who try to hit against the spin on spacious boundary venues.",
        "rr_partnership": "Bowls high-leverage middle overs without requiring RR to sacrifice a specialist batter. Locks down scoring at just 7.12 RPO.",
        "stat_callout": "7.12 HP Economy Rate • 84.6% Clutch Consistency • +0.82 Runs Prevented/Over",
        "why_bid": "Highest consistency rate (84.6%) among all spin candidates. Offers dual-discipline reliability across the entire 40-over contest."
    },
    "Krunal Pandya": {
        "tier": "Tactical Matchup Enforcer (₹4.0–6.5 Cr)",
        "origin": "Domestic Capped (India)",
        "jaipur_fit": "Fires flat, fast darts into the pitch, denying batters room to elevate over the 82m straight boundaries at SMS Stadium.",
        "rr_partnership": "Provides defensive left-arm orthodox balance, matches up favorably against right-handed power hitters, and brings title-winning experience.",
        "stat_callout": "7.85 HP Economy • +0.51 Runs Prevented/Over • 17 Wickets Under Pressure",
        "why_bid": "Seasoned IPL campaigner with proven tactical temperament in playoff matches. Enhances tactical depth and squad resilience."
    },
    "Harpreet Brar": {
        "tier": "Domestic Matchup Weapon (₹2.5–4.5 Cr)",
        "origin": "Domestic Capped (India)",
        "jaipur_fit": "High-arm release creates steep bounce on Jaipur surfaces. Pinches batters for room when they attempt to muscle shots over the leg side.",
        "rr_partnership": "Direct weapon against right-hand heavy top and middle-orders (e.g. Kohli, Maxwell, Rohit). Provides economical domestic spin coverage.",
        "stat_callout": "7.64 HP Economy • +0.21 Economy Suppression • Gun Outfield Catcher",
        "why_bid": "Specialist matchup bowler who regularly out-thinks elite international batters. Low purse footprint with high tactical upside."
    },
    "Matheesha Pathirana": {
        "tier": "Marquee Death Spearhead (₹9.0–13.5 Cr)",
        "origin": "Overseas (Sri Lanka)",
        "jaipur_fit": "Malinga-esque slingy trajectory produces unplayable toe-crushers and dipping slower yorkers that cannot be elevated over the boundary cushions.",
        "rr_partnership": "Pairs with Jofra Archer to form the most lethal death-bowling combination in T20 history (overs 17–20 lockdown guarantee).",
        "stat_callout": "41 High-Pressure Wickets (94% Middle/Death) • 431 High-Pressure Balls",
        "why_bid": "Generational death specialist. Wicket probability of 0.095 per ball at the death guarantees RR defensive dominance."
    },
    "Noor Ahmad": {
        "tier": "Young Mystery Spin Asset (₹5.5–9.0 Cr)",
        "origin": "Overseas (Afghanistan)",
        "jaipur_fit": "Rapid arm action and disguised googly create tremendous uncertainty. Batters cannot read his spin out of the hand on dry Jaipur decks.",
        "rr_partnership": "Operates as RR's primary middle-overs attacking wrist-spinner, pairing with finger-spinners to spin the ball both ways.",
        "stat_callout": "26 High-Pressure Wickets • 386 HP Balls • Left-Arm Wrist Spin Rarity",
        "why_bid": "At just 21 years old, he provides Rajasthan Royals an elite, long-term franchise anchor in the rare left-arm wrist-spin category."
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

# Table rows generation
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
        <td class="text-center"><button class="btn-dossier" onclick="event.stopPropagation(); openPlayerModal('{b['name']}')">Dossier →</button></td>
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
        <td class="text-center"><button class="btn-dossier" onclick="event.stopPropagation(); openPlayerModal('{bw['name']}')">Dossier →</button></td>
      </tr>
    '''

# Detailed cards for Jaipur / Squad Fit section
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
            <span class="m-label">Δ vs Baseline</span>
            <span class="m-val text-green font-bold">+{b['delta_sr']:.1f}</span>
          </div>
          <div class="metric-mini">
            <span class="m-label">Consistency</span>
            <span class="m-val text-navy">{b['ccr']:.1f}%</span>
          </div>
        </div>

        <div class="squad-section">
          <div class="section-tag-mini text-pink">🏟️ Sawai Mansingh Stadium Dimension Fit</div>
          <p class="squad-text">{dos.get('jaipur_fit', '')}</p>
        </div>

        <div class="squad-section">
          <div class="section-tag-mini text-navy">🤝 Strategic Fit in Rajasthan Royals XI</div>
          <p class="squad-text">{dos.get('rr_partnership', '')}</p>
        </div>

        <div class="squad-footer">
          <strong>Why RR Must Back:</strong> {dos.get('why_bid', '')}
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
            <span class="m-label">Δ Suppression</span>
            <span class="m-val text-green font-bold">{delta_str}</span>
          </div>
          <div class="metric-mini">
            <span class="m-label">HP Wickets</span>
            <span class="m-val text-navy font-bold">{bw['wkts']}</span>
          </div>
        </div>

        <div class="squad-section">
          <div class="section-tag-mini text-blue">🏟️ Sawai Mansingh Stadium Dimension Fit</div>
          <p class="squad-text">{dos.get('jaipur_fit', '')}</p>
        </div>

        <div class="squad-section">
          <div class="section-tag-mini text-navy">🤝 Strategic Fit in Rajasthan Royals XI</div>
          <p class="squad-text">{dos.get('rr_partnership', '')}</p>
        </div>

        <div class="squad-footer">
          <strong>Why RR Must Back:</strong> {dos.get('why_bid', '')}
        </div>
      </div>
    '''

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Rajasthan Royals War Room Analytics — IPL 2027 Auction Intelligence</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Cabinet+Grotesk:wght@700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
:root {{
  --rr-pink: #EA1A7F;
  --rr-pink-light: #FDF2F8;
  --rr-pink-glow: rgba(234, 26, 127, 0.25);
  --rr-blue: #254AA5;
  --rr-blue-light: #EFF6FF;
  --rr-navy: #0B1938;
  --rr-dark: #071024;
  --rr-card-dark: #0D1C3D;
  --rr-gold: #F59E0B;
  --rr-gold-light: #FEF3C7;
  --rr-emerald: #10B981;
  --rr-emerald-light: #ECFDF5;
  --rr-red: #EF4444;
  --rr-slate-50: #F8FAFC;
  --rr-slate-100: #F1F5F9;
  --rr-slate-200: #E2E8F0;
  --rr-slate-300: #CBD5E1;
  --rr-slate-400: #94A3B8;
  --rr-slate-600: #475569;
  --rr-slate-800: #1E293B;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -1px rgba(0, 0, 0, 0.04);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.03);
  --shadow-glow: 0 0 25px rgba(234, 26, 127, 0.18);
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-full: 9999px;
}}

* {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}

body {{
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: var(--rr-slate-50);
  color: var(--rr-slate-800);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  padding-bottom: 4rem;
}}

/* Top Navigation Bar */
.top-navbar {{
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(11, 25, 56, 0.94);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 0.75rem 1.5rem;
  transition: all 0.2s ease;
}}

.nav-container {{
  max-width: 1350px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}}

.brand-wrapper {{
  display: flex;
  align-items: center;
  gap: 0.85rem;
}}

.brand-crest {{
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, var(--rr-pink), var(--rr-blue));
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-family: 'Cabinet Grotesk', sans-serif;
  font-weight: 900;
  font-size: 1.15rem;
  letter-spacing: -0.05em;
  box-shadow: 0 2px 10px rgba(234, 26, 127, 0.4);
}}

.brand-title-wrap {{
  display: flex;
  flex-direction: column;
}}

.brand-title {{
  color: white;
  font-family: 'Cabinet Grotesk', sans-serif;
  font-weight: 800;
  font-size: 1.05rem;
  letter-spacing: 0.02em;
  line-height: 1.2;
}}

.brand-subtitle {{
  color: var(--rr-slate-400);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}}

.nav-links {{
  display: flex;
  gap: 0.4rem;
  align-items: center;
}}

.nav-item {{
  color: var(--rr-slate-300);
  text-decoration: none;
  font-size: 0.82rem;
  font-weight: 600;
  padding: 0.45rem 0.85rem;
  border-radius: var(--radius-sm);
  transition: all 0.15s ease;
  cursor: pointer;
  border: 1px solid transparent;
}}

.nav-item:hover {{
  color: white;
  background: rgba(255, 255, 255, 0.08);
}}

.nav-item.active {{
  color: white;
  background: var(--rr-pink);
  box-shadow: 0 2px 8px rgba(234, 26, 127, 0.4);
}}

.nav-actions {{
  display: flex;
  align-items: center;
  gap: 0.6rem;
}}

.btn-print {{
  background: linear-gradient(135deg, var(--rr-pink), #D81470);
  color: white;
  border: none;
  padding: 0.5rem 1.1rem;
  border-radius: var(--radius-sm);
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.45rem;
  box-shadow: 0 2px 10px rgba(234, 26, 127, 0.35);
  transition: all 0.2s ease;
}}

.btn-print:hover {{
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(234, 26, 127, 0.5);
}}

.btn-gh {{
  background: rgba(255, 255, 255, 0.1);
  color: white;
  text-decoration: none;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.5rem 0.9rem;
  border-radius: var(--radius-sm);
  font-size: 0.82rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  transition: all 0.2s ease;
}}

.btn-gh:hover {{
  background: rgba(255, 255, 255, 0.18);
}}

/* Hero Section */
.hero-section {{
  background: radial-gradient(circle at 80% 20%, rgba(234, 26, 127, 0.25) 0%, transparent 50%),
              radial-gradient(circle at 20% 80%, rgba(37, 74, 165, 0.35) 0%, transparent 60%),
              linear-gradient(135deg, var(--rr-dark) 0%, var(--rr-navy) 100%);
  color: white;
  padding: 3.5rem 2rem 3rem 2rem;
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}}

.hero-content {{
  max-width: 1350px;
  margin: 0 auto;
}}

.hero-pill {{
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(234, 26, 127, 0.15);
  border: 1px solid rgba(234, 26, 127, 0.4);
  color: #FFA5D2;
  padding: 0.35rem 0.9rem;
  border-radius: var(--radius-full);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 1.25rem;
}}

.pulse-dot {{
  width: 8px;
  height: 8px;
  background: var(--rr-pink);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--rr-pink);
  animation: pulse 2s infinite;
}}

@keyframes pulse {{
  0% {{ transform: scale(0.95); opacity: 0.8; }}
  50% {{ transform: scale(1.25); opacity: 1; }}
  100% {{ transform: scale(0.95); opacity: 0.8; }}
}}

.hero-title {{
  font-family: 'Cabinet Grotesk', sans-serif;
  font-weight: 900;
  font-size: 2.85rem;
  line-height: 1.15;
  letter-spacing: -0.03em;
  margin-bottom: 1rem;
}}

.hero-title span {{
  background: linear-gradient(135deg, #FFFFFF 30%, #FFAAD2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}}

.hero-desc {{
  color: var(--rr-slate-300);
  font-size: 1.08rem;
  max-width: 850px;
  line-height: 1.6;
  margin-bottom: 2.5rem;
  font-weight: 400;
}}

/* KPI Banner */
.kpi-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.25rem;
  margin-top: 1.5rem;
}}

.kpi-card {{
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: var(--radius-md);
  padding: 1.4rem;
  backdrop-filter: blur(10px);
  transition: all 0.25s ease;
}}

.kpi-card:hover {{
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(234, 26, 127, 0.4);
  transform: translateY(-2px);
}}

.kpi-val {{
  font-family: 'Cabinet Grotesk', sans-serif;
  font-weight: 900;
  font-size: 2.15rem;
  line-height: 1.1;
  margin-bottom: 0.25rem;
}}

.kpi-label {{
  color: var(--rr-slate-300);
  font-size: 0.82rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}

.kpi-sub {{
  color: var(--rr-slate-400);
  font-size: 0.72rem;
  margin-top: 0.35rem;
}}

/* Main Layout */
.main-content {{
  max-width: 1350px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}}

/* Content Card */
.content-card {{
  background: white;
  border: 1px solid var(--rr-slate-200);
  border-radius: var(--radius-lg);
  padding: 2.25rem;
  margin-bottom: 2.25rem;
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.2s ease;
}}

.content-card:hover {{
  box-shadow: var(--shadow-md);
}}

.card-header-bar {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid var(--rr-slate-200);
  padding-bottom: 1.25rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}}

.card-title-group {{
  display: flex;
  align-items: center;
  gap: 0.85rem;
}}

.section-num {{
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-family: 'Cabinet Grotesk', sans-serif;
  font-weight: 800;
  font-size: 1.1rem;
}}

.num-pink {{ background: var(--rr-pink); }}
.num-blue {{ background: var(--rr-blue); }}
.num-gold {{ background: var(--rr-gold); }}
.num-navy {{ background: var(--rr-navy); }}

.section-title {{
  font-family: 'Cabinet Grotesk', sans-serif;
  font-weight: 900;
  font-size: 1.55rem;
  color: var(--rr-navy);
  letter-spacing: -0.02em;
}}

.section-desc {{
  color: var(--rr-slate-600);
  font-size: 0.95rem;
  line-height: 1.65;
  margin-top: 0.25rem;
}}

/* Grid utilities */
.grid-2 {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
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
}}

@media (max-width: 900px) {{
  .grid-2, .grid-3, .grid-4 {{ grid-template-columns: 1fr; }}
  .hero-title {{ font-size: 2.1rem; }}
  .nav-links {{ display: none; }}
}}

/* Feasibility Boxes */
.feasibility-box {{
  background: var(--rr-slate-50);
  border: 1px solid var(--rr-slate-200);
  border-radius: var(--radius-md);
  padding: 1.35rem;
  transition: all 0.2s ease;
}}

.feasibility-box:hover {{
  border-color: var(--rr-pink);
  background: white;
  box-shadow: var(--shadow-sm);
}}

.feasibility-title {{
  font-weight: 800;
  font-size: 1rem;
  color: var(--rr-navy);
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}}

/* Formula Showcase */
.formula-card {{
  background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
  border: 1px solid var(--rr-slate-300);
  border-radius: var(--radius-md);
  padding: 1.25rem;
}}

.formula-display {{
  background: white;
  border: 1px solid var(--rr-slate-300);
  border-radius: var(--radius-sm);
  padding: 0.85rem 1.1rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.92rem;
  font-weight: 600;
  color: var(--rr-navy);
  margin: 0.65rem 0;
  overflow-x: auto;
}}

/* Search & Filter Toolbar */
.table-toolbar {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.25rem;
  background: var(--rr-slate-100);
  padding: 0.75rem 1.15rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--rr-slate-200);
}}

.search-box-wrap {{
  position: relative;
  flex: 1;
  max-width: 380px;
}}

.search-input {{
  width: 100%;
  padding: 0.55rem 0.85rem 0.55rem 2.2rem;
  border: 1px solid var(--rr-slate-300);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.85rem;
  outline: none;
  transition: all 0.15s ease;
}}

.search-input:focus {{
  border-color: var(--rr-pink);
  box-shadow: 0 0 0 3px var(--rr-pink-glow);
}}

.search-icon {{
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--rr-slate-400);
  font-size: 0.85rem;
}}

.filter-pills {{
  display: flex;
  gap: 0.4rem;
  align-items: center;
}}

.filter-pill {{
  background: white;
  border: 1px solid var(--rr-slate-300);
  padding: 0.4rem 0.85rem;
  border-radius: var(--radius-full);
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--rr-slate-600);
  cursor: pointer;
  transition: all 0.15s ease;
}}

.filter-pill:hover {{
  border-color: var(--rr-navy);
  color: var(--rr-navy);
}}

.filter-pill.active {{
  background: var(--rr-navy);
  border-color: var(--rr-navy);
  color: white;
}}

/* Elite Data Tables */
.table-wrap {{
  overflow-x: auto;
  border: 1px solid var(--rr-slate-200);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}}

table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 0.87rem;
  text-align: left;
  background: white;
}}

thead th {{
  background: var(--rr-navy);
  color: white;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 700;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.9rem 0.85rem;
  border-bottom: 2px solid var(--rr-slate-300);
  white-space: nowrap;
  user-select: none;
}}

thead th.sortable {{
  cursor: pointer;
  transition: background 0.15s ease;
}}

thead th.sortable:hover {{
  background: #172D5C;
}}

tbody tr.player-row {{
  border-bottom: 1px solid var(--rr-slate-200);
  transition: background 0.15s ease;
  cursor: pointer;
}}

tbody tr.player-row:hover {{
  background: var(--rr-pink-light);
}}

tbody tr.player-row:nth-child(even) {{
  background-color: #FCFDFE;
}}

tbody tr.player-row:nth-child(even):hover {{
  background-color: var(--rr-pink-light);
}}

tbody td {{
  padding: 0.85rem 0.85rem;
  vertical-align: middle;
  white-space: nowrap;
}}

/* Table Component Badges */
.rank-pill {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-family: 'Cabinet Grotesk', sans-serif;
  font-weight: 900;
  font-size: 0.95rem;
}}

.badge-gold {{ background: #FEF3C7; color: #B45309; border: 2px solid #F59E0B; }}
.badge-silver {{ background: #F1F5F9; color: #475569; border: 2px solid #94A3B8; }}
.badge-bronze {{ background: #FFEDD5; color: #C2410C; border: 2px solid #FB923C; }}
.badge-plain {{ background: #F8FAFC; color: #64748B; border: 1px solid #CBD5E1; }}

.player-cell {{
  display: flex;
  align-items: center;
  gap: 0.5rem;
}}

.player-name {{
  font-weight: 800;
  color: var(--rr-navy);
  font-size: 0.95rem;
}}

.team-badge {{
  background: #FCE7F3;
  color: #BE185D;
  border-radius: var(--radius-sm);
  padding: 0.15rem 0.45rem;
  font-size: 0.7rem;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
}}

.team-blue-badge {{
  background: #DBEAFE;
  color: #1E40AF;
}}

.score-badge {{
  font-family: 'Cabinet Grotesk', sans-serif;
  font-weight: 900;
  font-size: 1.15rem;
  padding: 0.2rem 0.6rem;
  border-radius: var(--radius-sm);
  display: inline-block;
}}

.score-pink {{ background: var(--rr-pink-light); color: var(--rr-pink); border: 1px solid rgba(234, 26, 127, 0.3); }}
.score-blue {{ background: var(--rr-blue-light); color: var(--rr-blue); border: 1px solid rgba(37, 74, 165, 0.3); }}

.delta-pos {{ color: var(--rr-emerald); font-weight: 800; }}
.delta-neg {{ color: var(--rr-red); font-weight: 800; }}

.phase-pill {{
  font-size: 0.72rem;
  font-weight: 800;
  padding: 0.25rem 0.65rem;
  border-radius: var(--radius-full);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: inline-block;
}}

.phase-death {{ background: #FEE2E2; color: #B91C1C; }}
.phase-mid {{ background: #E0E7FF; color: #4338CA; }}

.role-cell {{
  max-width: 260px;
  white-space: normal;
}}

.role-title {{
  font-weight: 700;
  color: var(--rr-slate-800);
  font-size: 0.85rem;
  line-height: 1.3;
}}

.tier-tag {{
  color: #64748B;
  font-size: 0.74rem;
  font-weight: 600;
  margin-top: 0.2rem;
}}

.btn-dossier {{
  background: var(--rr-slate-100);
  border: 1px solid var(--rr-slate-300);
  color: var(--rr-navy);
  padding: 0.35rem 0.65rem;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
}}

.btn-dossier:hover {{
  background: var(--rr-pink);
  color: white;
  border-color: var(--rr-pink);
}}

/* Figure Display */
.figure-container {{
  margin: 2rem 0;
  border: 1px solid var(--rr-slate-200);
  border-radius: var(--radius-md);
  overflow: hidden;
  background: white;
  box-shadow: var(--shadow-sm);
}}

.figure-container img {{
  width: 100%;
  height: auto;
  display: block;
}}

.figure-caption {{
  background: var(--rr-slate-50);
  padding: 0.85rem 1.25rem;
  font-size: 0.85rem;
  color: var(--rr-slate-600);
  border-top: 1px solid var(--rr-slate-200);
  font-style: italic;
}}

/* Squad Fit Cards */
.squad-card {{
  background: white;
  border-radius: var(--radius-md);
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}

.squad-card:hover {{
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}}

.batter-border {{ border: 1px solid #FBCFE8; border-top: 4px solid var(--rr-pink); }}
.bowler-border {{ border: 1px solid #BFDBFE; border-top: 4px solid var(--rr-blue); }}

.squad-card-header {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}}

.squad-card-title {{
  display: flex;
  align-items: center;
  gap: 0.5rem;
}}

.rank-mini {{
  width: 26px;
  height: 26px;
  border-radius: 50%;
  color: white;
  font-family: 'Cabinet Grotesk', sans-serif;
  font-weight: 900;
  font-size: 0.82rem;
  display: flex;
  align-items: center;
  justify-content: center;
}}

.pink-bg {{ background: var(--rr-pink); }}
.blue-bg {{ background: var(--rr-blue); }}

.name-bold {{
  font-family: 'Cabinet Grotesk', sans-serif;
  font-weight: 800;
  font-size: 1.15rem;
  color: var(--rr-navy);
}}

.team-tag {{
  background: var(--rr-slate-100);
  color: var(--rr-slate-600);
  padding: 0.15rem 0.45rem;
  border-radius: var(--radius-sm);
  font-size: 0.72rem;
  font-weight: 700;
}}

.squad-card-sub {{
  color: var(--rr-slate-400);
  font-size: 0.78rem;
  font-weight: 600;
  margin-top: 0.2rem;
}}

.squad-metrics-row {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.5rem;
  background: var(--rr-slate-50);
  padding: 0.75rem;
  border-radius: var(--radius-sm);
  margin-bottom: 1rem;
  border: 1px solid var(--rr-slate-200);
}}

.metric-mini {{
  display: flex;
  flex-direction: column;
  text-align: center;
}}

.m-label {{
  font-size: 0.68rem;
  color: var(--rr-slate-400);
  font-weight: 600;
  text-transform: uppercase;
}}

.m-val {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.95rem;
  font-weight: 800;
  margin-top: 0.15rem;
}}

.squad-section {{
  margin-bottom: 0.85rem;
}}

.section-tag-mini {{
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 0.25rem;
}}

.squad-text {{
  font-size: 0.86rem;
  color: var(--rr-slate-600);
  line-height: 1.5;
}}

.squad-footer {{
  background: #FFFBEB;
  border-left: 3px solid var(--rr-gold);
  padding: 0.65rem 0.85rem;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  font-size: 0.82rem;
  color: #92400E;
  line-height: 1.45;
  margin-top: 0.5rem;
}}

/* Modal / Scouting Drawer */
.modal-overlay {{
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(7, 16, 36, 0.75);
  backdrop-filter: blur(6px);
  z-index: 999;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}}

.modal-content {{
  background: white;
  border-radius: var(--radius-lg);
  max-width: 680px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.35);
  position: relative;
  border: 1px solid var(--rr-slate-300);
  animation: modalIn 0.25s ease forwards;
}}

@keyframes modalIn {{
  from {{ opacity: 0; transform: scale(0.96) translateY(10px); }}
  to {{ opacity: 1; transform: scale(1) translateY(0); }}
}}

.modal-header {{
  background: linear-gradient(135deg, var(--rr-navy) 0%, var(--rr-blue) 100%);
  color: white;
  padding: 1.75rem 2rem;
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  position: relative;
}}

.modal-close {{
  position: absolute;
  top: 1.25rem;
  right: 1.25rem;
  background: rgba(255, 255, 255, 0.15);
  border: none;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 1.2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}}

.modal-close:hover {{
  background: var(--rr-pink);
}}

.modal-body {{
  padding: 2rem;
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
  background: var(--rr-dark);
  color: var(--rr-slate-400);
  text-align: center;
  padding: 3rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: 4rem;
}}

footer a {{
  color: var(--rr-pink);
  text-decoration: none;
  font-weight: 600;
}}

footer a:hover {{
  text-decoration: underline;
}}

/* Print Stylesheet */
@media print {{
  .top-navbar, .nav-actions, .table-toolbar, .btn-dossier, .filter-pills, footer {{
    display: none !important;
  }}
  body {{
    background: white;
    color: black;
    padding: 0;
  }}
  .hero-section {{
    background: var(--rr-navy) !important;
    color: white !important;
    padding: 2rem 1rem !important;
  }}
  .content-card {{
    box-shadow: none !important;
    border: 1px solid #CCC !important;
    page-break-inside: avoid;
    margin-bottom: 2rem !important;
    padding: 1.5rem !important;
  }}
  table {{
    font-size: 0.72rem !important;
  }}
  thead th {{
    background: #0B1938 !important;
    color: white !important;
    padding: 0.4rem !important;
  }}
  tbody td {{
    padding: 0.35rem !important;
  }}
  .squad-card {{
    page-break-inside: avoid;
    margin-bottom: 1rem !important;
  }}
}}
</style>
</head>
<body>

<!-- TOP NAVIGATION -->
<nav class="top-navbar">
  <div class="nav-container">
    <div class="brand-wrapper">
      <div class="brand-crest">RR</div>
      <div class="brand-title-wrap">
        <span class="brand-title">RAJASTHAN ROYALS</span>
        <span class="brand-subtitle">War Room Player Evaluation</span>
      </div>
    </div>

    <div class="nav-links">
      <a class="nav-item active" href="#section-overview">Overview</a>
      <a class="nav-item" href="#section-feasibility">Auction Filters</a>
      <a class="nav-item" href="#section-math">Leverage Math</a>
      <a class="nav-item" href="#section-batters">Top 10 Batters</a>
      <a class="nav-item" href="#section-bowlers">Top 10 Bowlers</a>
      <a class="nav-item" href="#section-squad">Jaipur Ground Fit</a>
    </div>

    <div class="nav-actions">
      <button class="btn-print" onclick="window.print()">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
        Save as PDF
      </button>
      <a href="https://github.com/Shubhdix9/RR" target="_blank" class="btn-gh">GitHub</a>
    </div>
  </div>
</nav>

<!-- HERO SECTION -->
<header class="hero-section" id="section-overview">
  <div class="hero-content">
    <div class="hero-pill">
      <span class="pulse-dot"></span>
      IPL 2027 Auction Intelligence Model
    </div>
    <h1 class="hero-title">
      High-Pressure Execution &amp;<br>
      <span>Rajasthan Royals Squad Strategy</span>
    </h1>
    <p class="hero-desc">
      A continuous pre-delivery mathematical evaluation isolating <strong>200,999 balls (2022–2026)</strong> to identify actionable, high-leverage specialists for the <strong>Sawai Mansingh Stadium (Jaipur)</strong>. Retained marquee franchise faces and ineligible profiles excluded to guarantee actionable war room recruitment.
    </p>

    <!-- KPI STATS -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-val text-pink">200,999</div>
        <div class="kpi-label">Deliveries Analyzed</div>
        <div class="kpi-sub">Every ball across 883 matches</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-val text-blue">883</div>
        <div class="kpi-label">Elite T20 Matches</div>
        <div class="kpi-sub">371 IPL + 512 T20 Internationals</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-val" style="color:var(--rr-gold);">42.26</div>
        <div class="kpi-label">P80 Pressure Cutoff</div>
        <div class="kpi-sub">Exact calibrated 80th percentile</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-val text-green">20.0%</div>
        <div class="kpi-label">Leverage Deliveries</div>
        <div class="kpi-sub">Isolating the top 20% critical zone</div>
      </div>
    </div>
  </div>
</header>

<main class="main-content">

  <!-- SECTION 1: AUCTION FEASIBILITY FRAMEWORK -->
  <section class="content-card" id="section-feasibility">
    <div class="card-header-bar">
      <div class="card-title-group">
        <div class="section-num num-gold">★</div>
        <div>
          <h2 class="section-title">Auction Feasibility Framework: Exclusion of Star Retentions &amp; Ineligibles</h2>
          <p class="section-desc">Guaranteeing 100% actionable war room recommendations by removing impossible auction targets</p>
        </div>
      </div>
    </div>

    <div class="grid-2">
      <div class="feasibility-box">
        <div class="feasibility-title text-pink">🚫 1. Exclusion of Retained Franchise Mega-Stars</div>
        <p style="font-size:0.88rem; color:#475569; line-height:1.6;">
          Recommending <strong>Virat Kohli, Jasprit Bumrah, Rohit Sharma, Suryakumar Yadav, Heinrich Klaasen, Shubman Gill, Rishabh Pant, or Sanju Samson</strong> is a fatal sports analytics error. Under IPL regulations, these marquee names are locked on multi-year retention contracts of ₹18–25+ Cr or guaranteed RTM slabs. <strong>They cannot enter the open auction pool for RR in 2027.</strong> Recommending them wastes analytic bandwidth and provides zero actionable recruitment value.
        </p>
      </div>

      <div class="feasibility-box">
        <div class="feasibility-title text-navy">⚖️ 2. Exclusion of Legally Ineligible Nationals</div>
        <p style="font-size:0.88rem; color:#475569; line-height:1.6;">
          Pursuant to BCCI governance rules and IPL operating directives, Pakistani cricketers (e.g. Babar Azam, Mohammad Rizwan, Shaheen Afridi) are prohibited from entering the IPL auction player register. All Pakistani players have been strictly removed from consideration to preserve legal and operational compliance.
        </p>
      </div>

      <div class="feasibility-box">
        <div class="feasibility-title text-blue">🏏 3. Exclusion of Top-Order Openers (Positions 1–3)</div>
        <p style="font-size:0.88rem; color:#475569; line-height:1.6;">
          Rajasthan Royals have already locked their elite opening pair in <strong>Yashasvi Jaiswal and Vaibhav Sooryavanshi</strong>, with Sanju Samson at #3. Allocating auction capital to top-order anchors creates roster redundancy. Our model strictly isolates specialist <strong>#4–7 Middle-Order Enforcers &amp; Death Finishers</strong>.
        </p>
      </div>

      <div class="feasibility-box">
        <div class="feasibility-title text-green">🎯 4. Exclusion of Powerplay Opening Bowlers (&gt;25% PP Overs)</div>
        <p style="font-size:0.88rem; color:#475569; line-height:1.6;">
          RR's new-ball seam battery is solidified by Jofra Archer, Sandeep Sharma, and Nandre Burger. The war room's quantifiable pain point has been <strong>Middle-Overs Spin Restriction (Overs 7–15)</strong> and <strong>Death-Overs Yorker Execution (Overs 16–20)</strong>. Bowlers delivering &gt;25% of their balls in the powerplay are filtered out.
        </p>
      </div>
    </div>
  </section>

  <!-- SECTION 2: MATHEMATICAL MODEL -->
  <section class="content-card" id="section-math">
    <div class="card-header-bar">
      <div class="card-title-group">
        <div class="section-num num-navy">1</div>
        <div>
          <h2 class="section-title">Pre-Delivery Leverage Framework: Mathematical Foundation</h2>
          <p class="section-desc">Modeling continuous pressure before the ball is bowled across 200,999 deliveries to prevent outcome bias</p>
        </div>
      </div>
    </div>

    <div class="grid-2">
      <div class="formula-card">
        <h3 style="font-family:'Cabinet Grotesk',sans-serif; color:var(--rr-pink); font-size:1.15rem; margin-bottom:0.5rem;">
          2nd Innings: Chasing Leverage Model
        </h3>
        <p style="font-size:0.85rem; color:#64748B;">Evaluates required run rate stress, wicket resources, and time urgency:</p>
        <div class="formula-display">
          PS = [35 × S_RRR + 30 × S_wkt + 20 × S_urgency + 15 × L_t] / 100
        </div>
        <ul style="font-size:0.83rem; color:#475569; margin-left:1.1rem; line-height:1.6;">
          <li><strong>S_RRR (35%):</strong> min[100, (RRR / 8.50)^2.2 × 28] — non-linear penalty when required rate surpasses par.</li>
          <li><strong>S_wkt (30%):</strong> (Wickets Down / 9)^1.8 × 100 — compounding resource scarcity.</li>
          <li><strong>S_urgency (20%):</strong> [1 - (Balls Left / 120)]^1.5 × 100 — exponential death-overs urgency.</li>
          <li><strong>L_t (15%):</strong> 4 × WP × (1 - WP) — peaks in 50-50 contests; dampens blowouts to zero leverage.</li>
        </ul>
      </div>

      <div class="formula-card">
        <h3 style="font-family:'Cabinet Grotesk',sans-serif; color:var(--rr-blue); font-size:1.15rem; margin-bottom:0.5rem;">
          1st Innings: Target-Setting Leverage Model
        </h3>
        <p style="font-size:0.85rem; color:#64748B;">Evaluates phase variance, top-order collapse, and par score deficit:</p>
        <div class="formula-display">
          PS = [40 × S_phase + 35 × S_collapse + 25 × S_deficit] × Knockout_Multiplier
        </div>
        <ul style="font-size:0.83rem; color:#475569; margin-left:1.1rem; line-height:1.6;">
          <li><strong>S_phase (40%):</strong> Overs 16–20 carry maximum scoring variance (10.48 RPO par).</li>
          <li><strong>S_collapse (35%):</strong> Evaluates batting under crisis (excess wickets lost vs expected curve).</li>
          <li><strong>S_deficit (25%):</strong> Pressure generated when scoring lags behind 8.50 RPO par total.</li>
          <li><strong>Knockout Multiplier:</strong> 1.15× bonus applied for playoffs, qualifiers, and championship finals.</li>
        </ul>
      </div>
    </div>

    <!-- EMPIRICAL PAR BREAKDOWN -->
    <div style="margin-top:1.5rem; background:var(--rr-slate-50); border:1px solid var(--rr-slate-200); border-radius:var(--radius-md); padding:1.25rem;">
      <h4 style="font-family:'Cabinet Grotesk',sans-serif; font-size:1.05rem; color:var(--rr-navy); margin-bottom:0.75rem;">
        Empirical Par Benchmarks Computed from 200,999 Deliveries
      </h4>
      <div class="grid-3">
        <div style="background:white; padding:1rem; border-radius:var(--radius-sm); text-align:center; border:1px solid var(--rr-slate-200);">
          <div style="font-size:0.75rem; font-weight:700; color:var(--rr-blue); text-transform:uppercase;">Powerplay (Overs 1–6)</div>
          <div style="font-size:1.4rem; font-weight:900; color:var(--rr-navy); font-family:'Cabinet Grotesk',sans-serif;">8.02 RPO</div>
          <div style="font-size:0.75rem; color:#64748B;">Expected Wickets: 0.048 / ball</div>
        </div>
        <div style="background:white; padding:1rem; border-radius:var(--radius-sm); text-align:center; border:1px solid var(--rr-slate-200);">
          <div style="font-size:0.75rem; font-weight:700; color:var(--rr-navy); text-transform:uppercase;">Middle Overs (Overs 7–15)</div>
          <div style="font-size:1.4rem; font-weight:900; color:var(--rr-navy); font-family:'Cabinet Grotesk',sans-serif;">7.74 RPO</div>
          <div style="font-size:0.75rem; color:#64748B;">Expected Wickets: 0.051 / ball</div>
        </div>
        <div style="background:white; padding:1rem; border-radius:var(--radius-sm); text-align:center; border:1px solid var(--rr-slate-200);">
          <div style="font-size:0.75rem; font-weight:700; color:var(--rr-pink); text-transform:uppercase;">Death Overs (Overs 16–20)</div>
          <div style="font-size:1.4rem; font-weight:900; color:var(--rr-pink); font-family:'Cabinet Grotesk',sans-serif;">10.48 RPO</div>
          <div style="font-size:0.75rem; color:#64748B;">Overs 19–20: 11.49 RPO (0.089 wkt/ball)</div>
        </div>
      </div>
    </div>

    <!-- FIGURE 1 -->
    <div class="figure-container">
      <img src="data:image/png;base64,{fig1_b64}" alt="Figure 1: Pressure Score Distribution">
      <div class="figure-caption">
        <strong>Figure 1:</strong> Pre-delivery continuous pressure score distribution across 200,999 deliveries, establishing the exact P80 threshold (42.26) that isolates the top 20% highest-leverage game situations.
      </div>
    </div>
  </section>

  <!-- SECTION 3: TOP 10 BATTERS -->
  <section class="content-card" id="section-batters">
    <div class="card-header-bar">
      <div class="card-title-group">
        <div class="section-num num-pink">2</div>
        <div>
          <h2 class="section-title">Top 10 Middle-Order &amp; Death Finishers (#4–7)</h2>
          <p class="section-desc">Evaluated by Clutch Batting Index (CBI): 30% HP SR, 25% xRA, 20% ΔSR, 15% Boundaries, 10% Consistency</p>
        </div>
      </div>
    </div>

    <!-- TABLE TOOLBAR -->
    <div class="table-toolbar">
      <div class="search-box-wrap">
        <span class="search-icon">🔍</span>
        <input type="text" class="search-input" id="batterSearch" placeholder="Search batter by name or team..." onkeyup="filterTable('batter')">
      </div>
      <div style="font-size:0.8rem; color:#64748B; font-weight:600;">
        💡 Click on any player row to view full Scouting Dossier
      </div>
    </div>

    <!-- BATTER TABLE -->
    <div class="table-wrap">
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
            <th class="text-center">Primary Phase</th>
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
    <div class="figure-container">
      <img src="data:image/png;base64,{fig2_b64}" alt="Figure 2: Batting Delta Strike Rate">
      <div class="figure-caption">
        <strong>Figure 2:</strong> Career baseline strike rate vs high-pressure strike rate (ΔSR). Notice the extraordinary acceleration under severe pressure from Ashutosh Sharma (+46.1) and Shubham Dubey (+46.9).
      </div>
    </div>
  </section>

  <!-- SECTION 4: TOP 10 BOWLERS -->
  <section class="content-card" id="section-bowlers">
    <div class="card-header-bar">
      <div class="card-title-group">
        <div class="section-num num-blue">3</div>
        <div>
          <h2 class="section-title">Top 10 Middle-Overs &amp; Death Bowlers (Overs 7–20)</h2>
          <p class="section-desc">Evaluated by Pressure Bowling Index (PBI): 30% xRP, 25% Econ Suppression, 20% Wickets, 15% ΔEcon, 10% Consistency</p>
        </div>
      </div>
    </div>

    <!-- TABLE TOOLBAR -->
    <div class="table-toolbar">
      <div class="search-box-wrap">
        <span class="search-icon">🔍</span>
        <input type="text" class="search-input" id="bowlerSearch" placeholder="Search bowler by name or team..." onkeyup="filterTable('bowler')">
      </div>
      <div style="font-size:0.8rem; color:#64748B; font-weight:600;">
        💡 Click on any player row to view full Scouting Dossier
      </div>
    </div>

    <!-- BOWLER TABLE -->
    <div class="table-wrap">
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
            <th class="text-center">Primary Phase</th>
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
    <div class="figure-container">
      <img src="data:image/png;base64,{fig3_b64}" alt="Figure 3: Bowling Delta Economy">
      <div class="figure-caption">
        <strong>Figure 3:</strong> Career baseline vs high-pressure economy rate (ΔEcon). Positive values show bowlers whose economy significantly tightens under pressure (e.g. Umran Malik +1.71 suppression, Gudakesh Motie +0.36).
      </div>
    </div>
  </section>

  <!-- SECTION 5: SQUAD FIT & JAIPUR CONDITIONS -->
  <section class="content-card" id="section-squad">
    <div class="card-header-bar">
      <div class="card-title-group">
        <div class="section-num num-navy">4</div>
        <div>
          <h2 class="section-title">Rajasthan Royals Squad Strengthening &amp; Jaipur Dynamics</h2>
          <p class="section-desc">Translating analytical leverage into tactical acquisitions for the Sawai Mansingh Stadium in IPL 2027</p>
        </div>
      </div>
    </div>

    <div style="background:#FFFBEB; border:1px solid #FCD34D; border-radius:var(--radius-md); padding:1.25rem; margin-bottom:2rem;">
      <h3 style="font-family:'Cabinet Grotesk',sans-serif; color:#B45309; font-size:1.15rem; margin-bottom:0.35rem;">
        🏟️ Sawai Mansingh Stadium (Jaipur) Dimension &amp; Surface Blueprint
      </h3>
      <p style="font-size:0.88rem; color:#78350F; line-height:1.6;">
        SMS Stadium features large <strong>75–82 meter straight and square boundaries</strong>. Unlike small venues where mistimed edges fly for six, Jaipur severely punishes false strokes while rewarding batters with genuine 360° clearance power and spinners who deceive in flight. Our recruitment targets solve RR's two primary structural vulnerabilities: <strong>explosive #6/7 death boundary hitting</strong> and <strong>middle-overs spin strangulation</strong>.
      </p>
    </div>

    <!-- BATTERS SQUAD FIT CARDS -->
    <h3 style="font-family:'Cabinet Grotesk',sans-serif; color:var(--rr-pink); font-size:1.35rem; margin-bottom:1rem; border-bottom:2px solid var(--rr-pink); padding-bottom:0.35rem;">
      🏏 Batters (#4–7 Finishers): Tactical Rationale for All 10 Targets
    </h3>
    <div class="grid-2" style="margin-bottom:2.5rem;">
{batter_cards_html}
    </div>

    <!-- BOWLERS SQUAD FIT CARDS -->
    <h3 style="font-family:'Cabinet Grotesk',sans-serif; color:var(--rr-blue); font-size:1.35rem; margin-bottom:1rem; border-bottom:2px solid var(--rr-blue); padding-bottom:0.35rem;">
      🎯 Bowlers (Overs 7–20 Specialists): Tactical Rationale for All 10 Targets
    </h3>
    <div class="grid-2">
{bowler_cards_html}
    </div>

    <!-- FIGURE 4 -->
    <div class="figure-container" style="margin-top:2.5rem;">
      <img src="data:image/png;base64,{fig4_b64}" alt="Figure 4: RR Auction Target Matrix">
      <div class="figure-caption">
        <strong>Figure 4:</strong> Rajasthan Royals IPL 2027 Auction Target Matrix: High-Pressure Performance Index vs High-Pressure Sample Volume. Demonstrates the strategic balance between proven volume assets (Tim David, Chahal, Pathirana) and high-ceiling domestic steals (Ashutosh Sharma, Sameer Rizvi, Shubham Dubey).
      </div>
    </div>
  </section>

  <!-- SECTION 6: RELIABILITY & LIMITATIONS -->
  <section class="content-card">
    <div class="card-header-bar">
      <div class="card-title-group">
        <div class="section-num num-gold">5</div>
        <div>
          <h2 class="section-title">Model Reliability, Bayesian Shrinkage &amp; Analytical Limitations</h2>
          <p class="section-desc">Rigorous statistical verification and acknowledged analytical boundaries</p>
        </div>
      </div>
    </div>

    <div class="grid-2">
      <div style="background:var(--rr-slate-50); border:1px solid var(--rr-slate-200); border-radius:var(--radius-md); padding:1.5rem;">
        <h4 style="font-family:'Cabinet Grotesk',sans-serif; color:var(--rr-navy); font-size:1.1rem; margin-bottom:0.75rem;">
          Statistical Verification &amp; Bias Mitigation
        </h4>
        <ul style="font-size:0.88rem; color:#475569; line-height:1.7; margin-left:1.25rem;">
          <li><strong>Empirical Bayes Shrinkage:</strong> Regresses small sample sizes toward population priors (K=50 balls for batting, K=60 for bowling) to eliminate one-match sample flukes.</li>
          <li><strong>Clutch Consistency Rate (CCR):</strong> Evaluates the percentage of individual high-pressure matches where a player delivered net-positive output (xRA &gt; 0 or xRP &gt; 0). Penalizes volatile boom-or-bust players.</li>
          <li><strong>Competition Tier Weighting:</strong> IPL matches receive 1.30× weighting; ICC T20 World Cup matches receive 1.20×; bilateral T20Is receive 1.00×.</li>
        </ul>
      </div>

      <div style="background:var(--rr-slate-50); border:1px solid var(--rr-slate-200); border-radius:var(--radius-md); padding:1.5rem;">
        <h4 style="font-family:'Cabinet Grotesk',sans-serif; color:var(--rr-navy); font-size:1.1rem; margin-bottom:0.75rem;">
          Acknowledged Analytical Limitations
        </h4>
        <ul style="font-size:0.88rem; color:#475569; line-height:1.7; margin-left:1.25rem;">
          <li><strong>Absence of Ball-Tracking Trajectory Data:</strong> Hawkeye pitch-map and swing/seam deviation coordinates are proprietary to broadcasters, preventing precise quantification of pitch deterioration.</li>
          <li><strong>Dew Factor Invariance:</strong> Evening matches with heavy 2nd-innings dew reduce bowler grip, creating unavoidable run-rate variance between 1st and 2nd innings.</li>
          <li><strong>Captain Matchup Shielding:</strong> Certain specialized batters are shielded by captains from unfavorable matchups (e.g. left-arm spin vs left-handers).</li>
        </ul>
      </div>
    </div>
  </section>

</main>

<!-- PLAYER SCOUTING DOSSIER MODAL -->
<div class="modal-overlay" id="playerModal" onclick="closePlayerModal()">
  <div class="modal-content" onclick="event.stopPropagation()">
    <div class="modal-header">
      <button class="modal-close" onclick="closePlayerModal()">✕</button>
      <div style="font-size:0.78rem; font-weight:700; color:#FFA5D2; letter-spacing:0.05em; text-transform:uppercase;" id="modalCategory">WAR ROOM SCOUTING DOSSIER</div>
      <h2 style="font-family:'Cabinet Grotesk',sans-serif; font-weight:900; font-size:2rem; margin-top:0.25rem;" id="modalName">Player Name</h2>
      <div style="display:flex; gap:0.5rem; align-items:center; margin-top:0.5rem;">
        <span class="team-badge" id="modalTeam">TEAM</span>
        <span style="font-size:0.82rem; color:var(--rr-slate-300);" id="modalTier">Auction Tier</span>
      </div>
    </div>
    <div class="modal-body">
      <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:0.75rem; background:var(--rr-slate-50); padding:1rem; border-radius:var(--radius-md); border:1px solid var(--rr-slate-200); margin-bottom:1.5rem;">
        <div style="text-align:center;">
          <div style="font-size:0.72rem; color:#64748B; font-weight:700; text-transform:uppercase;">Performance Index</div>
          <div style="font-size:1.5rem; font-weight:900; font-family:'Cabinet Grotesk',sans-serif;" id="modalScore" class="text-pink">85.7</div>
        </div>
        <div style="text-align:center;">
          <div style="font-size:0.72rem; color:#64748B; font-weight:700; text-transform:uppercase;" id="modalMetricLabel">HP Strike Rate</div>
          <div style="font-size:1.5rem; font-weight:900; font-family:'JetBrains Mono',monospace;" id="modalMetricVal" class="text-navy">183.7</div>
        </div>
        <div style="text-align:center;">
          <div style="font-size:0.72rem; color:#64748B; font-weight:700; text-transform:uppercase;" id="modalDeltaLabel">Δ vs Baseline</div>
          <div style="font-size:1.5rem; font-weight:900; font-family:'JetBrains Mono',monospace;" id="modalDeltaVal" class="text-green">+46.1</div>
        </div>
      </div>

      <div style="margin-bottom:1.25rem;">
        <div style="font-size:0.8rem; font-weight:800; color:var(--rr-pink); text-transform:uppercase; letter-spacing:0.04em; margin-bottom:0.25rem;">
          🏟️ Sawai Mansingh Stadium (Jaipur) Fit
        </div>
        <p style="font-size:0.9rem; color:#334155; line-height:1.5;" id="modalJaipurFit">Fit details</p>
      </div>

      <div style="margin-bottom:1.25rem;">
        <div style="font-size:0.8rem; font-weight:800; color:var(--rr-blue); text-transform:uppercase; letter-spacing:0.04em; margin-bottom:0.25rem;">
          🤝 Fit with RR Core XI
        </div>
        <p style="font-size:0.9rem; color:#334155; line-height:1.5;" id="modalRRFit">RR fit details</p>
      </div>

      <div style="background:#FFFBEB; border-left:3px solid var(--rr-gold); padding:0.85rem 1rem; border-radius:0 var(--radius-sm) var(--radius-sm) 0;">
        <div style="font-size:0.78rem; font-weight:800; color:#B45309; text-transform:uppercase; margin-bottom:0.2rem;">
          Auction Strategic Rationale
        </div>
        <p style="font-size:0.85rem; color:#92400E; line-height:1.5;" id="modalWhyBid">Why bid details</p>
      </div>
    </div>
  </div>
</div>

<footer>
  <div style="max-width:800px; margin:0 auto;">
    <h3 style="color:white; font-family:'Cabinet Grotesk',sans-serif; font-size:1.35rem; margin-bottom:0.5rem;">
      Rajasthan Royals War Room Player Evaluation
    </h3>
    <p style="font-size:0.85rem; margin-bottom:1.25rem;">
      Proprietary Delivery-Level Analysis across 200,999 Deliveries (2022–2026) • Prepared for SupeRR Selector Season 2
    </p>
    <p style="font-size:0.8rem; color:#64748B;">
      <a href="https://github.com/Shubhdix9/RR">GitHub Repository</a> • 
      <a href="https://shubhdix9.github.io/RR/">Live Dashboard URL</a>
    </p>
  </div>
</footer>

<!-- INTERACTIVE SCRIPTS -->
<script>
// Embedded Player Data
const playersData = {players_json_str};

// Search Filter
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

// Modal Controller
function openPlayerModal(playerName) {{
  const player = playersData.find(p => p.name === playerName);
  if (!player) return;

  document.getElementById('modalCategory').innerText = player.type === 'batter' 
    ? 'WAR ROOM BATTING DOSSIER • RANK #' + player.rank 
    : 'WAR ROOM BOWLING DOSSIER • RANK #' + player.rank;
  
  document.getElementById('modalName').innerText = player.name;
  document.getElementById('modalTeam').innerText = player.team;
  document.getElementById('modalTier').innerText = player.tier;
  document.getElementById('modalScore').innerText = player.score.toFixed(1);
  document.getElementById('modalScore').className = player.type === 'batter' ? 'text-pink' : 'text-blue';

  if (player.type === 'batter') {{
    document.getElementById('modalMetricLabel').innerText = 'HP Strike Rate';
    document.getElementById('modalMetricVal').innerText = player.primary_metric.toFixed(1);
    document.getElementById('modalDeltaLabel').innerText = 'Δ vs Baseline';
    document.getElementById('modalDeltaVal').innerText = '+' + player.delta.toFixed(1);
    document.getElementById('modalDeltaVal').className = 'text-green';
  }} else {{
    document.getElementById('modalMetricLabel').innerText = 'HP Economy';
    document.getElementById('modalMetricVal').innerText = player.primary_metric.toFixed(2);
    document.getElementById('modalDeltaLabel').innerText = 'Δ Suppression';
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

// Close modal on Escape
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

print("Successfully generated elite RR_WAR_ROOM_REPORT.html and index.html!")

