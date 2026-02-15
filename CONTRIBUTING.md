# Contributing Guide

Thanks for contributing to TransBench.

## Development Setup

1. Install `uv`.
2. Create `.env` from `.env.example` and fill required values.
3. Install deps and run:

```bash
uv sync
./run.sh --tasks zh_en,en_zh
```

## Project Structure

- `src/parser.py`: parse `exam.txt`
- `src/translator.py`: LLM translation logic
- `src/main.py`: CLI orchestration and concurrency
- `src/writer.py`: CSV output

## Pull Request Rules

- Keep PRs focused and small.
- Add/update docs when behavior changes.
- Ensure commands pass before opening PR:

```bash
python -m compileall src
```

## Commit Messages

Prefer clear prefixes:

- `feat:` new functionality
- `fix:` bug fix
- `docs:` docs only
- `refactor:` code refactor

## Reporting Issues

Use issue templates and include:

- expected behavior
- actual behavior
- reproduction steps
- sample input/output (if available)
