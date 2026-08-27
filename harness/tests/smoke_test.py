#!/usr/bin/env python3
"""Offline smoke test for the published evaluation-processing flow."""

from __future__ import annotations

import csv
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PUBLISHED = ROOT / "results/massive-run-article"


def run(*parts: str) -> None:
    command = [sys.executable, *map(str, parts)]
    shown = " ".join(str(part) for part in parts)
    print(f"\n$ python3 {shown}", flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def check_entry_points() -> None:
    scripts = [
        "harness/collect/collect_claude.py",
        "harness/collect/collect_codex_subagents.py",
        "harness/collect/collect_codex_rag.py",
        "harness/collect/parse_claude.py",
        "harness/collect/parse_codex.py",
        "harness/collect/validate_run.py",
        "harness/score/validate_score_run.py",
        "harness/score/merge_score_cards.py",
        "harness/report/generate_report.py",
    ]
    for script in scripts:
        run(script, "--help")


def check_profiles() -> None:
    profile_dir = ROOT / "harness/workspaces/codex-profiles"
    profiles = sorted(profile_dir.glob("*.config.toml"))
    assert len(profiles) == 4, profiles
    dataset_ids = {
        "c1-raw-rag.config.toml": "REPLACE_C1_SOURCES_DATASET_ID",
        "c1-wr-rag.config.toml": "REPLACE_C1_WORK_REGISTRY_DATASET_ID",
        "c2-raw-rag.config.toml": "REPLACE_C2_SOURCES_DATASET_ID",
        "c2-wr-rag.config.toml": "REPLACE_C2_WORK_REGISTRY_DATASET_ID",
    }
    for profile in profiles:
        config = tomllib.loads(profile.read_text(encoding="utf-8"))
        assert config["model"] == "gpt-5.6-terra"
        assert config["features"]["shell_tool"] is False
        assert config["tools"]["web_search"] is False
        assert config["mcp_servers"]["tl-v1"]["enabled_tools"] == [
            "ragflow_retrieval"
        ]
        text = profile.read_text(encoding="utf-8")
        assert "REPLACE_REPO_ROOT" in text
        assert dataset_ids[profile.name] in text
    print("\nprofiles: four fixed-dataset TOML profiles verified")


def check_prompt_classification() -> None:
    sys.path.insert(0, str(ROOT / "harness/collect"))
    from collect_claude import classify_arm
    from collect_codex_subagents import parse_agent_path

    assert classify_arm("Use dataset REPLACE_C1_SOURCES_DATASET_ID") == "sources"
    assert classify_arm("Use dataset REPLACE_C2_WORK_REGISTRY_DATASET_ID") == "workrag"
    assert classify_arm("Use only /tmp/c1 directory to answer") == "directory"
    assert classify_arm("Answer only from internal/parametric knowledge") == "baseline"
    assert parse_agent_path("/root/c1_q01_r1_wrdir") == {
        "arm": "directory",
        "corpus": "c1",
        "key": "Q01",
        "round": 1,
        "retry": False,
    }
    assert parse_agent_path("/root/baseline_c2_r1_q01")["arm"] == "baseline"
    print("\ncollection: fixed dataset IDs and prompt markers verified")


def check_parse_pipeline() -> None:
    with tempfile.TemporaryDirectory(prefix="work-registry-eval-parse-") as tmp:
        base = Path(tmp)
        parse_run = base / "run"
        claude_logs = parse_run / "logs/claude"
        codex_logs = parse_run / "logs/codex-dir"
        raw_rag = base / "raw-rag"
        claude_logs.mkdir(parents=True)
        codex_logs.mkdir(parents=True)
        raw_rag.mkdir()

        shutil.copy2(
            PUBLISHED / "logs/claude/c1-Q01-claude-directory-r1.jsonl",
            claude_logs / "c1-Q01-claude-directory-r1.jsonl",
        )
        shutil.copy2(
            PUBLISHED / "logs/codex-dir/c1-Q01-codex-dir-directory-r1.jsonl",
            codex_logs / "c1-Q01-codex-dir-directory-r1.jsonl",
        )
        shutil.copy2(
            PUBLISHED / "logs/codex-rag/c1-Q01-codex-rag-sources-r1.jsonl",
            raw_rag / "c1-q01-raw-r1.jsonl",
        )
        (raw_rag / "c1-q01-raw-r1.status").write_text("0\n", encoding="utf-8")

        run(
            "harness/collect/collect_codex_rag.py",
            str(raw_rag),
            "--run-dir",
            str(parse_run),
        )
        run("harness/collect/parse_claude.py", "--run-dir", str(parse_run))
        run("harness/collect/parse_codex.py", "--run-dir", str(parse_run))
        run(
            "harness/collect/validate_run.py",
            "--run-dir",
            str(parse_run),
            "--expect-rounds",
            "1",
        )

        usage = csv_rows(parse_run / "usage.csv")
        assert len(usage) == 3, len(usage)
        for row in usage:
            response = (
                parse_run / "logs" / row["tool"] / f"{row['run_id']}.md"
            ).read_text(encoding="utf-8")
            assert "<!-- RESPONSE_START -->" in response
        print("\ncollection/parse: three representative sessions verified")


def check_pipeline() -> None:
    assert PUBLISHED.is_dir(), PUBLISHED
    run("harness/tests/test_analyze_session_synth.py")
    run("harness/score/validate_answer_keys.py")
    run(
        "harness/collect/validate_run.py",
        "--run-dir",
        str(PUBLISHED),
        "--expect-rounds",
        "3",
        "--expect-baseline-rounds",
        "1",
    )
    run("harness/score/validate_score_run.py", "--run-dir", str(PUBLISHED))

    with tempfile.TemporaryDirectory(prefix="work-registry-eval-smoke-") as tmp:
        smoke_run = Path(tmp) / "run"
        smoke_run.mkdir()
        shutil.copy2(PUBLISHED / "usage.csv", smoke_run / "usage.csv")
        # Exercise the fresh-run snapshot, including dashed C2 answer-key IDs.
        shutil.copy2(ROOT / "harness/questions.csv", smoke_run / "questions.csv")
        shutil.copytree(PUBLISHED / "scores", smoke_run / "scores")
        (smoke_run / "logs").symlink_to(PUBLISHED / "logs", target_is_directory=True)

        run("harness/score/validate_score_run.py", "--run-dir", str(smoke_run))
        run("harness/score/merge_score_cards.py", "--run-dir", str(smoke_run))
        run("harness/report/generate_report.py", "--run-dir", str(smoke_run))

        cards = csv_rows(smoke_run / "score-cards.csv")
        assert len(cards) == 570, len(cards)
        expected_reports = {
            "accuracy_by_arm.csv",
            "cost_by_arm.csv",
            "cost_deltas.csv",
            "cost_per_correct.csv",
            "per_question.csv",
            "report.md",
        }
        actual_reports = {path.name for path in (smoke_run / "report").iterdir()}
        assert actual_reports == expected_reports, actual_reports
        print("\nmerge/report: 570 sessions and six report artifacts verified")


def main() -> None:
    check_entry_points()
    check_profiles()
    check_prompt_classification()
    check_parse_pipeline()
    check_pipeline()
    print("\nSMOKE TEST PASSED")


if __name__ == "__main__":
    main()
