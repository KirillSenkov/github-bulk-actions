# github-bulk-actions

A small, focused utility for performing bulk actions on GitHub repositories via API.

Built for real use. Brushed for little less shame. Published as-is.

---

## What it does

Currently supports one operation:

- **make all repositories private**

The script fetches all repositories for a user and converts every public repository to private using the GitHub API.

---

## Why this exists

At some point, manual repo cleanup stops being practical.

This tool exists to:

- avoid repetitive manual actions
- reduce human error
- apply consistent changes across all repositories

---

## Scope

This is not a general-purpose GitHub client.

It is a deliberately narrow utility with a single responsibility:
> bulk repository visibility management

Unimplemented parts of the API layer are intentional.

---

## How it works

- fetch repositories via paginated GitHub API
- filter public repositories
- send PATCH requests to update visibility
- print results and errors to stdout

---

## Requirements

- Python 3.12+
- GitHub Personal Access Token with repo permissions

---

## Setup

Create a `.env` file in the project root:

```env
gituser=your_username
token=your_token
repos_url=https://api.github.com/user/repos
repo_url=https://api.github.com/repos
```

## Usage

`python main.py` or `python -m main`

## Output

The script prints:

- per-repository result
- API error messages (if any)
- summary statistics

Example:

```stdout
'repo-1' - Ok
'repo-2' response:
    status_code: 4..
    response: ...
    message: ...
'repo-3' - Ok
'repo-4' - Ok
private: 6
public: 4
3 made private of 10 repos total (30.0%)
```

## Notes

- Only public repositories are affected
- Private repositories are skipped
- Fork visibility is constrained by GitHub rules

## License

MIT (or your choice)
