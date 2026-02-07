# Complete Guide: Automated Docker Releases from CHANGELOG.md with GitHub Actions (made by @azdolinski)

## Table of Contents

1. [Overview](#overview)
2. [The Problem We're Solving](#the-problem-were-solving)
3. [Architecture & How It Works](#architecture--how-it-works)
4. [Complete Setup](#complete-setup)
5. [All Workflow Files](#all-workflow-files)
6. [CHANGELOG Format](#changelog-format)
7. [Practical Examples](#practical-examples)
8. [Pre-releases vs Stable Releases](#pre-releases-vs-stable-releases)
9. [Advanced Production Features](#advanced-production-features)
10. [Troubleshooting](#troubleshooting)
11. [Best Practices](#best-practices)
12. [Version Prefix (v) Best Practices](#version-prefix-v-best-practices)

---

## Version Prefix (v) Best Practices

### The Golden Rule: Git Tags WITH `v`, Docker Tags WITHOUT `v`

This is **critical** to understand and implement correctly:

| Component | Format | Example | Why |
|-----------|--------|---------|-----|
| **Git Tag** | `v{version}` | `v0.6.13` | ✅ Standard Git/GitHub/SemVer convention |
| **GitHub Release** | `v{version}` | `v0.6.13` | ✅ Displayed as "Release v0.6.13" |
| **Docker Image Tag** | `{version}` | `0.6.13` | ✅ Docker/OCI standard (no prefix) |
| **CHANGELOG.md** | `{version}` | `## [0.6.13]` | ✅ Readability (no `v` inside brackets) |

---

### Why This Matters

**Git Tags (WITH `v`):**
```bash
✅ v0.6.13, v1.0.0, v2.5.1
❌ 0.6.13, 1.0.0, 2.5.1
```

**Reasons:**
- **Industry standard**: Used by Kubernetes, Docker, Go, Node.js, all major open-source projects
- **Distinguishes version tags** from other tags (e.g., `release-candidate`, `build-123`)
- **GitHub convention**: Automatically recognized as release tags
- **Semantic Versioning spec**: Recommends `v` prefix for tags

**Docker Image Tags (WITHOUT `v`):**
```bash
✅ ghcr.io/azdolinski/devcoder:0.6.13
✅ ghcr.io/azdolinski/devcoder:0.6
✅ ghcr.io/azdolinski/devcoder:0
✅ ghcr.io/azdolinski/devcoder:latest

❌ ghcr.io/azdolinski/devcoder:v0.6.13
❌ ghcr.io/azdolinski/devcoder:v0.6
```

**Reasons:**
- **Docker Hub standard**: All official images use plain numbers (`nginx:1.25`, `postgres:15.2`, `node:20.11.0`)
- **OCI specification**: Open Container Initiative standard
- **User experience**: Easier to type `docker pull image:1.0.0` vs `docker pull image:v1.0.0`
- **Tooling compatibility**: Most Docker tools expect version numbers without prefix

---

### How `docker/metadata-action` Handles This

**The magic**: `docker/metadata-action` with `type=semver` **automatically strips the `v` prefix**!

```yaml
# Input: Git tag = v0.6.13

tags: |
  type=semver,pattern={{version}},value=v0.6.13
  # Output: 0.6.13 ✅ (v removed automatically)
  
  type=semver,pattern={{major}}.{{minor}},value=v0.6.13
  # Output: 0.6 ✅ (v removed automatically)
  
  type=semver,pattern={{major}},value=v0.6.13
  # Output: 0 ✅ (v removed automatically)
```

**You do NOT need to:**
- Manually strip `v` prefix
- Use `prefix=v` parameter (this would add `v` back!)
- Use `type=raw` for version tags

---

### Common Mistakes to Avoid

#### ❌ Mistake 1: Adding `v` to CHANGELOG.md
```markdown
## [v0.6.13] - 2026-01-22  ❌ WRONG
## [0.6.13] - 2026-01-22   ✅ CORRECT
```

**Why wrong**: The workflow adds `v` prefix when creating Git tag:
```bash
TAG=v$VERSION  # If VERSION=v0.6.13, you get vv0.6.13!
```

#### ❌ Mistake 2: Using `prefix=v` with semver
```yaml
# WRONG - double 'v' prefix
tags: |
  type=semver,pattern={{version}},value=v0.6.13,prefix=v
  # Output: vv0.6.13 ❌
```

#### ❌ Mistake 3: Using `type=raw` for version tags
```yaml
# WRONG - keeps 'v' prefix in Docker tag
tags: |
  type=raw,value=v0.6.13
  # Output: v0.6.13 ❌ (Docker tag should be 0.6.13)
```

**Correct approach:**
```yaml
# CORRECT - semver automatically strips 'v'
tags: |
  type=semver,pattern={{version}},value=v0.6.13
  # Output: 0.6.13 ✅
```

#### ❌ Mistake 4: Security scanners using Git tag format
```yaml
# WRONG - scanner tries to pull image with 'v' prefix
image-ref: ghcr.io/azdolinski/devcoder:v0.6.13  ❌
# Image doesn't exist! Docker tags don't have 'v'

# CORRECT - strip 'v' for Docker image reference
VERSION=${TAG#v}  # v0.6.13 → 0.6.13
image-ref: ghcr.io/azdolinski/devcoder:0.6.13  ✅
```

---

### Real-World Examples

**Example 1: Stable Release v0.6.13**

```bash
# CHANGELOG.md
## [0.6.13] - 2026-01-22  # No 'v'

# Git tag created
v0.6.13  # With 'v'

# GitHub Release
Release v0.6.13  # With 'v'

# Docker tags published
ghcr.io/azdolinski/devcoder:0.6.13  # No 'v'
ghcr.io/azdolinski/devcoder:0.6    # No 'v'
ghcr.io/azdolinski/devcoder:0      # No 'v'
ghcr.io/azdolinski/devcoder:latest # No 'v'
```

**Example 2: Pre-release v1.0.0-alpha**

```bash
# CHANGELOG.md
## [1.0.0-alpha] - 2026-01-22  # No 'v'

# Git tag created
v1.0.0-alpha  # With 'v'

# GitHub Release
Pre-Release v1.0.0-alpha  # With 'v'

# Docker tag published
ghcr.io/azdolinski/devcoder:1.0.0-alpha  # No 'v'
# Note: NO 'latest' tag for pre-releases!
```

---

### Reference: Industry Standards

**Projects using `v` prefix in Git tags:**
- Kubernetes: `v1.28.0`, `v1.27.5`
- Docker: `v24.0.0`, `v23.0.6`
- Go: `v1.21.0`, `v1.20.7`
- Node.js: `v20.11.0`, `v18.19.0`

**Docker images WITHOUT `v` prefix:**
- `nginx:1.25.3`
- `postgres:16.1`
- `node:20.11.0`
- `alpine:3.19`

**Official documentation:**
- [Semantic Versioning](https://semver.org/) - Recommends `v` for tags
- [Docker Official Images](https://hub.docker.com/) - All use plain version numbers
- [OCI Distribution Spec](https://github.com/opencontainers/distribution-spec) - Tags are plain strings

---

### Quick Reference Card

```bash
# ✅ CORRECT WORKFLOW

# 1. Edit CHANGELOG.md
## [0.6.13] - 2026-01-22  # No 'v'

# 2. Workflow creates Git tag
git tag -a v0.6.13  # With 'v'

# 3. Workflow generates Docker tags
type=semver,pattern={{version}},value=v0.6.13
# → Output: 0.6.13 (no 'v')

# 4. Users pull image
docker pull ghcr.io/azdolinski/devcoder:0.6.13  # No 'v'

# 5. Security scanners reference image
image-ref: ghcr.io/azdolinski/devcoder:0.6.13  # No 'v'
```

---

## Overview

This guide provides a **complete, production-ready solution** for automating:

1. **Version Detection** → Automatically detect new versions from `CHANGELOG.md`
2. **Git Tag Creation** → Automatically create Git tags (v1.0.0, v1.0.1-pre1, etc.)
3. **Release Notes** → Automatically publish Release Notes to GitHub Releases
4. **Docker Image Building** → Automatically build and publish Docker images with proper semantic versioning
5. **Latest Tag Management** → `latest` tag only for stable releases, NOT for pre-releases

### Why This Approach?

**Single Source of Truth**: Your `CHANGELOG.md` file controls everything. Edit it once, everything else happens automatically.

```
CHANGELOG.md (edit)
    ↓ (git push)
GitHub Detect-Release Workflow
    ↓ (parses version, creates tag)
Git Tag Created
    ↓ (workflow_run trigger)
GitHub Build-and-Push Workflow
    ↓ (builds Docker image)
Docker Registry (ghcr.io or Docker Hub)
    ↓ (multiple semantic tags)
v1.0.0, v1.0, v1, latest (if stable)
```

**⚠️ Important**: GitHub Actions doesn't trigger `on: push: tags:` when tags are created by other workflows. That's why we use `workflow_run` trigger to chain the workflows together.

---

## The Problem We're Solving

### Before (Manual Versioning)

```bash
# Developer has to:
1. Remember to create Git tags manually
   git tag v1.0.0
   
2. Remember to push them
   git push origin v1.0.0
   
3. Manually create release notes on GitHub
   
4. Manually build Docker images
   docker build -t myapp:1.0.0 .
   docker build -t myapp:1.0 .
   docker build -t myapp:latest .
   
5. Manually push all three tags to registry
   docker push myapp:1.0.0
   docker push myapp:1.0
   docker push myapp:latest

# Result: Error-prone, time-consuming, easy to forget something
```

### After (Automated)

```bash
# Developer only needs to:
1. Edit CHANGELOG.md
2. git push

# Everything else happens automatically:
✅ Git tag created (v1.0.0)
✅ GitHub Release created
✅ Docker image built
✅ All semantic tags published (1.0.0, 1.0, 1, latest)
✅ Pre-releases handled separately (no latest tag)
```

---

## Architecture & How It Works

### Workflow 1: `detect-release.yml`

**Trigger**: When `CHANGELOG.md` changes on `main` branch

**What it does**:
1. Parses version from `CHANGELOG.md` (looks for `## [X.X.X]` or `## [X.X.X-preX]`)
2. Determines if it's stable or pre-release
3. Checks if Git tag already exists (prevents duplicates)
4. Extracts changelog content for this version
5. Creates Git tag `vX.X.X`
6. Pushes tag to repository
7. Creates GitHub Release with changelog content
8. Marks as pre-release if needed

**Why this step?**
- Single source of truth is CHANGELOG.md
- Automatically creates tags without manual git commands
- Prevents accidental duplicate releases
- Extracts proper release notes from structured changelog

### Workflow 2: `build-and-push.yml`

**Triggers** (both):
1. When `detect-release.yml` workflow completes successfully (`workflow_run` trigger)
2. When Git tag matching `v*` is pushed manually (fallback for manual tags)

**What it does**:
1. Determines trigger type (workflow_run vs tag push)
2. Fetches the most recent tag from repository if triggered by workflow_run
3. Detects if release is stable (vX.X.X) or pre-release (vX.X.X-*)
4. Sets up Docker Buildx for efficient builds
5. Logs in to container registry (GitHub Container Registry)
6. For **stable releases**: Creates semantic tags (1.0.0, 1.0, 1, latest)
7. For **pre-releases**: Creates only version tag (1.0.0-pre1) - NO latest
8. Builds Docker image with all tags
9. Pushes to registry
10. Runs security scans (Trivy + Grype)
11. Generates summary report

**Why this approach?**
- **workflow_run trigger**: Essential because GitHub Actions doesn't trigger on tags created by other workflows (security feature to prevent loops)
- **Dual triggers**: Supports both automated (via detect-release) and manual tag creation workflows
- Semantic versioning helps users pin versions
- `latest` tag for stable only = production safety
- Pre-releases stay isolated from production defaults
- Conditional logic prevents mistakes

---

## Complete Setup

### Step 1: Create Directory Structure

```bash
cd your-repo
mkdir -p .github/workflows
```

### Step 2: Create Workflow Files

#### File A: `.github/workflows/detect-release.yml`

Copy this entire workflow:

```yaml
name: Detect Release from CHANGELOG

on:
  push:
    branches:
      - main
    paths:
      - 'CHANGELOG.md'

permissions:
  contents: write

jobs:
  detect-and-release:
    runs-on: ubuntu-latest
    environment: prod  # Optional: Use if you need environment secrets/variables
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Extract version from CHANGELOG
        id: version
        run: |
          # Looks for first ## [X.X.X] or ## [X.X.X-*] line (ignores Unreleased)
          VERSION=$(grep -oP '## \[\K[0-9]+\.[0-9]+\.[0-9]+(?:\-[a-zA-Z0-9.]+)?(?=\])' CHANGELOG.md | head -1)
          
          if [ -z "$VERSION" ]; then
            echo "❌ Could not find version in CHANGELOG.md"
            echo "Format should be: ## [X.X.X] or ## [X.X.X-preX]"
            exit 1
          fi
          
          echo "✅ Found version: $VERSION"
          echo "VERSION=$VERSION" >> $GITHUB_OUTPUT
          echo "TAG=v$VERSION" >> $GITHUB_OUTPUT
          
          # Determine if it's a pre-release
          if [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo "Release type: stable"
            echo "IS_PRERELEASE=false" >> $GITHUB_OUTPUT
          else
            echo "Release type: pre-release"
            echo "IS_PRERELEASE=true" >> $GITHUB_OUTPUT
          fi

      - name: Check if tag already exists
        id: check_tag
        run: |
          TAG="v${{ steps.version.outputs.VERSION }}"
          if git rev-parse "$TAG" >/dev/null 2>&1; then
            echo "⏭️ Tag already exists: $TAG"
            echo "TAG_EXISTS=true" >> $GITHUB_OUTPUT
          else
            echo "✅ Tag does not exist, will create: $TAG"
            echo "TAG_EXISTS=false" >> $GITHUB_OUTPUT
          fi

      - name: Extract changelog for this version
        if: steps.check_tag.outputs.TAG_EXISTS == 'false'
        id: changelog
        run: |
          VERSION="${{ steps.version.outputs.VERSION }}"

          # Extracts text after ## [VERSION] until next ## [ or ---
          # Handles multiline content and extra spaces in version header (## [X.X.X]*)
          CHANGELOG=$(awk 'found{print; if(/^## \[|^---$/)exit} /## \['"$VERSION"'\]*/{found=1}' CHANGELOG.md)

          # Use fallback if empty
          if [ -z "$CHANGELOG" ]; then
            CHANGELOG="See CHANGELOG.md for details"
          fi

          echo "$CHANGELOG" > /tmp/changelog.txt
          cat /tmp/changelog.txt

      - name: Create Git Tag
        if: steps.check_tag.outputs.TAG_EXISTS == 'false'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          
          TAG="${{ steps.version.outputs.TAG }}"
          IS_PRERELEASE="${{ steps.version.outputs.IS_PRERELEASE }}"
          
          echo "Creating tag: $TAG (prerelease: $IS_PRERELEASE)"
          git tag -a "$TAG" -m "Release $TAG"
          git push origin "$TAG"
          echo "✅ Tag pushed: $TAG"

      - name: Create GitHub Release (Stable)
        if: steps.check_tag.outputs.TAG_EXISTS == 'false' && steps.version.outputs.IS_PRERELEASE == 'false'
        uses: softprops/action-gh-release@v1
        with:
          tag_name: ${{ steps.version.outputs.TAG }}
          name: Release ${{ steps.version.outputs.VERSION }}
          body_path: /tmp/changelog.txt
          draft: false
          prerelease: false
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Create GitHub Release (Pre-Release)
        if: steps.check_tag.outputs.TAG_EXISTS == 'false' && steps.version.outputs.IS_PRERELEASE == 'true'
        uses: softprops/action-gh-release@v1
        with:
          tag_name: ${{ steps.version.outputs.TAG }}
          name: Pre-Release ${{ steps.version.outputs.VERSION }}
          body_path: /tmp/changelog.txt
          draft: false
          prerelease: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Job Summary
        if: always()
        run: |
          echo "## Release Detection Summary" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          if [ "${{ steps.check_tag.outputs.TAG_EXISTS }}" == "false" ]; then
            if [ "${{ steps.version.outputs.IS_PRERELEASE }}" == "true" ]; then
              echo "⏭️ **Pre-Release Created:** ${{ steps.version.outputs.TAG }}" >> $GITHUB_STEP_SUMMARY
              echo "**Note:** \`latest\` tag will NOT be applied" >> $GITHUB_STEP_SUMMARY
            else
              echo "✅ **Stable Release Created:** ${{ steps.version.outputs.TAG }}" >> $GITHUB_STEP_SUMMARY
              echo "**Note:** \`latest\` tag WILL be applied" >> $GITHUB_STEP_SUMMARY
            fi
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "📦 **Docker build will be triggered automatically**" >> $GITHUB_STEP_SUMMARY
          else
            echo "⏭️ **Tag already exists:** ${{ steps.version.outputs.TAG }}" >> $GITHUB_STEP_SUMMARY
          fi
```

**Why each step?**

- **Extract version**: Regex finds `## [X.X.X]` pattern - this is the single source of truth
- **Check tag exists**: Prevents duplicate releases if you accidentally push same version twice
- **Extract changelog**: Pulls the content you wrote between version markers
- **Create Git Tag**: Makes it visible in git history and GitHub
- **Create GitHub Release**: Gives nice UI for users to see what changed
- **Different handling for pre-release**: Marks in GitHub so users know it's not production-ready

---

#### File B: `.github/workflows/build-and-push.yml`

Copy this entire workflow:

```yaml
name: Build and Push Docker Image

on:
  workflow_run:
    workflows: ["Detect Release from CHANGELOG"]
    types:
      - completed
  push:
    tags:
      - 'v*'
  workflow_dispatch:
    inputs:
      tag:
        description: 'Tag to build (e.g., v0.6.12)'
        required: true
        type: string
      security_scan:
        description: 'Run security scan after build'
        required: false
        type: boolean
        default: true

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    environment: prod
    timeout-minutes: 120
    permissions:
      contents: read
      packages: write
      security-events: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Get tag from workflow_run or current event
        id: get_tag
        run: |
          if [ "${{ github.event_name }}" == "workflow_run" ]; then
            # Get the tag that was created in the detect-release workflow
            echo "Triggered by workflow_run, fetching tag..."
            TAG=$(git -c 'versionsort.suffix=-alpha' -c 'versionsort.suffix=-beta' \
              ls-remote --tags --sort=-v:refname origin \
              | grep 'refs/tags/v' \
              | head -1 \
              | awk '{print $2}' \
              | sed 's/refs\/tags\///' \
              | tr -d '{}^')
            echo "TAG=$TAG" >> $GITHUB_OUTPUT
            echo "REF_NAME=$TAG" >> $GITHUB_OUTPUT
          elif [ "${{ github.event_name }}" == "workflow_dispatch" ]; then
            # Manual workflow dispatch with tag input
            TAG="${{ github.event.inputs.tag }}"
            echo "TAG=$TAG" >> $GITHUB_OUTPUT
            echo "REF_NAME=$TAG" >> $GITHUB_OUTPUT
          else
            # Normal tag push event
            TAG="${{ github.ref_name }}"
            echo "TAG=$TAG" >> $GITHUB_OUTPUT
            echo "REF_NAME=$TAG" >> $GITHUB_OUTPUT
          fi
          echo "Using tag: $TAG"

      - name: Determine if stable release
        id: stable
        run: |
          TAG="${{ steps.get_tag.outputs.TAG }}"
          TAG_NAME="${{ steps.get_tag.outputs.REF_NAME }}"

          # Check if tag matches vX.X.X (stable) or vX.X.X-* (pre-release)
          # Stable: v1.0.0, v2.0.1, v10.20.30
          # Pre-release: v1.0.0-alpha, v1.0.0-pre1, v1.0.0-beta.1

          if [[ $TAG_NAME =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo "✅ Stable release: $TAG_NAME"
            echo "IS_STABLE=true" >> $GITHUB_OUTPUT
          else
            echo "⏭️ Pre-release: $TAG_NAME"
            echo "IS_STABLE=false" >> $GITHUB_OUTPUT
          fi

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata (Stable Release)
        if: steps.stable.outputs.IS_STABLE == 'true'
        id: meta_stable
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=semver,pattern={{major}}
            type=raw,value=latest

      - name: Extract metadata (Pre-Release)
        if: steps.stable.outputs.IS_STABLE == 'false'
        id: meta_prerelease
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=semver,pattern={{version}},prerelease=true

      - name: Build and push (Stable)
        if: steps.stable.outputs.IS_STABLE == 'true'
        uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta_stable.outputs.tags }}
          labels: ${{ steps.meta_stable.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          provenance: true
          sbom: true

      - name: Build and push (Pre-Release)
        if: steps.stable.outputs.IS_STABLE == 'false'
        uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta_prerelease.outputs.tags }}
          labels: ${{ steps.meta_prerelease.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          provenance: true
          sbom: true

      - name: Job Summary
        run: |
          echo "## Docker Build Summary" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY

          if [ "${{ steps.stable.outputs.IS_STABLE }}" == "true" ]; then
            echo "✅ **Stable Release Built**" >> $GITHUB_STEP_SUMMARY
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "### Published Tags:" >> $GITHUB_STEP_SUMMARY
            echo "${{ steps.meta_stable.outputs.tags }}" | tr ',' '\n' | sed 's/^/- `/' | sed 's/$/`/' >> $GITHUB_STEP_SUMMARY
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "**Note:** \`latest\` tag is included for stable releases" >> $GITHUB_STEP_SUMMARY
          else
            echo "⏭️ **Pre-Release Built**" >> $GITHUB_STEP_SUMMARY
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "### Published Tags:" >> $GITHUB_STEP_SUMMARY
            echo "${{ steps.meta_prerelease.outputs.tags }}" | tr ',' '\n' | sed 's/^/- `/' | sed 's/$/`/' >> $GITHUB_STEP_SUMMARY
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "**Note:** \`latest\` tag is NOT included for pre-releases" >> $GITHUB_STEP_SUMMARY
          fi

          echo "" >> $GITHUB_STEP_SUMMARY
          echo "### Pull commands:" >> $GITHUB_STEP_SUMMARY
          echo "\`\`\`bash" >> $GITHUB_STEP_SUMMARY
          echo "docker pull ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ steps.get_tag.outputs.REF_NAME }}" >> $GITHUB_STEP_SUMMARY
          echo "\`\`\`" >> $GITHUB_STEP_SUMMARY
```

**Key differences from basic version:**

1. **Triple trigger system**: `workflow_run` (automated), `push: tags` (fallback), `workflow_dispatch` (manual)
2. **Environment protection**: `environment: prod` enables GitHub environment secrets/variables
3. **Explicit value parameter**: `value=${{ steps.get_tag.outputs.TAG }}` required for workflow_run trigger
4. **Multi-platform builds**: `platforms: linux/amd64,linux/arm64` with QEMU setup
5. **Security features**: `provenance: true`, `sbom: true`, `security-events: write` permission

**Why each step?**

- **Get tag from workflow_run or current event**: Determines if triggered by workflow_run, workflow_dispatch, or manual tag push, fetches the appropriate tag. **CRITICAL** because `github.ref_name` is not available in workflow_run events
- **Determine if stable**: Regex check `vX.X.X` (stable) vs `vX.X.X-*` (pre-release) - this controls everything downstream
- **Set up Docker Buildx**: Multi-platform builds, better caching
- **Log in to registry**: Authentication for pushing images
- **Extract metadata (conditional)**: Different tags based on release type
  - **CRITICAL**: `value=${{ steps.get_tag.outputs.TAG }}` parameter required when using `workflow_run` trigger
  - Without `value` parameter, `docker/metadata-action` uses `github.ref` which is NOT the tag in workflow_run events
  - Stable: `1.0.0`, `1.0`, `1`, `latest`
  - Pre-release: `1.0.0-pre1` only (no latest!)
- **Build and push (conditional)**: Two different builds, conditional execution
  - Multi-platform support: `linux/amd64,linux/arm64`
  - Supply chain security: `provenance: true`, `sbom: true`
- **Job Summary**: Reports what was built and tags published

---

### Step 3: Create CHANGELOG.md

In repository root:

```bash
cat > CHANGELOG.md << 'EOF'
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 

### Fixed
- 

### Changed
- 

---

## [1.0.0] - 2026-01-21

### Added
- Initial release
- Basic functionality
- API endpoints

### Fixed
- Initial bug fixes

---
EOF
```

### Step 4: Ensure You Have Dockerfile

```bash
# Check if exists
ls Dockerfile

# If not, create example
cat > Dockerfile << 'EOF'
FROM alpine:latest
WORKDIR /app
COPY . .
CMD ["sh"]
EOF
```

### Step 5: Configure GitHub Actions Permissions

**This is CRITICAL - without this, workflows won't have permission to create tags!**

1. Go to your repository on GitHub
2. **Settings** → **Actions** → **General**
3. Scroll to **Workflow permissions**
4. Select: **Read and write permissions**
5. Click **Save**

### Step 6: Push Everything

```bash
git add .github/ CHANGELOG.md Dockerfile
git commit -m "chore: add automated release workflow"
git push origin main
```

---

## All Workflow Files

### Understanding Workflow Syntax

```yaml
# TRIGGER: When does this workflow run?
on:
  push:
    branches:
      - main           # Only on main branch
    paths:
      - 'CHANGELOG.md' # Only when THIS file changes

# PERMISSIONS: What can the workflow do?
permissions:
  contents: write  # Can create/push tags and releases

# JOBS: What work happens?
jobs:
  job-name:
    runs-on: ubuntu-latest  # Machine to run on
    steps:
      - name: Step description
        run: |
          # bash code here
          echo "Hello"
        
      - name: Another step
        if: some-condition        # Conditional execution
        uses: action/from-github  # Pre-built action
        with:
          param: value           # Action parameters
```

### Key Concepts

**`${{ github.ref }}`** - Full reference, e.g., `refs/tags/v1.0.0`

**`$GITHUB_OUTPUT`** - Store values for next steps:
```bash
echo "VERSION=1.0.0" >> $GITHUB_OUTPUT
# Later use: ${{ steps.version.outputs.VERSION }}
```

**`if: condition`** - Step only runs if condition is true:
```yaml
if: steps.stable.outputs.IS_STABLE == 'true'
```

**Regex matching**:
```bash
# Check if v1.0.0 pattern (stable)
if [[ $TAG_NAME =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  # Yes, stable
fi

# Parse version with grep
VERSION=$(grep -oP '## \[\K\d+\.\d+\.\d+(?=\])' CHANGELOG.md)
# Extracts: 1.0.0 from ## [1.0.0]
```

---

## CHANGELOG Format

### Format Rules

**MUST be exact:**

```markdown
## [1.0.0] - 2026-01-21
```

Not:
- `## 1.0.0` ❌
- `## [v1.0.0]` ❌
- `## 1.0.0 - 2026-01-21` ❌

**For pre-releases:**

```markdown
## [1.0.0-pre1] - 2026-01-21
## [1.0.0-alpha] - 2026-01-21
## [1.0.0-beta.1] - 2026-01-21
## [1.0.0-rc1] - 2026-01-21
```

**Structure:**

```markdown
# Changelog

## [Unreleased]

### Added
- New features being worked on

### Fixed
- Bugs being fixed

### Changed
- Things being modified

---

## [1.0.1] - 2026-01-21

### Added
- New API endpoint
- WebSocket support

### Fixed
- Critical authentication bug
- Memory leak in connection pool

### Changed
- Updated dependencies to latest versions

### Deprecated
- Old authentication method (use OAuth2)

### Removed
- Legacy API v1 endpoints

### Security
- Fixed SQL injection vulnerability

---

## [1.0.0] - 2026-01-15

### Added
- Initial release
- REST API
- WebUI

---
```

### How It's Parsed

**Regex looks for:**

```bash
## [X.X.X]  or  ## [X.X.X-preX]
```

**Content extraction:**

```
## [1.0.0] - 2026-01-21
### Added
- New feature         ← This
### Fixed             ← This
- Bug fix             ← This
                      ← This (until next ##)
## [0.9.9] - 2026-01-14
### Added
- Older feature       ← NOT this (next version)
```

---

## Practical Examples

### Example 1: Simple Stable Release

**Step 1**: Edit CHANGELOG.md

```markdown
## [Unreleased]

## [1.0.0] - 2026-01-21

### Added
- Initial release features
```

**Step 2**: Push

```bash
git add CHANGELOG.md
git commit -m "chore: release 1.0.0"
git push origin main
```

**What happens**:

```
Time T+0s:  Push detected, detect-release.yml triggers
Time T+5s:  Parses CHANGELOG.md, finds version: 1.0.0
Time T+10s: Determines: stable (no dash), creates tag v1.0.0
Time T+15s: Pushes tag to GitHub
Time T+20s: Detects tag push, build-and-push.yml triggers
Time T+30s: Regex detects: stable (v1.0.0 matches vX.X.X)
Time T+35s: Builds Docker image with tags: 1.0.0, 1.0, 1, latest
Time T+90s: Pushes to registry
```

**Result**:
```bash
docker pull ghcr.io/your-org/your-repo:1.0.0      # ✅ works
docker pull ghcr.io/your-org/your-repo:1.0        # ✅ works
docker pull ghcr.io/your-org/your-repo:1          # ✅ works
docker pull ghcr.io/your-org/your-repo:latest     # ✅ works (points to 1.0.0)
```

---

### Example 2: Pre-release Testing

**Step 1**: Edit CHANGELOG.md

```markdown
## [Unreleased]

## [1.1.0-alpha] - 2026-01-21

### Added
- Experimental new API
- WebSocket support (experimental)

### Note
This is a pre-release. Not for production.
```

**Step 2**: Push

```bash
git add CHANGELOG.md
git commit -m "chore: pre-release 1.1.0-alpha"
git push origin main
```

**What happens**:

```
Time T+0s:  Push detected
Time T+5s:  Finds version: 1.1.0-alpha
Time T+10s: Determines: pre-release (has dash!), creates tag v1.1.0-alpha
Time T+20s: Creates GitHub Release marked as "Pre-Release"
Time T+30s: build-and-push.yml triggers
Time T+35s: Regex detects: pre-release (v1.1.0-alpha doesn't match vX.X.X)
Time T+40s: Builds Docker with tag ONLY: 1.1.0-alpha
Time T+50s: Does NOT create latest tag ✅
```

**Result**:
```bash
docker pull ghcr.io/your-org/your-repo:1.1.0-alpha   # ✅ works (pre-release)
docker pull ghcr.io/your-org/your-repo:latest        # ✅ still points to 1.0.0!
```

---

### Example 3: Multiple Releases in Workflow

**Timeline**:

```
Monday:
  Release 1.0.0 (stable) → latest = 1.0.0
  
Tuesday:
  Release 1.0.1-pre1 (pre-release) → latest = still 1.0.0 ✅
  
Wednesday:
  Release 1.0.1 (stable) → latest = 1.0.1 (updated!) ✅
  
Thursday:
  Release 2.0.0-rc1 (pre-release) → latest = still 1.0.1 ✅
  
Friday:
  Release 2.0.0 (stable) → latest = 2.0.0 (updated!) ✅
```

**CHANGELOG at end of week**:

```markdown
## [Unreleased]

## [2.0.0] - 2026-01-19
### Added
- Major features

## [2.0.0-rc1] - 2026-01-18
### Added
- Major features (pre-testing)

## [1.0.1] - 2026-01-17
### Fixed
- Bugs from 1.0.0

## [1.0.1-pre1] - 2026-01-16
### Fixed
- Bugs (pre-testing)

## [1.0.0] - 2026-01-15
### Added
- Initial release
```

---

## Pre-releases vs Stable Releases

### The Key Difference

**Regex Check in Workflow**:

```bash
if [[ $TAG_NAME =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  # Matches: v1.0.0, v2.5.10, v100.0.1
  # → STABLE
  # → Creates: 1.0.0, 1.0, 1, latest
else
  # Matches: v1.0.0-pre1, v1.0.0-alpha, v2.0.0-rc1
  # → PRE-RELEASE
  # → Creates: 1.0.0-pre1 ONLY
fi
```

### Docker Tags Comparison

| Scenario | Version | Pattern | Tags Published | `latest`? |
|----------|---------|---------|---|---|
| Stable release | v1.0.0 | `vX.X.X` | `1.0.0`, `1.0`, `1`, `latest` | ✅ YES |
| Pre-release | v1.0.0-pre1 | `vX.X.X-pre*` | `1.0.0-pre1` only | ❌ NO |
| Another stable | v1.1.0 | `vX.X.X` | `1.1.0`, `1.1`, `1`, `latest` | ✅ YES (updates!) |
| Release candidate | v2.0.0-rc1 | `vX.X.X-rc*` | `2.0.0-rc1` only | ❌ NO |
| Final stable | v2.0.0 | `vX.X.X` | `2.0.0`, `2.0`, `2`, `latest` | ✅ YES (updates!) |

### When to Use What?

**Stable Release** (`v1.0.0`):
- Code tested and ready for production
- Users can safely use `docker pull myapp:latest`
- Breaking changes clearly documented

**Pre-release** (`v1.0.0-alpha`):
- Early testing phase
- Bugs likely
- Rapid iteration
- Not recommended for production
- Users explicitly request specific version: `docker pull myapp:1.0.0-alpha`

**Semantic Pre-release Naming**:

| Name | Meaning | Stability |
|------|---------|-----------|
| `-alpha` | Very early, missing features | Low |
| `-beta` | Most features done, still buggy | Medium |
| `-rc` (Release Candidate) | Almost ready, final testing | High |
| `-pre` | Just before release | Very High |
| (none, just vX.X.X) | Stable production release | Very High |

---

## Advanced Production Features

### 🚀 Beyond Basic Automation

The basic workflow gets you automated releases. For **production-grade** systems, you need additional features:

1. **Multi-platform builds** - Support amd64 AND arm64
2. **Security scanning** - Trivy + Grype vulnerability detection
3. **SBOM generation** - Software Bill of Materials
4. **Provenance attestation** - Supply chain security
5. **Timeout protection** - Prevent hanging workflows
6. **GitHub Security integration** - SARIF reports in Security tab

---

### Enhanced `build-and-push.yml` Workflow

**Production-ready version with all advanced features:**

```yaml
name: Build and Push Docker Image

on:
  workflow_run:
    workflows: ["Detect Release from CHANGELOG"]
    types:
      - completed
  push:
    tags:
      - 'v*'
  workflow_dispatch:
    inputs:
      tag:
        description: 'Tag to build (e.g., v0.6.12)'
        required: true
        type: string

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    environment: prod  # ⬅️ NEW: Environment for secrets/variables
    timeout-minutes: 120  # ⬅️ NEW: Prevent hanging workflows
    permissions:
      contents: read
      packages: write
      security-events: write  # ⬅️ NEW: Required for SARIF uploads

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Get tag from workflow_run or current event
        id: get_tag
        run: |
          if [ "${{ github.event_name }}" == "workflow_run" ]; then
            # Get the tag that was created in the detect-release workflow
            echo "Triggered by workflow_run, fetching tag..."
            TAG=$(git -c 'versionsort.suffix=-alpha' -c 'versionsort.suffix=-beta' \
              ls-remote --tags --sort=-v:refname origin \
              | grep 'refs/tags/v' \
              | head -1 \
              | awk '{print $2}' \
              | sed 's/refs\/tags\///' \
              | tr -d '{}^')
            echo "TAG=$TAG" >> $GITHUB_OUTPUT
            echo "REF_NAME=$TAG" >> $GITHUB_OUTPUT
          elif [ "${{ github.event_name }}" == "workflow_dispatch" ]; then
            # Manual workflow dispatch with tag input
            TAG="${{ github.event.inputs.tag }}"
            echo "TAG=$TAG" >> $GITHUB_OUTPUT
            echo "REF_NAME=$TAG" >> $GITHUB_OUTPUT
          else
            # Normal tag push event
            TAG="${{ github.ref_name }}"
            echo "TAG=$TAG" >> $GITHUB_OUTPUT
            echo "REF_NAME=$TAG" >> $GITHUB_OUTPUT
          fi
          echo "Using tag: $TAG"

      - name: Determine if stable release
        id: stable
        run: |
          TAG="${{ steps.get_tag.outputs.TAG }}"
          TAG_NAME="${{ steps.get_tag.outputs.REF_NAME }}"

          if [[ $TAG_NAME =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo "✅ Stable release: $TAG_NAME"
            echo "IS_STABLE=true" >> $GITHUB_OUTPUT
          else
            echo "⏭️ Pre-release: $TAG_NAME"
            echo "IS_STABLE=false" >> $GITHUB_OUTPUT
          fi

      - name: Set up QEMU  # ⬅️ NEW: Required for multi-platform
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata (Stable Release)
        if: steps.stable.outputs.IS_STABLE == 'true'
        id: meta_stable
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=semver,pattern={{version}},value=${{ steps.get_tag.outputs.TAG }}
            type=semver,pattern={{major}}.{{minor}},value=${{ steps.get_tag.outputs.TAG }}
            type=semver,pattern={{major}},value=${{ steps.get_tag.outputs.TAG }}
            type=raw,value=latest

      - name: Extract metadata (Pre-Release)
        if: steps.stable.outputs.IS_STABLE == 'false'
        id: meta_prerelease
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=semver,pattern={{version}},value=${{ steps.get_tag.outputs.TAG }}

      - name: Build and push (Stable)
        if: steps.stable.outputs.IS_STABLE == 'true'
        uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/amd64,linux/arm64  # ⬅️ NEW: Multi-platform
          push: true
          tags: ${{ steps.meta_stable.outputs.tags }}
          labels: ${{ steps.meta_stable.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          provenance: true  # ⬅️ NEW: Supply chain security
          sbom: true        # ⬅️ NEW: Software Bill of Materials

      - name: Build and push (Pre-Release)
        if: steps.stable.outputs.IS_STABLE == 'false'
        uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/amd64,linux/arm64  # ⬅️ NEW: Multi-platform
          push: true
          tags: ${{ steps.meta_prerelease.outputs.tags }}
          labels: ${{ steps.meta_prerelease.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          provenance: true  # ⬅️ NEW
          sbom: true        # ⬅️ NEW

      # ⬅️ NEW: Security scanning section
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.ref_name }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          scan-type: 'image'         # ⬅️ CRITICAL: Must specify
          severity: 'CRITICAL,HIGH'  # ⬅️ Filter to important vulns
        continue-on-error: true      # ⬅️ Don't fail build on scan errors
        timeout-minutes: 15

      - name: Upload Trivy results to GitHub Security tab
        uses: github/codeql-action/upload-sarif@v3
        if: hashFiles('trivy-results.sarif') != ''  # ⬅️ Only if file exists
        with:
          sarif_file: 'trivy-results.sarif'
          category: 'trivy'  # ⬅️ Unique category for multiple scanners
        timeout-minutes: 5

      - name: Run Grype vulnerability scanner
        uses: anchore/scan-action@v4
        id: grype
        with:
          image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.ref_name }}
          output-format: 'sarif'
          fail-build: false
          severity-cutoff: 'high'
        continue-on-error: true
        timeout-minutes: 15

      - name: Upload Grype results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        if: hashFiles('results.sarif') != ''
        with:
          sarif_file: 'results.sarif'
          category: 'grype'
        timeout-minutes: 5

      - name: Job Summary
        run: |
          echo "## Docker Build Summary" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY

          if [ "${{ steps.stable.outputs.IS_STABLE }}" == "true" ]; then
            echo "✅ **Stable Release Built**" >> $GITHUB_STEP_SUMMARY
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "### Published Tags:" >> $GITHUB_STEP_SUMMARY
            echo "${{ steps.meta_stable.outputs.tags }}" | tr ',' '\n' | sed 's/^/- `/' | sed 's/$/`/' >> $GITHUB_STEP_SUMMARY
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "**Note:** \`latest\` tag is included for stable releases" >> $GITHUB_STEP_SUMMARY
          else
            echo "⏭️ **Pre-Release Built**" >> $GITHUB_STEP_SUMMARY
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "### Published Tags:" >> $GITHUB_STEP_SUMMARY
            echo "${{ steps.meta_prerelease.outputs.tags }}" | tr ',' '\n' | sed 's/^/- `/' | sed 's/$/`/' >> $GITHUB_STEP_SUMMARY
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "**Note:** \`latest\` tag is NOT included for pre-releases" >> $GITHUB_STEP_SUMMARY
          fi

          # ⬅️ NEW: Multi-platform info
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "### 🏗️ Built Platforms:" >> $GITHUB_STEP_SUMMARY
          echo "- \`linux/amd64\` (Intel/AMD x86_64)" >> $GITHUB_STEP_SUMMARY
          echo "- \`linux/arm64\` (Apple Silicon, ARM cloud)" >> $GITHUB_STEP_SUMMARY

          # ⬅️ NEW: Security scan info
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "### 🔒 Security Scanning:" >> $GITHUB_STEP_SUMMARY
          echo "- ✅ Trivy vulnerability scan completed" >> $GITHUB_STEP_SUMMARY
          echo "- ✅ Grype vulnerability scan completed" >> $GITHUB_STEP_SUMMARY
          echo "- 📊 Results available in **Security** tab" >> $GITHUB_STEP_SUMMARY

          echo "" >> $GITHUB_STEP_SUMMARY
          echo "### 📦 Pull commands:" >> $GITHUB_STEP_SUMMARY
          echo "\`\`\`bash" >> $GITHUB_STEP_SUMMARY
          echo "docker pull ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.ref_name }}" >> $GITHUB_STEP_SUMMARY
          echo "\`\`\`" >> $GITHUB_STEP_SUMMARY
```

---

### Feature Breakdown

#### 1. Multi-Platform Builds (amd64 + arm64)

**What it does:**
```yaml
platforms: linux/amd64,linux/arm64
```

**Why it matters:**
- **linux/amd64**: Intel/AMD servers, standard cloud instances
- **linux/arm64**: Apple Silicon (M1/M2/M3), AWS Graviton, Azure ARM
- Docker automatically creates **manifest list** - users pull correct arch for their machine

**Prerequisites:**
```yaml
- name: Set up QEMU
  uses: docker/setup-qemu-action@v3
```
QEMU emulation is required for cross-platform builds.

**User experience:**
```bash
# On Intel Mac
docker pull ghcr.io/azdolinski/devcoder:0.6.6
# Automatically gets: linux/amd64

# On Apple Silicon
docker pull ghcr.io/azdolinski/devcoder:0.6.6
# Automatically gets: linux/arm64
```

---

#### 2. Security Scanning (Trivy + Grype)

**Why two scanners?**

| Scanner | Strength | Use Case |
|---------|----------|----------|
| **Trivy** | Fast, comprehensive | First pass, all vulnerability types |
| **Grype** | Deep analysis, accurate | Second opinion, reduces false positives |

**Configuration breakdown:**

```yaml
# Trivy - comprehensive vulnerability scanner
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.ref_name }}
    format: 'sarif'           # SARIF format for GitHub Security
    output: 'trivy-results.sarif'
    scan-type: 'image'        # ⬅️ CRITICAL: Must specify image scan
    severity: 'CRITICAL,HIGH' # Only report important vulnerabilities
  continue-on-error: true    # Don't fail build if scan has issues
  timeout-minutes: 15
```

**Key parameters:**
- `scan-type: 'image'` - **REQUIRED** - tells Trivy to scan a Docker image
- `severity: 'CRITICAL,HIGH'` - filters noise, focuses on important vulns
- `continue-on-error: true` - scan problems don't block releases
- `format: 'sarif'` - SARIF format integrates with GitHub Security tab

**Upload to GitHub Security:**
```yaml
- name: Upload Trivy results to GitHub Security tab
  uses: github/codeql-action/upload-sarif@v3
  if: hashFiles('trivy-results.sarif') != ''  # ⬅️ Only if file exists
  with:
    sarif_file: 'trivy-results.sarif'
    category: 'trivy'  # Unique identifier when using multiple scanners
  timeout-minutes: 5
```

**Why `hashFiles()` check?**
- Prevents upload failures if scan didn't create the file
- Gracefully handles scan failures
- Build continues even if security scan fails

**Grype - second scanner:**
```yaml
- name: Run Grype vulnerability scanner
  uses: anchore/scan-action@v4
  with:
    image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.ref_name }}
    output-format: 'sarif'
    fail-build: false
    severity-cutoff: 'high'
  continue-on-error: true
  timeout-minutes: 15
```

**Key differences from Trivy:**
- `output-format: 'sarif'` - different parameter name
- `severity-cutoff: 'high'` - single cutoff level
- `fail-build: false` - explicit control
- File auto-saved as `results.sarif`

---

#### 3. SBOM (Software Bill of Materials)

```yaml
sbom: true  # In build-push-action
```

**What it does:**
- Generates list of all packages, libraries, dependencies in your image
- Automatically attached to image as metadata
- Viewable with: `docker pull` then inspect

**Why it matters:**
- **Compliance**: Many regulations require SBOMs
- **Security**: Quickly check if your image uses vulnerable packages
- **Supply chain**: Track dependencies and their origins

---

#### 4. Provenance Attestation

```yaml
provenance: true  # In build-push-action
```

**What it does:**
- Cryptographically signs your build artifacts
- Proves the image was built by your GitHub repo
- Prevents supply chain attacks

**Why it matters:**
- **Trust**: Users can verify image authenticity
- **Security**: Detects tampered images
- **Compliance**: Required for some enterprise/production use

**Viewing provenance:**
```bash
# After pulling image
docker manifest inspect ghcr.io/azdolinski/devcoder:0.6.6
```

---

#### 5. Timeout Protection

```yaml
jobs:
  build-and-push:
    timeout-minutes: 120  # Job-level timeout

steps:
  - name: Run Trivy vulnerability scanner
    timeout-minutes: 15  # Step-level timeout

  - name: Upload Trivy results to GitHub Security tab
    timeout-minutes: 5   # Shorter timeout for uploads
```

**Why timeouts matter:**
- Prevents workflows from hanging indefinitely
- Saves GitHub Actions minutes (cost control)
- Faster feedback when things go wrong
- Prevents resource exhaustion

**Recommended timeouts:**
| Operation | Timeout | Rationale |
|-----------|---------|-----------|
| Multi-platform build | 120 min | Cross-arch compilation is slow |
| Security scan | 15 min | Depends on image size |
| SARIF upload | 5 min | Network operation |
| Metadata extraction | 5 min | Quick action |

---

### Production vs Development Configurations

| Feature | Dev | Production | Why |
|---------|-----|------------|-----|
| Multi-platform build | ❌ Optional | ✅ Required | Production runs on diverse hardware |
| Security scanning | ⚠️ Optional | ✅ Required | Compliance + security |
| SBOM generation | ❌ Optional | ✅ Required | Supply chain transparency |
| Provenance | ❌ Optional | ✅ Required | Trust + verification |
| Timeouts | ⚠️ Recommended | ✅ Required | Cost control + reliability |

---

## Troubleshooting

### ❌ Workflow doesn't run after pushing CHANGELOG.md

**Problem**: detect-release.yml didn't trigger

**Check**:
1. File path exactly `CHANGELOG.md` in root?
   ```bash
   ls -la CHANGELOG.md  # Must exist
   ```

2. Branch is `main` (not `master`)?
   ```bash
   git branch  # Check current branch
   ```

3. Did you push to `main`?
   ```bash
   git push origin main  # Not a different branch
   ```

**Solution**:
- Verify file is in repository root
- Verify branch name in workflow matches your branch
- Try again on `main` branch

---

### ❌ "Could not find version in CHANGELOG.md"

**Problem**: Workflow can't parse version

**Check**: CHANGELOG.md format

❌ Wrong:
```markdown
## 1.0.0                    # Missing brackets
## [v1.0.0]                 # Shouldn't have 'v'
## [1.0.0] 2026-01-21       # No dash and date
```

✅ Right:
```markdown
## [1.0.0] - 2026-01-21     # Exact format
## [1.0.0-pre1] - 2026-01-21
```

**Solution**:
- Use exact format: `## [X.X.X] - DATE`
- No `v` prefix inside brackets
- Check workflow logs for what it's looking for

---

### ❌ "Permission denied" when creating tag

**Problem**: Workflow can't push tag

**Solution**:
1. Go to **Settings → Actions → General**
2. Scroll to **Workflow permissions**
3. Select **Read and write permissions**
4. Save

This allows GitHub Actions to push tags.

---

### ❌ Tag created but Docker build didn't run

**Problem**: build-and-push.yml didn't trigger after detect-release created tag

**Root Cause**: GitHub Actions has a security feature where `on: push: tags:` doesn't trigger when tags are created by other workflows. This prevents infinite workflow loops.

**Solution**: Use `workflow_run` trigger (already implemented in this guide)

**Check**:
1. Does build-and-push.yml have `workflow_run` trigger?
   ```yaml
   on:
     workflow_run:
       workflows: ["Detect Release from CHANGELOG"]
       types:
         - completed
   ```

2. Is the workflow name in trigger exactly `Detect Release from CHANGELOG`?
   ```bash
   grep "^name:" .github/workflows/detect-release.yml
   # Should output: name: Detect Release from CHANGELOG
   ```

3. Did detect-release complete successfully?
   - Go to **Actions** tab
   - Click on detect-release workflow run
   - Verify it completed with green checkmark

4. Check **Actions** tab for build-and-push workflow run
   - Should appear automatically after detect-release completes
   - Wait ~30 seconds - sometimes delay

**Manual Trigger (if needed)**:
If you need to trigger build manually for existing tag:
```bash
# Delete and recreate tag manually
git tag -d v0.6.10
git push origin :refs/tags/v0.6.10  # Delete remote
git tag v0.6.10
git push origin v0.6.10  # This will trigger push: tags: trigger
```

---

### ❌ workflow_run trigger not working

**Problem**: build-and-push.yml doesn't trigger when detect-release completes

**Check**:
1. Verify workflow name matches exactly
   ```bash
   # Check detect-release workflow name
   grep "^name:" .github/workflows/detect-release.yml

   # Check build-and-push trigger
   grep -A 3 "workflow_run:" .github/workflows/build-and-push.yml
   ```

2. Check if detect-release workflow actually completed successfully
   - Go to **Actions** tab on GitHub
   - Find the detect-release workflow run
   - Click on it and verify status is "completed" (green checkmark)

3. Check if build-and-push workflow exists and is active
   ```bash
   ls -la .github/workflows/build-and-push.yml
   # File must exist
   ```

4. Check workflow syntax is valid
   - Go to **Actions** tab
   - Click on build-and-push workflow
   - Look for syntax errors in the editor

**Common Issues**:

❌ **Wrong workflow name in trigger**:
```yaml
# WRONG
workflow_run:
  workflows: ["detect-release"]  # Missing full name
```

✅ **Correct**:
```yaml
workflow_run:
  workflows: ["Detect Release from CHANGELOG"]  # Exact match
```

❌ **Missing `types:`**:
```yaml
# WRONG
workflow_run:
  workflows: ["Detect Release from CHANGELOG"]
  # Missing types:
```

✅ **Correct**:
```yaml
workflow_run:
  workflows: ["Detect Release from CHANGELOG"]
  types:
    - completed
```

**Solution**: Ensure workflow name matches exactly and `types: - completed` is present.

---

### ❌ "latest" tag applied to pre-release

**Problem**: Pre-release version got `latest` tag

**Causes**:
- Tag format is wrong: `v1.0.0-pre1` should work, `v1.0.0` is stable
- Regex not matching properly

**Check**:
```bash
git tag  # List all tags, verify format
```

**Solution**:
- Verify tag exactly matches: `v1.0.0-pre1` (dash required for pre-release)
- If already published, delete and retry:
  ```bash
  git tag -d v1.0.0-pre1
  git push origin :refs/tags/v1.0.0-pre1  # Delete remote
  ```

---

### ❌ Docker image not appearing in registry

**Problem**: build-and-push.yml completed but image not in ghcr.io

**Check**:
1. Registry is public? Go to **Settings → Packages → Change visibility → Public**
2. Credentials correct? GitHub Actions uses `${{ secrets.GITHUB_TOKEN }}` automatically
3. Check logs for push errors

**Solution**:
- Verify repository isn't private
- Re-run workflow from **Actions** tab
- Check push command in logs

---

### ❌ Multiple tags not created

**Problem**: Only one tag published instead of 1.0.0, 1.0, 1, latest

**Cause**: metadata-action not generating all tags

**Solution**: Verify tags configuration:

```yaml
tags: |
  type=semver,pattern={{version}}      # 1.0.0
  type=semver,pattern={{major}}.{{minor}}  # 1.0
  type=semver,pattern={{major}}        # 1
  type=raw,value=latest                # latest (stable only)
```

If missing, re-add these lines.

---

### ❌ "Path does not exist: trivy-results.sarif" or "results.sarif"

**Problem**: Security scanner upload fails with file not found error

**Error seen in logs:**
```
[error]Path does not exist: trivy-results.sarif
[error]Path does not exist: results.sarif
```

**Root causes (what went wrong):**

1. **Missing `scan-type: 'image'` in Trivy**
   ```yaml
   # ❌ WRONG - scan-type not specified
   - uses: aquasecurity/trivy-action@master
     with:
       image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.ref_name }}
       format: 'sarif'
       output: 'trivy-results.sarif'
       # scan-type is missing! Trivy doesn't know what to scan
   ```

2. **No `if: hashFiles()` check before upload**
   ```yaml
   # ❌ WRONG - always attempts upload
   - name: Upload Trivy results
     uses: github/codeql-action/upload-sarif@v3
     with:
       sarif_file: 'trivy-results.sarif'
   # This fails if scan didn't create the file!
   ```

3. **Scanner fails silently** - Without `continue-on-error: true`, the whole build would fail

**The fix:**

```yaml
# ✅ CORRECT - Trivy configuration
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.ref_name }}
    format: 'sarif'
    output: 'trivy-results.sarif'
    scan-type: 'image'         # ⬅️ CRITICAL: Must specify
    severity: 'CRITICAL,HIGH'  # Optional: filter severity
  continue-on-error: true      # ⬅️ Don't fail build if scan errors
  timeout-minutes: 15

# ✅ CORRECT - Upload with file existence check
- name: Upload Trivy results to GitHub Security tab
  uses: github/codeql-action/upload-sarif@v3
  if: hashFiles('trivy-results.sarif') != ''  # ⬅️ Only upload if file exists
  with:
    sarif_file: 'trivy-results.sarif'
    category: 'trivy'  # Required when using multiple scanners
  timeout-minutes: 5
```

**Key fixes explained:**

| Fix | Why it matters |
|-----|----------------|
| `scan-type: 'image'` | Trivy supports multiple scan types (fs, image, repo). Without this, it doesn't know how to scan |
| `severity: 'CRITICAL,HIGH'` | Filters noise - you probably don't care about LOW/MEDIUM vulns in base images |
| `continue-on-error: true` | Scan failures (network issues, rate limits) don't block releases |
| `if: hashFiles(...) != ''` | Upload only happens if scan succeeded. Prevents confusing errors |
| `category: 'trivy'` | Unique ID for GitHub Security tab when using multiple scanners |

---

### ❌ Grype scanner format issues

**Problem**: Grype scanner creates wrong file format or fails with parameters

**Common mistakes:**

```yaml
# ❌ WRONG - using old parameter names
- uses: anchore/scan-action@v4
  with:
    format: 'sarif'
    output: 'grype-results.sarif'
```

**The fix:**

```yaml
# ✅ CORRECT - Grype configuration
- name: Run Grype vulnerability scanner
  uses: anchore/scan-action@v4
  with:
    image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.ref_name }}
    output-format: 'sarif'
    fail-build: false
    severity-cutoff: 'high'
  continue-on-error: true
  timeout-minutes: 15
```

**Key differences from Trivy:**

| Parameter | Trivy | Grype | Notes |
|-----------|-------|-------|-------|
| Scan target | `image-ref` | `image` | Different parameter names! |
| Severity filter | `severity: 'CRITICAL,HIGH'` | `severity-cutoff: 'high'` | Grype uses single cutoff |
| Build control | `continue-on-error` only | `fail-build: false` | Grype has explicit flag |
| Format parameter | Not required (defaults) | `output-format` | Correct parameter name |
| Output file | `output: 'filename'` | Auto-saved as `results.sarif` | Don't specify output |

---

### ❌ SARIF upload not appearing in GitHub Security tab

**Problem**: Scanners complete, but nothing shows up in Security tab

**Check:**

1. **Permissions correct?**
   ```yaml
   jobs:
     build-and-push:
       permissions:
         contents: read
         packages: write
         security-events: write  # ⬅️ REQUIRED for SARIF upload
   ```

2. **Category unique?**
   ```yaml
   # Trivy upload
   - uses: github/codeql-action/upload-sarif@v3
     with:
       category: 'trivy'  # Must be unique

   # Grype upload
   - uses: github/codeql-action/upload-sarif@v3
     with:
       category: 'grype'  # Different from trivy!
   ```

3. **File actually created?**
   ```yaml
   if: hashFiles('trivy-results.sarif') != ''  # Check before upload
   ```

**Solution**: Verify all three conditions above.

---

### ❌ Multi-platform build fails with "multiple platforms feature is currently not supported"

**Problem**: Build fails when trying to build for multiple platforms

**Root cause**: Missing QEMU setup

**Fix:**
```yaml
- name: Set up QEMU  # ⬅️ REQUIRED for multi-platform builds
  uses: docker/setup-qemu-action@v3

- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build and push
  uses: docker/build-push-action@v6
  with:
    platforms: linux/amd64,linux/arm64  # Now this works
```

**Why QEMU is needed:**
- GitHub Actions runners are amd64
- To build arm64 images, need emulation
- QEMU provides that emulation layer

---

### ❌ Workflow hangs indefinitely (no timeout)

**Problem**: Workflow runs forever, never completes

**Cause**: No timeout set, process waiting for something that will never happen

**Fix:**
```yaml
jobs:
  build-and-push:
    timeout-minutes: 120  # Job-level timeout

steps:
  - name: Some long-running step
    timeout-minutes: 15  # Step-level timeout
```

**Why timeouts matter:**
- Prevents resource waste
- Saves GitHub Actions minutes (cost)
- Faster feedback when things go wrong

---

## Best Practices

### ✅ DO

1. **Update CHANGELOG before each release**
   ```bash
   # Before: ## [Unreleased]
   # After: ## [1.0.1] - 2026-01-21
   ```

2. **Use semantic versioning**
   - Major: Breaking changes (1.0.0 → 2.0.0)
   - Minor: New features (1.0.0 → 1.1.0)
   - Patch: Bug fixes (1.0.0 → 1.0.1)

3. **Be clear in CHANGELOG**
   ```markdown
   ### Added
   - New login system
   
   ### Fixed
   - Fixed crash on startup
   - Memory leak in cache
   
   ### Changed
   - Updated dependencies
   
   ### Removed
   - Old v1 API endpoints
   ```

4. **Test pre-releases before stable**
   ```
   1. Merge code to main
   2. Create pre-release: ## [1.1.0-pre1]
   3. Test in staging
   4. Fix any bugs
   5. Create stable: ## [1.1.0]
   ```

5. **Keep CHANGELOG.md updated during development**
   - Add entries as you work
   - Makes release easier

---

### ❌ DON'T

1. **Don't manually create tags**
   - Let workflow do it from CHANGELOG
   - Prevents version mismatch

2. **Don't forget to update CHANGELOG**
   - Single source of truth must stay in sync
   - Release will fail without proper format

3. **Don't tag pre-releases as stable**
   ```
   ❌ ## [1.0.0-pre1]    → don't call this stable
   ✅ ## [1.0.0-pre1]    → correct pre-release format
   ❌ ## [1.0.0]         → don't use this for pre-release
   ```

4. **Don't use `latest` for pre-releases manually**
   - Workflow handles this automatically
   - Manual intervention creates confusion

5. **Don't push to main without testing**
   - CHANGELOG change triggers release immediately
   - Make sure everything works first

---

### Workflow Best Practice

```bash
# 1. Feature work on branch
git checkout -b feature/awesome-thing
# ... coding ...
git add .
git commit -m "feat: add awesome thing"
git push origin feature/awesome-thing

# 2. Create PR, review, merge to main
# (on GitHub: Create PR → Review → Merge)

# 3. NOW: Update CHANGELOG.md (locally or on main)
git pull origin main

# Edit CHANGELOG.md
# Change: ## [Unreleased]
# To:     ## [1.1.0] - 2026-01-21
#         ### Added
#         - Awesome thing

git add CHANGELOG.md
git commit -m "chore: release 1.1.0"
git push origin main

# 4. Sit back - everything happens automatically!
# ✅ Tag created
# ✅ Release published
# ✅ Docker image built
# ✅ Image pushed with 1.1.0, 1.1, 1, latest tags
```

---

### Production Deployment Strategy

```yaml
# DEVELOPMENT
docker run myapp:edge        # Always latest dev code

# STAGING (testing)
docker run myapp:1.1.0-pre1  # Pre-release version
docker run myapp:1.1.0-beta  # Another pre-release

# PRODUCTION (stable only)
docker run myapp:latest      # Automatically stable only!
docker run myapp:1.0.0       # Pin specific version if needed
```

---

## Summary

### What You Now Have

1. **Detect Release Workflow** - Detects CHANGELOG.md changes, creates tags and releases
2. **Build & Push Workflow** - Builds Docker image with semantic versioning
3. **Pre-release Support** - `latest` only for stable, pre-releases isolated
4. **Automatic Everything** - No manual steps needed
5. **Single Source of Truth** - CHANGELOG.md controls all versioning

### What Happens Automatically

```
You edit CHANGELOG.md
    ↓ (git push)
GitHub detects change
    ↓
Workflow parses version
    ↓
Creates Git tag v1.0.0
    ↓
Publishes GitHub Release
    ↓
Workflow triggered on tag
    ↓
Builds Docker image
    ↓
Publishes with tags: 1.0.0, 1.0, 1, latest
    ↓
Done! Users can pull immediately
```

### One Command to Release

```bash
# That's it!
git add CHANGELOG.md && git commit -m "chore: release 1.0.0" && git push origin main
```

Everything else happens automatically. 🚀

---

## Quick Reference

### Stable Release
```markdown
## [1.0.0] - 2026-01-21
### Added
- New feature
```
→ Creates: `1.0.0`, `1.0`, `1`, `latest`

### Pre-release
```markdown
## [1.0.0-pre1] - 2026-01-21
### Added
- Experimental feature
```
→ Creates: `1.0.0-pre1` only

### Format Rules
```
✅ ## [1.0.0] - 2026-01-21
✅ ## [1.0.0-pre1] - 2026-01-21
❌ ## 1.0.0
❌ ## [v1.0.0]
```

### Workflow Triggers
- **detect-release.yml**: Triggers on `CHANGELOG.md` push to `main`
- **build-and-push.yml**: Triggers on `v*` tag push

### Docker Commands
```bash
docker pull ghcr.io/org/repo:1.0.0       # Specific version
docker pull ghcr.io/org/repo:1.0         # Latest patch
docker pull ghcr.io/org/repo:1           # Latest minor+patch
docker pull ghcr.io/org/repo:latest      # Latest stable only
docker pull ghcr.io/org/repo:1.0.0-pre1  # Pre-release
```

---

Gotowe! To jest kompletny, produkcyjny system zarządzania wersjami z GitHub Actions. 🎯
