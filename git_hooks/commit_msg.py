""" This hook verifies that the commit message contains a reference to a Linear issue
    as well as a conventional commit type at the start
    The commit message needs to conform to
    <Linear issue>/<conventional commit type>[!]: <description>
    e.g. T-5482/feat: Amazing new commit-msg hook
    See https://www.conventionalcommits.org for details on conventional commits
"""

import sys
import re

from git_hooks import common

ERRC = "\033[91m"
ENDC = "\033[0m"

success = (
    "Commit message contains reference to Linear issue and conventional commit type."
)
error = """
Commit message needs to be prefixed with a reference to a Linear issue
and a conventional commit type, e.g.

    T-5482/feat: Amazing new feature

See https://github.com/two-inc/git-hooks/blob/24.06.17-6/README.md for more info.

"""


def main():
    commit_msg = open(sys.argv[1], "r").read()
    if match := re.match(common.valid_commit_regex, commit_msg):
        print(success)
    else:
        print(f"{ERRC}{error}{ENDC}{common.commit_type_doc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
