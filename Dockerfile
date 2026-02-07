FROM lscr.io/linuxserver/vscodium:latest

# Remove broken NodeSource repository (expired SHA1-signed key) and add updated one
RUN if [ -f /etc/apt/sources.list.d/nodesource.list ]; then \
        rm -f /etc/apt/sources.list.d/nodesource.list; \
    fi && \
    if [ -f /etc/apt/trusted.gpg.d/nodesource.gpg ]; then \
        rm -f /etc/apt/trusted.gpg.d/nodesource.gpg; \
    fi && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_22.x nodistro main" > /etc/apt/sources.list.d/nodesource.list

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      python-is-python3 \
      python3-pip \
      terminator \
      scite \
      tint2 \
      rofi \
      wget \
      libfuse2 \
      dbus-x11 \
      gnome-keyring \
      libsecret-1-0 \
      git \
      gh \
      gdb \
      htop \
      dnsutils \
      net-tools \
      iputils-ping \
      mc \
      nano \
      xz-utils \
      unzip; \
    rm -rf /var/lib/apt/lists/*;

#ENV TMPDIR=/config/tmp
#RUN mkdir -p /config/tmp && chmod 1777 /config/tmp && \
#    rm -rf /tmp && ln -s /config/tmp /tmp

COPY ./src /
RUN chmod +x /usr/bin/codium && \
    ln -s /usr/bin/codium /usr/bin/code-server && \
    chmod +x /defaults/rofi/run && \
    mkdir -p /opt/google/chrome && \
    ln -s /usr/bin/chromium /opt/google/chrome/chrome && \
    /usr/bin/sed -i 's|Exec=/usr/share/codium/codium|Exec=/usr/bin/codium|g' /usr/share/applications/codium.desktop && \
    find /etc/s6-overlay/s6-rc.d/ -name "run" -type f -exec chmod +x {} \; 

    
