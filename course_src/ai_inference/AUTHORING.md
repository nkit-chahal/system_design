# Authoring guide: AI Inference Engineering

The course is written in the style of the **Generative AI** and **Machine Learning System Design**
chapters in this repo: long, plain-spoken chapters with numbered draw.io-style figures, a
Candidate/Interviewer dialogue, comparison tables, a "which option fits?" decision, talking points,
a summary, and numbered references. `003.html` (KV Cache) is the reference lesson. Read it and its
figures before writing anything.

## Files

| What | Where |
|---|---|
| Lesson source (HTML fragment) | `course_src/ai_inference/NNN.html` |
| Figures (hand-drawn SVG) | `AI Inference Engineering/images/NNN-short-slug.svg` |
| Summary mind-map spec (turned into an image later) | `course_src/ai_inference/summary/NNN.txt` |
| Built page (never edit by hand) | `AI Inference Engineering/NNN Title.html` |

Build one or more lessons, then preview them:

```bash
python generate_inference_course.py 7 8            # builds 007 and 008 only
python course_src/ai_inference/preview.py figs <out_dir> "AI Inference Engineering/images/007-*.svg"
python course_src/ai_inference/preview.py page <out_dir> 7
```

`preview.py` writes PNGs into `<out_dir>`; open them and look. Titles and numbering live in
`CURRICULUM` in `generate_inference_course.py`. The hub and sidebar are rebuilt with
`python build_index.py && python build_unified_nav_data.py`.

## Fragment syntax

A fragment is the article body only: plain HTML (`h2`, `h3`, `h4`, `p`, `ul`, `ol`, `table`,
`strong`, `em`, `code`, `a`), plus these tags that the generator expands:

```html
<fig src="007-batching-timeline.svg" caption="Static versus continuous batching">
Alt text: one or two sentences describing what the figure shows, for screen readers.
</fig>
<fig src="007-summary.png" caption="Continuous batching summary" optional="1">Alt text</fig>

<codetabs>
<tab label="vLLM" lang="bash">
raw code here, no HTML escaping: a < b && c > d
</tab>
<tab label="Client" lang="python">
...
</tab>
</codetabs>

<tex>q K^\top</tex>                       inline math (LaTeX, rendered to MathML)
<texblock>\text{TTFT} = t_{queue} + t_{prefill}</texblock>   display math
<callout kind="tip" title="Interview tip">One or two sentences.</callout>   kind: tip | warn | info
```

* Figures are numbered automatically ("Figure 1:", "Figure 2:" …). Refer to them as "Figure 2"
  in the text in the same order.
* Tables are wrapped automatically. Put a caption right after a table as
  `<p style="text-align:center">Table 1: …</p>`.
* `lang` can be `python`, `bash`, `yaml`, `json`, `promql`, or `text`.
* In LaTeX, write multi-letter subscripts as `\text{...}`: `d_{\text{head}}`, not `d_{head}`.
  `\%` inside `\text{}` renders literally; write percentages outside `\text{}` or in prose.
* vLLM doc URLs now use trailing slashes (`.../quantized_kvcache/`); the old `.html` form redirects.
* Do not write `<header>`, `<h1>`, or the lesson number; the generator adds them.

## Page skeleton

### Topic lessons

1. `h2` **Introduction**: the problem in plain words, why it matters for serving, Figure 1
   showing the core idea, and a closing "In this lesson, we …" paragraph.
2. `h2` **Clarifying the Problem**: a Candidate/Interviewer exchange of 4–7 turns, in the exact
   format of `003.html` (`<p><strong>Candidate</strong>: …<br><strong>Interviewer</strong>: …</p>`).
   It fixes the scenario with concrete numbers (model, GPU, traffic, latency target). End with a
   paragraph stating the real question underneath.
3. **Two to four core `h2` sections** with `h3`/`h4` structure. Explain the mechanism step by step,
   give the math where it exists, and work at least one example with real numbers from the
   scenario. Compare options in a table. Include at least one `h4` decision in the form
   "Which … fits our deployment?" that picks an option and says why, as the GenAI chapters do.
4. `h2` **In Practice**: a `<codetabs>` block (one to three tabs) of runnable, correct code or
   config, introduced by a paragraph saying what each tab does.
5. `h2` **Other Talking Points**: "If there is extra time at the end of the interview, here are
   some additional talking points:" followed by 5–8 bullets, cited where possible.
