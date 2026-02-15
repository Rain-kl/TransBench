# TransBench

A benchmark tool for evaluating large language models on Chinese-English translation tasks.

## Features

- Parse `exam.txt` with `<zh_en>` and `<en_zh>` sections
- Skip empty lines and comment lines (`# ...`)
- Concurrent translation with configurable worker count
- Optional per-task random sampling (`ZH_EN_LIMIT` / `EN_ZH_LIMIT`)
- CSV outputs per task and combined output
- Progress bar (`tqdm`) and structured logs (`loguru`)

## Quick Start

### 1. Prepare environment

```bash
cp .env.example .env
```

Fill required values in `.env`:

- `OPENAI_API_KEY`
- `MODEL_NAME`

### 2. Run

```bash
./run.sh
```

Or run with custom arguments:

```bash
./run.sh --tasks zh_en,en_zh --workers 8 --zh_en_limit 50 --en_zh_limit 50 --random_seed 42
```

## Input Format (`exam.txt`)

```text
<exam>
<zh_en>
# comment
高质量发展
</zh_en>
<en_zh>
High-quality development
</en_zh>
</exam>
```

## Outputs

Generated under `outputs/`:

- `result_zh_en.csv`
- `result_en_zh.csv`
- `result_combine.csv`

Log files are generated under `logs/`.

## Configuration

See `.env.example` for all options, including:

- API/model settings
- timeout/retry
- concurrency workers
- per-task sample limits

## Development

```bash
uv sync
python -m compileall src
```

## License

MIT. See `LICENSE`.
