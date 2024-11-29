"""This hook verifies that the commit message contains a reference to a Linear issue as well as a conventional commit type.
The commit message needs to conform to <linear issue>/<conventional commit type>[!]: <title>. e.g.
    T-5482/feat: Amazing new commit-msg hook
See https://www.conventionalcommits.org for examples of conventional commit types.
"""

import sys
import re

from git_hooks import common

ERRC = "\033[91m"
ENDC = "\033[0m"

success = (
    "Commit message contains reference to Linear issue and conventional commit type."
)
error = f"""{ERRC}
Commit message needs to be prefixed with a reference to a Linear issue
and a conventional commit type, e.g.

    T-5482/feat: Amazing new feature

See https://github.com/two-inc/git-hooks/blob/24.11.29/README.md for more info.
{ENDC}
{common.commit_types_doc}
"""


def get_exit_code(commit_msg) -> int:
    return 0 if re.match(common.valid_commit_regex, commit_msg) else 1


def main():
    commit_msg = open(sys.argv[1], "r").read()
    exit_code = get_exit_code(commit_msg)
    print(success if exit_code == 0 else error, file=sys.stderr)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
