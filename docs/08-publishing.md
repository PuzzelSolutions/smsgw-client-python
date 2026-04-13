# Publishing to PyPI <!-- omit in toc -->

This guide explains how to build and publish the `puzzel-sms-gateway-client` package to PyPI using [uv](https://github.com/astral-sh/uv).

## Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [Bump the Version](#bump-the-version)
- [Build the Package](#build-the-package)
- [Publish to TestPyPI (Recommended First)](#publish-to-testpypi-recommended-first)
- [Publish to PyPI](#publish-to-pypi)
- [Verify the Release](#verify-the-release)
- [Credentials Reference](#credentials-reference)

---

## Prerequisites

1. **uv installed** — see [01-uv-setup.md](01-uv-setup.md).
2. **PyPI account** — register at [pypi.org](https://pypi.org/account/register/).
3. **API token** — generate a token at *Account Settings → API tokens* on PyPI (and optionally on [test.pypi.org](https://test.pypi.org) for the test step).

> Use API tokens rather than username/password. Tokens are scoped to a single project and can be revoked without changing your account password.

---

## Bump the Version

Update the version in [pyproject.toml](../pyproject.toml) before every release:

```toml
[project]
version = "3.1.0"   # ← change this
```

Follow [Semantic Versioning](https://semver.org):

| Change type | Example |
|---|---|
| Bug fix / patch | `3.0.0` → `3.0.1` |
| New feature (backwards-compatible) | `3.0.0` → `3.1.0` |
| Breaking change | `3.0.0` → `4.0.0` |

---

## Build the Package

From the `clients/smsgw-client-python/` directory:

```bash
uv build
```

This produces two artefacts in `dist/`:

```
dist/
├── puzzel_sms_gateway_client-3.1.0-py3-none-any.whl   # wheel (binary distribution)
└── puzzel_sms_gateway_client-3.1.0.tar.gz              # sdist (source distribution)
```

Inspect the wheel contents to confirm everything looks correct before uploading:

```bash
uv run python -m zipfile -l dist/puzzel_sms_gateway_client-*.whl
```

---

## Publish to TestPyPI (Recommended First)

Upload to [test.pypi.org](https://test.pypi.org) first to verify the package installs and renders correctly without affecting the real index.

```bash
uv publish \
  --publish-url https://test.pypi.org/legacy/ \
  --token pypi-your-test-token-here
```

Then install from TestPyPI and do a quick smoke test:

```bash
uv pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  puzzel-sms-gateway-client==3.1.0
```

> The `--extra-index-url` flag allows pip to resolve dependencies (Kiota packages) from the real PyPI if they are not mirrored on TestPyPI.

---

## Publish to PyPI

Once you are satisfied with the TestPyPI release, publish to the real index:

```bash
uv publish --token pypi-your-production-token-here
```

`uv publish` defaults to `https://upload.pypi.org/legacy/`, so no `--publish-url` is needed for the main PyPI.

### Storing the token in an environment variable

Instead of passing the token on the command line every time, set it as an environment variable:

```bash
export UV_PUBLISH_TOKEN=pypi-your-production-token-here
uv publish
```

Or store it in a `.env` file (make sure `.env` is listed in `.gitignore`):

```bash
# .env
UV_PUBLISH_TOKEN=pypi-your-production-token-here
```

```bash
# Load it before publishing
source .env && uv publish
```

### Storing the token in `~/.pypirc`

You can also configure credentials once in `~/.pypirc` so you never have to pass them explicitly:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-your-production-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-token-here
```

With this in place, publishing is just:

```bash
uv publish               # → PyPI
uv publish --publish-url https://test.pypi.org/legacy/   # → TestPyPI
```

> `~/.pypirc` is read by both `uv publish` and `twine`. Keep this file private (`chmod 600 ~/.pypirc`).

---

## Verify the Release

After a successful upload, confirm the package is live:

```bash
# Install the freshly published version
uv pip install "puzzel-sms-gateway-client==3.1.0"

# Quick import check
python -c "from src.mt_http_client import MtHttpClient; print('OK')"
```

Check the PyPI project page to ensure the description, classifiers, and links rendered correctly:

```
https://pypi.org/project/puzzel-sms-gateway-client/
```

---

## Credentials Reference

| Variable / file | Purpose |
|---|---|
| `UV_PUBLISH_TOKEN` | API token passed via environment variable |
| `~/.pypirc` | Persistent credential store (both `[pypi]` and `[testpypi]` sections) |
| `--token` flag | One-off token passed directly to `uv publish` |

Never commit tokens or `~/.pypirc` contents to version control.
