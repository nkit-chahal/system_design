"""
audit_course.py — Mechanical review of a generated course's lesson sources.

Checks per lesson: [n] citations vs the reference list (both directions), "Lesson N, Title" and
"Inference Lesson N, Title" cross-references vs the curricula, Python code tabs compile, YAML/JSON
tabs parse. With --arxiv it also looks up every cited arXiv ID and flags references whose title
does not match arXiv's record (the usual sign of an invented or mistyped reference).

Usage (from the repo root):
  python course_src/audit_course.py --course ai_training [--arxiv] [lesson numbers...]
"""
import argparse
import difflib
import html
import json
import re
import sys
import urllib.request
import os
import xml.etree.ElementTree as ET

sys.path.insert(0, os.getcwd())  # run from the repo root, where the course generators live
import generate_inference_course  # noqa: E402
import generate_training_course

COURSES = {'ai_inference': generate_inference_course, 'ai_training': generate_training_course}
CODE_RE = re.compile(r'<tab\b([^>]*)>(.*?)</tab>', re.S)


def titles(module):
    return {n: t for n, _, t in module.CURRICULUM}


def check_xrefs(src, own, inference):
    problems = []
    for m in re.finditer(r'(Inference )?Lesson (\d+), ([^<]{0,90})', src):
        table = inference if m.group(1) else own
        num, after = int(m.group(2)), m.group(3)
        if num not in table:
            problems.append(f'reference to missing lesson: {m.group(0)[:70]!r}')
        elif not after.startswith(table[num]) and re.match(r'[A-Z](?!esson\b)[a-z]*[ -]', after):
            # "Lesson 3, Training Memory" must use the real title; "In Lesson 3, the cache..." is prose.
            problems.append(f'title mismatch: {m.group(0)[:70]!r} (expected {table[num]!r})')
    return problems


def check_citations(src):
    body, _, refs = src.partition('Reference Material</h2>')
    body = re.sub(r'<codetabs>.*?</codetabs>|<code>.*?</code>', '', body, flags=re.S)
    # [n] is a citation unless it is an index such as choices[0]; adjacent citations [3][4] still count.
    cited = {int(m.group(1)) for m in re.finditer(r'\[(\d+)\]', body)
             if not (m.start() > 0 and body[m.start() - 1].isalnum())}
    listed = set(map(int, re.findall(r'\[(\d+)\]', refs)))
    problems = []
    if cited - listed:
        problems.append(f'cited but not listed: {sorted(cited - listed)}')
    if listed - cited:
        problems.append(f'listed but not cited: {sorted(listed - cited)}')
    return problems


def check_code(src):
    problems = []
    for attrs, code in CODE_RE.findall(src):
        lang = (re.search(r'lang="([^"]+)"', attrs) or [None, 'text'])[1]
        code = html.unescape(code) if '&lt;' in code else code
        try:
            if lang == 'python':
                compile(code, '<tab>', 'exec')
            elif lang == 'json':
                try:
                    json.loads(code)
                except json.JSONDecodeError:  # JSON Lines: one object per line
                    for line in code.strip().splitlines():
                        if line.strip():
                            json.loads(line)
            elif lang == 'yaml':
                import yaml
                list(yaml.safe_load_all(code))
        except Exception as exc:  # report and continue
            problems.append(f'{lang} tab does not parse: {type(exc).__name__}: {str(exc)[:80]}')
    return problems


