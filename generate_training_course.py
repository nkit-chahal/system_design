"""
generate_training_course.py — Builds the AI Training Engineering course from lesson
fragments in course_src/ai_training/ (page building lives in course_builder.py).
"""
import os
import sys

from course_builder import Course, build_all

COURSE_DIR = 'AI Training Engineering'
SRC_DIR = os.path.join('course_src', 'ai_training')

STAGES = {
    'start': 'Start Here',
    's1': 'Stage 1 · How Training Works',
    's2': 'Stage 2 · Compute and Scaling',
    's3': 'Stage 3 · Distributed Training',
    's4': 'Stage 4 · Data',
    's5': 'Stage 5 · Post-Training',
    's6': 'Stage 6 · Training at Scale',
    's7': 'Stage 7 · Evaluation',
}

CURRICULUM = [
    (1, 'start', 'Introduction and Overview'),
    (2, 's1', 'Forward and Backward Passes'),
    (3, 's1', 'Training Memory'),
    (4, 's1', 'Optimizers - SGD, Adam and Beyond'),
    (5, 's1', 'Mixed Precision Training - BF16 and FP8'),
    (6, 's1', 'Lab - Train a Small GPT and Account for Every GB'),
    (7, 's2', 'Training FLOPs, Time and MFU'),
    (8, 's2', 'Scaling Laws'),
    (9, 's2', 'Lab - Size a Training Run'),
    (10, 's3', 'Data Parallelism and All-Reduce'),
    (11, 's3', 'ZeRO and FSDP'),
    (12, 's3', 'Tensor, Sequence and Context Parallelism'),
    (13, 's3', 'Pipeline Parallelism'),
    (14, 's3', 'Combining Parallelism - 3D and 4D'),
    (15, 's3', 'Expert Parallelism for MoE Training'),
    (16, 's3', 'Lab - DDP vs FSDP'),
    (17, 's4', 'Pretraining Data Pipelines'),
    (18, 's4', 'Deduplication and Quality Filtering'),
    (19, 's4', 'Tokenizers'),
    (20, 's4', 'Data Mixtures and Curriculum'),
    (21, 's4', 'Lab - Build a Filtering and Dedup Pipeline'),
    (22, 's5', 'Supervised Fine-Tuning'),
    (23, 's5', 'LoRA and QLoRA'),
    (24, 's5', 'Reward Models and RLHF'),
    (25, 's5', 'DPO and Preference Optimization'),
    (26, 's5', 'RL with Verifiable Rewards - GRPO'),
    (27, 's5', 'Lab - LoRA Fine-Tune Then DPO'),
    (28, 's6', 'Checkpointing'),
    (29, 's6', 'Failures, Restarts and Elastic Training'),
    (30, 's6', 'Cluster Networking and Collectives'),
    (31, 's6', 'Job Scheduling - Slurm and Kubernetes'),
    (32, 's6', 'Training Stability - Loss Spikes and Divergence'),
    (33, 's6', 'Lab - Recover a Run From a Failure'),
    (34, 's7', 'Evaluation During Training'),
    (35, 's7', 'Benchmarks and Contamination'),
]

COURSE = Course('AI Training Engineering', COURSE_DIR, SRC_DIR, STAGES, CURRICULUM)

if __name__ == '__main__':
    build_all(COURSE, {int(a) for a in sys.argv[1:]} or None)
