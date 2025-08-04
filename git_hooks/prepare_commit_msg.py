"""This hook prepares a commit message containing a reference to a Linear issue as well as a conventional commit type.
It uses the branch name to determine the issue number and the commit message title as well as the conventional commit type.
If LINEAR_API_KEY is set, it fetches the issue title and description from Linear and populates the commit message with it.
If DEFAULT_COMMIT_TYPE is set, it uses that as the default commit type when none is detected (defaults to "feat").
See https://www.conventionalcommits.org for examples of conventional commit types.
"""

import os
import re
import sys
import subprocess
import gql
from gql.transport.requests import RequestsHTTPTransport

from git_hooks import common

EDITOR_TEXT = "# Please enter the commit message for your changes."

LINEAR_API_KEY = os.environ.get("LINEAR_API_KEY")
DEFAULT_COMMIT_TYPE = os.environ.get("DEFAULT_COMMIT_TYPE", "feat")


# Convert branch name to commit message
def branch_to_commit_msg(branch: str) -> str:
    return branch.replace("-", " ").replace("_", " ").capitalize()


# Check prefix for hints like hotfix/feat/etc:
def prefix_to_commit_type(prefix: str) -> str:
    if prefix_match := re.match(common.prefix_regex, prefix):
        return prefix_match.group(1)
    return DEFAULT_COMMIT_TYPE


def get_branch_name() -> str | None:
    try:
        return (
            subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"])
            .strip()
            .decode()
        )
    except subprocess.CalledProcessError:
        # If branch name cannot be determined, there is nothing else to do
        pass


def linear_client() -> gql.Client:
    transport = RequestsHTTPTransport(
        url="https://api.linear.app/graphql",
        headers={"Authorization": LINEAR_API_KEY},
    )
    return gql.Client(transport=transport, fetch_schema_from_transport=True)


def retrieve_linear_issue(issue: str) -> dict[str, str]:
    client = linear_client()
    query = gql.gql(
        """
        query Issue ($issue: String!) {
            issue(id: $issue) {
                title
                description
            }
        }
        """
    )
    values = {"issue": issue}
    response = client.execute(query, variable_values=values)
    title = response["issue"]["title"]
    description = response["issue"]["description"]
    return {
        "title": title.strip() if title else "",
        "description": f"{description.strip()}\n\n" if description else "",
    }


def extract_commit_msg_title_data(commit_msg_title: str) -> dict[str, str]:
    issue = ""
    commit_type = ""
    # If the commit message has linear ref, extract it from the commit message title
    if commit_msg_match := re.match(common.commit_msg_issue_regex, commit_msg_title):
        issue = commit_msg_match.group(1).upper()
        commit_msg_title = commit_msg_match.group(2)
    # If the commit message only has conventional commit tag but no linear ref, use those
    if commit_msg_match := re.match(common.commit_msg_title_regex, commit_msg_title):
        commit_type = commit_msg_match.group(1)
        commit_msg_title = commit_msg_match.group(2)
    return {
        "issue": issue,
        "commit_type": commit_type,
        "commit_msg_title": commit_msg_title,
    }


def extract_branch_data(branch: str) -> dict[str, str]:
    issue = ""
    commit_type = ""
    commit_msg_title = ""
    _branch = branch
    # If the branch has hints about linear reference, extract those
    if branch_regex_match := re.match(common.branch_regex, branch):
        prefix = branch_regex_match.group(1).lower()
        commit_type = prefix_to_commit_type(prefix)
        issue = branch_regex_match.group(2).upper()
        _branch = branch_regex_match.group(3)
    elif partial_branch_regex_match := re.match(common.partial_branch_regex, branch):
        issue = partial_branch_regex_match.group(1).upper()
        _branch = partial_branch_regex_match.group(2)
    commit_msg_title = branch_to_commit_msg(_branch)

    return {
        "issue": issue,
        "commit_type": commit_type,
        "commit_msg_title": commit_msg_title,
    }


def retrieve_linear_data(issue: str, edit_mode: bool) -> dict[str, str]:
    # If LINEAR_API_KEY is set and issue number is not empty, fetch issue details
    if LINEAR_API_KEY:
        try:
            linear_issue = retrieve_linear_issue(issue)
            return {
                "commit_msg_title": linear_issue["title"],
                "commit_msg_body": linear_issue["description"],
            }
        except Exception as exception:
            if not edit_mode:
                return {}
            error_details = [
                "# Error fetching issue details from Linear:",
                "#",
            ]
            if hasattr(exception, "errors") and isinstance(exception.errors, list):
                error_details += [f"#\t{e['message']}" for e in exception.errors]
            else:
                error_details += [f"#\t{str(exception)}"]
            error_details += ["#"]
            return {
                "commit_msg_body": "\n".join(error_details),
            }
    else:
        if not edit_mode:
            return {}
        linear_info = [
            "# NEW FEATURE: Use Linear API key to fetch commit title and description:",
            "#",
            "#\tTo populate commit message with title and description for an issue number detected",
            "#\tin the branch name, ensure that the environment variable LINEAR_API_KEY is set.",
            "#\tGet this from Personal API keys section at linear.app/tillit/settings/api.",
            "#",
        ]
        return {
            "commit_msg_body": "\n".join(linear_info),
        }


def prepare_commit_msg(raw_commit_msg: str, branch: str) -> str:
    commit_msg_lines = raw_commit_msg.splitlines()
    edit_mode = EDITOR_TEXT in raw_commit_msg
    branch_data = extract_branch_data(branch)
    raw_commit_msg_title = commit_msg_lines[0] if len(commit_msg_lines) > 0 else ""

    linear_data = {}
    if (issue := branch_data["issue"]) and not raw_commit_msg_title:
        linear_data = retrieve_linear_data(issue, edit_mode)

    commit_msg_title_data = extract_commit_msg_title_data(
        linear_data.get("commit_msg_title") or raw_commit_msg_title
    )
    commit_type = commit_msg_title_data["commit_type"] or branch_data["commit_type"] or DEFAULT_COMMIT_TYPE
    commit_msg_title = (
        commit_msg_title_data["commit_msg_title"] or branch_data["commit_msg_title"]
    )
    commit_type_lines = [common.commit_types_doc_commented] if edit_mode else []
    linear_commit_msg_lines = (
        [linear_data["commit_msg_body"]] if linear_data.get("commit_msg_body") else []
    )
    commit_msg_body = "\n".join(
        linear_commit_msg_lines + commit_msg_lines[1:] + commit_type_lines
    )

    # Write to commit message
    message = commit_msg_title
    if commit_msg_body:
        message = f"{message}\n\n{commit_msg_body}"
    if commit_type:
        message = f"{commit_type}: {message}"
    if issue:
        message = f"{issue}/{message}"

    return message


def main():
    # Commit message filepath is always the first argument
    commit_msg_filepath = sys.argv[1]
    if (branch := get_branch_name()) is None:
        return

    # Read raw commit message
    raw_commit_msg = open(commit_msg_filepath).read()

    # Commit message is already valid, nothing else to do
    if re.match(common.valid_commit_regex, raw_commit_msg):
        return

    message = prepare_commit_msg(raw_commit_msg, branch)

    with open(commit_msg_filepath, "w+") as fh:
        _ = fh.seek(0, 0)
        _ = fh.write(message)


if __name__ == "__main__":
    main()
