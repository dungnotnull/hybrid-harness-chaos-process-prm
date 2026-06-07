#!/usr/bin/env python3
"""Pre-commit hook: Validate all SKILL.md files before allowing commit.

Install: Add to .pre-commit-config.yaml or copy to .git/hooks/pre-commit
Usage: python scripts/pre-commit-validate.py [--project-root .] [--quiet]
"""
import os
import sys

# Ensure project root is on path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tools.validate_skills import validate_all_skills, format_results


def main():
    project_root_arg = "."
    quiet = False
    json_output = False

    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == "--project-root" and i + 1 < len(args):
            project_root_arg = args[i + 1]
        elif arg == "--quiet":
            quiet = True
        elif arg == "--json":
            json_output = True

    result = validate_all_skills(project_root_arg)
    output = format_results(result, use_json=json_output, quiet=quiet)
    print(output)

    if result.failed > 0:
        print(f"\nPre-commit hook FAILED: {result.failed} skill(s) have errors.")
        print("Fix the errors above and re-commit.")
        sys.exit(1)
    elif result.warnings > 0 and not quiet:
        print(f"\nPre-commit hook PASSED with {result.warnings} warning(s).")

    sys.exit(0)


if __name__ == "__main__":
    main()
