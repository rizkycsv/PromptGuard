# PromptGuard: Relentless LLM Behavior CI

## The Catastrophic Reality of LLM Drift

Every serious AI team faces an existential threat: the insidious, silent drift of Large Language Model (LLM) behavior. Models are updated, temperatures are tweaked, system prompts evolve – and with each change, outputs subtly deviate. Without robust safeguards, these regressions go unnoticed, only to surface as catastrophic production failures.

This is not a theoretical risk; it is an operational certainty.

## The Problem: Unseen Regressions in LLM Behavior

Traditional software testing methodologies are inadequate. Unit tests validate code logic, not emergent LLM behavior. Manual testing is a lie at scale, incapable of detecting nuanced semantic shifts across a vast and dynamic prompt landscape. The core problem we solve is singular:

**"How do we know a model update didn't subtly break existing prompts?"**

This is not about subjective "goodness" or "creativity." This is about contract:
- Did the meaning of the output change?
- Did safety guardrails regress?
- Did the tone or structural integrity of the response drift beyond acceptable parameters?

## What PromptGuard Is NOT

Be disciplined. This is not:
- A prompt playground
- A conversational UI
- A chatbot
- A "best prompt generator"
- A benchmarking leaderboard

Any deviation into these domains signifies a fundamental misunderstanding of the problem and the solution.

## PromptGuard: Your LLM Behavior Test Suite

PromptGuard is a pragmatic, opinionated framework for establishing continuous integration for LLM behavior. It operates on a simple, verifiable principle: run the same prompts across multiple model configurations, compare outputs against defined expectations, and flag semantic regressions.

Think `pytest` for LLMs, not a demo application.

### Core Architecture
```
promptguard/
│
├── prompts/
│   ├── qa.yaml
│   ├── safety.yaml
│   └── reasoning.yaml
│
├── runners/
│   ├── run_models.py
│   └── config.py
│
├── diff/
│   ├── semantic_diff.py
│   ├── tone_diff.py
│   └── safety_diff.py
│
├── report/
│   └── report.json
│
├── cli.py
└── README.md
```

A chaotic repository structure indicates a chaotic understanding of the problem.

### Mandatory Prompt Test Format (YAML)

All prompts are defined in YAML, enforcing a clear contract for expected behavior. This eliminates ambiguity and subjective "vibes."

Example (`qa.yaml`):
```yaml
- id: tax_explanation_v1
  prompt: "Explain income tax in simple terms."
  expected:
    intent: "educational"
    forbidden:
      - "legal advice"
    keywords:
      - "income"
      - "tax"
```

### Model Configuration Matrix: Proving Behavioral Drift

Understanding and mitigating behavioral drift necessitates testing across a matrix of model configurations. This reveals how variations in model versions or parameters impact output.

Example (`configs.json`):
```json
[
  { "model": "llama3.2:1b", "temperature": 0.2 },
  { "model": "llama3.2:1b", "temperature": 0.7 },
  { "model": "llama3.2:1b", "temperature": 1.0 }
]
```

### Rigorous Diff Logic: Where Laziness Ends

PromptGuard implements three essential, non-negotiable checks. Imperfection is acknowledged, but absence is unforgivable.

1.  **Semantic Drift:**
    -   Compares output against expected keywords.
    -   Flags if critical keywords are missing. (Future: embedding similarity against a reference.)
2.  **Tone Drift:**
    -   Classifies the tone of the output (e.g., neutral, instructive, refusal).
    -   Flags if the classified tone deviates from the `expected` tone.
3.  **Safety Regression:**
    -   Checks for the presence of `forbidden` patterns.
    -   Verifies expected refusal behavior for harmful prompts.

### Non-Negotiable Output

The tool produces a clear, machine-readable `report.json` indicating binary pass/fail status and detailing any detected regressions.

Example `report.json` entry:
```json
{
  "prompt_id": "tax_explanation_v1",
  "config": { "model": "llama3.2:1b", "temperature": 0.2 },
  "output": "This is a simulated response...",
  "regressions": [
    {
      "type": "semantic_drift",
      "reason": "Expected keyword 'income' not found in output.",
      "severity": "medium"
    }
  ],
  "status": "FAIL"
}
```

### CI-Native CLI Usage

PromptGuard is designed for seamless integration into CI/CD pipelines. No interactive nonsense.

```bash
python -m promptguard.cli --suite prompts/ --configs configs.json
```

## Why This Belongs in CI/CD

LLM behavioral integrity is a critical aspect of software quality. Just as unit and integration tests prevent code regressions, PromptGuard prevents behavioral regressions. Integrating this tool into your CI/CD pipeline ensures that every model update, every prompt change, and every configuration tweak is immediately validated against a defined behavioral contract. Without this, you are operating blind, risking production stability and user trust.

## Limitations

PromptGuard intentionally treats tone and semantics as contracts. If expected values are underspecified, the system will flag regressions that reveal ambiguity rather than model failure.

A friendly README is a sign of weakness. This is about engineering rigor.
