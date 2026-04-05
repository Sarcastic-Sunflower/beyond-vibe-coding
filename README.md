# Beyond Vibe Coding: LLM-Assisted Chess Engine Refactoring

This repository contains the experimental assets and results for a study evaluating Gemini-3.0-Flash as a software engineering assistant. The research investigates the reliability of Large Language Models (LLMs) in refactoring tasks within rule-constrained domains, using chess as a benchmark to evaluate sycophancy and code hallucination.

---

## Repository Structure

The project is organised into several functional areas to support the empirical investigation, combining benchmarking, datasets, and a large set of structured experimental runs.

### Project Tree

```bash
.
├── README.md
├── benchmarks
│ ├── accuracy
│ ├── lizard
│ └── runtimes
├── datasets
│ ├── ground_truth
│ └── input
├── docs
└── experiments
  ├── prelim_results
  ├── prompts
  └── runs

```

A total of **210 directories and 494 files** are included, reflecting extensive iterative experimentation.

---

### 1. benchmarks

This directory contains the automated evaluation suite used to analyse generated code iterations.

- **accuracy**  
  Scripts and summaries used to verify move generation against ground truth datasets (e.g. `test_accuracy.sh`, `baseline_accuracy.sh`, and dataset-specific summaries).

- **lizard**  
  Python scripts and logs used to compute Cyclomatic Complexity, enabling structural comparison between baseline and refactored implementations.

- **runtimes**  
  Benchmarking scripts and logs used to measure execution time and compare performance against baseline implementations.

---

### 2. datasets

This directory contains the controlled inputs and expected outputs used for evaluation.

- **input**  
  Scenario data and test cases for multiple datasets, including move sequences and intermediate outputs.

- **ground_truth**  
  Verified correct move sets used for automated accuracy validation.

---

### 3. docs

Supporting documentation for the experimental process.

- Chat logs and references (`Links-to-Chats.txt`)
- Supplementary notes and analysis show board setups and planning.

---

### 4. experiments

This is the core of the repository and contains all LLM-generated outputs and iterations.

- **prelim_results**  
  Early-stage exploratory runs and initial improvements.

- **prompts**  
  The full set of multi-turn prompts used to guide LLM behaviour during refactoring.

- **runs**  
  A comprehensive record of all experimental runs, organised by:
  - Dataset (D1–D3)
  - Chat/session (C1–C10)
  - Iteration (1–5)

Each run directory contains:
- Source code variations (`engine.py`, `board.py`, `main.py`, etc.)
- Input move files (`moves*.txt`)
- Generated outputs (`output*.txt`)
- Compiled artefacts (`__pycache__`)

This structure enables precise tracking of how code evolves across iterations and prompt refinements.

---

## Experimental Requirements

All generated code iterations were evaluated using a fixed output structure:

1. Board state as a list of positions after three moves  
2. List of all possible moves (legal and illegal)  
3. List of all legal moves  
4. List of all illegal moves  

---

## Findings Summary

The study found that Gemini-3.0-Flash is effective in reducing Cyclomatic Complexity, indicating an ability to simplify code structure. However, it demonstrates fragile logic when maintaining domain-specific correctness. Iterative human-in-the-loop feedback improves performance to some extent but does not ensure consistent correctness or efficient optimisation.

---

## Context

This repository serves as the technical documentation for the ELEN4010 Individual Project (2026) at the University of the Witwatersrand.
