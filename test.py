#!/usr/bin/env python3
"""
Automated tester for solve.py or C++ solution with colored output, exit code, and test filtering.
Supports:
- Python scripts (.py)
- C++ files (.cpp) (auto-compiles)
- Filtering by test ID or tags
"""

import subprocess
import sys
from pathlib import Path
import yaml
from difflib import unified_diff
import argparse

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Configuration
SOLVE_SCRIPT = "solve.py"  # Change to your Python or C++ solution
METADATA_FILE = "tests.yaml"
TEST_DIR = Path("./tests")  # Contains inputs/ and tests.yaml

def normalize_output(text: str) -> str:
    """Strip trailing spaces and ensure final newline"""
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines).strip() + "\n"

def color_text(text: str, color: str) -> str:
    return f"{color}{text}{RESET}"

def parse_args():
    parser = argparse.ArgumentParser(description="Run tests from tests.yaml")
    parser.add_argument("--include", type=str, help="Comma-separated test IDs to INCLUDE (e.g. test1,test3)")
    parser.add_argument("--exclude", type=str, help="Comma-separated test IDs to EXCLUDE (e.g. test2,test5)")
    parser.add_argument("--include-tags", type=str, help="Comma-separated tags to INCLUDE")
    parser.add_argument("--exclude-tags", type=str, help="Comma-separated tags to EXCLUDE")
    return parser.parse_args()

def extract_tags(description: str):
    """
    Extracts tags from description like:
    'Types=random,near_power | T=5'
    Returns a set of tags.
    """
    if not description.startswith("Types="):
        return set()
    try:
        part = description.split("|")[0]  # "Types=..."
        tags_str = part.split("=")[1]
        return set(tag.strip() for tag in tags_str.split(",") if tag.strip())
    except:
        return set()

def prepare_solution():
    if SOLVE_SCRIPT.endswith(".py"):
        return [sys.executable, SOLVE_SCRIPT]

    elif SOLVE_SCRIPT.endswith(".cpp"):
        # Place the binary inside the TEST_DIR
        binary = TEST_DIR / "solution_bin"
        print(f"Compiling C++ solution to {binary} ...")
        compile_result = subprocess.run(
            ["g++", "-O2", "-std=c++17", SOLVE_SCRIPT, "-o", str(binary)],
            capture_output=True,
            text=True
        )
        if compile_result.returncode != 0:
            print(color_text("Compilation failed:", RED))
            print(compile_result.stderr)
            sys.exit(1)

        if not binary.is_file():
            print(color_text(f"Compilation succeeded but binary '{binary}' not found!", RED))
            sys.exit(1)

        print(color_text("Compilation successful ✓", GREEN))
        return [str(binary)]

    else:
        print(color_text("Unsupported file type", RED))
        sys.exit(1)

def run_test(test_info, cmd):
    test_id = test_info["id"]
    input_file = test_info["filename"]
    expected = test_info["expected_output"].strip()

    input_path = TEST_DIR / input_file
    if not input_path.is_file():
        print(f"[{test_id}] {color_text('SKIPPED', RED)} - input file not found: {input_file}")
        return False

    print(f"[{test_id}] Running: {test_info.get('description', '')}")

    try:
        result = subprocess.run(
            cmd,
            stdin=open(input_path, "r", encoding="utf-8"),
            capture_output=True,
            text=True,
            timeout=15,
            check=False
        )

        actual_output = result.stdout
        norm_actual = normalize_output(actual_output)
        norm_expected = normalize_output(expected)

        if norm_actual == norm_expected:
            print(f"[{test_id}] {color_text('PASSED', GREEN)}")
            return True
        else:
            print(f"[{test_id}] {color_text('FAILED', RED)}")
            print("─" * 70)
            print("Expected:")
            print(expected)
            print("─" * 70)
            print("Got:")
            print(actual_output.rstrip())
            print("─" * 70)

            diff = unified_diff(
                expected.splitlines(keepends=True),
                actual_output.splitlines(keepends=True),
                fromfile="expected",
                tofile="actual"
            )
            print("Diff:")
            print("".join(diff).rstrip())
            print("─" * 70)

            if result.stderr:
                print(f"{color_text('stderr not empty:', RED)}")
                print(result.stderr)

            return False

    except subprocess.TimeoutExpired:
        print(f"[{test_id}] {color_text('TIMEOUT', RED)} after 15 seconds")
        return False
    except Exception as e:
        print(f"[{test_id}] {color_text('ERROR', RED)}: {e}")
        return False

def main():
    args = parse_args()

    include_ids = set(args.include.split(",")) if args.include else None
    exclude_ids = set(args.exclude.split(",")) if args.exclude else set()
    include_tags = set(args.include_tags.split(",")) if args.include_tags else None
    exclude_tags = set(args.exclude_tags.split(",")) if args.exclude_tags else set()

    metadata_path = TEST_DIR / METADATA_FILE
    if not metadata_path.is_file():
        print(f"{color_text('Error:', RED)} Metadata file not found: {METADATA_FILE}")
        sys.exit(1)

    with open(metadata_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    tests = data.get("tests", [])
    if not tests:
        print(f"{color_text('No tests found in metadata file.', RED)}")
        sys.exit(1)

    print(f"Found {len(tests)} tests in {METADATA_FILE}")
    if include_ids:
        print(f"Including only test IDs: {', '.join(include_ids)}")
    if exclude_ids:
        print(f"Excluding test IDs: {', '.join(exclude_ids)}")
    if include_tags:
        print(f"Including tags: {', '.join(include_tags)}")
    if exclude_tags:
        print(f"Excluding tags: {', '.join(exclude_tags)}")
    print("")

    # Prepare solution command
    cmd = prepare_solution()

    passed = 0
    failed = 0

    for test_info in tests:
        test_id = test_info["id"]
        description = test_info.get("description", "")
        tags = extract_tags(description)

        # ID filters
        if include_ids and test_id not in include_ids:
            continue
        if test_id in exclude_ids:
            continue

        # TAG filters
        if include_tags and not (tags & include_tags):
            continue
        if tags & exclude_tags:
            continue

        if run_test(test_info, cmd):
            passed += 1
        else:
            failed += 1

    print("\n" + "═" * 70)
    summary = f"Summary: {passed} passed, {failed} failed, {len(tests)} total (filtered)"
    if failed == 0:
        print(f"{color_text(summary, GREEN)}")
        print(f"{color_text('ALL TESTS PASSED ✓', GREEN)}")
        sys.exit(0)
    else:
        print(f"{color_text(summary, RED)}")
        print(f"{color_text(f'{failed} test(s) failed ✗', RED)}")
        sys.exit(1)

if __name__ == "__main__":
    main()