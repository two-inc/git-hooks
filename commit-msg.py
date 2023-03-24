#!/usr/bin/env python3
""" This hook verifies that the commit message contains a reference to a Linear issue
    as well as a conventional commit type at the start
    The commit message needs to conform to
    <Linear issue>/<conventional commit type>[!]: <description>
    e.g. T-5482/feat: Amazing new commit-msg hook
    See https://www.conventionalcommits.org for details on conventional commits
"""

import sys
import re
from common import commit_types_doc
from common import valid_commit_regex

commit_msg = open(sys.argv[1], "r").read()
error = f"""
Commit message needs to be prefixed with a reference to a Linear issue
and a conventional commit type, e.g. 'T-5482/feat: Amazing new feature'.

See https://github.com/two-inc/git-hooks/blob/23.03.23-6/README.md for more info."
"""

if match := re.match(valid_commit_regex, commit_msg):
    print(
        "Commit message contains reference to Linear issue and conventional commit type."
    )
else:
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    print(f"{FAIL}{error}{ENDC}{commit_types_doc}")
    sys.exit(1)
