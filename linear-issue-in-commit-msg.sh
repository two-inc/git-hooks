#!/bin/sh
#
# This hook verifies that the commit message contains a reference to a Linear issue

RED=$(tput setaf 1)
NORMAL=$(tput sgr0)
# check for Linear issue number anywhere in the commit message
regex="(T|t)-[0-9]{4}"
# check for Linear issue number at the start of the commit message
# regex="^(T|t)-[0-9]{4}"
# check commit message conforms to <Linear issue reference>/<type>[!]: <description>
# e.g. T-1234/feat: add PIS to email template
# regex="^(T|t)-[0-9]{4}\/(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)!?:[[:space:]]"
msg=$(cat $1) # The commit message

# If the commit message does not match the regex
if ! [[ "$msg" =~ $regex ]]; then
    echo "$RED Commit message is missing reference to Linear issue, e.g. t-5482 $NORMAL"
    exit 1
else
    echo "Linear issue reference present in commit message"
fi

exit 0
