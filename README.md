# git-hooks

This repo contains custom git hooks we use at Two. To add a hook to a repo you have to add it to the repo's `.pre-commit-config.yaml` file

## Add Hook To Repo

First make sure you have installed pre-commit in your repo with `brew install pre-commit` and installed the relevant hooks with `pre-commit install --hook-type <type>`. See `stages` in [.pre-commit-hooks.yaml](.pre-commit-hooks.yaml) for relevant hook types. For more information on pre-commit usage, refer to [docs](https://pre-commit.com/#developing-hooks-interactively).

### Example Config

To only check for a reference to a Linear issue in your commit message, add this:

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/two-inc/git-hooks.git
  rev: 22.11.30
    hooks:
      - id: linear-ref
```

To check for both a reference to a Linear issue as well as a conventional commit type (`<Linear ref>/<conventional commit type>[!]: <description>`), add this:

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/two-inc/git-hooks.git
  rev: 22.11.30
    hooks:
      - id: commit-type-with-linear-ref
```

Alternatively, you can use ssh

```yaml
# .pre-commit-config.yaml
- repo: git@github.com:two-inc/git-hooks.git
  rev: 22.11.30
    hooks:
      - id: commit-type-with-linear-ref
```


## Release Process (git-hooks repo)

1. Check if `master` is ahead of `staging`, and if so, first merge `master` into `staging` (via PR unless you have permissions to push directly to `staging`).
2. Check out `staging` branch and pull latest from origin.
3. If you have permission to push to staging directly, skip to step 4. Otherwise create a new Linear ticket with a title "git-hooks release vX.Y.Z" and a new branch based on that Linear ticket branching off of staging
4. Run `bumpver update --dry` to check version update will be as expected.
5. Run `bumpver update` to update git-hooks version. This creates a bump commit.
6. Push directly to `staging` if you have permission to do so or via a PR if not.
7. Create PR from `staging` into `master` and call it "Release vX.Y.Z".
   The last commit in this PR should be the version bump.
8. Check out `master` branch and set tag with `git tag vX.Y.Z` based on [CalVer](https://calver.org/) convention.
9. Push tags with `git push --tags`.
10. Go to GH and draft a new release - choose tag and select "generate release notes".