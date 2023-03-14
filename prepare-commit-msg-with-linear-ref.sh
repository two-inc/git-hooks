#!/usr/bin/env python3
import sys, re
from subprocess import check_output

commit_msg_filepath = sys.argv[1]

branch = check_output(['git', 'symbolic-ref', '--short', 'HEAD']).strip().decode()
linear_ref = branch.split('/')[1].split('-')[1]
regex = '^(.*)\/(\w+-\d+)-(.*)'
if regex_match := re.match(regex, branch):
    prefix = regex_match.group(1)
    issue = regex_match.group(2).upper()
    message = regex_match.group(3).replace('-', ' ')
    print(dict(prefix=prefix, issue=issue))
    with open(commit_msg_filepath, 'r+') as fh:
        commit_msg = fh.read()
        fh.seek(0, 0)
        fh.write(f'{issue}/fix: {message}\n{commit_msg}')
elif branch not in {"master", "staging"}:
    print('Incorrect branch name')
    sys.exit(1)
