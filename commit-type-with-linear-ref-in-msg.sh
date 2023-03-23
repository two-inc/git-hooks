#!/usr/bin/env bash
# This hook verifies that the commit message contains a reference to a Linear issue
# as well as a conventional commit type at the start
# The commit message needs to conform to
# <Linear issue>/<conventional commit type>[!]: <description>
# e.g. t-5482/feat: amazing new commit-msg hook
# See https://www.conventionalcommits.org for details on conventional commits

red=$(tput setaf 1)
normal=$(tput sgr0)
commit_msg=$(cat $1)
linear_ref=$'(t|T)-[0-9]{3,4}'
conventional_commit_types=$'(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)'
# skip on "Merge branch...", "Merge pull...", etc.
skip_if=$'|Merge .+|Revert .+|Bump version .+'
regex="^$linear_ref\/$conventional_commit_types!?:[[:space:]]$skip_if"
error="Commit message needs to be prefixed with a reference to a Linear issue
and a conventional commit type, e.g. 't-5482/feat: amazing new feature'.\n
See https://github.com/two-inc/git-hooks/blob/23.03.23-3/README.md for more info."

if ! [[ "$commit_msg" =~ $regex ]]; then
    echo "$commit_msg"
    echo "$red$error$normal"
    exit 1
else
    echo "Commit message contains reference to Linear issue and conventional commit type."
fi

exit 0
