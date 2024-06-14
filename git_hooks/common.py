commit_type_doc = """
 Valid conventional commit types are:

\tbuild    updating build configuration, development tools
\tchore    updating grunt tasks etc. @
\tci       updating deployment configuration
\tdocs     changes to documentation
\tfix      patching a bug in the codebase
\tfeat     adding a new feature to the code
\tfeat!    adding a new feature that introduces breaking API change
\thotfix   updating a bug in production
\tperf     updating code to make performance enhancements
\trefactor updating code without any functional change
\trevert   updating code to earlier change
\tstyle    formatting changes, missing semicolons, etc.
\ttest     for adding missing tests, refactoring tests; no production code change"""

commented_commit_type_doc = commit_type_doc.replace("\n", "\n#")

commit_type_regex = (
    "(?:build|chore|ci|docs|feat|fix|hotfix|perf|refactor|revert|style|test)"
)
linear_ref = "(?:t|T|kna|KNA|cet|CET|nor|NOR|l2|L2)-[0-9]{1,5}"
valid_commit_regex = (
    f"^{linear_ref}/{commit_type_regex}!?: |Merge .+|Revert .+|Bump version .+"
)
branch_regex = f"^(.*)/({linear_ref})[-|_](.*)"
commit_msg_title_regex = f"^({commit_type_regex}!?):? (.*)"
commit_msg_issue_regex = f"^({linear_ref})/(.*)"
issue_regex = f"^{linear_ref}$"
prefix_regex = f"^({commit_type_regex})"
