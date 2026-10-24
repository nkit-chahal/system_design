# Authoring guide: AI Training Engineering

This course is the companion to **AI Inference Engineering** and is written the same way.
Fragment syntax, page skeleton, voice, length, the SVG figure style and the summary spec format
are exactly as in `course_src/ai_inference/AUTHORING.md`. Read that file first; this file only
lists what is different for the training course.

The reference lesson for depth, voice, structure and drawing style is the inference course's
`course_src/ai_inference/003.html` (KV Cache) with its figures
`AI Inference Engineering/images/003-*.svg`. Match it.

## Files

| What | Where |
|---|---|
| Lesson source (HTML fragment) | `course_src/ai_training/NNN.html` |
| Figures (hand-written SVG) | `AI Training Engineering/images/NNN-short-slug.svg` |
| Summary mind-map spec | `course_src/ai_training/summary/NNN.txt` |
| Built page (never edit by hand) | `AI Training Engineering/NNN Title.html` |

Build and preview (from the repo root):

```bash
python generate_training_course.py 10 11          # builds 010 and 011 only
python course_src/preview.py --course ai_training figs <out_dir> "AI Training Engineering/images/010-*.svg"
python course_src/preview.py --course ai_training page <out_dir> 10
```

Titles, numbers and stages are in `CURRICULUM` in `generate_training_course.py`. Cross-reference
lessons as "Lesson 11, ZeRO and FSDP". Link to the inference course as
"Inference Lesson 35, Mixture-of-Experts Serving" (titles are in `generate_inference_course.py`);
do not re-teach what it covers (KV cache, serving engines, quantization for serving, GPU
architecture and attention kernels in Inference Lesson 33, distillation in Inference Lesson 14).

## Page skeleton differences

* Topic lessons follow the inference skeleton: Introduction, Clarifying the Problem (Candidate /
  Interviewer dialogue), two to four core sections with a "Which … fits our run?" decision,
  In Practice, Other Talking Points, Summary, Reference Material.
* Labs are 006, 009, 016, 021, 027 and 033; Stage 7 has no lab. Labs follow the inference lab
  skeleton. Their small path must run on one consumer GPU or a free Colab-class GPU with a model of
  at most ~125M parameters (or LoRA on a 0.5B–1.5B model); their full path uses one or more
  8×H100 nodes and states the cost as an assumption.
* In Practice code is PyTorch (2.x), Hugging Face Transformers v5 (`dtype=`, not `torch_dtype=`),
  TRL, PEFT, Accelerate, DeepSpeed, Megatron-LM or torchtitan, as fits the topic. Verify every API,
  flag and config key against current docs before writing it.

## Running scenarios

Use these so numbers agree across lessons. A lesson that needs a different scenario says so.

**Pretraining run (Stages 1–4, 6, 7).** Pretrain a model with the Llama 3.1 8B architecture on
1 trillion tokens on 256 H100 GPUs (32 nodes × 8, NVLink inside a node, 8 × 400 Gb/s InfiniBand
NICs per node), sequence length 8,192, global batch ≈ 4M tokens (512 sequences), target 40% MFU.

**Post-training run (Stage 5).** Fine-tune Llama 3.1 8B Instruct for a customer-support product on
one 8×H100 node: SFT on 50,000 conversations of ≈ 1,000 tokens, then DPO on 20,000 preference
pairs; LoRA/QLoRA variants for teams with one GPU.

## Facts to keep consistent

| Fact | Value |
|---|---|
| Llama 3.1 8B architecture | 8.03B params; 32 layers; hidden 4,096; FFN 14,336; 32 query heads, 8 KV heads, head dim 128; vocab 128,256 |
| Training FLOPs | ≈ 6 × N × D (2ND forward, 4ND backward); ≈ 8ND with full activation recomputation |
| Pretraining run compute | 6 × 8.03e9 × 1e12 ≈ 4.8e22 FLOPs |
| Pretraining run time | 256 × 989 TFLOPS × 0.40 ≈ 1.01e17 FLOPS ⇒ ≈ 4.75e5 s ≈ 5.5 days ≈ 33,800 GPU-hours |
| GPU price | Not a fact: "assume $3.00 per H100-hour" everywhere ⇒ pretraining run ≈ $101,000 |
| Mixed-precision Adam memory | 16 bytes per parameter: BF16 weights 2 + BF16 gradients 2 + FP32 master weights 4 + Adam m 4 + Adam v 4 ⇒ 8B model ≈ 128.5 GB before activations, so it does not fit on one 80 GB H100 |
| ZeRO-3 / FSDP over 8 GPUs | ≈ 16 GB of model and optimizer state per GPU for the 8B model, plus activations |
| Chinchilla rule of thumb | compute-optimal ≈ 20 tokens per parameter (Hoffmann et al., 2022); Llama 3 8B was trained on over 15T tokens, far past that, to be cheaper to serve |
| Ring all-reduce traffic | each GPU sends and receives ≈ 2(N−1)/N × message size; BF16 gradients of the 8B model are ≈ 16 GB per step |
| H100 SXM 80 GB | ≈ 79.6 GiB visible; HBM3 3.35 TB/s; ≈ 989 TFLOPS dense BF16; ≈ 1,979 TFLOPS dense FP8; NVLink 900 GB/s per GPU |
| InfiniBand NDR | 400 Gb/s ≈ 50 GB/s per NIC; 8 NICs ⇒ ≈ 400 GB/s per node |
| A100 80 GB SXM | ≈ 2.0 TB/s; 312 TFLOPS dense BF16; no FP8 |

Numbers from papers or model cards (training GPU-hours, MFU reported for Llama 3, failure counts
during training, dataset sizes) must be verified against the source and cited. Never invent a URL,
arXiv ID, flag, config key or benchmark number; if you cannot verify it, leave it out.
