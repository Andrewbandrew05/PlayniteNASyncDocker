#!/bin/bash
# If the config file is missing, copy a template
if [ ! -f /etc/samba/smb.conf ]; then
    echo "Creating default smb.conf..."
    cat > /etc/samba/smb.conf <<EOF
[global]
   workgroup = WORKGROUP
   server string = Samba Server
   security = user
   map to guest = Bad User
   dns proxy = no
EOF
fi
# Ensure the private directory exists for passwords
mkdir -p /var/lib/samba/private