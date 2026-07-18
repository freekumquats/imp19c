#!/usr/bin/env python3
"""Check brace balance in GUI files."""
import sys
import re

def count_braces(filepath):
    """Count { and } outside of comments (# to EOL)."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Strip comments: from # to end of line
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        # Find # position, but be naive (not checking quotes)
        hash_pos = line.find('#')
        if hash_pos >= 0:
            line = line[:hash_pos]
        cleaned_lines.append(line)

    cleaned = '\n'.join(cleaned_lines)

    # Count braces
    open_count = cleaned.count('{')
    close_count = cleaned.count('}')
    diff = open_count - close_count

    return open_count, close_count, diff

def main():
    files = [
        '/Users/alan.chiang/github.com/imp19c/gui/province_window.gui',
        '/Users/alan.chiang/github.com/imp19c/gui/diplomatic_view.gui',
        '/Users/alan.chiang/github.com/imp19c/gui/imp19c_windows.gui',
        '/Users/alan.chiang/github.com/imp19c/gui/shared/gui_templates.gui',
    ]

    for filepath in files:
        try:
            open_count, close_count, diff = count_braces(filepath)
            status = "BALANCED" if diff == 0 else "UNBALANCED"
            print(f"\n{filepath}:")
            print(f"  Open braces:   {open_count}")
            print(f"  Close braces:  {close_count}")
            print(f"  Difference:    {diff:+d}")
            print(f"  Status:        {status}")
        except Exception as e:
            print(f"\n{filepath}: ERROR - {e}")

if __name__ == '__main__':
    main()