6. `h2` **Summary**: the optional summary figure (`NNN-summary.png`, `optional="1"`) followed by
   5–7 bullets that state the key facts and numbers.
7. `h2` **Reference Material**: one `<p>` with `[n] Author et al. Title. <a href=…>url</a>.<br>`
   lines, exactly as in `003.html`. Every `[n]` in the text must appear here and vice versa.

### Lab lessons (006, 012, 016, 021, 027, 032; Stage 7 has no lab)

Labs turn a stage's "Practice" goal into a guided exercise:

1. `h2` **Introduction**: the goal, what you will build or measure, and Figure 1 showing the setup.
2. `h2` **What You Need**: a table of hardware, software, and models, with a small path (a laptop
   or consumer GPU with a 0.5B–3B model; vLLM needs Linux or WSL2 on Windows) and a full path
   (a cloud H100). State a rough cost for the full path and say it is an assumption.
3. `h2` **Step 1: …** to **Step N: …**: commands and scripts in `<codetabs>`, each followed by
   what you should see.
4. `h2` **Reading the Results**: how to interpret the output, with a figure of the typical shape
   of the result.
5. `h2` **Common Pitfalls**, `h2` **Stretch Goals**, then **Summary** and **Reference Material**
   as above.

Never present invented measurements as real results. Expected output is either derived from
arithmetic you show, or clearly labelled "illustrative" (in the text and in the figure caption).

## Voice

* Write like the GenAI chapters: calm, precise, textbook prose. Use "we" for the design walk-through.
* Short paragraphs (2–4 sentences). Bold a term the first time you define it.
* Prefer concrete numbers to adjectives: "about 21 ms per step", not "very slow".
* Plain words, no hype, no emojis, American spelling.
* Refer to other lessons as "Lesson 8, PagedAttention". The curriculum is in `generate_inference_course.py`.
* Length: topic lessons 2,500–4,500 words; labs 2,000–4,000. Five to nine figures per lesson
  (not counting the summary image), one to three tables.

## Figures

