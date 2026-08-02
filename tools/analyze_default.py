#!/usr/bin/env python3
"""Analyze setup/main/00_default.txt for ownership, capitals, and structure."""

import re
from collections import defaultdict

FILE_PATH = "/Users/alan.chiang/github.com/imp19c/setup/main/00_default.txt"

def strip_comment(line):
    """Remove everything from # to end of line."""
    idx = line.find('#')
    if idx >= 0:
        return line[:idx]
    return line

def main():
    # Read file as bytes first to check BOM
    with open(FILE_PATH, 'rb') as f:
        raw_bytes = f.read()

    # 1. BOM CHECK
    print("=" * 60)
    print("1. BOM CHECK")
    print("=" * 60)
    if raw_bytes.startswith(b'\xef\xbb\xbf'):
        print("BOM: present")
        has_bom = True
    else:
        print("BOM: absent")
        has_bom = False
    print()

    # Decode to string
    if has_bom:
        content = raw_bytes[3:].decode('utf-8')
    else:
        content = raw_bytes.decode('utf-8')

    lines = content.splitlines()

    # 2. BRACE BALANCE
    print("=" * 60)
    print("2. BRACE BALANCE")
    print("=" * 60)

    stripped_content = ""
    for line in lines:
        stripped_content += strip_comment(line) + "\n"

    open_braces = stripped_content.count('{')
    close_braces = stripped_content.count('}')

    print(f"Open braces: {open_braces}")
    print(f"Close braces: {close_braces}")
    if open_braces == close_braces:
        print("Braces: BALANCED")
    else:
        print(f"Braces: UNBALANCED (diff = {open_braces - close_braces})")
    print()

    # 3-7. Parse structure
    print("=" * 60)
    print("3. PARSING own_control_core BLOCKS")
    print("=" * 60)

    # Track state
    current_tag = None
    in_country_block = False
    in_tag_block = False
    in_own_control_core = False
    brace_depth = 0
    country_brace_depth = 0
    tag_brace_depth = 0
    occ_brace_depth = 0

    # Storage
    own_control_blocks = []  # List of (tag, [province_ids])
    capitals = []  # List of (tag, capital_id, line_num)

    # Province ownership tracking
    province_to_tags = defaultdict(list)  # province_id -> [tags]

    line_num = 0
    current_occ_provinces = []
    last_uppercase_token = None

    for line in lines:
        line_num += 1
        stripped = strip_comment(line).strip()

        if not stripped:
            continue

        # Track all 3-4 letter uppercase tokens for fallback
        uppercase_match = re.search(r'\b([A-Z][A-Z0-9]{2,3})\b', stripped)
        if uppercase_match:
            last_uppercase_token = uppercase_match.group(1)

        # Check for country = {
        if re.match(r'^\s*country\s*=\s*\{', stripped):
            in_country_block = True
            country_brace_depth = 1
            continue

        # Track brace depth
        for char in stripped:
            if char == '{':
                brace_depth += 1
                if in_country_block and not in_tag_block:
                    country_brace_depth += 1
                if in_tag_block and not in_own_control_core:
                    tag_brace_depth += 1
                if in_own_control_core:
                    occ_brace_depth += 1
            elif char == '}':
                brace_depth -= 1
                if in_own_control_core:
                    occ_brace_depth -= 1
                    if occ_brace_depth == 0:
                        # End of own_control_core block
                        own_control_blocks.append((current_tag or last_uppercase_token or f"BLOCK_{len(own_control_blocks)}",
                                                   current_occ_provinces[:]))
                        for prov in current_occ_provinces:
                            province_to_tags[prov].append(current_tag or last_uppercase_token or f"BLOCK_{len(own_control_blocks)-1}")
                        current_occ_provinces = []
                        in_own_control_core = False
                elif in_tag_block:
                    tag_brace_depth -= 1
                    if tag_brace_depth == 0:
                        in_tag_block = False
                        current_tag = None
                elif in_country_block:
                    country_brace_depth -= 1
                    if country_brace_depth == 0:
                        in_country_block = False

        # Check for TAG = { (3-letter uppercase tag)
        tag_match = re.match(r'^\s*([A-Z][A-Z0-9]{2})\s*=\s*\{', stripped)
        if tag_match and in_country_block:
            current_tag = tag_match.group(1)
            in_tag_block = True
            tag_brace_depth = 1
            continue

        # Check for capital = NNN
        capital_match = re.search(r'\bcapital\s*=\s*(\d+)', stripped)
        if capital_match and in_tag_block:
            cap_id = int(capital_match.group(1))
            capitals.append((current_tag or last_uppercase_token, cap_id, line_num))

        # Check for own_control_core = {
        if re.search(r'\bown_control_core\s*=\s*\{', stripped):
            in_own_control_core = True
            occ_brace_depth = 1
            current_occ_provinces = []
            continue

        # If inside own_control_core, collect province IDs
        if in_own_control_core:
            # Extract all integers from this line
            integers = re.findall(r'\b(\d+)\b', stripped)
            for num_str in integers:
                prov_id = int(num_str)
                current_occ_provinces.append(prov_id)

    print(f"Found {len(own_control_blocks)} own_control_core blocks")
    for i, (tag, provs) in enumerate(own_control_blocks[:5]):
        print(f"  Block {i}: TAG={tag}, {len(provs)} provinces (first 10: {provs[:10]})")
    print()

    # 4. DOUBLE-OWNERSHIP
    print("=" * 60)
    print("4. DOUBLE-OWNERSHIP CHECK")
    print("=" * 60)

    double_owned = {}
    for prov_id, tag_list in province_to_tags.items():
        if len(tag_list) > 1:
            double_owned[prov_id] = tag_list

    if double_owned:
        print(f"Found {len(double_owned)} double-owned provinces:")
        for prov_id in sorted(double_owned.keys()):
            tags = double_owned[prov_id]
            print(f"  Province {prov_id}: appears {len(tags)} times in blocks: {', '.join(tags)}")
    else:
        print("NO DOUBLE-OWNED")
    print()

    # 5. UNOWNED CHECK
    print("=" * 60)
    print("5. UNOWNED CHECK (specific provinces)")
    print("=" * 60)

    check_ids = [5863, 9933, 4807, 146]
    for prov_id in check_ids:
        count = len(province_to_tags.get(prov_id, []))
        tags = province_to_tags.get(prov_id, [])
        if tags:
            print(f"Province {prov_id}: appears {count} time(s) in blocks: {', '.join(tags)}")
        else:
            print(f"Province {prov_id}: appears 0 times (UNOWNED)")
    print()

    # 6. CAPITAL-OWNED CHECK
    print("=" * 60)
    print("6. CAPITAL-OWNED CHECK (specific capital IDs)")
    print("=" * 60)

    capital_check_ids = [6219, 1108, 3171, 1571, 8805, 2416, 4316, 695, 484, 9840, 5810, 6270]
    for cap_id in capital_check_ids:
        if cap_id in province_to_tags:
            tags = province_to_tags[cap_id]
            print(f"Capital {cap_id}: OWNED by {len(tags)} block(s): {', '.join(tags)}")
        else:
            print(f"Capital {cap_id}: NOT OWNED by any block")
    print()

    # 7. ALL CAPITALS CHECK
    print("=" * 60)
    print("7. ALL CAPITALS OWNERSHIP CHECK")
    print("=" * 60)

    print(f"Found {len(capitals)} capital declarations")
    ownerless_capitals = []
    for tag, cap_id, line_no in capitals:
        if cap_id not in province_to_tags:
            ownerless_capitals.append((tag, cap_id, line_no))

    if ownerless_capitals:
        print(f"Found {len(ownerless_capitals)} OWNERLESS CAPITALS (potential crash):")
        for tag, cap_id, line_no in ownerless_capitals:
            print(f"  Line {line_no}: TAG={tag}, capital={cap_id} NOT in any own_control_core block")
    else:
        print("All capitals are owned (appear in at least one own_control_core block)")
    print()

    # 8. COMMENT-CORRUPTION SANITY
    print("=" * 60)
    print("8. COMMENT-CORRUPTION SANITY CHECK")
    print("=" * 60)

    print("Searching for 'spa_america':")
    found_spa = False
    line_num = 0
    for line in lines:
        line_num += 1
        if 'spa_america' in line.lower():
            print(f"  Line {line_num}: {line.strip()}")
            found_spa = True
    if not found_spa:
        print("  (no matches)")
    print()

    print("Checking for broken number-comment merges (tokens like '123#' or similar):")
    line_num = 0
    suspicious = []
    for line in lines:
        line_num += 1
        # Look for patterns like digit followed immediately by # without space
        if re.search(r'\d#[^\s]', line):
            suspicious.append((line_num, line.strip()))

    if suspicious:
        print(f"Found {len(suspicious)} suspicious lines:")
        for ln, text in suspicious[:20]:  # Limit to first 20
            print(f"  Line {ln}: {text}")
    else:
        print("  (no obvious broken number-comment merges found)")
    print()

    print("=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    main()
