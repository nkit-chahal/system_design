import glob
import os
import re

DIRS = [
    'Behavioral Interview',
    'Coding Interview Patterns',
    'Generative AI System Design Interview',
    'Machine Learning System Design Interview',
    'Mobile System Design Interview',
    'Object-Oriented Design Interview',
    'System Design Interview'
]

def main():
    total = 0
    fixed = 0

    csp_pattern = re.compile(r'<meta[^>]*content-security-policy[^>]*>', re.IGNORECASE)
    
    for dir_name in DIRS:
        files = sorted(glob.glob(os.path.join(dir_name, '*.html')))
        for fpath in files:
            total += 1
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            if csp_pattern.search(content):
                # Remove CSP tag
                new_content = csp_pattern.sub('', content)
                with open(fpath, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(new_content)
                fixed += 1
                
    print(f"Total files checked: {total}")
    print(f"Files fixed (CSP removed): {fixed}")

if __name__ == '__main__':
    main()
