"""
generate_inference_course.py — Builds the AI Inference Engineering course from lesson
fragments in course_src/ai_inference/ (page building lives in course_builder.py).
"""
import os
import sys

from course_builder import Course, build_all

COURSE_DIR = 'AI Inference Engineering'
SRC_DIR = os.path.join('course_src', 'ai_inference')

STAGES = {
    'start': 'Start Here',
    's1': 'Stage 1 · How a Model Generates',
    's2': 'Stage 2 · Serving Engines',
    's3': 'Stage 3 · Smaller and Faster Models',
    's4': 'Stage 4 · GPU Math and Cost',
    's5': 'Stage 5 · Production Serving',
    's6': 'Stage 6 · Observability',
    's7': 'Stage 7 · Advanced Serving',
}

CURRICULUM = [
    (1, 'start', 'Introduction and Overview'),
    (2, 's1', 'Prefill vs Decode'),
    (3, 's1', 'KV Cache'),
    (4, 's1', 'Time to First Token'),
    (5, 's1', 'Tokens per Second'),
    (6, 's1', 'Lab - Measure TTFT and Throughput'),
    (7, 's2', 'Continuous Batching'),
    (8, 's2', 'PagedAttention'),
    (9, 's2', 'vLLM'),
    (10, 's2', 'SGLang'),
    (11, 's2', 'TensorRT-LLM'),
    (12, 's2', 'Lab - Benchmark Two Engines at 50 Concurrent Users'),
    (13, 's3', 'Quantization - FP8, INT8 and 4-bit'),
    (14, 's3', 'Distillation'),
    (15, 's3', 'Speculative Decoding'),
    (16, 's3', 'Lab - Halve Model Memory Without Losing Quality'),
    (17, 's4', 'VRAM Budgeting'),
    (18, 's4', 'Tensor Parallelism'),
    (19, 's4', 'GPU Utilization'),
    (20, 's4', 'Cost per Million Tokens'),
    (21, 's4', 'Lab - GPUs for 1,000 Requests per Minute Under a 2s SLA'),
    (22, 's5', 'Autoscaling'),
    (23, 's5', 'Cold Starts'),
    (24, 's5', 'Prefix Caching'),
    (25, 's5', 'Request Routing'),
    (26, 's5', 'Rate Limiting'),
    (27, 's5', 'Lab - Surviving a 10x Traffic Spike'),
    (28, 's6', 'p50, p95 and p99 Latency'),
    (29, 's6', 'Queue Depth'),
    (30, 's6', 'GPU Metrics'),
    (31, 's6', 'Per-Request Token Accounting'),
    (32, 's6', 'Lab - A Dashboard That Explains Latency Spikes'),
    (33, 's7', 'GPU Architecture and Attention Kernels'),
    (34, 's7', 'Disaggregated Prefill and Decode'),
    (35, 's7', 'Mixture-of-Experts Serving'),
    (36, 's7', 'Long-Context Serving'),
    (37, 's7', 'Multi-LoRA and Multi-Tenant Serving'),
    (38, 's7', 'Structured Output and Tool Calling'),
    (39, 's7', 'Batch and Offline Inference'),
    (40, 's7', 'Reliability and Rollouts'),
]

COURSE = Course('AI Inference Engineering', COURSE_DIR, SRC_DIR, STAGES, CURRICULUM)

if __name__ == '__main__':
    build_all(COURSE, {int(a) for a in sys.argv[1:]} or None)
