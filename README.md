# git-hooks

This repo contains custom git hooks we use at Two. To add a hook to a repo you have to add it to the repo's `.pre-commit-config.yaml` file

## Setup

First make sure you have installed pre-commit in your repo with `brew install pre-commit` and installed the relevant hooks with `pre-commit install --hook-type <type>`. See `stages` in [.pre-commit-hooks.yaml](.pre-commit-hooks.yaml) for relevant hook types. For more information on pre-commit usage, refer to [docs](https://pre-commit.com/#developing-hooks-interactively).

### Example Config

To only check for a reference to a Linear issue in your commit message, add this:

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/two-inc/git-hooks.git
  rev: 0.0.1
    hooks:
      - id: linear-ref
```

To check for both a reference to a Linear issue as well as a conventional commit type (`<Linear ref>/<conventional commit type>[!]: <description>`), add this:

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/two-inc/git-hooks.git
  rev: 0.0.1
    hooks:
      - id: commit-type-with-linear-ref
```

Alternatively, you can use ssh

```yaml
# .pre-commit-config.yaml
- repo: git@github.com:two-inc/git-hooks.git
  rev: 0.0.1
    hooks:
      - id: commit-type-with-linear-ref
```
