#!/usr/bin/env python3
import re
import sys
import subprocess
from common import commented_commit_types_doc
from common import commit_types

commit_msg_filepath = sys.argv[1]

try:
    branch = (
        subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"])
        .strip()
        .decode()
    )
except subprocess.CalledProcessError:
    sys.exit(0)

branch_regex = "^(.*)\/(\w+-\d+)-(.*)"
issue_regex = "^(\w+-\d+)$"
commit_msg_title_regex = f"^({commit_types}!?): (.*)"

if branch_regex_match := re.match(branch_regex, branch):
    issue = branch_regex_match.group(2).upper()
    commit_type = "fix"  # default commit message type
    commit_msg = branch_regex_match.group(3).replace("-", " ").capitalize()
    with open(commit_msg_filepath, "r+") as fh:
        commit_msg_lines = fh.read().splitlines()
        commit_msg_body = "\n".join(commit_msg_lines[1:])
        commit_msg_title = commit_msg_lines[0]
        if (
            commit_msg_title
            and len(commit_msg_title_parts := commit_msg_title.split("/", maxsplit=1))
            == 2
        ):
            commit_msg_issue, commit_msg = commit_msg_title_parts
            if re.match(issue_regex, commit_msg_issue):
                issue = commit_msg_issue
            if commit_msg_match := re.match(commit_msg_title_regex, commit_msg):
                commit_type = commit_msg_match.group(1)
                commit_msg = commit_msg_match.group(2)

        message = f"""{issue}/{commit_type}: {commit_msg}
{commit_msg_body}


{commented_commit_types_doc}
"""
        fh.seek(0, 0)
        fh.write(message)
