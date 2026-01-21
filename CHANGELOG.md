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
