# Technology Stack

Xvfb       → serwer X (DISPLAY)
Openbox    → window manager
Polybar    → panel (opcjonalnie)
Selkies    → streaming GUI do przeglądarki
VSCodium   → aplikacja

# Built-in environment variables

| Variable | Default / Notes |
| --- | --- |
| `TZ` | Etc/UTC |
| `CUSTOM_USER` | devcoder |
| `PASSWORD` | devcoder1234 |
| `APP_PORT` | 8443 |
| `SSHD_PORT` | empty = disabled (1-65535) |
| `NGROK_AUTHTOKEN` | empty = disabled |
| `NGROK_PORT` | 3000 |
| `NGROK_BIN` | auto-detected |

# Docker Mods → devcoder ENV mapping

| Original extension (Docker Mod) | Devcoder mapping (ENV) | Default / Notes |
| --- | --- | --- |
| linuxserver/mods:code-server-nodejs | `NPM_PACKAGES`, `NODEJS_MOD_VERSION` | NODEJS_MOD_VERSION=16 |
| linuxserver/mods:code-server-npmglobal | `NPM_PACKAGES` | empty = no installs |
| linuxserver/mods:code-server-python3 | `PIP3_SYSTEM_PACKAGES` | empty = no installs |
| linuxserver/mods:code-server-extension-arguments | `CODIUM_EXTENSIONS`, `CODIUM_EXTENSIONS_FORCE` | FORCE=false |
| linuxserver/mods:code-server-golang | `GOLANG_INSTALL` | false = disabled |
| linuxserver/mods:universal-package-install | `APT_PACKAGES`, `/devcoder-apt-*` files | handled by init-devcoder-mods-apt-installer |
| linuxserver/mods:universal-docker-in-docker | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-awscli | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-dotnet | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-flutter | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-java11 | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-julia | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-php | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-php8 | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-php-cli | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-pnpm | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-powershell | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-prolog | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-python3-poetry | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-r | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-ros2 | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-rust | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-scikit-learn | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-shellcheck | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-svn | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-terraform | not migrated yet | use Docker Mods for now |
| linuxserver/mods:code-server-zsh | not migrated yet | use Docker Mods for now |