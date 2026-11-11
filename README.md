# Agentic AI Learning Progress

This repository tracks daily learning and hands-on Python practice in Agentic AI. It brings the exercises together in day-wise order to make it easy to revisit concepts and follow the learning progress.

## What this repository covers

- Working with language models using Gemini, Groq, and Ollama.
- Processing PDF documents and splitting text into chunks.
- Creating embeddings and searching with ChromaDB and BM25.
- Building retrieval-augmented generation (RAG) workflows with hybrid search and reranking.
- Improving answers through query rewriting, citations, and evaluation.
- Learning tool calling with practical Python examples.
- Tracking operation IDs, retries, and dependencies between tool operations.
- Executing independent operations concurrently with Python threads.

## Current progress

Practice files now extend through **Day 20**. Day 19 has been expanded with retry handling, operation IDs, in-memory idempotency, and dependency-based execution. Day 20 adds concurrent execution examples and a Groq tool-calling exercise.

This records the exercises present in the repository, rather than claiming that every topic is mastered or every API-backed example has been verified end to end.

### Earlier practice

| Files | Practice covered |
| --- | --- |
| `1.py`, `2.py` | NLTK tokenization |
| `Day02-*.py` | Sentence embeddings and cosine similarity |
| `Day03-1.py`, `Day04-*.py` | Ollama examples and ChromaDB retrieval |
| `Day05-1.py` through `Day14-3.py` | RAG practice with PDFs, chunking, embeddings, reranking, BM25/hybrid search, query rewriting, citations, and evaluation; Gemini and later Groq examples |
| `Day15-1.py`, `Day16-1.py` | Tool schemas, Python function execution, and returning tool results to the model |
| `Day17-1.py`, `Day17-2.py` | Multiple tools, a tool registry, and iterative tool calling |
| `Day18-1.py` | Validating calls against a predefined list of pending operations |

### Latest exercises: Days 19 and 20

| File | What it demonstrates | Verification |
| --- | --- | --- |
| [Day19-1.py](Day19-1.py) | Handling multiple model-requested tool calls; Python executes them sequentially | Existing API exercise |
| [Day19-2.py](Day19-2.py) | A simulated temporary failure, per-tool retry counters, API error handling, operation IDs, and reuse of successful results with argument fingerprints | Syntax checked; live Groq run still to verify |
| [Day19-3.py](Day19-3.py) | A predefined operation plan with dependency checks, argument resolution, sequential execution, and detection of stalled/circular dependencies | Local run passed: results `20`, `70`, `14` |
| [Day20-1.py](Day20-1.py) | Three independent calculations using `ThreadPoolExecutor` | Local run passed: `[20, 100, 30]` |
| [Day20-2.py](Day20-2.py) | Concurrent execution of ready operations, then a dependent sum; results collected with `as_completed` | Local run passed: final result `120` |
| [Day20-3.py](Day20-3.py) | Concurrent execution of model-requested tools, separate tool responses, per-operation failure counts, and retry instructions | Syntax checked; live Groq run still to verify |

The plans in `Day19-3.py` and `Day20-2.py` are written in Python; the model does not generate them. Day 20's concurrency examples use simulated delays to make overlapping work visible.

These are learning scripts. `Day19-2.py` stores successful results only in memory for the current run. `Day20-3.py` does not implement that idempotency store or a dependency scheduler; its retry limit is communicated to the model, without a Python guard preventing another call after the limit. Strengthening those controls and checking API behavior remain follow-up work.

## Running the latest local examples

From the repository folder, with Python 3 available:

```powershell
python Day19-3.py
python Day20-1.py
python Day20-2.py
```

These three scripts use the Python standard library and do not need an API key.

For the recent Groq examples, activate a local virtual environment, install `groq` and `python-dotenv`, and set `GROQ_API_KEY` in a local `.env` file beside the scripts. Then run the desired file, such as `python Day20-3.py`. These scripts make external API requests and require access to the configured model. Earlier RAG exercises have additional dependencies and local model/document requirements; there is no consolidated dependency file yet.

Keep `.env`, real API keys, virtual environments, editor settings, and generated databases out of commits. The repository's `.gitignore` excludes these local files.

## Purpose

The goal is to understand these concepts by writing and exploring small examples, then gradually build towards AI applications that can retrieve information and use tools.
