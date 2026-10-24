"""
summary_prompt.py — Turns summary/NNN.txt mind-map specs into one prompt for the Antigravity
CLI (agy), which draws the lesson summary images in the style of the GenAI chapters' summaries.

Usage (from the repo root):
  agy --mode accept-edits --add-dir "<abs path to AI Inference Engineering/images>" \
      --print="$(python course_src/ai_inference/summary_prompt.py 2 4 5)"
Then review every image and regenerate any with misspelled or missing labels.
"""
import os
import sys

SPEC_DIR = os.path.join('course_src', 'ai_inference', 'summary')
IMG_DIR = os.path.abspath(os.path.join('AI Inference Engineering', 'images'))

STYLE = (
    'a clean left-to-right tree mind map on a plain pure-white background, in the style of a technical '
    'textbook summary diagram. Thin black curved connector lines branch from the root to each node. All '
    'labels are black sans-serif text without boxes, except the root, which sits in a small rounded '
    'rectangle with a thin black outline. No colors, no icons, no shadows, no title, no watermark, no extra '
    'words. Landscape, about 1600x1000 pixels, generous spacing, all text crisp and fully legible.'
)


def parse_spec(num):
    center, branches = None, []
    with open(os.path.join(SPEC_DIR, f'{num:03d}.txt'), encoding='utf-8') as f:
        for line in f:
            key, _, value = line.strip().partition(':')
            if key == 'center':
                center = value.strip()
            elif key == 'branch':
                name, *leaves = [part.strip() for part in value.split('|')]
                branches.append((name, leaves))
    return center, branches


def image_section(num):
    center, branches = parse_spec(num)
    lines = [f'Save as: {os.path.join(IMG_DIR, f"{num:03d}-summary.png")}', f'Root: "{center}"',
             'Children of the root, top to bottom, each with its own children to the right:']
    for i, (name, leaves) in enumerate(branches, 1):
        lines.append(f'{i}. "{name}" -> ' + ', '.join(f'"{leaf}"' for leaf in leaves))
    return '\n'.join(lines)


def build_prompt(nums):
    count = 'ONE image' if len(nums) == 1 else f'{len(nums)} separate images, one per specification below'
    sections = '\n\n'.join(f'Image {i}:\n{image_section(n)}' for i, n in enumerate(nums, 1))
    return (
        f'Use your image generation tool to create {count}, and save each as a PNG file at exactly the '
        f'path given (overwrite if it exists). Do not create or modify any other file and do not write code.\n\n'
        f'Every image uses the same style: {STYLE}\n\n{sections}\n\n'
        'Spell every label exactly as written. When done, reply with the saved file paths. If the image '
        'tool fails for any image, report its exact error text and do not claim that file was saved.'
    )


if __name__ == '__main__':
    print(build_prompt([int(a) for a in sys.argv[1:]]))
