# Information

This container is based on the [linuxserver/vscodium-web](https://github.com/linuxserver/docker-vscodium) image.

# Technology Stack

Xvfb       → serwer X (DISPLAY)<br>
Openbox    → window manager<br>
Polybar    → panel (opcjonalnie)<br>
Selkies    → streaming GUI do przeglądarki<br>
VSCodium   → aplikacja

# Docker Mods → devcoder ENV mapping to old Linuxserver.io Modes

| Devcoder ENV | Default | Match Original extension |
| --- | --- | --- |
| `INSTALL_NPM_PACKAGES`<br>`NODEJS_MOD_VERSION` | `INSTALL_NPM_PACKAGES`=<br>`NODEJS_MOD_VERSION`=`24` | linuxserver/mods:code-server-nodejs<br>linuxserver/mods:code-server-npmglobal |
| `INSTALL_PIP3_PACKAGES` | `INSTALL_PIP3_PACKAGES`= | linuxserver/mods:code-server-python3 |
| `INSTALL_CODIUM_EXTENSIONS`<br>`INSTALL_CODIUM_EXTENSIONS_FORCE` |`INSTALL_CODIUM_EXTENSIONS`=<br>`INSTALL_CODIUM_EXTENSIONS_FORCE`=`false` | linuxserver/mods:code-server-extension-arguments |
| `INSTALL_GOLANG` | `INSTALL_GOLANG`=`false` | linuxserver/mods:code-server-golang |
| `INSTALL_APT_PACKAGES` | `INSTALL_APT_PACKAGES`= | linuxserver/mods:universal-package-install |
| `INSTALL_TERRAFORM` | `INSTALL_TERRAFORM`=`false` | linuxserver/mods:code-server-terraform |
| not migrated yet | use Docker Mods for now | linuxserver/mods:universal-docker-in-docker |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-awscli |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-dotnet |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-flutter |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-java11 |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-julia |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-php |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-php8 |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-php-cli |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-pnpm |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-powershell |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-prolog |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-python3-poetry |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-r |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-ros2 |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-rust |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-scikit-learn |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-shellcheck |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-svn |
| not migrated yet | use Docker Mods for now | linuxserver/mods:code-server-zsh |


## Othere ENV Defaults:

### System Configuration
```bash
TZ=Etc/UTC                                    # Timezone
CUSTOM_USER=devcoder                          # Username for the internal user
PASSWORD=devcoder1234                         # Password for the user/web access
APP_PORT=8443                                 # External HTTPS port mapping
DEBUG_DEVCODER=false                          # Enable verbose logging for devcoder init scripts
PUID=911                                      # User ID for the internal user `abc`
PGID=911                                      # Group ID for the internal user `abc`
ROOT_PASSWORD=  
ABC_PASSWORD=
S6_MERMAID=false                              # Generate Mermaid diagram of s6 service
```

### Services 
#### SSHD
```bash
SSHD_PORT=                                    # SSH server port (1-65535). Empty = disabled
SSHD_PERMITROOTLOGIN=false                    # Set to "true" to allow root login
```
#### NGROK
```bash
NGROK_AUTHTOKEN=                              # Ngrok authentication token. Empty = disabled
NGROK_BIN=/usr/local/bin/ngrok                # Path to ngrok binary
NGROK_PORT=3000                               # Port for ngrok tunnel
```
#### SYNCTHING
```bash
SYNCTHING_ENABLED=false                       # Set to "true" to enable Syncthing file synchronization
SYNCTHING_HOME=/config/syncthing	          # Syncthing home directory
SYNCTHING_DATA=/config/syncthing/data	      # Syncthing data directory
SYNCTHING_PASSWORD=	                          # Syncthing GUI password
```

#### RustDesk
```bash
RUSTDESK_INSTALL=false                        # Possible values: false/proot/system
```

#### OpenClaw
```bash
INSTALL_OPENCLAW=false                        # Set to "true" to install OpenClaw AI Gateway
OPENCLAW_PORT=18789                           # Gateway port
OPENCLAW_BIND=loopback                        # Bind address: loopback, lan, tailnet, auto
OPENCLAW_TOKEN=                               # Optional: authentication token
OPENCLAW_PASSWORD=                            # Optional: authentication password
OPENCLAW_VERBOSE=false                        # Enable verbose logging
```

OpenClaw is a personal, open-source AI assistant. When enabled, it installs via npm and runs a gateway service. Requires `openclaw onboard` to be run first to create configuration.

