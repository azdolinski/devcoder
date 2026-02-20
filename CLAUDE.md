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
- `init-devcoder-*`: Various feature installers (codium-extensions, nodejs, pip3, golang, terraform, syncthing, sshd, openclaw)
- `init-devcoder-mods`: Orchestrates all mod installers
- `svc-devcoder-syncthing`: Syncthing file synchronization service
- `svc-devcoder-sshd`: SSH server
- `svc-devcoder-ngrok`: Ngrok tunneling
- `svc-devcoder-openclaw`: OpenClaw AI Gateway service (runs `openclaw gateway`)

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

**Logging Module (`echo_module.sh`):**
All services use a shared logging module for consistent output:
```bash
source /etc/s6-overlay/s6-rc.d/echo_module.sh
set_module_name "my-service"
say "message"  # outputs: [my-service] message
```
When `DEBUG_DEVCODER=true`, logs are also written to `/var/log/<service>.log`.

### Environment Variable Configuration

DevCoder uses ENV vars to replace LinuxServer Docker Mods. Key mappings:

| Feature | ENV Variable | Default |
|---------|--------------|---------|
| User ID | `PUID` | 911 |
| Group ID | `PGID` | 911 |
| SSH Port | `SSHD_PORT` | (empty = disabled) |
| HTTP Auth User | `CUSTOM_USER` | abc |
| HTTP Auth Password | `PASSWORD` | (required) |
| Codium Extensions | `INSTALL_CODIUM_EXTENSIONS` | See docker-compose.yaml |
| NPM Packages | `INSTALL_NPM_PACKAGES` | `@anthropic-ai/claude-code` |
| PIP3 Packages | `INSTALL_PIP3_PACKAGES` | `pandas` |
| Syncthing | `SYNCTHING_ENABLED` | false (was true in v0.6.7) |
| Terraform | `INSTALL_TERRAFORM` | false |
| Golang | `INSTALL_GOLANG` | false |
| OpenClaw | `INSTALL_OPENCLAW` | false |
| OpenClaw Port | `OPENCLAW_PORT` | 18789 |
| Homebrew | `INSTALL_HOMEBREW` | false |
| OpenClaw Bind | `OPENCLAW_BIND` | loopback |
| APT Packages | `APT_PACKAGES` | (empty) |

### Dynamic Package Installation System

DevCoder supports dynamic package installation via file-based triggers during the first 60 seconds of container startup. Other services can create trigger files that are picked up by installers.

**`/devcoder-apt-*` Files (APT Packages)**
- Created by any service to request APT package installation
- Processed by `init-devcoder-mods-apt-installer`
- File format: one package per line or space-separated
- Example from `init-devcoder-nodejs`: creates `/devcoder-apt-nodejs.txt` containing `nodejs yarn`

**`/devcoder-codium-ext-*` Files (Codium Extensions)**
- Created at runtime to install VSCodium extensions
- Processed by `init-devcoder-codium-extensions`
- File format: extension IDs (space/newline/comma separated)
- Example: `echo "ms-python.python vscodevim.vim" > /devcoder-codium-ext-custom`

**How It Works:**
1. Service creates a trigger file (e.g., `/devcoder-apt-nodejs.txt`)
2. Installer service detects file (polls for 60 seconds after startup)
3. Installer reads packages, runs `apt-get install -y --no-install-recommends`
4. Trigger file is deleted after processing
5. Idle timer resets; if no files for 60s, listener exits

**File-based Configuration:**
- `/devcoder-apt-*` files in container root for APT package installation
- `/config/.config/extensions.txt` for Codium extensions
- `/devcoder-codium-ext-*` files for runtime extension installation

### VSCodium Customizations

**Custom Binary:** `/usr/bin/codium` wrapper script replaces default `/usr/share/codium/codium`

**User Data:** Stored in `$HOME/.codium` (not `/config`)

**Extension Installation:**
- During container init: from `INSTALL_CODIUM_EXTENSIONS` ENV
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

### OpenClaw Integration

[OpenClaw](https://github.com/openclaw/openclaw) is a personal, open-source AI assistant that can be self-hosted.

**Installation:**

Set `INSTALL_OPENCLAW=true` to install the OpenClaw CLI globally via npm.

```yaml
environment:
  - INSTALL_OPENCLAW=true
```

**Configuration:**

After installation, OpenClaw requires initialization (`openclaw onboard`) which creates the `~/.openclaw` directory with configuration. The `svc-devcoder-openclaw` service will only start the gateway once this directory exists.

```yaml
environment:
  - INSTALL_OPENCLAW=true
  - OPENCLAW_PORT=18789        # Gateway port (default: 18789)
  - OPENCLAW_BIND=lan          # Bind address: loopback, lan, tailnet, auto
  - OPENCLAW_TOKEN=xxx         # Optional: authentication token
  - OPENCLAW_PASSWORD=xxx      # Optional: authentication password
  - OPENCLAW_VERBOSE=true      # Optional: enable verbose logging
```

**Services:**

- `init-devcoder-openclaw`: Installs OpenClaw globally via npm (oneshot)
- `svc-devcoder-openclaw`: Runs the OpenClaw gateway (longrun)

**Gateway Access:**

Once running, the Control UI is available at `http://<host>:18789/` (or configured port).

### Homebrew Integration

[Homebrew](https://brew.sh/) is the missing package manager for Linux.

**Installation:**

Set `INSTALL_HOMEBREW=true` to install Homebrew.

```yaml
environment:
  - INSTALL_HOMEBREW=true
```

**Usage:**

Homebrew is installed to `$HOME/.linuxbrew/` and is automatically added to PATH in new shell sessions. To use immediately:

```bash
eval "\$(\$HOME/.linuxbrew/bin/brew shellenv)"
```

**Important:**
- Homebrew runs as non-root user (required by installer)
- Install dependencies: build-essential, procps, curl, file, git
- Homebrew binaries are installed to `$HOME/.linuxbrew/bin/`

**Services:**

- `init-devcoder-homebrew`: Installs Homebrew as non-root user (oneshot)

