#!/bin/sh
# This hook verifies that the commit message contains a reference to a Linear issue

red=$(tput setaf 1)
normal=$(tput sgr0)
commit_msg=$(cat $1)
regex=$'(t|T)-[0-9]{4}'
error=$'Commit message needs to contain a reference to a Linear issue, e.g. t-5482\n'
error+=$'See https://github.com/two-inc/git-hooks/README.md for more info.'

if ! [[ "$commit_msg" =~ $regex ]]; then
    echo "$red$error$normal"
    exit 1
else
    echo "Commit message contains reference to Linear issue and conventional commit type."
fi

exit 0
