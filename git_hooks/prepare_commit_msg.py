import os
import re
import sys
import subprocess
import gql
from gql.transport.aiohttp import AIOHTTPTransport

from git_hooks import common

EDITOR_TEXT = "# Please enter the commit message for your changes."

LINEAR_API_KEY = os.environ.get("LINEAR_API_KEY")


# Convert branch name to commit message
def branch_to_commit_msg(branch: str) -> str:
    return branch.replace("-", " ").replace("_", " ").capitalize() + "\n"


# Check prefix for hints like hotfix/feat/etc:
def prefix_to_commit_type(prefix: str) -> str | None:
    if prefix_match := re.match(common.prefix_regex, prefix):
        return prefix_match.group(1)


def get_branch_name() -> str:
    try:
        return (
            subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"])
            .strip()
            .decode()
        )
    except subprocess.CalledProcessError:
        # If branch name cannot be determined, there is nothing else to do
        sys.exit(0)


def linear_client() -> gql.Client:
    transport = AIOHTTPTransport(
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


def extract_branch_data(branch: str) -> dict[str, str]:
    issue = ""
    commit_type = "fix"
    commit_msg_title = ""
    # If the branch has hints about linear reference, extract those
    if branch_regex_match := re.match(common.branch_regex, branch):
        prefix = branch_regex_match.group(1).lower()
        commit_type = prefix_to_commit_type(prefix) or commit_type
        issue = branch_regex_match.group(2).upper()
        commit_msg_title = branch_to_commit_msg(branch_regex_match.group(3))
    else:
        commit_msg_title = branch_to_commit_msg(branch)
    # If the commit message has linear ref, extract it from the commit message title
    if commit_msg_match := re.match(common.commit_msg_issue_regex, commit_msg_title):
        issue = commit_msg_match.group(1).capitalize()
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

def prepare_commit_msg(raw_commit_msg: str, branch: str) -> str:
    # Default values
    branch_data = extract_branch_data(branch)
    issue = branch_data["issue"]
    commit_type = branch_data["commit_type"]
    commit_msg_title = branch_data["commit_msg_title"]
    commit_msg_body = ""
    commit_msg_lines = raw_commit_msg.splitlines()
    if EDITOR_TEXT in commit_msg_lines:
        commit_msg_body = "\n".join(commit_msg_lines[1:] + [common.commented_commit_type_doc])

        # If LINEAR_API_KEY is set and issue number is not empty, fetch issue details
        if LINEAR_API_KEY and issue:
            try:
                linear_issue = retrieve_linear_issue(issue)
                commit_msg_title = linear_issue["title"] or commit_msg_title
                commit_msg_body = linear_issue["description"] + commit_msg_body
            except Exception as exception:
                error_details = ["# Error while fetching issue details from Linear:", "#"]
                if hasattr(exception, "errors") and isinstance(exception.errors, list):
                    error_details += [f"#\t{e['message']}" for e in exception.errors]
                else:
                    error_details += [f"#\t{str(exception)}"]
                error_details += ["#"]
                commit_msg_body += "\n" + "\n".join(error_details)
        else:
            linear_info = [
                "# Cannot fetch issue details from Linear with API key:",
                "#",
                "#\tTo populate commit message with title and description for an issue number detected",
                "#\tin the branch name, ensure that the environment variable LINEAR_API_KEY is set.",
                "#\tGet this from Personal API keys section at linear.app/tillit/settings/api.",
                "#",
            ]
            commit_msg_body += "\n" + "\n".join(linear_info)
    else:
        commit_msg_title = commit_msg_lines[0] if len(commit_msg_lines) > 0 else ""
        commit_msg_body = "\n".join(line for line in commit_msg_lines[1:] if not line.startswith("#"))

    # Write to commit message
    message = f"{commit_type}: {commit_msg_title}\n\n{commit_msg_body}"
    if issue:
        message = f"{issue}/{message}"

    return message


def main():
    # Commit message filepath is always the first argument
    commit_msg_filepath = sys.argv[1]
    branch = get_branch_name()

    # Read raw commit message
    raw_commit_msg = open(commit_msg_filepath).read()

    # Commit message is already valid, nothing else to do
    if re.match(common.valid_commit_regex, raw_commit_msg):
        sys.exit(0)

    message = prepare_commit_msg(raw_commit_msg, branch)

    with open(commit_msg_filepath, "w+") as fh:
        _ = fh.seek(0, 0)
        _ = fh.write(message)


if __name__ == "__main__":
    main()
