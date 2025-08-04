from unittest import mock
import pytest
import subprocess
from prepare_commit_msg import extract_branch_data
from prepare_commit_msg import extract_commit_msg_title_data
from prepare_commit_msg import get_branch_name
from prepare_commit_msg import retrieve_linear_issue
from prepare_commit_msg import prepare_commit_msg
from prepare_commit_msg import prefix_to_commit_type
from prepare_commit_msg import main

from prepare_commit_msg import EDITOR_TEXT


@mock.patch("prepare_commit_msg.linear_client")
@mock.patch("prepare_commit_msg.get_branch_name")
@mock.patch("sys.argv", ["prepare_commit_msg.py", "COMMIT_MSG"])
@mock.patch("prepare_commit_msg.LINEAR_API_KEY", "API_KEY")
@pytest.mark.parametrize(
    "read_data, branch, linear_called",
    [
        ("T-5482/feat: Amazing new feature", "t-1234-issue-title", False),
        ("feat: Amazing new feature", "issue-title", False),
        (f"\n{EDITOR_TEXT}", "test/t-1234-issue-title", True),
    ],
)
@pytest.mark.parametrize("exception", [None, Exception])
def test_main(
    mock_get_branch_name,
    mock_linear_client,
    read_data,
    branch,
    linear_called,
    exception,
):
    mock_get_branch_name.return_value = branch
    mock_client = mock.Mock()
    mock_client.execute.return_value = {
        "issue": {"title": "Title", "description": "Description"}
    }
    mock_client.execute.side_effect = exception
    mock_linear_client.return_value = mock_client
    with mock.patch("builtins.open", mock.mock_open(read_data=read_data)):
        # check exit code
        main()
    mock_get_branch_name.assert_called_once()
    if linear_called:
        mock_client.execute.assert_called_once()
    else:
        mock_client.execute.assert_not_called()


@pytest.mark.parametrize("expected", ["feat/branch", "branch", None])
def test_get_branch_name(expected):
    with mock.patch(
        "subprocess.check_output",
        return_value=expected.encode() if expected else expected,
        side_effect=None if expected else subprocess.CalledProcessError(1, "git"),
    ):
        assert get_branch_name() == expected


@mock.patch("prepare_commit_msg.linear_client")
def test_retrieve_linear_issue(mock_linear_client):
    mock_client = mock.Mock()
    mock_linear_client.return_value = mock_client
    mock_client.execute.return_value = {
        "issue": {"title": "Title", "description": "Description"}
    }
    assert retrieve_linear_issue("T-5482") == {
        "title": "Title",
        "description": "Description\n\n",
    }


@pytest.mark.parametrize(
    "branch, expected",
    [
        (
            "feat/cet-123-branch-title",
            {
                "issue": "CET-123",
                "commit_type": "feat",
                "commit_msg_title": "Branch title",
            },
        ),
        (
            "cet-123-branch-title",
            {
                "issue": "CET-123",
                "commit_type": "",
                "commit_msg_title": "Branch title",
            },
        ),
        (
            "branch-title",
            {
                "issue": "",
                "commit_type": "",
                "commit_msg_title": "Branch title",
            },
        ),
        (
            "dae-75-design-spec-for-configurable-oidc-provider-for-merchants",
            {
                "issue": "DAE-75",
                "commit_type": "",
                "commit_msg_title": "Design spec for configurable oidc provider for merchants",
            },
        ),
        (
            "feat/dae-75-design-spec-for-configurable-oidc-provider-for-merchants",
            {
                "issue": "DAE-75",
                "commit_type": "feat",
                "commit_msg_title": "Design spec for configurable oidc provider for merchants",
            },
        ),
        (
            "fix/abc-123-very-long-branch-name-with-many-hyphens-and-words",
            {
                "issue": "ABC-123",
                "commit_type": "fix",
                "commit_msg_title": "Very long branch name with many hyphens and words",
            },
        ),
        (
            "hotfix/xyz-456-update-critical-security-vulnerability-in-auth-module",
            {
                "issue": "XYZ-456",
                "commit_type": "hotfix",
                "commit_msg_title": "Update critical security vulnerability in auth module",
            },
        ),
    ],
)
def test_extract_branch_data(branch, expected):
    assert extract_branch_data(branch) == expected


