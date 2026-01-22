# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added 🆕
-

### Fixed 🐛
-

### Changed 🔄
-

### Security 🔒
-

---

## [0.6.15] - 2026-01-22

### Fixed 🐛
- 🔑 **SSHD key generation**: Fixed incorrect logic in SSH host key generation
  - Removed unnecessary `rm -f /etc/ssh/ssh_host_*` that was deleting existing keys
  - Now properly preserves existing SSH keys between container restarts
  - `ssh-keygen -A` only generates missing keys, no interactive prompts
  - Fixes "Overwrite (y/n)?" prompt that blocked container startup

---

## [0.6.14] - 2026-01-22

### Added 🆕
- 📚 **Documentation**: Complete guide for Docker tagging and versioning best practices
  - Added comprehensive "Version Prefix (v) Best Practices" section
  - Documented Git tags (with `v`) vs Docker tags (without `v`) conventions
  - Updated workflow examples to match current implementation

### Fixed 🐛
-

### Changed 🔄
- 🔧 **Workflows**: Updated documentation to reflect actual workflow implementation
  - Added `workflow_dispatch` trigger documentation
  - Documented `environment: prod` usage
  - Clarified `value` parameter requirement for `docker/metadata-action`

### Security 🔒
-

---

## [0.6.13] - 2026-01-22

### Added 🆕
- 🔐 **SSHD PermitRootLogin**: New `SSHD_PERMITROOTLOGIN` env var to allow root SSH login
  - Default: `false` (root login disabled)
  - Set to `true` to enable `PermitRootLogin yes` in sshd_config
  - Works together with `SSHD_PORT` and `ROOT_PASSWORD` configuration
- 🔑 **ROOT_PASSWORD support**: New `ROOT_PASSWORD` env var to set root user password
  - Only sets password when variable is defined and not empty
  - Useful in combination with `SSHD_PERMITROOTLOGIN=true`

### Fixed 🐛
-

### Changed 🔄
-

### Security 🔒
-

---

## [0.6.12] - 2026-01-22

### Added 🆕
- 🖥️ **RustDesk support**: New s6-overlay service for RustDesk remote desktop application
  - Configurable via `RUSTDESK_INSTALL` env var (default: false)
  - Two installation methods:
    - `proot`: PRoot-based installation (isolated environment)
    - `system` or `true`: System package installation via .deb file
  - Supports x86_64, aarch64 (ARM64), and armv7 architectures
  - Automatic dependency installation via gstreamer1.0-pipewire
  - Downloads latest version from GitHub releases

### Changed 🔄
- 📝 **docker-compose.yaml**: Improved volume mount comments with clearer SUGGEST/EXAMPLE prefixes
- 📂 **Projects directory**: Added `/mnt/data:/projects` volume mapping as example for project workspace

### Documentation 📚
- 📋 **workflow-analysis.txt**: Added GitHub Actions workflow analysis document with trigger and job information

---

## [0.6.11] - 2026-01-22

### Added 🆕
- 🔄 **workflow_run trigger**: Added `workflow_run` trigger to `build-and-push.yml` to properly chain workflows
- 🏷️ **Dynamic tag detection**: Added `get_tag` step that determines tag from both `workflow_run` and `push: tags` events
- 📚 **Complete guide**: Updated `/tmp/complete-guide-en.md` with comprehensive documentation of the new workflow architecture

### Fixed 🐛
- 🔧 **GitHub Actions automation**: Fixed critical issue where `build-and-push.yml` wasn't triggering when tags were created by `detect-release.yml`
  - **Root cause**: GitHub Actions doesn't trigger `on: push: tags:` when tags are created by other workflows (security feature to prevent infinite loops)
  - **Solution**: Implemented `workflow_run` trigger that reacts to completion of `detect-release.yml` workflow
  - **Fallback**: Kept `push: tags` trigger for manual tag creation workflows

### Changed 🔄
- 🔄 **build-and-push.yml**: Updated all references from `${{ github.ref_name }}` to `${{ steps.get_tag.outputs.REF_NAME }}`
- 📖 **Documentation**: Enhanced troubleshooting section with workflow_run-specific issues and solutions

### Technical Details 🛠️
- **Dual trigger system**: Workflow now supports both automated (via detect-release) and manual tag creation
- **Tag fetching logic**: When triggered by `workflow_run`, workflow fetches the most recent tag using `git ls-remote`
- **Backward compatible**: Manual tag pushes still work via fallback `push: tags` trigger

---

## [0.6.10] - 2026-01-22

### Added 🆕
- 🔗 **code-server symlink**: Added `/usr/bin/code-server` symlink pointing to `/usr/bin/codium` for compatibility
- 📁 **Chrome directory**: Created `/opt/google/chrome` directory structure for compatibility
- 🔗 **Chrome symlink**: Added symlink from `/usr/bin/chromium` to `/opt/google/chrome/chrome` for tools expecting Google Chrome

### Changed 🔄
- 🐟 **Core dumps**: Added `core.*` pattern to `.gitignore` to exclude core dump files
- 🔧 **VSCodium wrapper**: Simplified codium launcher - removed duplicate root/user logic, added automatic `$HOME` directory change when launched without arguments
- 🖥️ **Openbox menu**: Removed `--password-store="gnome-libsecret"` flag from VSCodium menu entry (moved to wrapper)
- 🔐 **SSHD service**: Changed from oneshot to longrunning service - now properly keeps SSHD running in foreground
- ⚙️ **Syncthing default**: Changed `SYNCTHING_ENABLED` default from `true` to `false` (users must explicitly enable)
- 🔧 **Dockerfile**: Added symlinks for code-server and Chrome during build

### Removed 🗑️
- 📄 **code-server wrapper**: Removed duplicate `/usr/bin/code-server` script (now symlinked to codium wrapper)

