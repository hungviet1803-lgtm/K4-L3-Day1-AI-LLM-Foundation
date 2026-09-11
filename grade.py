#!/usr/bin/env python3
"""
Chấm điểm tự động — K4 Ngày 1: Khám Phá LLM API

Chạy:
    python grade.py

Tổng điểm: 100
    - Part 1: 15 điểm
    - Part 2: 15 điểm
    - Part 3: 15 điểm
    - Part 4 Basic: 15 điểm
    - Part 4 Scenario: 15 điểm
    - Exercises: 25 điểm

Mục tiêu:
    >= 75/100
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


DAY_DIR = Path(__file__).resolve().parent

TEST_GROUPS = [
    (
        "CP1 — Part 1: API cơ bản",
        ["tests/test_part1.py"],
        15,
    ),
    (
        "CP2 — Part 2: System prompt & token",
        ["tests/test_part2.py"],
        15,
    ),
    (
        "CP3 — Part 3: Streaming & retry",
        ["tests/test_part3.py"],
        15,
    ),
    (
        "CP4 — Part 4: Mini-project cơ bản",
        ["tests/test_part4.py", "-k", "Basic"],
        15,
    ),
    (
        "Demo — Kịch bản hội thoại tự động",
        ["tests/test_part4.py", "-k", "Scenario"],
        15,
    ),
]

EXERCISES_POINTS = 25
TOTAL_QUESTIONS = 9
ANSWER_PLACEHOLDER = "> *Câu trả lời của bạn*"


class _Collector:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.total = 0

    def pytest_runtest_logreport(self, report):
        if report.when != "call":
            return

        self.total += 1

        if report.passed:
            self.passed += 1

        elif report.failed:
            self.failed += 1

        elif report.skipped:
            self.skipped += 1


def run_test_group(pytest_args: list[str]) -> tuple[int, int]:
    resolved_args = []

    for arg in pytest_args:
        if arg.startswith("tests/"):
            resolved_args.append(str(DAY_DIR / arg))
        else:
            resolved_args.append(arg)

    collector = _Collector()

    exit_code = pytest.main(
        resolved_args
        + [
            "-q",
            "--tb=no",
            "--no-header",
            "-p",
            "no:cacheprovider",
        ],
        plugins=[collector],
    )

    if collector.total == 0 and exit_code != 0:
        return 0, 1

    return collector.passed, collector.total


def _rel(path: Path | None) -> str:
    if path is None:
        return "(không tìm thấy)"

    try:
        return str(path.relative_to(DAY_DIR))
    except ValueError:
        return str(path)


def resolve_targets() -> tuple[Path | None, Path | None]:
    solution_dir = DAY_DIR / "solution"

    code_candidates = [
        solution_dir / "solution.py",
        DAY_DIR / "template.py",
    ]

    exercise_candidates = [
        solution_dir / "exercises.md",
        DAY_DIR / "exercises.md",
    ]

    code_file = next(
        (path for path in code_candidates if path.exists()),
        None,
    )

    exercises_file = next(
        (path for path in exercise_candidates if path.exists()),
        None,
    )

    return code_file, exercises_file


def grade_exercises() -> tuple[int, Path | None]:
    _, candidate = resolve_targets()

    if candidate is None:
        return 0, None

    try:
        content = candidate.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return 0, candidate

    lines = content.splitlines()

    unanswered = sum(
        1
        for line in lines
        if line.strip() == ANSWER_PLACEHOLDER
    )

    answered = TOTAL_QUESTIONS - unanswered

    answered = max(0, min(answered, TOTAL_QUESTIONS))

    return answered, candidate


def calculate_score(
    passed: int,
    total: int,
    max_points: float,
) -> float:
    if total <= 0:
        return 0.0

    passed = max(0, min(passed, total))

    return round(
        max_points * passed / total,
        1,
    )


def print_progress(score: float):
    print()

    if score >= 75:
        print(">>> MỤC TIÊU: ĐẠT ≥ 75/100")
        print(">>> TRẠNG THÁI: ĐẠT")
    else:
        remaining = round(75 - score, 1)

        print(">>> MỤC TIÊU: ĐẠT ≥ 75/100")
        print(">>> TRẠNG THÁI: CHƯA ĐẠT")
        print(f">>> Cần thêm: {remaining} điểm")


def main() -> int:
    print("=" * 75)
    print("CHẤM ĐIỂM TỰ ĐỘNG — K4 Ngày 1: KHÁM PHÁ LLM API")
    print("=" * 75)

    code_file, exercises_file = resolve_targets()

    print(f"Đang chấm code:       {_rel(code_file)}")
    print(f"Đang chấm exercises:  {_rel(exercises_file)}")

    if code_file is None:
        print()
        print("LỖI: Không tìm thấy file code để chấm.")
        print("Cần có:")
        print("  solution/solution.py")
        print("hoặc:")
        print("  template.py")
        return 1

    rows = []
    total_score = 0.0

    for name, args, max_points in TEST_GROUPS:
        print()
        print(f">>> {name}")

        passed, total = run_test_group(args)

        score = calculate_score(
            passed,
            total,
            max_points,
        )

        total_score += score

        rows.append(
            (
                name,
                f"{passed}/{total} test",
                score,
                max_points,
            )
        )

    answered, exercises_file = grade_exercises()

    exercise_score = round(
        EXERCISES_POINTS
        * answered
        / TOTAL_QUESTIONS,
        1,
    )

    total_score += exercise_score

    exercise_detail = (
        f"{answered}/{TOTAL_QUESTIONS} câu"
        if exercises_file
        else "không tìm thấy exercises.md"
    )

    rows.append(
        (
            "Exercises — câu hỏi phản ánh",
            exercise_detail,
            exercise_score,
            EXERCISES_POINTS,
        )
    )

    total_score = round(total_score, 1)

    print()
    print("=" * 75)
    print("BẢNG ĐIỂM")
    print("=" * 75)

    for name, detail, score, max_points in rows:
        print(
            f"{name:<42}"
            f"{detail:<18}"
            f"{score:>5.1f}/{max_points}"
        )

    print("-" * 75)

    print(
        f"{'TỔNG':<42}"
        f"{'':<18}"
        f"{total_score:>5.1f}/100"
    )

    print("=" * 75)

    print_progress(total_score)

    print()
    print("Phân tích:")

    if total_score >= 75:
        print("  ✓ Bạn đã đạt mục tiêu tối thiểu 75/100.")
    else:
        print(
            f"  ✗ Bạn chưa đạt mục tiêu. "
            f"Còn thiếu {round(75 - total_score, 1)} điểm."
        )

    print()
    print(
        "Lưu ý: Exercises được tính theo số câu đã điền. "
        "Chất lượng câu trả lời có thể được giảng viên chấm lại."
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())