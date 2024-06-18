import pytest
from unittest import mock
from commit_msg import get_exit_code
from commit_msg import main


@pytest.mark.parametrize(
    "commit_msg, exit_code",
    [
        ("T-5482/feat: Amazing new feature", 0),
        ("feat: Amazing new feature", 1),
        ("X-5482/feat: Amazing new feature", 1),
        ("X-5482/Amazing new feature", 1),
    ],
)
def test_get_exit_code(commit_msg, exit_code):
    assert get_exit_code(commit_msg) == exit_code


@mock.patch("sys.argv", ["commit_msg.py", "COMMIT_MSG"])
def test_main():
    with mock.patch(
        "builtins.open", mock.mock_open(read_data="T-5482/feat: Amazing new feature")
    ):
        # check exit code
        with mock.patch("sys.exit") as mock_exit:
            main()
            mock_exit.assert_called_once_with(0)
