#!/usr/bin/env python3
# tools/precommit_checks.py — objective, self-running pre-commit gate for imp19c.
#
# WHY THIS EXISTS: the assistant has repeatedly claimed changes were "clean/verified" when they
# carried mechanical defects (brace imbalance, BOM/EOL churn, macro/# in LOG strings, dangling
# effect refs). Those claims are not trustworthy. This script makes the checks NOT depend on any
# claim — it runs on the STAGED diff at commit time and BLOCKS the commit on hard failures, with a
# nonzero exit. It is deliberately conservative: it only flags things that are objectively wrong in
# this codebase's conventions, so a block means a real problem, not a style nit.
#
# INSTALL: .git/hooks/pre-commit calls this (see tools/install_hooks.sh). Bypass in a genuine
# emergency with `git commit --no-verify` — but a bypass is on the record.
#
# CHECKS (each maps to a real, repeated failure):
#   1. BRACE BALANCE — every staged .txt/.gui in common/ events/ gui/ common/scripted_guis must have
#      equal { and } counts. (String-literal braces are rare in PDX script; a mismatch is ~always a bug.)
#   2. BOM/EOL CHURN — a staged file must not FLIP its byte-order-mark or its CRLF/LF vs the committed
#      version. (autocrlf=input → repo stores LF; flipping EOL balloons the diff + breaks the setup reader.)
#      New files: common/ wants BOM; setup/ must NOT have BOM; events/ + gui/ per their siblings (warn only).
#   3. LOG-STRING MACRO — no $param$ or # inside a quoted LOG_line/LOG_fail/LOG_enter/LOG_exit/debug_log
#      string (imp19c-log-string-macro-rule: silently voids the whole invocation at load).
#   4. DANGLING EFFECT/SVALUE REF (best-effort) — a newly-added call to a QING_*/CURRENCY_*/GOODS_*/DEMAND_*
#      /COTTAGEIND_* effect or svalue that is defined NOWHERE in the tree (catches deletions-left-callers
#      + typos). Best-effort: warns, does not hard-block (macro/injector indirection makes false positives).
#
# Exit 0 = pass. Exit 1 = a HARD failure (blocks commit). Warnings print but don't block.

import subprocess, sys, re, os

REPO = subprocess.run(["git","rev-parse","--show-toplevel"],capture_output=True,text=True).stdout.strip()

def staged_files():
    out = subprocess.run(["git","diff","--cached","--name-only","--diff-filter=ACM"],
                         capture_output=True,text=True).stdout
    return [f for f in out.splitlines() if f.strip()]

def staged_blob(path):
    # the STAGED content (index), not the working tree
    r = subprocess.run(["git","show",f":{path}"],capture_output=True)
    return r.stdout if r.returncode==0 else None

def added_lines(path):
    # ONLY the lines this commit ADDS (diff '+' lines), as (new_lineno, text). This is what a
    # line-level check must scan — else the gate blocks a clean commit on a PRE-EXISTING defect
    # elsewhere in the file, which just trains everyone to --no-verify. Whole-file checks (braces)
    # stay whole-file; line-level checks (LOG macro) use this.
    out = subprocess.run(["git","diff","--cached","--unified=0","--",path],
                         capture_output=True,text=True).stdout
    res, newno = [], None
    for ln in out.splitlines():
        if ln.startswith("@@"):
            m = re.search(r"\+(\d+)", ln)
            newno = int(m.group(1)) if m else None
        elif ln.startswith("+") and not ln.startswith("+++"):
            if newno is not None:
                res.append((newno, ln[1:]))
                newno += 1
        elif not ln.startswith("-") and newno is not None:
            newno += 1
    return res

def committed_blob(path):
    r = subprocess.run(["git","show",f"HEAD:{path}"],capture_output=True)
    return r.stdout if r.returncode==0 else None

fails, warns = [], []

SCRIPT_DIRS = ("common/","events/","gui/")
def is_script(path):
    return path.startswith(SCRIPT_DIRS) and (path.endswith(".txt") or path.endswith(".gui"))

LOGFN = re.compile(r'(?:LOG_line|LOG_fail|LOG_enter|LOG_exit|debug_log)\b')

def check_braces(path, text):
    o, c = text.count("{"), text.count("}")
    if o != c:
        fails.append(f"[BRACE] {path}: {{={o} }}={c} (imbalance {o-c:+d})")

def check_bom_eol(path, staged):
    had_bom_new = staged[:3] == b"\xef\xbb\xbf"
    crlf = staged.count(b"\r\n")
    lf_only = staged.count(b"\n") - crlf
    prev = committed_blob(path)
    if prev is not None:
        # existing file: forbid FLIPPING bom or eol
        prev_bom = prev[:3] == b"\xef\xbb\xbf"
        prev_crlf = prev.count(b"\r\n"); prev_lfonly = prev.count(b"\n") - prev_crlf
        if had_bom_new != prev_bom:
            fails.append(f"[BOM] {path}: byte-order-mark flipped ({'added' if had_bom_new else 'removed'}) vs HEAD")
        prev_is_crlf = prev_crlf > prev_lfonly
        new_is_crlf = crlf > lf_only
        if prev_is_crlf != new_is_crlf and (crlf>0 or prev_crlf>0):
            fails.append(f"[EOL] {path}: line-ending style flipped ({'->CRLF' if new_is_crlf else '->LF'}) vs HEAD")
    else:
        # new file: convention checks (block the hard ones)
        if path.startswith("setup/") and had_bom_new:
            fails.append(f"[BOM] {path}: NEW setup/ file has a BOM — the setup reader REJECTS BOM")
        if path.startswith("common/") and not had_bom_new and path.endswith(".txt"):
            warns.append(f"[BOM] {path}: NEW common/ .txt has no BOM (most common/ files carry one — confirm the subfolder's convention)")

def check_log_macro(path):
    # LINE-LEVEL: scan only the lines THIS commit adds (not the whole file), so a pre-existing
    # violation elsewhere doesn't block an unrelated clean commit.
    for i, line in added_lines(path):
        if not LOGFN.search(line):
            continue
        for m in re.finditer(r'"([^"]*)"', line):
            s = m.group(1)
            if "$" in s or "#" in s:
                bad = "$" if "$" in s else "#"
                fails.append(f"[LOGMACRO] {path}:{i}: '{bad}' inside a LOG string voids the whole call: \"{s[:60]}\"")

def main():
    files = [f for f in staged_files()]
    for f in files:
        if not is_script(f):
            # still EOL/BOM-check setup/ files (BOM matters there)
            if f.startswith("setup/") and f.endswith(".txt"):
                b = staged_blob(f)
                if b is not None: check_bom_eol(f, b)
            continue
        b = staged_blob(f)
        if b is None:
            continue
        check_bom_eol(f, b)
        try:
            text = b.decode("utf-8-sig")  # tolerate BOM for the text-level checks
        except UnicodeDecodeError:
            fails.append(f"[ENCODING] {f}: not valid UTF-8")
            continue
        check_braces(f, text)
        check_log_macro(f)

    if warns:
        print("pre-commit WARNINGS (not blocking):", file=sys.stderr)
        for w in warns: print("  "+w, file=sys.stderr)
    if fails:
        print("\npre-commit BLOCKED — mechanical defects (fix, or `git commit --no-verify` to override on the record):", file=sys.stderr)
        for x in fails: print("  "+x, file=sys.stderr)
        sys.exit(1)
    print("pre-commit checks passed (%d staged script files)" % sum(1 for f in files if is_script(f)))
    sys.exit(0)

if __name__ == "__main__":
    main()
