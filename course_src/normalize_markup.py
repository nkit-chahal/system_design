"""
normalize_markup.py — Repairs the markup slips that LLM-written lesson fragments commonly have:
  * `$` delimiters left inside <tex>/<texblock> (they render as literal dollar signs);
  * HTML entities inside <tex> (latex2mathml needs literal < > &);
  * Markdown backtick spans in prose, which become <code>...</code>.
Code tabs and existing <code> spans are left untouched. Prints what it changed per file.

Usage (from the repo root):
  python course_src/normalize_markup.py course_src/ai_training/0*.html
"""
import glob
import html
import re
import sys

PROTECTED = re.compile(r'<codetabs>.*?</codetabs>|<code>.*?</code>', re.S)
TEX = re.compile(r'(<tex(?:block)?>)(.*?)(</tex(?:block)?>)', re.S)
BACKTICK = re.compile(r'(?<![`\w])`([^`\n]{1,80})`(?![`\w])')


def fix_tex(m):
    body = re.sub(r'(?<!\\)\$', '', m.group(2))  # keep \$, which is a literal dollar sign
    body = body.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    return m.group(1) + body + m.group(3)


def fix_segment(seg, counts):
    new, n = TEX.subn(fix_tex, seg)
    counts['tex'] += sum(1 for a, b in zip(TEX.finditer(seg), TEX.finditer(new)) if a.group(2) != b.group(2))
    # Backticks only outside math.
    parts, last = [], 0
    for m in TEX.finditer(new):
        chunk, k = BACKTICK.subn(lambda b: f'<code>{html.escape(b.group(1), quote=False)}</code>', new[last:m.start()])
        counts['code'] += k
        parts += [chunk, m.group(0)]
        last = m.end()
    chunk, k = BACKTICK.subn(lambda b: f'<code>{html.escape(b.group(1), quote=False)}</code>', new[last:])
    counts['code'] += k
    parts.append(chunk)
    return ''.join(parts)


def normalize(src):
    counts = {'tex': 0, 'code': 0}
    out, last = [], 0
    for m in PROTECTED.finditer(src):
        out += [fix_segment(src[last:m.start()], counts), m.group(0)]
        last = m.end()
    out.append(fix_segment(src[last:], counts))
    return ''.join(out), counts


def main():
    paths = sorted({p for pattern in sys.argv[1:] for p in glob.glob(pattern)})
    if not paths:
        sys.exit(__doc__)
    for p in paths:
        src = open(p, encoding='utf-8', newline='').read()
        new, counts = normalize(src)
        if new != src:
            open(p, 'w', encoding='utf-8', newline='').write(new)
            print(f'{p}: fixed {counts["tex"]} math blocks, {counts["code"]} backtick spans')


if __name__ == '__main__':
    main()
