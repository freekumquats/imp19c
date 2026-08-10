export const meta = {
  name: 'overnight-diff-review-70',
  description: 'Adversarial review of the entire overnight diff (merge-overnight vs pre-run base), clustered by subsystem, find -> adversarial-verify, confirmed bugs only',
  phases: [
    { title: 'Find', detail: 'one adversarial finder per subsystem cluster over its diff hunks' },
    { title: 'Verify', detail: 'adversarially verify each finding; drop what cannot be confirmed' },
  ],
}

// #70: the user opted into a workflow to review the ENTIRE overnight diff, iterate-until-clean.
// Diff base = deee0b3f0 (parent of the run's first commit c2375d4d2); HEAD = merge-overnight.
// Each cluster's finder reads its OWN files' diff hunks + surrounding source, hunts REAL shipped
// bugs (not style), returns structured findings; each finding is then independently verified by a
// skeptic instructed to REFUTE. Only CONFIRMED bugs reach the caller. One Workflow run = one pass.

const BASE = 'deee0b3f0aee105789ef4d76d93ab15b541ae316'
const HEAD = 'merge-overnight'

const TRAPS = `imp19c standing traps to check: brace imbalance; BOM convention (common/ + loc want a UTF-8 BOM, setup/ REJECTS BOM, events/ + se_ are no-BOM/LF); CRLF vs LF flips (autocrlf=input, repo stores LF); a $macro$ or # INSIDE a quoted LOG_line/LOG_fail/debug_log string (silently voids the whole call); an arg passed to a macro the body never references (compile-fails the call); var: on a comparison RHS (illegal — RHS must be a literal or svalue); set_variable/change_variable INSIDE a script_value (illegal — svalues are pure arithmetic); has_variable true even when a var was set to empty/none (set-but-empty operand); ordered_* iterators default max=1 (multi-add needs explicit max); loc reads saved scopes BARE [x.GetName] never [scope:x]; add_law is UNPROVEN (never in shipped code); RHS of comparison cannot be a var. Only report a trap you can point to at a real file:line in the diff.`

const FINDER_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          file: { type: 'string' },
          line: { type: 'integer' },
          severity: { type: 'string', enum: ['CRITICAL', 'HIGH', 'MED', 'LOW'] },
          category: { type: 'string' },
          summary: { type: 'string', description: 'one-sentence defect statement' },
          failure_scenario: { type: 'string', description: 'concrete inputs/state -> wrong output/crash' },
          evidence: { type: 'string', description: 'the specific code + why it is wrong, cite file:line' },
        },
        required: ['file', 'severity', 'summary', 'failure_scenario', 'evidence'],
      },
    },
  },
  required: ['findings'],
}

const VERDICT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    verdict: { type: 'string', enum: ['CONFIRMED', 'REFUTED', 'UNCERTAIN'] },
    reasoning: { type: 'string', description: 'what you checked in source and what you found' },
    corrected_severity: { type: 'string', enum: ['CRITICAL', 'HIGH', 'MED', 'LOW'] },
    fix: { type: 'string', description: 'the concrete fix if CONFIRMED' },
  },
  required: ['verdict', 'reasoning'],
}

