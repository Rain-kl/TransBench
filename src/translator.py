from __future__ import annotations

import time
import threading
from dataclasses import dataclass

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from .config import AppConfig

SYSTEM_PROMPTS = {
    "zh_en": (
        "You are a professional translator. Translate the user's Chinese text into natural, accurate English. "
        "Return translation only, without notes."
    ),
    "en_zh": (
        "You are a professional translator. Translate the user's English text into natural, accurate Simplified Chinese. "
        "Return translation only, without notes."
    ),
}


@dataclass(slots=True)
class TranslationResult:
    text: str
    error: Exception | None = None


class Translator:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self._local = threading.local()

    def _get_client(self) -> ChatOpenAI:
        client = getattr(self._local, "client", None)
        if client is None:
            client = ChatOpenAI(
                model=self.config.model_name,
                api_key=self.config.api_key,
                base_url=self.config.base_url,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                timeout=self.config.timeout,
            )
            self._local.client = client
        return client

    def translate(self, task: str, source: str) -> TranslationResult:
        if task not in SYSTEM_PROMPTS:
            return TranslationResult(text="", error=ValueError(f"Unsupported task: {task}"))

        messages = [
            SystemMessage(content=SYSTEM_PROMPTS[task]),
            HumanMessage(content=source),
        ]

        last_error: Exception | None = None
        for attempt in range(1, self.config.retries + 1):
            try:
                response = self._get_client().invoke(messages)
                translated = str(response.content).strip()
                return TranslationResult(text=translated)
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                if attempt < self.config.retries:
                    time.sleep(0.5 * attempt)

        return TranslationResult(text="", error=last_error)
