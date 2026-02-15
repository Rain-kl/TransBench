from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(slots=True)
class AppConfig:
    api_key: str
    base_url: str | None
    model_name: str
    temperature: float
    max_tokens: int | None
    timeout: float
    retries: int
    workers: int
    continue_on_error: bool


def load_config(
    continue_on_error: bool | None = None,
    workers: int | None = None,
    env_file: str = ".env",
) -> AppConfig:
    load_dotenv(env_file)

    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    if not api_key:
        raise ValueError("Missing API key. Set OPENAI_API_KEY or LLM_API_KEY in .env")

    model_name = os.getenv("MODEL_NAME")
    if not model_name:
        raise ValueError("Missing MODEL_NAME in .env")

    base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("LLM_BASE_URL")
    temperature = float(os.getenv("TEMPERATURE", "0"))

    max_tokens_raw = os.getenv("MAX_TOKENS", "").strip()
    max_tokens = int(max_tokens_raw) if max_tokens_raw else None

    timeout = float(os.getenv("TIMEOUT", "30"))
    retries = int(os.getenv("RETRIES", "3"))
    resolved_workers = workers if workers is not None else int(os.getenv("WORKERS", "4"))
    if resolved_workers <= 0:
        raise ValueError("WORKERS must be a positive integer")

    resolved_continue = continue_on_error
    if resolved_continue is None:
        resolved_continue = os.getenv("CONTINUE_ON_ERROR", "true").lower() in {"1", "true", "yes", "y"}

    return AppConfig(
        api_key=api_key,
        base_url=base_url,
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
        retries=retries,
        workers=resolved_workers,
        continue_on_error=resolved_continue,
    )


def ensure_dirs(base_dir: Path, outdir: str) -> tuple[Path, Path]:
    logs_dir = base_dir / "logs"
    output_dir = base_dir / outdir
    logs_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir, output_dir
