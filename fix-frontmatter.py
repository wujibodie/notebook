#!/usr/bin/env python3
"""
Fix indented YAML frontmatter in Obsidian markdown files for Quartz compatibility.

The issue: some files have frontmatter like:
    ---
        type: primary-source
        tags:
        - foo
        ---

Quartz's YAML parser needs:
    ---
    type: primary-source
    tags:
    - foo
    ---

Usage:
    python3 fix-frontmatter.py <file-or-directory>
    python3 fix-frontmatter.py ~/Documents/History  # fix entire vault
    python3 fix-frontmatter.py --dry-run ~/Documents/History  # preview only
"""

import sys
import os
import re

FRONTMATTER_PATTERN = re.compile(r'^\s*---\s*$')
OPENING_ONLY = re.compile(r'^---\s*$')  # opening must be at column 0

def needs_fix(filepath):
    """Check if a file has indented YAML frontmatter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return has_indented_frontmatter(content)

def has_indented_frontmatter(content):
    """Check if the first --- block has indented content."""
    lines = content.split('\n')
    if not lines or not OPENING_ONLY.match(lines[0]):
        return False

    # Find closing ---
    end_idx = None
    for i in range(1, len(lines)):
        if FRONTMATTER_PATTERN.match(lines[i]) and not (i == 0):
            end_idx = i
            break

    if end_idx is None:
        return False  # no closing ---

    # Check if closing --- is indented
    return lines[end_idx].startswith(' ')

def fix_file(content, dry_run=False):
    """
    Un-indent frontmatter content.
    Detects common indentation of the closing '---' and strips that much
    whitespace from every frontmatter line.
    """
    lines = content.split('\n')

    # Find frontmatter boundaries
    if not OPENING_ONLY.match(lines[0]):
        return content  # no frontmatter, return unchanged

    end_idx = None
    for i in range(1, len(lines)):
        if FRONTMATTER_PATTERN.match(lines[i].strip()):
            end_idx = i
            break

    if end_idx is None:
        return content  # no closing delimiter

    # Get the indentation of the closing ---
    indent = len(lines[end_idx]) - len(lines[end_idx].lstrip())
    if indent == 0:
        return content  # already correct

    if dry_run:
        return None

    # Strip that much indent from all frontmatter lines (1..end_idx)
    fixed = [lines[0]]  # opening --- stays as-is
    for i in range(1, end_idx):
        line = lines[i]
        if line.startswith(' ' * indent):
            fixed.append(line[indent:])
        elif line.strip() == '':
            fixed.append('')
        else:
            # Less indented than expected — strip what we can
            stripped = line.lstrip()
            fixed.append(stripped)
    fixed.append(lines[end_idx].lstrip())  # closing --- un-indented

    # Rest of file unchanged
    fixed.extend(lines[end_idx+1:])

    return '\n'.join(fixed)


def process_file(filepath, dry_run=False):
    """Process a single markdown file. Returns True if changed."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if not has_indented_frontmatter(content):
        return False

    result = fix_file(content, dry_run=dry_run)
    if result is None:  # dry run
        return True

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result)
    return True


def main():
    args = sys.argv[1:]
    dry_run = False
    if '--dry-run' in args:
        dry_run = True
        args.remove('--dry-run')

    if not args:
        print("Usage: fix-frontmatter.py [--dry-run] <file-or-directory>")
        sys.exit(1)

    target = args[0]
    if os.path.isfile(target):
        paths = [target]
    elif os.path.isdir(target):
        paths = []
        for root, dirs, files in os.walk(target):
            # Skip hidden directories and common non-vault dirs
            dirs[:] = [d for d in dirs if not d.startswith('.')
                       and d not in ('.git', '.obsidian', '.trash', 'node_modules')]
            for f in files:
                if f.endswith('.md'):
                    paths.append(os.path.join(root, f))
    else:
        print(f"Error: {target} not found")
        sys.exit(1)

    fixed_count = 0
    error_count = 0
    for path in paths:
        try:
            if process_file(path, dry_run=dry_run):
                rel = os.path.relpath(path, os.path.expanduser('~'))
                print(f"  {'WOULD FIX' if dry_run else 'FIXED'}  {rel}")
                fixed_count += 1
        except Exception as e:
            rel = os.path.relpath(path, os.path.expanduser('~'))
            print(f"  ERROR     {rel}: {e}", file=sys.stderr)
            error_count += 1

    print()
    if fixed_count == 0:
        print("No files needed fixing.")
    else:
        action = "Would fix" if dry_run else "Fixed"
        print(f"{action} {fixed_count} file(s).{f' ({error_count} errors)' if error_count else ''}")


if __name__ == '__main__':
    main()
