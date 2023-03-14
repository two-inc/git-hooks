commit_types_doc = """
Valid conventional commit types are:

    fix      patching a bug in the codebase
    feat     adding a new feature to the code
    feat!    adding a new feature that introduces breaking API change
    chore    updating grunt tasks etc. @
    build    updating build configuration, development tools
    ci       updating deployment configuration
    refactor updating code without any functional change
    perf     updating code to make performance enhancements
    revert   updating code to earlier change
    style    formatting changes, missing semicolons, etc.
    test     for adding missing tests, refactoring tests; no production code change
    docs     changes to documentation
"""

commented_commit_types_doc = commit_types_doc.replace("\n", "\n# ")

commit_types = "(?:build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)"
