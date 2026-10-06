# GitHub Actions Setup Guide

This guide will help you set up the CI/CD pipeline for this project.

## Step 1: Enable Workflow Permissions

The workflow uses GitHub Container Registry (GHCR), which is **free and unlimited** - perfect for multiple projects!

1. Go to your GitHub repository
2. Navigate to **Settings** → **Actions** → **General**
3. Under **Workflow permissions**, ensure:
   - ✅ **Read and write permissions** is selected
   - ✅ **Allow GitHub Actions to create and approve pull requests** (optional, for PR workflows)

**That's it!** No secrets needed - the workflow uses the built-in `GITHUB_TOKEN`.

## Step 2: Update README Badge (Optional)

1. Open `README.md`
2. Find the badge at the top:
   ```markdown
   [![CI/CD Pipeline](https://github.com/YOUR_USERNAME/django-base-app/actions/workflows/ci-cd.yml/badge.svg)]
   ```
3. Replace `YOUR_USERNAME` with your actual GitHub username

## Step 3: Test the Workflow

1. Push a commit to your repository:
   ```bash
   git add .
   git commit -m "Add CI/CD pipeline"
   git push origin main
   ```

2. Go to the **Actions** tab in your GitHub repository
3. You should see the workflow running
4. Once complete, check the **Packages** section (right sidebar) - your image should be available!

## Why GitHub Container Registry?

- ✅ **Free and unlimited** - No repository limits (unlike Docker Hub's 1 free private repo)
- ✅ **No setup** - Uses built-in GitHub token, no secrets needed
- ✅ **Private by default** - Images are private unless you make them public
- ✅ **Integrated** - Works seamlessly with GitHub Actions
- ✅ **Multiple projects** - Each repository gets its own registry space

## Troubleshooting

### Workflow not running

- Make sure you're pushing to the `main` or `master` branch
- Check that the workflow file is in `.github/workflows/ci-cd.yml`
- Verify the workflow file has valid YAML syntax

### Tests failing

- Check the Actions tab for detailed error messages
- Ensure all dependencies are in `requirements.txt`
- Verify test configuration in `settings.py`

### Docker build/push failing

- Verify workflow permissions are set correctly (Settings → Actions → General)
- Ensure `GITHUB_TOKEN` has package write permissions (usually automatic)
- Check that the repository owner/organization allows package creation
- Verify the Dockerfile path is correct (`deploy/Dockerfile`)

### Image not appearing in GHCR

- Check that the workflow completed successfully
- Go to your repository → **Packages** (right sidebar) to see published packages
- Verify the image name: `ghcr.io/<owner>/django-base-app`
- Check package visibility settings (private by default)
- If private, you'll need to authenticate: `echo $GITHUB_TOKEN | docker login ghcr.io -u <username> --password-stdin`

## Workflow Behavior

### On Push to main/master:
- ✅ Runs tests on Python 3.12, 3.13
- ✅ Builds Docker image
- ✅ Pushes to GitHub Container Registry (GHCR) with tags: `latest`, `main`, `main-<sha>`

### On Pull Request:
- ✅ Runs tests only
- ❌ Does NOT build or push images

### On Version Tag (v*):
- ✅ Runs tests
- ✅ Builds Docker image
- ✅ Pushes to GHCR with version tags: `v1.0.0`, `v1.0`, `v1`, `latest`

## Example: Creating a Version Release

```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0

# The workflow will automatically:
# 1. Run tests
# 2. Build the Docker image
# 3. Tag it as: v1.0.0, v1.0, v1, and latest
```

## Need Help?

- Check the [GitHub Actions documentation](https://docs.github.com/en/actions)
- Review the workflow file: `.github/workflows/ci-cd.yml`
- See the detailed README: `.github/workflows/README.md`

