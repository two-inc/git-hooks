#!/usr/bin/env python3
import re
import sys
import subprocess
from common import commented_commit_type_doc
from common import commit_type_regex
from common import linear_ref
from common import valid_commit_regex

branch_regex = f"^(.*)\/({linear_ref})[-|_](.*)"
commit_msg_title_regex = f"^({commit_type_regex}!?):? (.*)"
commit_msg_issue_regex = f"^({linear_ref})\/(.*)"
issue_regex = f"^{linear_ref}$"
prefix_regex = f"^({commit_type_regex})"
editor_text = "# Please enter the commit message for your changes."

# Convert branch name to commit message
def branch_to_commit_msg(branch):
    return branch.replace("-", " ").replace("_", " ").capitalize() + "\n"

# Check prefix for hints like hotfix/feat/etc:
def prefix_to_commit_type(prefix):
    if prefix_match := re.match(prefix_regex, prefix):
        return prefix_match.group(1)

def get_branch_name():
    try:
        return (
            subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"])
            .strip()
            .decode()
        )
    except subprocess.CalledProcessError:
        # This can occur during a rebase, return ignore
        pass
    
if __name__ == "__main__":
    # Commit message filepath is always the first argument
    commit_msg_filepath = sys.argv[1]

    # If branch name cannot be determined, there is nothing else to do
    if not (branch := get_branch_name()):
        sys.exit(0)

    # Read raw commit message
    raw_commit_msg = open(commit_msg_filepath).read()

    # Commit message is already valid, nothing else to do
    if re.match(valid_commit_regex, raw_commit_msg):
        sys.exit(0)

    # Default values
    issue = "T-"
    commit_type = "fix"
    
    # If the branch has hints about linear reference, extract those
    if branch_regex_match := re.match(branch_regex, branch):
        prefix = branch_regex_match.group(1).lower()
        commit_type = prefix_to_commit_type(prefix) or commit_type
        issue = branch_regex_match.group(2).upper()
        commit_msg = branch_to_commit_msg(branch_regex_match.group(3))
    else:
        commit_msg = branch_to_commit_msg(branch)
    
    commit_msg_lines = raw_commit_msg.splitlines()
    commit_msg_title = commit_msg_lines[0]

    # Only append to commit message body 
    commit_msg_body = ""
    if editor_text in raw_commit_msg:
        commit_msg_body = "\n".join(commit_msg_lines[1:] + [commented_commit_type_doc])
    
    # If the commit message has linear ref, extract it from the commit message title
    if commit_msg_match := re.match(commit_msg_issue_regex, commit_msg_title):
        issue = commit_msg_match.group(1).capitalize()
        commit_msg_title = commit_msg_match.group(2)
    # If the commit message only has conventional commit tag but no linear ref, use those
    if commit_msg_match := re.match(commit_msg_title_regex, commit_msg_title):
        commit_type = commit_msg_match.group(1)
        commit_msg = commit_msg_match.group(2).capitalize()
    
    # Write to commit message
    message = f"{commit_msg}\n{commit_msg_body}"
    message = f"{issue}/{commit_type}: {message}"
    with open(commit_msg_filepath, "w+") as fh:
        fh.seek(0, 0)
        fh.write(message)
