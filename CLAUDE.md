# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DevCoder is a containerized development environment based on [linuxserver/vscodium-web](https://github.com/linuxserver/docker-vscodium). It provides VSCodium IDE accessible via web browser with pre-installed development tools, extensions, and services.

## Build & Run Commands

### Local Development
```bash
# Build the image
docker build -t devcoder .

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Release Workflow
Releases are automated via GitHub Actions when `CHANGELOG.md` is updated:
1. Update `CHANGELOG.md` with new version (format: `## [X.X.X]`)
2. Commit and push to `main` branch
3. `.github/workflows/detect-release.yml` triggers automatically
4. Creates git tag `vX.X.X` and GitHub release
5. Triggers `.github/workflows/build-and-push.yml` to build Docker image
6. Triggers `.github/workflows/security-scan.yml` for security scanning

### Manual Workflow Trigger
```bash
# Manually trigger security scan
gh workflow run security-scan.yml -f image_ref=ghcr.io/azdolinski/devcoder:v0.6.8 -f severity=HIGH

# Check workflow status
gh run list --workflow=security-scan.yml
gh run view <run-id>
```

## Architecture

### Container Stack
- **Xvfb**: X11 server (DISPLAY)
- **Openbox**: Window manager
- **Selkies**: Browser-based GUI streaming
- **VSCodium**: Main application (IDE)
- **s6-overlay**: Service management and initialization

### s6-overlay Service Structure

Services are located in `src/etc/s6-overlay/s6-rc.d/`:

**Service Types:**
- `oneshot`: Runs once at startup (initialization)
- `longrun`: Continuous background services

**Service Naming:**
- `init-*`: Initialization services (oneshot)
- `svc-*`: Long-running services (longrun)

**Key Services:**
- `init-chown-config`: Sets `/config` ownership based on `PUID`/`PGID` environment variables
- `init-devcoder-*`: Various feature installers (codium-extensions, nodejs, pip3, golang, terraform, syncthing, sshd)
- `init-devcoder-mods`: Orchestrates all mod installers
- `svc-devcoder-syncthing`: Syncthing file synchronization service
- `svc-devcoder-sshd`: SSH server
- `svc-devcoder-ngrok`: Ngrok tunneling

**Service Dependencies:**
Services can depend on each other using `dependencies.d/` files. Example:
```
init-devcoder-codium-extensions/
  dependencies.d/
    init-devcoder-mods        # Requires mods to complete first
    init-devcoder-mods-apt-installer
```

**User Bundle:**
Services to start are defined in `src/etc/s6-overlay/s6-rc.d/user/contents.d/` - empty files that list which services run.

### Environment Variable Configuration

DevCoder uses ENV vars to replace LinuxServer Docker Mods. Key mappings:

| Feature | ENV Variable | Default |
|---------|--------------|---------|
| User ID | `PUID` | 911 |
| Group ID | `PGID` | 911 |
| SSH Port | `SSHD_PORT` | (empty = disabled) |
| HTTP Auth User | `CUSTOM_USER` | abc |
| HTTP Auth Password | `PASSWORD` | (required) |
| Codium Extensions | `CODIUM_EXTENSIONS` | See docker-compose.yaml |
| NPM Packages | `NPM_PACKAGES` | `@anthropic-ai/claude-code` |
| PIP3 Packages | `PIP3_SYSTEM_PACKAGES` | `pandas` |
| Syncthing | `SYNCTHING_ENABLED` | false (was true in v0.6.7) |
| Terraform | `TERRAFORM_INSTALL` | false |
| Golang | `GOLANG_INSTALL` | false |

**File-based Configuration:**
- `/devcoder-apt-*` files in container root for APT package installation
- `/config/.config/extensions.txt` for Codium extensions
- `/devcoder-codium-ext-*` files for runtime extension installation

### VSCodium Customizations

**Custom Binary:** `/usr/bin/codium` wrapper script replaces default `/usr/share/codium/codium`

**User Data:** Stored in `$HOME/.codium` (not `/config`)

**Extension Installation:**
- During container init: from `CODIUM_EXTENSIONS` ENV
- At runtime: by creating `/devcoder-codium-ext-*` files (listens for 60s after startup)

### GitHub Actions Environments

**Important:** Jobs requiring deployment secrets must specify `environment: prod`:
```yaml
jobs:
  some-job:
    environment: prod  # Required for secrets like SNYK_TOKEN
    steps: ...
```

See `.github/workflows/build-and-push.yml` and `security-scan.yml` for examples.

### File Structure

```
src/
├── etc/s6-overlay/s6-rc.d/     # s6-overlay services
│   ├── init-*/                  # Initialization scripts
│   ├── svc-*/                   # Long-running services
│   ├── user/contents.d/         # Services to start
│   └── echo_module.sh           # Logging helper
├── defaults/                    # Default configurations
└── scripts/                     # Utility scripts

data/                            # Persistent volumes (not in git)
├── config/                      # User data (mounted to /config)
└── root/                        # Root home (mounted to /root)
```

### Version Tagging

**Tag Format:** `vX.X.X` (with `v` prefix)

**Stable vs Pre-release:**
- Stable: `v0.6.8` → gets `latest` tag
- Pre-release: `v0.6.8-alpha` → no `latest` tag

**CHANGELOG Format:**
```markdown
## [0.6.8] - 2026-01-21

### Added 🆕
- New features

### Fixed 🐛
- Bug fixes

### Changed 🔄
- Modifications

### Security 🔒
- Security updates
```

### Docker-in-Docker

Requires `privileged: true` in docker-compose.yaml. Not fully migrated from LinuxServer mods yet.
