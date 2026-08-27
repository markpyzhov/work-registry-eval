"""Extract the prompt and final answer from Claude Code or Codex JSONL logs."""

from __future__ import annotations

import json
from pathlib import Path


_PROMPT_NOISE_PREFIXES = (
    "The following is the Codex agent history",
    "<",
)


def _load(path: Path) -> list[dict]:
    records = []
    with Path(path).open(encoding="utf-8") as handle:
        for line in handle:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def _is_noise(text: str) -> bool:
    return any(text.startswith(prefix) for prefix in _PROMPT_NOISE_PREFIXES)


def _claude_text(content) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                return (block.get("text") or "").strip()
    return ""


def extract_transcript(path: Path, source: str,
                       prompt_override: str | None = None) -> tuple[str, str]:
    """Return ``(prompt, final_response)`` from one session log."""
    records = _load(path)
    prompt = response = ""

    if source == "codex":
        for record in records:
            payload = record.get("payload") or {}
            if (record.get("type") == "event_msg"
                    and payload.get("type") == "user_message"):
                text = (payload.get("message") or "").strip()
                if text and not _is_noise(text):
                    prompt = text
                    break

        # Subagent logs may contain an explicit FINAL_ANSWER sent to the parent.
        for record in records:
            payload = record.get("payload") or {}
            if (record.get("type") != "response_item"
                    or payload.get("type") != "agent_message"):
                continue
            content = payload.get("content") or []
            text = "\n".join(
                block.get("text", "") for block in content
                if isinstance(block, dict) and block.get("type") == "input_text"
            ).strip()
            if text.startswith("Message Type: FINAL_ANSWER"):
                response = text.split("Payload:\n", 1)[-1].strip()

        if not response:
            for record in reversed(records):
                payload = record.get("payload") or {}
                if (record.get("type") == "event_msg"
                        and payload.get("type") == "agent_message"):
                    text = (payload.get("message") or "").strip()
                    if text:
                        response = text
                        break
    else:
        for record in records:
            if record.get("type") == "user" and isinstance(record.get("message"), dict):
                text = _claude_text(record["message"].get("content"))
                if text and not _is_noise(text):
                    prompt = text
                    break
        for record in reversed(records):
            if record.get("type") != "assistant" or not isinstance(record.get("message"), dict):
                continue
            content = record["message"].get("content")
            if isinstance(content, list):
                text = "\n".join(
                    block.get("text", "") for block in content
                    if isinstance(block, dict) and block.get("type") == "text"
                ).strip()
                if text:
                    response = text
                    break

    return prompt_override or prompt, response
