FROM lscr.io/linuxserver/vscodium:latest

# Note: NodeSource repository is already configured by the base image
# If you need to update Node.js version, modify NODEJS_MOD_VERSION in docker-compose.yaml

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

    