### Fixed 🐛
- 🐛 **SSHD startup**: Fixed SSHD service to properly run as longrunning process instead of oneshot initialization

---

## [0.6.9] - 2026-01-21

### Added 🆕
- 📊 **S6_MERMAID**: New environment variable to enable Mermaid dependency diagram generation (default: false)

### Changed 🔄
- 📝 **.env.example**: Added missing environment variables (SYNCTHING_ENABLED, S6_MERMAID)

### Fixed 🐛
- 🐛 **svc-s6-tree**: Service now respects S6_MERMAID environment variable (previously always ran)

---

## [0.6.8] - 2026-01-21

### Added 🆕
- 🔧 **init-chown-config**: New s6-overlay service for proper ownership management of /config directory based on PUID/PGID environment variables
- 📋 **Syncthing dependency tracking**: Added `up` file to ensure proper initialization order for Syncthing service

### Fixed 🐛
- 🐛 **VSCodium desktop entry**: Fixed incorrect Exec path in `/usr/share/applications/codium.desktop` from `/usr/share/codium/codium` to `/usr/bin/codium` for proper application launching

### Changed 🔄
- ⚙️ **Syncthing default**: Changed `SYNCTHING_ENABLED` default from `true` to `false` - users must explicitly enable Syncthing

### Security 🔒
-

---

## [0.6.7]  - 2026-01-21

### Added 🆕
- 🔄 **Syncthing**: Full file synchronization service with s6-overlay integration
  - Configurable via `SYNCTHING_ENABLED` env var (default: true)
  - GUI password protection via `SYNCTHING_PASSWORD`
  - Configurable home/data directories via `SYNCTHING_HOME`/`SYNCTHING_DATA`
  - GUI accessible on port 8384
  - Automatic setup with official Syncthing repository
- 📝 **SciTE**: Lightweight text editor added to base image
- 📦 **xz-utils**: Compression utilities added to base image

### Fixed 🐛
- 🐛 **Trivy/Grype scanners**: Corrected scanner configuration with proper `scan-type: 'image'` for Trivy and string format for `severity-cutoff` in Grype
- 🐛 **VSCodium data directory**: Changed user data directory from `/config` to `$HOME/.codium` for better compatibility

### Changed 🔄
- ✅ **GitHub Actions**: Added `prod` environment to all deployment workflows for proper environment variables/secrets access and deployment tracking
- 📁 Added `.claude` to `.gitignore`

### Security 🔒
-

---

## [0.6.6] - 2026-01-21

### Added 🆕
- 🔒 **Security scanning**: Trivy + Grype vulnerability scanners before image publishing
- 📊 **SARIF reports**: Security findings automatically uploaded to GitHub Security tab
- 🏗️ **Multi-platform support**: Now builds for both linux/amd64 AND linux/arm64 (Apple Silicon, AWS Graviton, Azure ARM)
- 📜 **SBOM generation**: Software Bill of Materials included in every image
- 🔐 **Provenance attestation**: Image provenance metadata for supply chain security
- ⏱️ **Timeout protection**: All jobs now have proper timeouts (2h for build, 15m for scans)

### Changed 🔄
- 🔨 Improved Docker Buildx setup (removed silent error handling)
- ✅ Enhanced job summaries with platform info and security scan results
- 📦 Added `security-events: write` permission for vulnerability reporting

### Fixed 🐛
- 🐛 Removed `continue-on-error: true` from Buildx setup (errors now properly fail the build)

---

## [0.6.5] - 2026-01-21

### Added 🆕
- ✨ Initial DevCoder container setup with full VSCodium IDE
- 🐳 LinuxServer.io base image with s6-overlay for reliable service management
- 🐍 Python 3 environment with pandas for data science
- 🛠️ Essential development tools pre-installed: git, gdb, htop, mc, nano, terminator, tint2, rofi
- 🔧 VSCode extensions bundled out-of-the-box:
  - vscode-icons-team.vscode-icons (File icons 🎨)
  - ms-azuretools.vscode-docker (Docker support 🐳)
  - ms-python.python + ms-python.vscode-pylance (Python IntelliSense 🐍)
  - ms-python.flake8 + ms-python.pylint (Python linting 📏)
  - ms-pyright.pyright (Type checking 🔍)
  - redhat.vscode-yaml (YAML support 📄)
  - ms-azuretools.vscode-containers (Container support 📦)
  - kilocode.kilo-code (AI coding assistant 🤖)
  - anthropic.claude-code (Claude Code integration 🧠)
  - mermaidchart.vscode-mermaid-chart (Diagram support 📊)
- 🐋 Docker-in-Docker support via LinuxServer mods (for containerized development)
- 🔑 SSH server support (optional, configurable via SSHD_PORT)
- 💾 Persistent volumes for /config and /root directories
- 🔒 Keyring support with IPC_LOCK capability
- 🌐 Web-based IDE accessible via HTTPS on port 3001
- 📦 NPM global package support with @anthropic-ai/claude-code
- 🏥 Health check endpoint for container monitoring

### Changed 🔄
- 🔨 Refactored Docker image structure with proper s6-overlay services
- ⚙️ Improved build process with conditional chmod operations
- 📝 Added comprehensive environment variable configuration via .env
- 🎛️ Enhanced docker-compose with extensive documentation of available mods

### Fixed 🐛
- ✅ Fixed 'run' files being ignored in src/ directory (now properly tracked)
- ✅ Added conditional checks before chmod operations in Dockerfile to prevent build failures
- ✅ Corrected permissions for s6-overlay service scripts

---

## [0.0.1] - 2025-01-01

### Added 🆕
- 🎉 Initial project commit
- 📋 Basic docker-compose configuration skeleton


