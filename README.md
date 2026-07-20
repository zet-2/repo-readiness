# Repo Readiness

A dependency-free command-line checkup for public GitHub repositories.

Repo Readiness fetches repository metadata from GitHub's public REST API and
prints a compact summary. It is useful in scripts, release checklists, and quick
open-source hygiene reviews.

## Usage

Run directly from the repository:

```bash
PYTHONPATH=src python -m repo_readiness owner/repository
```

Or install the command locally:

```bash
python -m pip install .
repo-readiness owner/repository
```

The optional `GITHUB_TOKEN` environment variable raises the API rate limit for
repeated checks.

## Development

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

Repo Readiness supports Python 3.10 and newer.

## License

[MIT](LICENSE)
