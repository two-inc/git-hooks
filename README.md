# git-hooks

This repo contains custom git hooks we use at Two. To add a hook to a repo you have to add it to the repo's `.pre-commit-config.yaml` file

## Add Hook To Repo

First make sure you have installed pre-commit in your repo with `brew install pre-commit` and installed the relevant hooks with `pre-commit install --hook-type <type>`. See `stages` in [.pre-commit-hooks.yaml](.pre-commit-hooks.yaml) for relevant hook types. For more information on pre-commit usage, refer to [docs](https://pre-commit.com/#developing-hooks-interactively).

### Example Config

To only check for a reference to a Linear issue in your commit message, add this:

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/two-inc/git-hooks.git
  rev: 22.12.08
    hooks:
      - id: linear-ref
```

To check for both a reference to a Linear issue as well as a conventional commit type (`<Linear ref>/<conventional commit type>[!]: <description>`), add this:

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/two-inc/git-hooks.git
  rev: 22.12.08
    hooks:
      - id: commit-type-with-linear-ref
```

Alternatively, you can use ssh

```yaml
# .pre-commit-config.yaml
- repo: git@github.com:two-inc/git-hooks.git
  rev: 22.12.08
    hooks:
      - id: commit-type-with-linear-ref
```


## Setup
1. Create virtual environment:

        python3 -m venv venv

2. Install requirements:

        pip3 install -r requirements.txt

## Release Process (git-hooks repo)

1. On `main` run `bumpver update --dry` to check version update will be as expected.
5. Run `bumpver update` to update git-hooks version. This creates a bump commit.
6. Push directly to `main` if you have permission to do so or via a PR if not.
8. Check out `main` branch and set tag with `git tag X.Y.Z` based on [CalVer](https://calver.org/) convention.
9. Push tags with `git push --tags`.
10. Go to GH and draft a new release - choose tag and select "generate release notes".