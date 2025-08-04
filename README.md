# git-hooks

This repo contains custom git hooks we use at Two. To add a hook to a repo you
have to add it to the repo's `.pre-commit-config.yaml` file

## Add Hook To Repo

First make sure you have installed pre-commit in your repo with `brew install
pre-commit` and installed the relevant hooks with `pre-commit install
--hook-type <type>`. See `stages` in
[.pre-commit-hooks.yaml](.pre-commit-hooks.yaml) for relevant hook types. For
more information on pre-commit usage, refer to
[docs](https://pre-commit.com/#developing-hooks-interactively).

### Example Config

To only check for a reference to a Linear issue in your commit message, add this:

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/two-inc/git-hooks.git
  rev: 25.08.04
    hooks:
      - id: linear-ref
```

To check for both a reference to a Linear issue as well as a conventional
commit type (`<Linear ref>/<conventional commit type>[!]: <description>`), add
this:

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/two-inc/git-hooks.git
  rev: 25.08.04
    hooks:
      - id: commit-type-with-linear-ref
```

Alternatively, you can use ssh

```yaml
# .pre-commit-config.yaml
- repo: git@github.com:two-inc/git-hooks.git
  rev: 25.08.04
    hooks:
      - id: commit-type-with-linear-ref
```

## Developmment

### 1. Create virtual environment

```bash
source venv/bin/activate
python3 -m venv venv
```

### 2. Install requirements

```bash
pip3 install -e '.[dev]'
```

### 3. Release

1. If you have permission to push to main directly, skip to step 2. Otherwise
   create a new Linear ticket with a title "git-hooks release X.Y.Z" and a new
   branch based on that Linear ticket branching off of main.
2. Run `bumpver update --dry` to check version update will be as expected.
3. Run `bumpver update` to update git-hooks version. This creates a bump commit.
4. Push directly to `main` if you have permission to do so or via a PR if not.
5. Check out `main` branch and set tag with `git tag X.Y.Z` based on [CalVer](https://calver.org/) convention.
6. Push tags with `git push --tags`.
7. Go to GH and draft a new release - choose tag and select "generate release notes".
