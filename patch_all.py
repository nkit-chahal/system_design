"""
patch_all.py — Append nav_map.js and nav_inject.js script tags to all lesson HTML files.
Idempotent: skips files that are already patched.
"""
import glob
import os

DIRS = [
    'Behavioral Interview',
    'Coding Interview Patterns',
    'Generative AI System Design Interview',
    'Machine Learning System Design Interview',
    'Mobile System Design Interview',
    'Object-Oriented Design Interview',
    'System Design Interview'
]

MARKER = '<!-- nav-inject-patched -->'

def get_script_tags(dir_name):
    """Generate script tags with correct relative path back to root."""
    # Files are in "DirName/filename.html", so one level up to reach root
    return f"""
{MARKER}
<script src="../nav_map.js"></script>
<script src="../nav_inject.js"></script>
"""

def patch_file(fpath, dir_name):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    if MARKER in content:
        return 'skipped'

    tags = get_script_tags(dir_name)
    content += tags

    with open(fpath, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(content)

    return 'patched'

def main():
    total = 0
    patched = 0
    skipped = 0

    for dir_name in DIRS:
        files = sorted(glob.glob(os.path.join(dir_name, '*.html')))
        for fpath in files:
            result = patch_file(fpath, dir_name)
            total += 1
            if result == 'patched':
                patched += 1
            else:
                skipped += 1

    print(f'Total files: {total}')
    print(f'Patched: {patched}')
    print(f'Skipped (already patched): {skipped}')

if __name__ == '__main__':
    main()