Figures are hand-written SVG files in the draw.io look of the GenAI chapters: white background,
black arrows, Helvetica, pastel boxes. One idea per figure. Copy the boilerplate from any
`003-*.svg` file:

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="300" viewBox="0 0 800 300" font-family="Helvetica, Arial, sans-serif">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker>
  </defs>
  <style>
    text{font-size:14px;fill:#000}
    .sm{font-size:12px}.lg{font-size:16px}.b{font-weight:bold}
    .orange{fill:#ffe6cc;stroke:#d79b00;stroke-width:1.2}
    .blue{fill:#dae8fc;stroke:#6c8ebf;stroke-width:1.2}
    .green{fill:#d5e8d4;stroke:#82b366;stroke-width:1.2}
    .purple{fill:#e1d5e7;stroke:#9673a6;stroke-width:1.2}
    .yellow{fill:#fff2cc;stroke:#d6b656;stroke-width:1.2}
    .red{fill:#f8cecc;stroke:#b85450;stroke-width:1.2}
    .gray{fill:#f5f5f5;stroke:#666;stroke-width:1.2}
    .white{fill:#fff;stroke:#000;stroke-width:1.2}
    .group{fill:none;stroke:#000;stroke-width:1.2;stroke-dasharray:5 4}
    .edge{fill:none;stroke:#000;stroke-width:1.2;marker-end:url(#arrow)}
  </style>
  <rect width="100%" height="100%" fill="#fff"/>
  ...
</svg>
```

* Width 640–860 px; height as needed. Set `width`, `height`, and `viewBox` to the same size.
* Text 12–16 px. Budget about 7.5 px per character at 14 px. Keep labels short.
* Colors carry meaning, used consistently: **orange** = the component or work under discussion,
  **blue** = data, memory, or cache, **green** = a good or chosen outcome, **red** = a bad outcome
  or bottleneck, **purple** = queries, requests, or control, **gray** = supporting or neutral steps.
  Add a small legend when color is part of the message.
* Dashed rectangles group things; cylinders (`path` with arcs) are stores; arrows are 1.2 px black.
* Charts (latency curves, bar comparisons) are drawn as SVG too: axes, ticks, labelled units, and
  a note when data is illustrative. Every number in a figure must match the text.
* Name files `NNN-short-slug.svg`. Render them with `preview.py figs` and fix any overlap,
  clipped text, or crossing arrows before finishing.

## Summary image spec

Each lesson ends with a mind-map image generated later by another tool. Write its spec to
`course_src/ai_inference/summary/NNN.txt` in this format, using only labels that appear in the lesson:

```
center: KV Cache
branch: What is cached | keys and values | every layer and KV head
branch: Sizing | 2 × layers × KV heads × d × bytes | 128 KiB per token
branch: Capacity | ~426K tokens on one H100 | 170 chat requests
```

Four to six branches, two or three leaves each, each label at most five words. Write labels as
plain text: no underscores, subscripts, or LaTeX (write "KV heads", not "H_kv").

## Facts to keep consistent across lessons

Use these values whenever a lesson needs them, so numbers agree from page to page. Verify anything
not on this list against official documentation before using it.

| Fact | Value |
|---|---|
| Running example model | Llama 3.1 8B Instruct, BF16: 32 layers, 32 query heads, 8 KV heads, head dim 128, 8.03B params (≈ 16 GB / 15 GiB of weights) |
| Its KV cache | 128 KiB per token in BF16 (64 KiB in FP8); 8,192 tokens per GiB |
| Running example traffic | chat requests of ~2,000 prompt tokens and ~500 output tokens |
| Larger example model | Llama 3.1 70B: 80 layers, 64 query heads, 8 KV heads, head dim 128, ≈ 70.6B params (≈ 141 GB in BF16), 320 KiB KV per token |
| H100 SXM 80 GB | ≈ 79.6 GiB visible; HBM3 3.35 TB/s; ≈ 989 TFLOPS dense BF16; ≈ 1,979 TFLOPS dense FP8; NVLink 900 GB/s |
| H200 | 141 GB HBM3e, 4.8 TB/s, same compute as H100 |
| A100 80 GB SXM | ≈ 2.0 TB/s; 312 TFLOPS dense BF16; no FP8 |
| L4 | 24 GB, 300 GB/s, ≈ 121 TFLOPS dense FP16/BF16 |
| H100 + Llama 3.1 8B capacity (Lesson 3) | ≈ 52 GiB left for KV cache with `--gpu-memory-utilization 0.90` set explicitly (recent vLLM defaults to 0.92) ⇒ ≈ 426K tokens ⇒ ≈ 170 chat requests or 13 at 32K tokens |
| Running example traffic volume | average 1,000 requests/min ≈ 16.7 req/s; daily cycle ≈ 8–33 req/s; launch spikes up to 10× the average |
| Running example latency targets | p95 TTFT ≤ 500 ms; p95 TPOT ≤ 25 ms (≥ 40 tokens/s per stream). Lab 21 defines its own 2 s SLA |
| Per-H100 capacity at those targets | ≈ 5 requests/s for Llama 3.1 8B (Lesson 19's model: ≈ 53 concurrent streams at ≈ 21 ms per decode step) |
| Published checkpoint sizes (embeddings and LM head stay BF16) | Llama 3.1 8B: ≈ 16.1 GB BF16, ≈ 9.08 GB FP8, ≈ 5.74 GB W4A16; 70B: ≈ 72.7 GB FP8, ≈ 39.8 GB W4A16. FP8 is ≈ 57% of BF16 for the 8B, not 50% |
| vLLM online FP8 (Lesson 13) | in v0.31+ quantizing a BF16 checkpoint on the fly uses `--quantization fp8_per_tensor` (or `fp8_per_block`), per vLLM's Online Quantization doc |
| DCGM metric names | use the names dcgm-exporter exposes (`DCGM_FI_DEV_GPU_UTIL`, `DCGM_FI_PROF_SM_ACTIVE`, …); newer DCGM releases rename some fields, mention that once at most |
| Decode lower bound | step time ≥ (bytes of weights + bytes of KV cache read) ÷ memory bandwidth |
| GPU price | Not a fact: state it as an assumption. Use "assume $3.00 per H100-hour" everywhere |

Engine flags, metric names, and APIs change between versions. Check them in the current docs
(docs.vllm.ai, docs.sglang.io, nvidia.github.io/TensorRT-LLM, kubernetes.io, keda.sh, the NVIDIA DCGM
exporter, prometheus.io) before writing them down. Hugging Face Transformers is on v5 (`dtype=`,
not `torch_dtype=`). Never invent a URL, arXiv ID, flag, or metric: if you cannot verify it, leave
it out. Python snippets must at least pass `python -m py_compile`.
