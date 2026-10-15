# Agentic AI Learning Progress

Daily Python practice while learning Agentic AI, retrieval-augmented generation (RAG), and tool calling.

The folder contains earlier practice scripts and learning code through Day 15. Day filenames use two-digit day numbers (`Day02`, `Day03`, ..., `Day15`) so GitHub displays the exercises in day order, matching the reference repository.

## Source

Day 8 matches the original reference. Day 9–15 scripts were copied from [munixdelta/AGENTIC_AI_IN_TRIAL](https://github.com/munixdelta/AGENTIC_AI_IN_TRIAL). Day filenames match the reference repository. Credit for the imported learning examples belongs to the original author.

Reference commit: `2cc4b0ac6d50b17fbc20c5a7c6d839c753bf4223`.

## Local setup

Use a Python environment with the packages imported by the exercise you want to run. Some exercises use Gemini, some use Groq, and earlier exercises may use Ollama. Keep the required `GEMINI_API_KEY` or `GROQ_API_KEY` in a local `.env` file. API keys and virtual environments are excluded from Git.

Run exercises from this folder so the relative `documents/` path resolves, for example:

```powershell
python Day15-1.py
```

The scripts were checked for Python syntax before upload. Live API calls and model downloads were not run as part of the import.
