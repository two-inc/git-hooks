commit_types: dict[str, str] = {
    "build": "updating build configuration, development tools",
    "chore": "updating grunt tasks etc.",
    "ci": "updating deployment configuration",
    "docs": "changes to documentation",
    "fix": "patching a bug in the codebase",
    "feat": "adding a new feature to the code",
    "feat!": "adding a new feature that introduces breaking API change",
    "hotfix": "updating a bug in production",
    "perf": "updating code to make performance enhancements",
    "refactor": "updating code without any functional change",
    "revert": "updating code to earlier change",
    "style": "formatting changes, missing semicolons, etc.",
    "test": "for adding missing tests, refactoring tests; no production code change",
}

commit_types_title: str = "Valid conventional commit types are:"
commit_types_block: str = "\t" + "\n\t".join(
    [f"{k.ljust(10)}{v}" for k, v in commit_types.items()]
)
commit_types_doc: str = f"""
{commit_types_title}

{commit_types_block}
"""
commit_types_doc_commented: str = "\n".join(
    [
        f"# {commit_types_title}",
        "#" + commit_types_block.replace("\n", "\n#"),
    ]
)

commit_type_regex: str = f"(?:{'|'.join(commit_types.keys())})"
teams: list[str] = [
    "T",
    "L2",
    "DAE"
]
linear_ref: str = (
    "(?:"
    f"{'|'.join(t for t in teams)}"
    "|"
    r"[A-Z]{3}"
    "|"
    f"{'|'.join(t.lower() for t in teams)}"
    "|"
    r"[a-z]{3}"
    ")-[0-9]{1,5}"
)
valid_commit_regex: str = (
    f"^{linear_ref}/{commit_type_regex}!?: |Merge .+|Revert .+|Bump version .+"
)
partial_branch_regex: str = f"({linear_ref})[-|_](.*)"
branch_regex: str = f"^(.*)/{partial_branch_regex}"
commit_msg_title_regex: str = f"^({commit_type_regex}!?):? (.*)"
commit_msg_issue_regex: str = f"^({linear_ref})/(.*)"
issue_regex: str = f"^{linear_ref}$"
prefix_regex: str = f"^({commit_type_regex})"
