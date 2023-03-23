#!/usr/bin/env python3
import re
import sys
import subprocess

commit_msg_filepath = sys.argv[1]

try:
    branch = subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"]).strip().decode()
except subprocess.CalledProcessError:
    sys.exit(0)
regex = "^(.*)\/(\w+-\d+)-(.*)"

if regex_match := re.match(regex, branch):
    prefix = regex_match.group(1)
    issue = regex_match.group(2).upper()
    message = regex_match.group(3).replace("-", " ").capitalize()
    with open(commit_msg_filepath, "r+") as fh:
        commit_msg = fh.read().capitalize()
        if not commit_msg.startswith(issue):
            commit_msg = f"{issue}/fix: {commit_msg or message}"
            fh.seek(0, 0)
            fh.write(commit_msg)
elif branch not in {"master", "staging"}:
    print("Incorrect branch name")
    sys.exit(1)
