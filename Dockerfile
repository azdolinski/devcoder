FROM lscr.io/linuxserver/vscodium:latest

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      python3-pip \
      terminator \
      tint2 \
      rofi \
      wget \
      libfuse2 \
      dbus-x11 \
      gnome-keyring \
      libsecret-1-0 \
      git \
      gdb \
      htop \
      dnsutils \
      net-tools \
      mc \
      nano \
      unzip; \
    rm -rf /var/lib/apt/lists/*;

#ENV TMPDIR=/config/tmp
#RUN mkdir -p /config/tmp && chmod 1777 /config/tmp && \
#    rm -rf /tmp && ln -s /config/tmp /tmp

COPY ./src /
RUN chmod +x /usr/bin/codium && \
    chmod +x /defaults/rofi/run && \
    find /etc/s6-overlay/s6-rc.d/ -name "run" -type f -exec chmod +x {} \;

