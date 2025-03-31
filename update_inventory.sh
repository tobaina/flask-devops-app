#!/bin/bash

# Beginner prompt
echo "🔧 Let's update your Ansible inventory!"

# Ask for new IPs
read -p "👉 Enter Debian node public IP: " debian_ip
read -p "👉 Enter Amazon Linux node public IP: " amazon_ip
read -p "👉 Enter Fedora/CentOS node public IP: " fedora_ip

# Set the path to inventory file
inventory_path="ansible/inventories/inventory.ini"

# Overwrite the file with new content
cat <<EOF > $inventory_path
[flask]
$debian_ip ansible_user=admin
$amazon_ip ansible_user=ec2-user
$fedora_ip ansible_user=fedora
EOF

# Feedback
echo ""
echo "✅ Done! Here’s the new inventory file:"
cat $inventory_path

