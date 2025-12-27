# Publishing Guide for func-to-script

This guide explains how to publish new versions of `func-to-script` to PyPI using modern Python packaging best practices (2025).

## Overview

The publishing process uses:
- **setuptools_scm**: Automatic versioning from git tags
- **python -m build**: Modern build tool (PEP 517)
- **GitHub Actions**: Automated CI/CD pipeline
- **Trusted Publishers**: Secure PyPI publishing without API tokens

## One-Time Setup: Configure Trusted Publishers

Trusted Publishers eliminate the need for API tokens by using OpenID Connect (OIDC) to verify that the package is being published from the correct GitHub repository.

### Setting up PyPI Trusted Publisher

1. Go to [https://pypi.org/manage/account/publishing/](https://pypi.org/manage/account/publishing/)
2. Scroll to "Add a new pending publisher"
3. Fill in:
   - **PyPI Project Name**: `func-to-script`
   - **Owner**: `Chris-hughes10`
   - **Repository name**: `func-to-script`
   - **Workflow name**: `release.yaml`
   - **Environment name**: `pypi`
4. Click "Add"

### Setting up Test PyPI Trusted Publisher

1. Go to [https://test.pypi.org/manage/account/publishing/](https://test.pypi.org/manage/account/publishing/)
2. Scroll to "Add a new pending publisher"
3. Fill in:
   - **PyPI Project Name**: `func-to-script`
   - **Owner**: `Chris-hughes10`
   - **Repository name**: `func-to-script`
   - **Workflow name**: `release.yaml`
   - **Environment name**: `testpypi`
4. Click "Add"

**Note**: You only need to do this once. After the first successful publish, the "pending" publisher becomes permanent.

## Publishing a New Release

### 1. Ensure All Tests Pass

Before creating a release, make sure all tests pass:

```bash
# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Optional: Run formatter
black func_to_script/ test/
```

### 2. Create a GitHub Release (Recommended)

The easiest way to publish is through the GitHub web interface:

1. Go to https://github.com/Chris-hughes10/func-to-script/releases
2. Click **"Draft a new release"**
3. Click **"Choose a tag"** and type a new tag name (e.g., `v1.2.3`)
4. Select **"Create new tag on publish"**
5. Fill in the release title (e.g., `v1.2.3` or `Release 1.2.3`)
6. Add release notes describing what changed
7. Click **"Publish release"**

**Important**:
- Use semantic versioning: `vMAJOR.MINOR.PATCH` (e.g., `v1.2.3`)
- The `v` prefix is recommended but optional
- The version in the built package will be `1.2.3` (without the `v`)

### Alternative: Command-Line Tag Publishing

You can also create and push tags directly from the command line:

```bash
# Create a new tag (e.g., for version 1.2.3)
git tag v1.2.3

# Push the tag to GitHub
git push origin v1.2.3
```

Then optionally create a GitHub Release from the tag afterwards for release notes.

### 3. Automated Publishing

Once you publish a GitHub Release (or push a tag), GitHub Actions automatically:

1. **Test Job**: Runs tests on Python 3.8, 3.9, 3.10, 3.11, and 3.12
2. **Build Job**: Builds source distribution (`.tar.gz`) and wheel (`.whl`)
3. **Publish to Test PyPI**: Uploads to https://test.pypi.org/
4. **Publish to PyPI**: Uploads to https://pypi.org/

You can monitor the progress at:
https://github.com/Chris-hughes10/func-to-script/actions

### 4. Verify the Release

After the workflow completes:

**Test PyPI:**
```bash
pip install --index-url https://test.pypi.org/simple/ func-to-script
```

**Production PyPI:**
```bash
pip install func-to-script
```

## Local Testing (Before Publishing)

You can test the build process locally without publishing:

### Install Build Tools

```bash
pip install build
```

### Build the Package

```bash
# Clean any previous builds
rm -rf dist/ build/ *.egg-info

# Build both source distribution and wheel
python -m build
```

This creates:
- `dist/func-to-script-X.Y.Z.tar.gz` (source distribution)
- `dist/func_to_script-X.Y.Z-py3-none-any.whl` (wheel)

### Test the Built Package

```bash
# Install from the wheel in a virtual environment
python -m venv test-env
source test-env/bin/activate  # On Windows: test-env\Scripts\activate
pip install dist/func_to_script-*.whl

# Test that it works
python -c "from func_to_script import script; print(script.__doc__)"

# Deactivate and clean up
deactivate
rm -rf test-env
```

## Version Management

Versioning is fully automatic using `setuptools_scm`:

- **Tagged commits**: Use the tag as version (e.g., tag `v1.2.3` → version `1.2.3`)
- **Between tags**: Automatically append `.devN+gHASH` (e.g., `1.2.3.dev5+g1234abc`)
- **No tags**: Version starts at `0.1.dev0+...`

To check what version will be built:

```bash
python -m setuptools_scm
```

## Troubleshooting

### "No version found" Error

If you get a version error during build:

```bash
# Ensure you're in a git repository
git status

# Fetch all tags
git fetch --tags

# Check tags exist
git tag -l
```

### GitHub Actions Fails with Permission Error

If publishing fails with authentication errors:

1. Ensure Trusted Publishers are configured (see setup above)
2. Check that the workflow has `id-token: write` permission
3. Verify the environment names match (`pypi` and `testpypi`)

### Want to Publish Without Creating a Tag?

For testing purposes only, you can manually trigger a build:

```bash
# Build locally
python -m build

# Upload manually (requires PyPI token)
pip install twine
twine upload --repository testpypi dist/*
```

**Note**: This is NOT recommended for production releases. Always use git tags for official releases.

## Files Involved in Publishing

- **pyproject.toml**: Package metadata and dependencies (PEP 621)
- **.github/workflows/release.yaml**: CI/CD pipeline
- **func_to_script/_version.py**: Auto-generated version file (don't edit manually)
- **README.md**: Package description shown on PyPI

## Migration Notes

This package was recently migrated from legacy `setup.py` + `versioneer` to modern `pyproject.toml` + `setuptools_scm`. The old setup used API tokens; the new setup uses Trusted Publishers for improved security.

**What changed:**
- ✅ All metadata now in `pyproject.toml` (PEP 621)
- ✅ Automatic versioning with `setuptools_scm`
- ✅ Modern build process with `python -m build`
- ✅ Secure publishing with Trusted Publishers (no tokens needed)
- ✅ Multi-version testing in CI (Python 3.8-3.12)
- ❌ No more `setup.py`, `setup.cfg`, `versioneer.py`
- ❌ No more `PYPI_API_TOKEN` secrets needed

## Additional Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [setuptools_scm Documentation](https://setuptools-scm.readthedocs.io/)
- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)
