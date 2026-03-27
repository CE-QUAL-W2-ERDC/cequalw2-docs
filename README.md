# CE-QUAL-W2 ERDC Documentation

Source repository for the official USACE/ERDC CE-QUAL-W2 documentation. This is a **private** repository. The built documentation is deployed to the public CE-QUAL-W2 site via GitHub Actions.

## Quick Start

### Local Development

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Serve locally with live reload
mkdocs serve
```

The site will be available at `http://127.0.0.1:8000`.

### Building the Site

```bash
mkdocs build --strict
```

The built site is written to `site/`.

## Deployment

Deployment is automated via GitHub Actions. The workflow triggers on:

- **Push to `main`**: builds and deploys the `dev` version.
- **Tagged release** (e.g., `v2026.02`): builds, deploys the versioned release, and generates a PDF.

The built HTML is pushed to the `gh-pages` branch of the public `CE-QUAL-W2-ERDC/CE-QUAL-W2` repository.

### Setup Requirements

1. Create a GitHub Personal Access Token (PAT) with `repo` scope.
2. Add the PAT as a repository secret named `DEPLOY_TOKEN` in this repo's settings.

## PSU Manual Differencing

When PSU releases an updated manual:

```bash
python scripts/diff_psu_manuals.py old_manual.pdf new_manual.pdf --save-text
```

This generates a change report (`psu_manual_changes.md`) and optionally saves extracted text for version tracking. Review the report and create GitHub issues for changes to incorporate.

## Directory Structure

```
cequalw2-docs/
├── .github/workflows/   # CI/CD pipeline
├── docs/                 # Documentation source (Markdown)
│   ├── assets/           # Images, CSS
│   ├── getting-started/  # Installation, tutorials
│   ├── theory/           # Hydrodynamics, water quality, HAB modules
│   ├── user-guide/       # Input/output files, tools
│   ├── examples/         # Worked examples
│   ├── developer-guide/  # Code architecture, compilation, testing
│   └── release-notes/    # Changelog and version lineage
├── scripts/              # Utility scripts (PSU diff tool, etc.)
├── mkdocs.yml            # Site configuration
└── requirements.txt      # Python dependencies
```

## Contributing

1. Create a feature branch from `main`.
2. Edit Markdown files in `docs/`.
3. Preview locally with `mkdocs serve`.
4. Submit a pull request for review.
