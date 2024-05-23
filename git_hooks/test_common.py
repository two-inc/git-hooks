import re
import pytest
import common

@pytest.mark.parametrize("commit_type", [
    "feat:",
    "fix:",
    "hotfix:",
    "docs:",
    "style",
    "test:",
])
def test_commit_type_regex(commit_type: str):
    assert re.match(common.commit_type_regex, commit_type)


@pytest.mark.parametrize("issue", [
    "T-1234",
    "KNA-1234",
    "CET-1234",
    "NOR-1234",
    "L2-1234",
])
def test_linear_ref(issue: str):
    assert re.match(common.linear_ref, issue)


@pytest.mark.parametrize("commit", [
    "T-1234/feat: ",
    "T-1234/fix: ",
    "KNA-1234/hotfix: ",
    "CET-1234/docs: ",
    "NOR-1234/style: ",
    "L2-1234/test: ",
])
def test_valid_commit_regex(commit: str):
    assert re.match(common.valid_commit_regex, commit)


@pytest.mark.parametrize("branch", [
    "hotfix/T-1234-fix-something",
    "hotfix/brtknr/KNA-1234-add-something",
    "feat/CET-1234-fix-something",
    "bharat/L2-1234-add-something",
    "brtkwr/cet-281-fix-company-search-gb-bucket-permission"
])
def test_branch_regex(branch: str):
    result = re.match(common.branch_regex, branch)
    assert result
    assert len(result.groups()) == 3


@pytest.mark.parametrize("commit_msg", [
    "feat: add something",
    "fix: fix something",
    "hotfix: fix something",
    "docs: add something",
    "style add something",
    "test: add something",
])
def test_commit_msg_title_regex(commit_msg: str):
    result = re.match(common.commit_msg_title_regex, commit_msg)
    assert result
    assert len(result.groups()) == 2


@pytest.mark.parametrize("commit_msg", [
    "T-1234/feat: add something",
    "KNA-1234/fix: fix something",
    "CET-1234/hotfix: fix something",
    "NOR-1234/docs: add something",
    "L2-1234/style add something",
    "T-1234/test: add something",
])
def test_commit_msg_issue_regex(commit_msg: str):
    result = re.match(common.commit_msg_issue_regex, commit_msg)
    assert result
    assert len(result.groups()) == 2


@pytest.mark.parametrize("issue", [
    "T-1234",
    "KNA-1234",
    "CET-1234",
    "NOR-1234",
    "L2-1234",
])
def test_issue_regex(issue: str):
    assert re.match(common.issue_regex, issue)


@pytest.mark.parametrize("prefix", [
    "feat",
    "fix",
    "hotfix",
    "docs",
    "style",
    "test",
])
def test_prefix_regex(prefix: str):
    assert re.match(common.prefix_regex, prefix)
