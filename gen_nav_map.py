import re
import glob
import json
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

path_to_file = {}
file_to_info = {}

for dir_name in DIRS:
    files = sorted(glob.glob(os.path.join(dir_name, '*.html')))
    for fpath in files:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Extract the selected menu item's course path
        selected = re.findall(
            r'ant-menu-item-selected[^>]*data-menu-id=["\']?rc-menu-uuid-\d+-\d+-(/courses/[^\s"\'>\]]+)',
            content
        )
        if not selected:
            selected = re.findall(
                r'data-menu-id=["\']?rc-menu-uuid-\d+-\d+-(/courses/[^\s"\'>\]]+)[^>]*ant-menu-item-selected',
                content
            )
        
        clean_selected = []
        for s in selected:
            clean = re.sub(r'>[<].*', '', s)
            clean_selected.append(clean)
        
        if clean_selected:
            course_path = clean_selected[0]
            rel_file = fpath.replace('\\', '/')
            path_to_file[course_path] = rel_file

# Build ordered list per category for prev/next
category_order = {}
for dir_name in DIRS:
    files = sorted(glob.glob(os.path.join(dir_name, '*.html')))
    category_order[dir_name] = [f.replace('\\', '/') for f in files]

# Generate nav_map.js
js_lines = ['// Auto-generated navigation mapping']
js_lines.append('const NAV_MAP = ' + json.dumps(path_to_file, indent=2) + ';')
js_lines.append('')
js_lines.append('const CATEGORY_ORDER = ' + json.dumps(category_order, indent=2) + ';')

with open('nav_map.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(js_lines) + '\n')

print(f'Generated nav_map.js with {len(path_to_file)} path mappings across {len(category_order)} categories.')