def check_markup(src):
    """Markup slips that render as visible garbage: LaTeX dollar signs in prose, escaped operators
    inside <tex>, and Markdown that never became HTML."""
    problems = []
    text = re.sub(r'<codetabs>.*?</codetabs>|<code>.*?</code>', '', src, flags=re.S)
    for m in re.finditer(r'<tex(?:block)?>(.*?)</tex(?:block)?>', text, flags=re.S):
        if re.search(r'(?<!\\)\$', m.group(1)):  # \$ is a legitimate literal dollar sign
            problems.append(f'$ inside <tex> renders literally: {m.group(1)[:70]!r}')
        if re.search(r'&(lt|gt|amp);', m.group(1)):
            problems.append(f'HTML entity inside <tex> (write < > & literally): {m.group(1)[:70]!r}')
    prose = re.sub(r'<tex>.*?</tex>|<texblock>.*?</texblock>', '', text, flags=re.S)
    # A closing-delimiter $ right after a symbol (N_d$, 2Ψ$) or an opening $\ or ${. Currency
    # ("$3.00", "$ per million") does not match.
    for m in re.finditer(r'(?<=[\w)}\]])\$|\$[\\{]', prose):
        problems.append(f'stray $ in prose (LaTeX outside <tex>?): ...{prose[max(0, m.start() - 40):m.end() + 20]!r}')
    for m in re.finditer(r'\*\*[^*\n]{2,60}\*\*|(?<![`\w])`[^`\n]{1,60}`(?![`\w])|^#{1,4} |\\\(|\\\[|```', prose, flags=re.M):
        problems.append(f'Markdown in HTML fragment: {m.group(0)[:60]!r}')
    return problems[:12]  # the first few are enough to locate the habit


def arxiv_refs(src):
    refs = src.partition('Reference Material</h2>')[2]
    for line in re.split(r'<br\s*/?>', refs):
        m = re.search(r'arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})', line)
        if m:
            text = re.sub(r'<[^>]+>', '', line)
            text = re.sub(r'^\s*\[\d+\]\s*', '', text)
            yield m.group(1), text.strip()


def fetch_arxiv_titles(ids):
    found = {}
    ids = sorted(set(ids))
    for i in range(0, len(ids), 50):
        url = 'http://export.arxiv.org/api/query?max_results=100&id_list=' + ','.join(ids[i:i + 50])
        feed = ET.fromstring(urllib.request.urlopen(url, timeout=60).read())
        ns = {'a': 'http://www.w3.org/2005/Atom'}
        for entry in feed.findall('a:entry', ns):
            aid = re.search(r'(\d{4}\.\d{4,5})', entry.find('a:id', ns).text).group(1)
            found[aid] = ' '.join(entry.find('a:title', ns).text.split())
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--course', default='ai_inference', choices=COURSES)
    ap.add_argument('--arxiv', action='store_true')
    ap.add_argument('lessons', nargs='*', type=int)
    args = ap.parse_args()
    module = COURSES[args.course]
    own, inference = titles(module), titles(generate_inference_course)
    total, arxiv = 0, []
    for num, _, title in module.CURRICULUM:
        if args.lessons and num not in args.lessons:
            continue
        try:
            src = open(f'course_src/{args.course}/{num:03d}.html', encoding='utf-8').read()
        except FileNotFoundError:
            print(f'{num:03d}: missing source')
            total += 1
            continue
        problems = check_citations(src) + check_xrefs(src, own, inference) + check_code(src) + check_markup(src)
        for p in problems:
            print(f'{num:03d} {title}: {p}')
        total += len(problems)
        arxiv += [(num, aid, text) for aid, text in arxiv_refs(src)]
    if args.arxiv and arxiv:
        real = fetch_arxiv_titles([a for _, a, _ in arxiv])
        for num, aid, text in arxiv:
            if aid not in real:
                print(f'{num:03d}: arXiv {aid} not found')
                total += 1
            elif difflib.SequenceMatcher(None, real[aid].lower(), text.lower()).find_longest_match(
                    0, len(real[aid]), 0, len(text)).size < min(25, len(real[aid]) * 0.6):
                print(f'{num:03d}: arXiv {aid} is "{real[aid]}" but the reference says: {text[:110]}')
                total += 1
        print(f'{len(set(a for _, a, _ in arxiv))} distinct arXiv IDs checked')
    print(f'{total} problems')
    sys.exit(1 if total else 0)


if __name__ == '__main__':
    main()
