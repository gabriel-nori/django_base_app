# GitHub Actions Workflows

This directory contains GitHub Actions workflows for CI/CD.

## Workflows

### CI/CD Pipeline (`ci-cd.yml`)

This workflow handles:
1. **Testing**: Runs Django tests on multiple Python versions (3.12, 3.13)
2. **Building**: Builds Docker image using the Dockerfile in `deploy/Dockerfile`
3. **Pushing**: Pushes the image to GitHub Container Registry (GHCR)

#### Triggers

- **Push to main/master**: Runs tests and builds/pushes Docker image
- **Push tags (v*)**: Runs tests and builds/pushes Docker image with version tags
- **Pull Requests**: Runs tests only (no build/push)

#### Container Registry

This workflow uses **GitHub Container Registry (GHCR)** instead of Docker Hub because:
- ✅ **Free and unlimited** - No repository limits
- ✅ **Integrated with GitHub** - Uses built-in `GITHUB_TOKEN` (no extra secrets needed)
- ✅ **Private by default** - Images are private unless you make them public
- ✅ **Works with all your projects** - Each repository gets its own container registry

**No setup required!** The workflow automatically uses `GITHUB_TOKEN` which is provided by GitHub Actions.

If you want to make images public, go to your package settings on GitHub and change the visibility.

#### Image Tags

The workflow automatically creates the following tags:

- `latest` - Always points to the latest build from main/master branch
- `main` or `master` - Branch name tag
- `main-<sha>` - Branch name with commit SHA
- `v1.0.0` - Semantic version tags (when pushing git tags)
- `v1.0` - Major.minor version
- `v1` - Major version

#### Example Usage

```bash
# After pushing to main, the image will be available as:
docker pull ghcr.io/<your-github-username>/django-base-app:latest
docker pull ghcr.io/<your-github-username>/django-base-app:main
docker pull ghcr.io/<your-github-username>/django-base-app:main-abc1234

# For versioned releases:
git tag v1.0.0
git push origin v1.0.0
# Image will be tagged as: v1.0.0, v1.0, v1, latest

# To pull from GHCR, you may need to authenticate first:
echo $GITHUB_TOKEN | docker login ghcr.io -u <your-github-username> --password-stdin
```

**Note**: Replace `<your-github-username>` with your actual GitHub username or organization name.

#### Multi-platform Builds

The workflow builds for both `linux/amd64` and `linux/arm64` architectures, making the image compatible with:
- Standard x86_64 servers
- ARM-based servers (e.g., AWS Graviton, Apple Silicon)

#### Caching

Docker layer caching is enabled to speed up builds. The cache is stored in GHCR as `buildcache` tag.

## Local Testing

You can test the workflow locally using [act](https://github.com/nektos/act):

```bash
# Install act
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run the test job
act -j test

# Run the build job (uses GITHUB_TOKEN automatically)
act -j build-and-push
```

## Troubleshooting

### Tests failing

- Check that all dependencies are in `requirements.txt`
- Verify test database configuration in `settings.py`
- Ensure tests don't require external services (database, Redis, etc.)

### Docker build failing

- Verify the Dockerfile path is correct (`deploy/Dockerfile`)
- Check that the build context includes all necessary files
- Ensure workflow permissions are set correctly (Settings → Actions → General)

### Image not pushing

- **Permission denied errors**: The workflow now includes explicit `permissions: packages: write` in the build job. If you still get "denied: installation not allowed to Create organization package":
  1. Go to your GitHub organization → Settings → Actions → General
  2. Under "Workflow permissions", ensure "Read and write permissions" is selected
  3. Check "Allow GitHub Actions to create and approve pull requests" if needed
  4. Under "Package creation", ensure packages can be created by workflows
- Verify workflow permissions are set correctly (Settings → Actions → General)
- Ensure `GITHUB_TOKEN` has package write permissions (the workflow now explicitly requests this)
- Check that the repository owner/organization allows package creation
- Ensure the workflow is running on the correct branch (main/master)
- For organization packages, you may need to use a Personal Access Token (PAT) with `packages:write` scope instead of `GITHUB_TOKEN` if organization settings restrict it

