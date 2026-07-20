# Repo Readiness

A dependency-free command-line checkup for public GitHub repositories.

Repo Readiness fetches repository metadata from GitHub's public REST API and
prints a compact summary plus a readiness score. The score checks whether a
repository has a description, license, discovery topics, homepage, issue
tracking, and active status. It is useful in release checklists and quick
open-source hygiene reviews.

## Usage

Run directly from the repository:

```bash
PYTHONPATH=src python -m repo_readiness owner/repository
```

For CI jobs and scripts, request JSON and enforce a minimum score:

```bash
PYTHONPATH=src python -m repo_readiness owner/repository --json
PYTHONPATH=src python -m repo_readiness owner/repository --fail-under 80
```

`--fail-under` exits with status `1` when the score is below the requested
threshold.

Example:

```text
octocat/Hello-World
  My first repository on GitHub!
  state: active
  default branch: master
  stars: 3727
  forks: 6267
  open issues: 6703

Readiness score: 50/100
  [x] Repository has a description
  [ ] Repository declares a license
      Add a LICENSE file recognized by GitHub.
```

Or install the command locally:

```bash
python -m pip install .
repo-readiness owner/repository
```

The optional `GITHUB_TOKEN` environment variable raises the API rate limit for
repeated checks.

## GitHub API access

Public repositories work without authentication. For repeated checks, provide a
fine-grained token through the environment:

```bash
GITHUB_TOKEN=github_pat_... repo-readiness owner/repository
```

Repo Readiness sends the token only in the `Authorization` header of requests
to `api.github.com`; it does not print or persist the value. Granting repository
permissions is unnecessary when checking public repositories.

If GitHub returns a rate-limit error, wait for the limit to reset or retry with
`GITHUB_TOKEN` set. Private repositories require a token that can read the
target repository.

## Development

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Repo Readiness supports Python 3.10 and newer.

## License

[MIT](LICENSE)
