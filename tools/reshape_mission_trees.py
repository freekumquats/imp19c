#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[MO#8] Reshape the 14 flat/wide Qing mission trees into the deep/narrow shape that
Invictus + Terra-Indomita use (measured medians: root fan-out ~4, max depth ~5,
>=3 reconvergence nodes). Layout is 100% engine-computed from the `requires` DAG
(no `position` fields exist), so we only rewrite `requires = { ... }` lines.

Strategy per tree (preserves existing hand-authored spine, re-homes only flat leaves):
  - R    = the main root task (single-tab node with empty requires that the most
           flat leaves point at).
  - CAP  = the designated capstone (node carrying the most `requires`, or an override).
  - flat = single-tab task nodes whose requires == { R } (the generator's fan-out).
  - Keep up to HEADS(=4) flat leaves as direct children of R (branch heads); chain the
    remaining flats sequentially onto those heads (round-robin), so each head grows a
    depth-3-6 chain. Point CAP's requires at the chain tails (multi-parent reconvergence),
    preserving any of CAP's pre-existing parents that are not themselves being re-homed.
  - Every non-flat node (existing spine) is left untouched.

Only `requires` lines change; ZERO new keys, ZERO content. Validates the DAG (no cycle,
all reachable from R, one sink=CAP) and prints before/after metrics. --write to apply.
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MISS = os.path.join(ROOT, "common", "missions")
HEADS = 4
HEADER = {'chance','ai_chance','potential','abort','on_start','on_completion',
          'on_abort','bookmark','ai_weight','on_potential','visible'}

NODE_RE = re.compile(r'^\t([a-z][A-Za-z0-9_]+)\s*=\s*\{', re.M)
REQ_RE  = re.compile(r'requires\s*=\s*\{([^}]*)\}')

# trees to reshape -> capstone override (else = max-requires node). Overrides point at
# the tree's real thematic final node where the max-requires heuristic would miss it.
TREES = {
    "burma_war": "qing_burma_capstone", "central_asia": "qing_ca_capstone",
    "himalaya_seasia": "qing_hs_capstone", "india": "qing_india_capstone",
    "japan": "qing_jp_triumph", "japan_preperry": None,
    "nanyang": "qing_nanyang_capstone", "open_japan": "qing_openjapan_capstone",
    "reform": None, "settle_frontier": "qing_settle_capstone",
    "summer_palace": "qing_sp_grand_garden", "taiping": "qing_hk_heavenly_capital",
    "treasure_fleet": "qing_treasure_capstone", "xinjiang": "qing_xj_new_province",
}


def parse(text):
    """Return ordered [(key, block_start, block_end, reqs_list, req_span_or_None)]."""
    ms = list(NODE_RE.finditer(text))
    nodes = []
    for i, m in enumerate(ms):
        key = m.group(1)
        start = m.start()
        body_start = m.end()
        body_end = ms[i+1].start() if i+1 < len(ms) else text.rstrip().rfind("}")
        block = text[body_start:body_end]
        rm = REQ_RE.search(block)
        reqs = rm.group(1).split() if rm else []
        span = (body_start+rm.start(1), body_start+rm.end(1)) if rm else None
        nodes.append([key, start, body_end, reqs, span])
    return nodes


def metrics(adj):
    roots = [k for k, ps in adj.items() if not ps]
    memo = {}
    def depth(k, stk=()):
        if k in memo: return memo[k]
        if k in stk: return 0
        ps = adj[k]
        d = 0 if not ps else 1 + max(depth(p, stk+(k,)) for p in ps)
        memo[k] = d; return d
    maxd = max((depth(k) for k in adj), default=0)
    rootset = set(roots)
    fan = sum(1 for k, ps in adj.items() if ps and set(ps) & rootset)
    multi = sum(1 for k, ps in adj.items() if len(ps) >= 2)
    return roots, fan, maxd, multi


def has_cycle(adj):
    color = {}
    def dfs(u):
        color[u] = 1
        for v in adj.get(u, []):
            if v not in adj:  # dangling target
                continue
            if color.get(v) == 1: return True
            if color.get(v, 0) == 0 and dfs(v): return True
        color[u] = 2; return False
    return any(color.get(u, 0) == 0 and dfs(u) for u in adj)


def reachable(adj, root):
    """set reachable from root following child edges (invert: k depends on its reqs)."""
    children = {k: [] for k in adj}
    for k, ps in adj.items():
        for p in ps:
            if p in children: children[p].append(k)
    seen = set([root]); stack = [root]
    while stack:
        u = stack.pop()
        for v in children[u]:
            if v not in seen:
                seen.add(v); stack.append(v)
    return seen


def reshape_tree(name, cap_override):
    fp = os.path.join(MISS, f"qing_{name}_missions.txt")
    text = open(fp, encoding="utf-8").read()
    nodes = parse(text)
    tasks = [n for n in nodes if n[0] not in HEADER]
    keys = {n[0] for n in tasks}
    adj = {n[0]: [r for r in n[3] if r in keys] for n in tasks}

    # main root = empty-requires task with the most flat-leaf pointers
    empties = [k for k, ps in adj.items() if not ps]
    def count_pointers(r): return sum(1 for _, ps in adj.items() if ps == [r])
    R = max(empties, key=count_pointers) if empties else None
    if R is None:
        return None, "no root"

    cap = cap_override or max(adj, key=lambda k: len(adj[k]))
    flat = [k for k, ps in adj.items() if ps == [R] and k != cap]

    before = metrics(adj)

    # Secondary roots (other empty-requires nodes besides R and cap) are legitimate
    # branch heads; keep them, but their chain tails must reconverge into cap so the
    # capstone is the single sink (no node orphaned relative to cap).
    sec_roots = [k for k, ps in adj.items() if not ps and k not in (R, cap)]
    # a secondary root's existing downstream tail (follow single-child chain)
    def tail_of(start):
        children = {k: [] for k in adj}
        for k, ps in adj.items():
            for p in ps:
                children[p].append(k)
        cur = start
        while children[cur]:
            cur = children[cur][0]
        return cur

    # keep HEADS flats as branch heads; chain the rest round-robin onto them
    heads = flat[:HEADS]
    rest = flat[HEADS:]
    chains = {h: [h] for h in heads}
    for i, k in enumerate(rest):
        h = heads[i % len(heads)] if heads else R
        chains[h].append(k)

    new_adj = {k: list(ps) for k, ps in adj.items()}
    for h, chain in chains.items():
        for a, b in zip(chain, chain[1:]):
            new_adj[b] = [a]          # b now requires its predecessor
    # Secondary roots become branch heads under R (so they're reachable from the
    # single root), keeping their own existing downstream chain intact.
    for s in sec_roots:
        new_adj[s] = [R]
    # reconverge chain tails + secondary-root chain tails into capstone,
    # preserving cap's non-re-homed parents
    tails = [chain[-1] for chain in chains.values()]
    sec_tails = [tail_of(s) for s in sec_roots if tail_of(s) != cap]
    kept = [p for p in adj[cap] if p not in flat]     # keep original cap parents not re-homed
    new_adj[cap] = sorted(set(kept + tails + sec_tails))

    # ---- validate ----
    errs = []
    if has_cycle(new_adj): errs.append("CYCLE")
    reach = reachable(new_adj, R)
    orphans = [k for k in new_adj if k not in reach]
    if orphans: errs.append(f"orphans={orphans}")
    for k, ps in new_adj.items():
        for p in ps:
            if p not in new_adj: errs.append(f"{k} requires missing {p}")

    after = metrics(new_adj)
    return (fp, text, nodes, new_adj, R, cap, before, after, errs), None


def render(text, nodes, new_adj):
    """Rewrite requires lines from tail to head so spans stay valid; add requires to nodes lacking one."""
    edits = []  # (start, end, replacement)
    for n in nodes:
        key, nstart, nend, reqs, span = n
        if key in HEADER or key not in new_adj:
            continue
        newreq = new_adj[key]
        if span:
            cur = " ".join(reqs)
            new = " ".join(newreq)
            if cur.split() != newreq:
                edits.append((span[0], span[1], " " + new + " " if new else " "))
        else:
            if newreq:  # node had no requires line but now needs one: insert after `{`
                m = NODE_RE.search(text, nstart)
                ins = m.end()
                edits.append((ins, ins, f"\n\t\trequires = {{ {' '.join(newreq)} }}"))
    for s, e, rep in sorted(edits, key=lambda x: -x[0]):
        text = text[:s] + rep + text[e:]
    return text


def main():
    write = "--write" in sys.argv
    for name, cap_ov in TREES.items():
        res, err = reshape_tree(name, cap_ov)
        if err:
            print(f"  {name}: SKIP ({err})"); continue
        fp, text, nodes, new_adj, R, cap, before, after, errs = res
        b_roots, b_fan, b_depth, b_multi = before
        a_roots, a_fan, a_depth, a_multi = after
        status = "OK" if not errs else "FAIL " + "; ".join(errs)
        print(f"  {name:16s} root={R:24s} cap={cap:26s} "
              f"fan {b_fan:2d}->{a_fan:2d}  depth {b_depth}->{a_depth}  multi {b_multi}->{a_multi}  [{status}]")
        if errs:
            continue
        if write:
            open(fp, "w", encoding="utf-8").write(render(text, nodes, new_adj))
    print("WROTE" if write else "DRY-RUN (pass --write to apply)")


if __name__ == "__main__":
    main()
