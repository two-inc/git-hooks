commit_type_doc = """
Valid conventional commit types are:

    build    updating build configuration, development tools
    chore    updating grunt tasks etc. @
    ci       updating deployment configuration
    docs     changes to documentation
    fix      patching a bug in the codebase
    feat     adding a new feature to the code
    feat!    adding a new feature that introduces breaking API change
    hotfix   updating a bug in production
    perf     updating code to make performance enhancements
    refactor updating code without any functional change
    revert   updating code to earlier change
    style    formatting changes, missing semicolons, etc.
    test     for adding missing tests, refactoring tests; no production code change
"""

commented_commit_type_doc = commit_type_doc.replace("\n", "\n# ")

commit_type_regex = "(?:build|chore|ci|docs|feat|fix|hotfix|perf|refactor|revert|style|test)"
linear_ref = "[t|T]-[0-9]{3,5}"
valid_commit_regex = f"^{linear_ref}\/{commit_type_regex}!?: |Merge .+|Revert .+|Bump version .+"