@pytest.mark.parametrize(
    "commit_msg_title, expected",
    [
        (
            "cet-123/feat: commit title",
            {
                "issue": "CET-123",
                "commit_type": "feat",
                "commit_msg_title": "commit title",
            },
        ),
        (
            "CET-123/Commit title",
            {
                "issue": "CET-123",
                "commit_type": "",
                "commit_msg_title": "Commit title",
            },
        ),
        (
            "feat: Commit title",
            {
                "issue": "",
                "commit_type": "feat",
                "commit_msg_title": "Commit title",
            },
        ),
        (
            "Commit title",
            {
                "issue": "",
                "commit_type": "",
                "commit_msg_title": "Commit title",
            },
        ),
    ],
)
def test_extract_commit_msg_title_data(commit_msg_title, expected):
    assert extract_commit_msg_title_data(commit_msg_title) == expected


@mock.patch("prepare_commit_msg.LINEAR_API_KEY", None)
@pytest.mark.parametrize(
    "raw_commit_msg, branch, expected_commit_msg",
    [
        (
            "",
            "dae-75-design-spec-for-configurable-oidc-provider-for-merchants",
            "DAE-75/feat: Design spec for configurable oidc provider for merchants",
        ),
        (
            "",
            "feat/dae-75-design-spec-for-configurable-oidc-provider-for-merchants",
            "DAE-75/feat: Design spec for configurable oidc provider for merchants",
        ),
        (
            "",
            "fix/abc-123-very-long-branch-name-with-many-hyphens-and-words",
            "ABC-123/fix: Very long branch name with many hyphens and words",
        ),
        (
            "",
            "branch-without-issue",
            "feat: Branch without issue",
        ),
    ],
)
def test_prepare_commit_msg_with_default_commit_type(raw_commit_msg, branch, expected_commit_msg):
    result = prepare_commit_msg(raw_commit_msg, branch)
    assert result == expected_commit_msg


@mock.patch("prepare_commit_msg.LINEAR_API_KEY", None)
@mock.patch("prepare_commit_msg.DEFAULT_COMMIT_TYPE", "fix")
@pytest.mark.parametrize(
    "raw_commit_msg, branch, expected_commit_msg",
    [
        (
            "",
            "dae-75-design-spec-for-configurable-oidc-provider-for-merchants",
            "DAE-75/fix: Design spec for configurable oidc provider for merchants",
        ),
        (
            "",
            "abc-123-branch-without-prefix",
            "ABC-123/fix: Branch without prefix",
        ),
        (
            "",
            "branch-without-issue",
            "fix: Branch without issue",
        ),
    ],
)
def test_prepare_commit_msg_with_custom_default_commit_type(raw_commit_msg, branch, expected_commit_msg):
    result = prepare_commit_msg(raw_commit_msg, branch)
    assert result == expected_commit_msg


@mock.patch("prepare_commit_msg.DEFAULT_COMMIT_TYPE", "feat")
@pytest.mark.parametrize(
    "prefix, expected",
    [
        ("feat", "feat"),
        ("fix", "fix"),
        ("chore", "chore"),
        ("unknown", "feat"),  # Should fall back to DEFAULT_COMMIT_TYPE
        ("invalid", "feat"),  # Should fall back to DEFAULT_COMMIT_TYPE
    ],
)
def test_prefix_to_commit_type_with_default_feat(prefix, expected):
    result = prefix_to_commit_type(prefix)
    assert result == expected


@mock.patch("prepare_commit_msg.DEFAULT_COMMIT_TYPE", "chore")
@pytest.mark.parametrize(
    "prefix, expected",
    [
        ("feat", "feat"),
        ("fix", "fix"),
        ("chore", "chore"),
        ("unknown", "chore"),  # Should fall back to DEFAULT_COMMIT_TYPE
        ("invalid", "chore"),  # Should fall back to DEFAULT_COMMIT_TYPE
    ],
)
def test_prefix_to_commit_type_with_default_chore(prefix, expected):
    result = prefix_to_commit_type(prefix)
    assert result == expected