// Subsystem clusters. Each = {key, focus, files[]}. Files are the run-diff members of that subsystem.
const CLUSTERS = [
  {
    key: 'econ-currency',
    focus: 'The economy/currency core — the HIGHEST-risk cluster (#23 peg, #50 regional prices, #52 tier realism, #59 bimetallic, #62 NW double-count, #63 monetary-policy law, #67 paper money, #69 steel join). Hunt: any manufactured/trade price change that could cascade into the gold/silver currency peg (CURRENCY_wealth_value reads ONLY gold/silver — confirm nothing new feeds it); div/0 from a price or stockpile approaching 0; a mean-reverting/pull loop (bimetallic, currency stress) that could re-amplify like the #23 sawtooth; the paper-money mint allowance compounding month-over-month; the steel factory-count join double-counting or desyncing produce vs consume; DEMAND svalue changes over/under-producing; a var read-before-set flooding the log.',
    files: [
      'common/laws/00_monetary_policy_setting.txt',
      'common/on_action/economy/oa_economy_setup.txt',
      'common/on_action/economy/oa_wealth_changes.txt',
      'common/script_values/CURRENCY_svalues.txt',
      'common/script_values/DEMAND_luxury_svalues.txt',
      'common/script_values/DEMAND_svalues.txt',
      'common/script_values/GOODS_svalues.txt',
      'common/script_values/INDUSTRY_svalues.txt',
      'common/scripted_effects/se_DEMAND.txt',
      'common/scripted_effects/se_GLOBALTRADE_split.txt',
      'common/scripted_effects/se_GOODS.txt',
      'common/scripted_effects/se_QING_BIMETALLIC.txt',
      'common/scripted_effects/se_QING_DECLINE.txt',
    ],
  },
  {
    key: 'econ-log-probe',
    focus: 'The econ diagnostic/probe instrumentation (#51 gold/salt/luxury logs, #52 tzprobe, #35 restored #23 tooling). Hunt: read-before-set var floods (the #47 class — the single worst log source), a $macro$/# inside a LOG string, an unbalanced probe block, a probe that measures the WRONG good/var (the set-but-empty operand trap), a strip/restore that left a dangling call.',
    files: [
      'common/scripted_effects/se_ECON_LOG.txt',
      'common/scripted_effects/se_ECON_LOG_TZPROBE.txt',
    ],
  },
  {
    key: 'qing-fiscal',
    focus: 'Qing fiscal/revenue/salt/canton/piaohao subsystems (#44 salt monopoly + commissioner, #111 Canton/Hoppo, piaohao). Hunt: siphon/skim that hits the treasury or silver reserve when it should be char-state only; a revenue term that inflates income unboundedly; a commissioner-factor with no band clamp; log-macro violations; court-slot/cooldown throttles missing (the #41 flood class).',
    files: [
      'common/scripted_effects/se_QING_REVENUE.txt',
      'common/scripted_effects/se_QING_SALT.txt',
      'common/scripted_effects/se_QING_CANTON.txt',
      'common/scripted_effects/se_QING_PIAOHAO.txt',
      'common/scripted_effects/se_QING_ACCOUNTABILITY.txt',
    ],
  },
  {
    key: 'qing-frontier-caravan',
    focus: 'Frontier / caravan / aqsaqal / Xinjiang / Ili subsystems (#112 superintendent+aqsaqal+contest, #12 coupling). Hunt: a created character granted then dangling on revoke/death (lifecycle-teardown not paired), a create_character grant to a just-made char (crash gotcha), ownerless-capital, an event with no firing path OR that bypasses the shared court slot, a contest svalue with no clamp, is_subject_of not-recursive for nested subjects.',
    files: [
      'common/scripted_effects/se_QING_CARAVAN.txt',
      'common/scripted_effects/se_QING_FRONTIER.txt',
      'common/scripted_effects/se_QING_XINJIANG.txt',
      'common/scripted_effects/se_QING_ILI.txt',
      'common/scripted_effects/se_SUBJECT_QING.txt',
      'common/scripted_effects/se_QING_INTEG_CAPSTONE.txt',
    ],
  },
  {
    key: 'qing-court-personnel',
    focus: 'Qing court / council / personnel / governance / exam / deliberative / wenzhi. Hunt: an event recurring every quarter (no cooldown), always picking the same character (bad ordered_* / no exclusion), a personnel clash bypassing the realm cooldown, a meter that ratchets without a restoring drift (no-restoring-drift rule), a GC event throttle share missing.',
    files: [
      'common/scripted_effects/se_QING_COUNCIL.txt',
      'common/scripted_effects/se_QING_PERSONNEL.txt',
      'common/scripted_effects/se_QING_GOVERNANCE.txt',
      'common/scripted_effects/se_QING_EXAM.txt',
      'common/scripted_effects/se_QING_DELIBERATIVE.txt',
      'common/scripted_effects/se_QING_WENZHI.txt',
      'common/script_values/QING_governance_svalues.txt',
    ],
  },
  {
    key: 'qing-misc-mechanics',
    focus: 'Qing amban/diplo/legations/works/canal/buildings/population/war/summer-palace/selfstr/mechanics/foreignbuild/land. Hunt: amban minor-char crash class, diplomat=commander misuse, a modifier with no band gate, a building add that fails a potential and hides, a pop-boom modifier that runs away, a mission beat in a fleet-gated tree, on_action wiring that double-fires.',
    files: [
      'common/scripted_effects/se_QING_AMBAN.txt',
      'common/scripted_effects/se_QING_DIPLO.txt',
      'common/scripted_effects/se_QING_LEGATIONS.txt',
      'common/scripted_effects/se_QING_WORKS.txt',
      'common/scripted_effects/se_QING_CANAL.txt',
      'common/scripted_effects/se_QING_BUILDINGS.txt',
      'common/scripted_effects/se_QING_POPULATION.txt',
      'common/scripted_effects/se_QING_WAR.txt',
      'common/scripted_effects/se_QING_SUMMER_PALACE.txt',
      'common/scripted_effects/se_QING_SELFSTR.txt',
      'common/scripted_effects/se_QING_MECHANICS.txt',
      'common/scripted_effects/se_QING_FOREIGNBUILD.txt',
      'common/scripted_effects/se_LAND.txt',
      'common/buildings/00_infrastructure_buildings.txt',
      'common/buildings/qing_granary_buildings.txt',
      'common/missions/qing_settle_frontier_missions.txt',
      'common/modifiers/qing_migration_modifiers.txt',
      'common/opinions/imp19c_opinions.txt',
      'common/on_action/qing_mechanics_on_actions.txt',
      'common/script_values/00_event_values.txt',
    ],
  },
  {
    key: 'events-econ-fiscal',
    focus: 'Event files for the econ/fiscal/paper-money/salt/canton/revenue/piaohao/caravan/decline/currency subsystems. Hunt: an event with no firing path (no MTTH/is_triggered_only/dispatcher — the inert-lever class), an empty/missing trigger firing anachronistically (pre-1763-appropriate), a court-slot bypass, an option that claims an effect the loc promises but does not deliver, a $macro$/# in a LOG string, a dangling saved-scope in desc, an event double-firing.',
    files: [
      'events/imp19c_mod_events/qing_paper_money_events.txt',
      'events/imp19c_mod_events/currency_crisis_events.txt',
      'events/imp19c_mod_events/qing_revenue_events.txt',
      'events/imp19c_mod_events/qing_canton_events.txt',
      'events/imp19c_mod_events/qing_caravan_events.txt',
      'events/imp19c_mod_events/qing_piaohao_events.txt',
      'events/imp19c_mod_events/qing_decline_events.txt',
      'events/imp19c_mod_events/qing_opium_events.txt',
      'events/imp19c_mod_events/qing_americas_events.txt',
      'events/imp19c_mod_events/qing_canal_events.txt',
    ],
  },
  {
    key: 'events-court-frontier',
    focus: 'Event files for court/personnel/amban/frontier/caravan-contest/legation/diplo/keju/office/rites/household/culture/character/integration. Hunt: same as events-econ-fiscal — inert events, anachronistic triggers, court-slot bypass, dangling scopes, loc-promise-vs-effect mismatch, marriage/character picker selecting a forbidden target, an event recurring without cooldown.',
    files: [
      'events/imp19c_mod_events/qing_amban_events.txt',
      'events/imp19c_mod_events/qing_personnel_events.txt',
      'events/imp19c_mod_events/qing_frontier_events.txt',
      'events/imp19c_mod_events/qing_frontier_migration_events.txt',
      'events/imp19c_mod_events/qing_frontier_sea_events.txt',
      'events/imp19c_mod_events/qing_legation_events.txt',
      'events/imp19c_mod_events/qing_keju_events.txt',
      'events/imp19c_mod_events/qing_office_events.txt',
      'events/imp19c_mod_events/qing_household_events.txt',
      'events/imp19c_mod_events/qing_character_events.txt',
      'events/imp19c_mod_events/qing_culture_events.txt',
      'events/imp19c_mod_events/qing_integration_capstone_events.txt',
      'events/imp19c_mod_events/qing_subject_integration.txt',
      'events/imp19c_mod_events/FlavorEvents.txt',
    ],
  },
  {
    key: 'events-flavor-rest',
    focus: 'The remaining Qing event files (advisor/mandate/march/nanyang/pilgrimage/rebellion/reform/rites/roster/summer_palace/techtransfer/tribute/vassal/war/works/xinjiang/ili/golden_urn/greatgame/ethnic/force_setup). Hunt: same event traps.',
    files: [
      'events/imp19c_mod_events/qing_advisor_events.txt',
      'events/imp19c_mod_events/qing_mandate_events.txt',
      'events/imp19c_mod_events/qing_march_events.txt',
      'events/imp19c_mod_events/qing_march_relief_events.txt',
      'events/imp19c_mod_events/qing_nanyang_events.txt',
      'events/imp19c_mod_events/qing_pilgrimage_events.txt',
      'events/imp19c_mod_events/qing_rebellion_events.txt',
      'events/imp19c_mod_events/qing_reform_events.txt',
      'events/imp19c_mod_events/qing_rites_events.txt',
      'events/imp19c_mod_events/qing_roster_events.txt',
      'events/imp19c_mod_events/qing_summer_palace_events.txt',
      'events/imp19c_mod_events/qing_techtransfer_events.txt',
      'events/imp19c_mod_events/qing_tribute_events.txt',
      'events/imp19c_mod_events/qing_vassal_events.txt',
      'events/imp19c_mod_events/qing_war_events.txt',
      'events/imp19c_mod_events/qing_works_events.txt',
      'events/imp19c_mod_events/qing_xinjiang_events.txt',
      'events/imp19c_mod_events/qing_ili_events.txt',
      'events/imp19c_mod_events/qing_golden_urn.txt',
      'events/imp19c_mod_events/qing_greatgame_events.txt',
      'events/imp19c_mod_events/qing_ethnic_tension_events.txt',
      'events/imp19c_mod_events/qing_force_setup_events.txt',
      'events/imp19c_mod_events/qing_advisor_events.txt',
    ],
  },
  {
    key: 'gui-setup',
    focus: 'GUI panels + scripted_guis + setup/provinces (#64 crop seeding) + scripted_triggers. Hunt: a scripted_gui button chain that recurses at parse (AV crash), .IsSet on a char-valued var (renders nothing), a panel reading a saved scope with [scope:x] instead of bare, a fixed scrollarea cutoff, a setup/provinces file with a BOM (setup reader REJECTS BOM) or a trade_goods= typo, a dangling trigger.',
    files: [
      'common/scripted_guis/QING_caravan_panel.txt',
      'common/scripted_guis/QING_revenue_ministry_panel.txt',
      'common/scripted_guis/QING_salt_panel.txt',
      'common/scripted_guis/QING_works_ministry_panel.txt',
      'common/scripted_guis/QING_population_panel.txt',
      'common/scripted_guis/QING_deliberative_panel.txt',
      'common/scripted_guis/QING_household_panel.txt',
      'common/scripted_guis/QING_xinjiang_panel.txt',
      'common/scripted_guis/QING_mechanics_actions.txt',
      'common/scripted_guis/SUB_QING_amban.txt',
      'gui/imp19c_windows.gui',
      'gui/qing_caravan.gui',
      'gui/qing_revenue_ministry.gui',
      'gui/qing_works_ministry.gui',
      'common/scripted_triggers/00_imp19c_republic_triggers.txt',
      'common/scripted_triggers/qing_dynasty_triggers.txt',
      'setup/provinces/00_American_Southwest.txt',
      'setup/provinces/00_Antilles.txt',
      'setup/provinces/00_Argentina.txt',
      'setup/provinces/00_Central_America.txt',
      'setup/provinces/00_Eastern_Mexico.txt',
      'setup/provinces/00_Lower_Peru.txt',
      'setup/provinces/00_North_Brazil.txt',
      'setup/provinces/00_Northeast_Brazil.txt',
      'setup/provinces/00_Northern_Mexico.txt',
      'setup/provinces/00_Pacific_Mexico.txt',
      'setup/provinces/00_Peru.txt',
      'setup/provinces/00_South_Brazil.txt',
      'setup/provinces/00_Southeast_Brazil.txt',
    ],
  },
]

