# git-hooks

This repo contains custom git hooks we use at Two.
To add a hook to a repo you have to add it to the repo's `.pre-commit-config.yaml` file

## Example config

```yaml
repo: https://github.com/two-inc/git-hooks
rev: 1.0.0
    hooks:
        - id: linear-issue-in-commit-msg
```
