#!/usr/bin/env python3
"""
Code formatting and linting utility script.

Usage: python format_code.py [--check] [--lint-only]
"""
import subprocess
import sys
import argparse


def run_command(cmd, description):
    """Run a command and return its exit code."""
    print(f"\n🔍 {description}...")
    result = subprocess.run(cmd, shell=True, check=False)
    if result.returncode == 0:
        print(f"✅ {description} passed")
    else:
        print(f"❌ {description} failed")
    return result.returncode


def main():
    """Main function to parse arguments and run formatting/linting commands."""
    parser = argparse.ArgumentParser(description="Format and lint Python code")
    parser.add_argument(
        "--check", action="store_true", help="Check formatting without making changes"
    )
    parser.add_argument(
        "--lint-only", action="store_true", help="Only run linting, skip formatting"
    )

    args = parser.parse_args()

    exit_codes = []

    if not args.lint_only:
        # Black formatting
        black_cmd = "black --check --diff ." if args.check else "black ."
        description = "Checking code formatting" if args.check else "Formatting code"
        exit_codes.append(run_command(black_cmd, description))

    # Flake8 linting
    exit_codes.append(run_command("flake8 .", "Linting code"))

    # Summary
    total_errors = sum(1 for code in exit_codes if code != 0)
    if total_errors == 0:
        print("\n🎉 All checks passed!")
        sys.exit(0)
    else:
        print(f"\n💥 {total_errors} check(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