log(`#70 overnight-diff review: ${CLUSTERS.length} subsystem clusters, diff base ${BASE.slice(0, 9)} -> ${HEAD}`)

const results = await pipeline(
  CLUSTERS,
  // STAGE 1 — adversarial finder per cluster
  (cluster) => {
    const fileList = cluster.files.join(' ')
    return agent(
      `You are an ADVERSARIAL code reviewer for the imp19c mod (Imperatrix: Victoria — Qing/1763 total conversion of Imperator: Rome, Paradox Jomini script). Repo root: /Users/alan.chiang/github.com/imp19c.

You are reviewing the OVERNIGHT DIFF for the "${cluster.key}" subsystem cluster. Your job: find REAL, SHIPPED BUGS in the CHANGES — not style, not nitpicks, not pre-existing issues outside the diff.

FIRST, read the actual diff for this cluster's files (the ONLY files you review):
  git -C /Users/alan.chiang/github.com/imp19c diff ${BASE}..${HEAD} -- ${fileList}
Then read the surrounding source of any changed region you suspect, to confirm the bug is real and reachable (use Read/Grep — trace called svalues/effects, confirm a var is set before read, confirm an event has a firing path, confirm scope). Ground EVERY finding in a specific file:line that is IN THE DIFF (added/changed lines). A defect in unchanged code far from the diff is out of scope unless the diff newly EXPOSES it.

FOCUS FOR THIS CLUSTER: ${cluster.focus}

${TRAPS}

Report only defects that would ship broken or wrong: crashes, inert/unreachable mechanics, unbounded/runaway values, double-counts, log floods, peg/economy breaks, wrong character/target selection, missing throttles, loc-promise-vs-effect mismatches, anachronistic firing. For each, give the file:line, a one-sentence summary, a concrete failure scenario (inputs -> wrong result), and the evidence. If the cluster is clean, return an empty findings array — do NOT invent findings to look thorough. Be precise; a false positive wastes a verify agent.`,
      { label: `find:${cluster.key}`, phase: 'Find', schema: FINDER_SCHEMA }
    ).then((r) => ({ cluster: cluster.key, findings: (r && r.findings) || [] }))
  },
  // STAGE 2 — adversarially verify each finding from this cluster (concurrent)
  (found) => {
    if (!found || !found.findings.length) return { cluster: found ? found.cluster : 'unknown', verified: [] }
    return parallel(
      found.findings.map((f) => () =>
        agent(
          `You are a SKEPTICAL verifier for the imp19c mod (Paradox Jomini script). Repo root: /Users/alan.chiang/github.com/imp19c. Another reviewer claims this is a bug in the overnight diff. Your job is to REFUTE it — default to REFUTED unless you can CONFIRM it in source.

CLAIM (${found.cluster}): [${f.severity}] ${f.summary}
FILE:LINE: ${f.file}:${f.line || '?'}
FAILURE SCENARIO: ${f.failure_scenario}
EVIDENCE GIVEN: ${f.evidence}

Verify against ACTUAL source: open ${f.file} at that line, read the surrounding block, trace any called svalue/effect/event, confirm the scope, confirm whether the claimed failure can actually occur. Check the diff itself (git -C /Users/alan.chiang/github.com/imp19c diff ${BASE}..${HEAD} -- ${f.file}) to confirm the line is actually changed by this run and not pre-existing. Common reasons to REFUTE: the operand IS set before read; the event DOES have a firing path (dispatcher/MTTH/on_action); the value IS clamped/bounded elsewhere; a guard makes the scenario unreachable; the "bug" is in unchanged code; has_variable-set-but-empty is actually handled; the RHS is a literal not a var. If it IS a real, reachable, shipped defect, CONFIRM it and give the concrete fix. ${TRAPS}`,
          { label: `verify:${found.cluster}:${(f.file || '').split('/').pop()}`, phase: 'Verify', schema: VERDICT_SCHEMA }
        ).then((v) => ({ ...f, cluster: found.cluster, verdict: v }))
      )
    ).then((vs) => ({ cluster: found.cluster, verified: vs.filter(Boolean) }))
  }
)

// Collect only CONFIRMED findings, ranked by severity.
const SEV = { CRITICAL: 0, HIGH: 1, MED: 2, LOW: 3 }
const confirmed = results
  .filter(Boolean)
  .flatMap((r) => r.verified || [])
  .filter((f) => f.verdict && f.verdict.verdict === 'CONFIRMED')
  .map((f) => ({
    cluster: f.cluster,
    file: f.file,
    line: f.line,
    severity: f.verdict.corrected_severity || f.severity,
    summary: f.summary,
    failure_scenario: f.failure_scenario,
    fix: f.verdict.fix || '',
  }))
  .sort((a, b) => (SEV[a.severity] ?? 9) - (SEV[b.severity] ?? 9))

const raw = results.filter(Boolean).reduce((n, r) => n + (r.verified ? r.verified.length : 0), 0)
log(`#70 pass complete: ${raw} raw findings across ${CLUSTERS.length} clusters -> ${confirmed.length} CONFIRMED after adversarial verify`)

return {
  pass: 'overnight-diff-review',
  clusters: CLUSTERS.length,
  raw_findings: raw,
  confirmed_count: confirmed.length,
  clean: confirmed.length === 0,
  confirmed,
}
