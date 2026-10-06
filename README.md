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
  rev: 26.10.06
    hooks:
      - id: linear-ref
```

To check for both a reference to a Linear issue as well as a conventional
commit type (`<Linear ref>/<conventional commit type>[!]: <description>`), add
this:

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/two-inc/git-hooks.git
  rev: 26.10.06
    hooks:
      - id: commit-type-with-linear-ref
```

Alternatively, you can use ssh

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/two-inc/git-hooks
  rev: 26.10.06
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

Run the [Release workflow](https://github.com/two-inc/git-hooks/actions/workflows/release.yaml)
(Actions -> Release -> Run workflow). It runs `bumpver update` on `main`, which
commits the bump, tags it with today's [CalVer](https://calver.org/) version and
pushes, then creates a GitHub release with generated notes. Set `version` to
override the date-based version. Then bump `rev:` in consuming repos.
