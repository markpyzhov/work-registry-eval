#!/usr/bin/env python3
"""Validate arm-specific answer-key coverage and intentional differences."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QUESTIONS_CSV = ROOT / "harness/questions.csv"


def normalize(text: str) -> str:
    return " ".join(text.split())


def questions(path: Path) -> dict[str, str]:
    text = path.read_text()
    matches = list(re.finditer(r"^## ((?:Q|A)-?\d{2})\s*$", text, re.MULTILINE))
    result = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        question_id = match.group(1)
        assert question_id not in result, (path, "duplicate question ID", question_id)
        result[question_id] = normalize(text[match.end():end])
    return result


def validate_question_registry() -> None:
    markdown_questions = {
        "c1": questions(ROOT / "corpora/corpus-1/ground-truth/questions.md"),
        "c2": questions(ROOT / "corpora/corpus-2/ground-truth/questions.md"),
    }
    csv_questions: dict[str, dict[str, str]] = {"c1": {}, "c2": {}}
    with QUESTIONS_CSV.open(newline="") as handle:
        for row in csv.DictReader(handle):
            corpus = row["corpus"]
            if corpus not in csv_questions:
                continue
            question_id = row["key"]
            assert question_id not in csv_questions[corpus], (
                "questions.csv",
                corpus,
                "duplicate question ID",
                question_id,
            )
            csv_questions[corpus][question_id] = normalize(row["question"])

    for corpus in markdown_questions:
        assert csv_questions[corpus].keys() == markdown_questions[corpus].keys(), (
            corpus,
            "question ID mismatch between questions.csv and questions.md",
        )
        for question_id, markdown_text in markdown_questions[corpus].items():
            assert csv_questions[corpus][question_id] == markdown_text, (
                corpus,
                question_id,
                "question text mismatch between questions.csv and questions.md",
            )


def sections(path: Path) -> dict[str, str]:
    text = path.read_text()
    matches = list(re.finditer(r"^## ((?:Q|A)-?\d{2})\b.*$", text, re.MULTILINE))
    result = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[match.group(1)] = text[match.start():end]
    return result


def verdict_text(section: str) -> str:
    match = re.search(
        r"^\*\*Verdict:\*\*\s*(.*?)(?=^\*\*|^## |\Z)",
        section,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise AssertionError("section is missing a Verdict field")
    return " ".join(match.group(1).split())


def require(section: str, *phrases: str) -> None:
    normalized = " ".join(section.split())
    for phrase in phrases:
        if phrase not in normalized:
            raise AssertionError(f"missing required phrase: {phrase!r}")


def forbid(section: str, *phrases: str) -> None:
    normalized = " ".join(section.split())
    for phrase in phrases:
        if phrase in normalized:
            raise AssertionError(f"forbidden phrase present: {phrase!r}")


def validate_corpus(
    root: Path,
    expected_ids: list[str],
    verdict_invariant_ids: set[str],
    split_ids: set[str],
    full_invariant_ids: set[str],
    section_split_ids: set[str],
) -> tuple[dict[str, str], dict[str, str]]:
    sources = sections(root / "scoring/answer-key-sources.md")
    work = sections(root / "scoring/answer-key-work-registry.md")
    assert list(sources) == expected_ids, (root, "Sources IDs", list(sources))
    assert list(work) == expected_ids, (root, "Work Registry IDs", list(work))
    assert full_invariant_ids.isdisjoint(section_split_ids)
    assert full_invariant_ids | section_split_ids == set(expected_ids)
    for question_id in expected_ids:
        source_expected = verdict_text(sources[question_id])
        work_expected = verdict_text(work[question_id])
        require(sources[question_id], "**Incorrect if:**")
        require(work[question_id], "**Incorrect if:**")
        forbid(
            sources[question_id],
            "**Expected:",
            "**Evidence:",
            "**Grade boundary:",
            "CMT-",
        )
        forbid(
            work[question_id],
            "**Expected:",
            "**Evidence:",
            "**Grade boundary:",
            "CMT-",
        )
        if question_id in verdict_invariant_ids:
            assert source_expected == work_expected, (
                root,
                question_id,
                "unexpected arm difference",
            )
        if question_id in split_ids:
            assert source_expected != work_expected, (
                root,
                question_id,
                "missing arm difference",
            )
        if question_id in full_invariant_ids:
            assert sources[question_id].strip() == work[question_id].strip(), (
                root,
                question_id,
                "unchanged question sections must be identical",
            )
        if question_id in section_split_ids:
            assert sources[question_id].strip() != work[question_id].strip(), (
                root,
                question_id,
                "expected final-state section difference is missing",
            )
    return sources, work


def main() -> None:
    if not __debug__:
        raise SystemExit("error: every check here is an assert — do not run "
                         "this validator under -O")
    validate_question_registry()

    c1_ids = [f"Q{i:02d}" for i in range(1, 16)]
    c1_sources, c1_work = validate_corpus(
        ROOT / "corpora/corpus-1/ground-truth",
        c1_ids,
        set(c1_ids[:13]),
        {"Q14", "Q15"},
        {"Q06", "Q08", "Q10", "Q11", "Q13"},
        {"Q01", "Q02", "Q03", "Q04", "Q05", "Q07", "Q09", "Q12", "Q14", "Q15"},
    )
    require(c1_sources["Q14"], "No hard calendar deadline is established")
    require(c1_work["Q14"], "Hard no-ship", "2026-10-15")
    require(
        c1_sources["Q15"],
        "no numeric field timeout budget established",
    )
    require(c1_work["Q15"], "180ms", "5s", "30s")
    require(c1_work["Q15"], "simple timeout bump was declined")
    require(c1_sources["Q01"], "Fewer than three")
    require(c1_work["Q01"], "Fewer than three")
    require(c1_sources["Q07"], "Three or fewer")
    require(c1_work["Q07"], "Three or fewer")
    require(c1_work["Q02"], "Still above ~450MB", "800MB", "450MB")
    require(c1_sources["Q02"], "June 25 supersedes June 16")
    require(c1_work["Q02"], "June 25 supersedes June 16")
    require(c1_sources["Q03"], "Buffers remained retained after each chunk")
    require(c1_work["Q03"], "Buffers remained retained after each chunk")
    require(c1_work["Q04"], "2GB free disk", "10% buffer")
    require(c1_work["Q05"], "whole-bundle copyleft", "P0", "Engineering search alone")
    require(
        c1_sources["Q06"],
        "T005's listed assignee is Evan",
        "Evan owns the T005",
        "T029's listed assignee is Evan",
        "Alice owns T029",
        "T016's listed assignee is Diana",
        "Diana owns T016",
        "T030's listed assignee is Diana",
        "Charlie owns the T030",
    )
    require(
        c1_work["Q06"],
        "T005's listed assignee is Evan",
        "Evan owns the T005",
        "T029's listed assignee is Evan",
        "Alice owns T029",
        "T016's listed assignee is Diana",
        "Diana owns T016",
        "T030's listed assignee is Diana",
        "Charlie owns the T030",
    )
    require(
        c1_work["Q07"],
        "Legal sign-off",
        "approved split-escrow design",
        "nested Form XObject",
        "mixed external/internal",
    )
    require(c1_work["Q09"], "whole-bundle copyleft", "P0 Legal gate", "Engineering search alone")
    require(c1_sources["Q08"], "Alice is following up on certificate procurement")
    require(c1_work["Q08"], "Alice is following up on certificate procurement")
    require(c1_sources["Q11"], "T016 schema verification", "T030 parser search")
    require(c1_work["Q11"], "T016 schema verification", "T030 parser search")
    require(c1_sources["Q11"], "No ordering between T005 and T029 is established")
    require(c1_work["Q11"], "A required order between T005 and T029 asserted")
    forbid(c1_sources["Q11"], "no order between them")
    require(c1_sources["Q13"], "T008 OCR", "T014 manual-review", "T016 audit logging")
    require(c1_work["Q13"], "T008 OCR", "T014 manual-review", "T016 audit logging")
    require(c1_sources["Q14"], "T005 Docker/CVE", "T029 signing", "undated")
    forbid(c1_sources["Q02"], "800MB")
    forbid(c1_sources["Q03"], "4.7GB", "8GB")
    forbid(c1_sources["Q04"], "2GB production baseline")
    forbid(c1_sources["Q05"], "whole-bundle", "P0 gate")
    forbid(
        c1_sources["Q07"],
        "Form XObject",
        "Legal sign-off",
        "approved split escrow",
        "180ms",
        "30s",
    )
    forbid(c1_sources["Q09"], "whole-bundle", "P0 gate")
    forbid(c1_sources["Q14"], "2026-10-15")
    forbid(c1_sources["Q15"], "Singapore", "180ms", "30s")
    require(
        c1_work["Q12"],
        "approved split escrow",
        "T007 also waits on Legal sign-off",
        "T036 may require an internal Form XObject workaround",
    )
    forbid(c1_sources["Q12"], "split escrow approved", "mixed wait", "Form XObject")

    c2_ids = [f"Q-{i:02d}" for i in range(1, 10)] + [
        f"A-{i:02d}" for i in range(1, 7)
    ]
    c2_invariant = set(c2_ids) - {"Q-04", "A-01", "A-03"}
    c2_sources, c2_work = validate_corpus(
        ROOT / "corpora/corpus-2/ground-truth",
        c2_ids,
        c2_invariant,
        {"Q-04", "A-01", "A-03"},
        c2_invariant,
        {"Q-04", "A-01", "A-03"},
    )
    require(c2_work["Q-04"], "MultipartForm.RemoveAll()", "publication pending")
    require(
        c2_sources["Q-04"],
        "pursued/leading approach",
        "No cleanup is published",
        "not in Sources",
    )
    forbid(
        c2_sources["Q-04"],
        "SIG assigned ownership",
        "No cleanup method selected",
        "Open and unresolved",
        "confirmed as final",
    )
    forbid(
        c2_work["Q-04"],
        "SIG assigned ownership",
        "Conflict resolution/tests",
        "Final commits unpushed",
    )
    require(
        c2_sources["A-01"],
        "is being pursued",
        "pursued, proposed, or agreed",
        "not in Sources",
    )
    require(c2_work["A-01"], "MultipartForm.RemoveAll()", "publication pending")
    forbid(c2_sources["A-01"], "No adopted method", "asserted as confirmed or final")
    require(
        c2_sources["A-03"],
        "v1.39.0 confirmed",
        "closed (completed)",
        "not in Sources",
    )
    require(c2_work["A-03"], "deferred/not done", "v1.39.0")
    require(c2_sources["A-03"], "**Partial if:**", "Only the confirmed release")
    require(c2_work["A-03"], "**Partial if:**", "Only the confirmed release")
    forbid(c2_sources["A-03"], "closed/completed", "Either identify")
    forbid(c2_sources["A-03"], "deferred", "CMT")
    forbid(
        c2_sources["A-03"],
        "closure treated as proof",
        "artifact invented",
    )

    print("arm-specific answer keys: coverage and intentional splits verified")


if __name__ == "__main__":
    main()
