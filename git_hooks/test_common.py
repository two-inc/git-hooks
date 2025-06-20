import re
import pytest
import common


@pytest.mark.parametrize(
    "commit_type",
    [
        "feat:",
        "fix:",
        "hotfix:",
        "docs:",
        "style",
        "test:",
    ],
)
def test_commit_type_regex(commit_type: str):
    assert re.match(common.commit_type_regex, commit_type)


@pytest.mark.parametrize(
    "issue",
    [
        "T-1234",
        "L2-1234",
        "ABC-1234",
        "xyz-1234",
        "T-1",
        "L2-99999",
    ],
)
def test_linear_ref(issue: str):
    assert re.match(common.linear_ref, issue)


@pytest.mark.parametrize(
    "commit",
    [
        "T-1234/feat: ",
        "L2-1234/fix: ",
        "ABC-1234/hotfix: ",
        "xyz-1234/docs: ",
        "T-1/style: ",
        "L2-99999/test: ",
    ],
)
def test_valid_commit_regex(commit: str):
    assert re.match(common.valid_commit_regex, commit)


@pytest.mark.parametrize(
    "branch",
    [
        "hotfix/T-1234-fix-something",
        "feat/L2-1234-add-something",
        "fix/ABC-1234-fix-something",
        "bharat/xyz-1234-add-something",
        "brtkwr/abc-281-fix-company-search-gb-bucket-permission",
        "shelmig/xyz-13-update-credentials",
    ],
)
def test_branch_regex(branch: str):
    result = re.match(common.branch_regex, branch)
    assert result
    assert len(result.groups()) == 3


@pytest.mark.parametrize(
    "commit_msg",
    [
        "feat: add something",
        "fix: fix something",
        "hotfix: fix something",
        "docs: add something",
        "style add something",
        "test: add something",
    ],
)
def test_commit_msg_title_regex(commit_msg: str):
    result = re.match(common.commit_msg_title_regex, commit_msg)
    assert result
    assert len(result.groups()) == 2


@pytest.mark.parametrize(
    "commit_msg",
    [
        "T-1234/feat: add something",
        "L2-1234/fix: fix something",
        "ABC-1234/hotfix: fix something",
        "xyz-1234/docs: add something",
        "T-1/style add something",
        "L2-99999/test: add something",
    ],
)
def test_commit_msg_issue_regex(commit_msg: str):
    result = re.match(common.commit_msg_issue_regex, commit_msg)
    assert result
    assert len(result.groups()) == 2


@pytest.mark.parametrize(
    "issue",
    [
        "T-1234",
        "L2-1234",
        "ABC-1234",
        "xyz-1234",
        "T-1",
        "L2-99999",
    ],
)
def test_issue_regex(issue: str):
    assert re.match(common.issue_regex, issue)


@pytest.mark.parametrize(
    "prefix",
    [
        "build",
        "chore",
        "ci",
        "docs",
        "feat",
        "fix",
        "hotfix",
        "perf",
        "refactor",
        "revert",
        "style",
        "test",
    ],
)
def test_prefix_regex(prefix: str):
    assert re.match(common.prefix_regex, prefix)
