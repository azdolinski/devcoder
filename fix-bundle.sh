#!/bin/bash
echo "Fixing s6-overlay bundle references..."

cd /opt/docker/devcoder/src/etc/s6-overlay/s6-rc.d/user/contents.d/

# Remove incorrect references
echo "Removing incorrect references..."
rm -f init-mod-npm-install
rm -f init-mod-ngrok-install  
rm -f init-mod-sshd

echo "Bundle fixed. Current contents:"
ls -la

echo "Done!"
