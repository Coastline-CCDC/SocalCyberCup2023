#!/usr/bin/env bash

filename=~/baseline.txt
spacer='\n-----------------------------------------------------------------\n'
date_stamp=$(date '+%F %T %Z')

# Enhanced check for command existence
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Write section header to file
write_section() {
    echo -e "\n# $1 \n$spacer" >>"$filename"
}

# Run command and write output to file, checks if command exists
capture_output() {
    if command_exists "$2"; then
        echo -e "# $1 \n" >>"$filename"
        $2 >>"$filename"
    else
        echo -e "# $1 \n- Command $2 not found on this system.\n" >>"$filename"
    fi
}

# Attempt to source .bashrc to capture aliases, if they are defined there
if [ -f "$HOME/.bashrc" ]; then
    source "$HOME/.bashrc"
fi

# Prepare baseline file
echo -e "# System Baseline captured on $date_stamp $spacer" >"$filename"

# User and Password lists
awk -F':' 'sh$/ {print $1,$7}' /etc/passwd >~/userlist_1.txt
sudo awk -F':' '{print $1,$2}' /etc/shadow >~/passwordlist_1.txt

# System Information
capture_output "LSB Release Information" "lsb_release --all"
capture_output "Kernel Information" "uname -a"
capture_output "Network Interfaces" "ip addr"
capture_output "IP Routing Information" "ip route show"
capture_output "Disk Filesystem Usage" "df -hal"
capture_output "Environment Variables" "env"

# Alias Information
capture_output "Defined Aliases" "alias"

# Cron Information
write_section "System Cron Information"
sudo find /etc/cron* -type f -exec cat {} + >>"$filename" 2>/dev/null

write_section "User Cron Information"
sudo find /var/spool/cron/crontabs -type f -exec cat {} + >>"$filename" 2>/dev/null

# Firewall Information
capture_output "IPTables Rules" "iptables --list-rules"

# System Users
capture_output "System Users (/etc/passwd)" "cat /etc/passwd"
capture_output "Password Information (/etc/shadow)" "sudo cat /etc/shadow"

# Installed Applications and Services
capture_output "Installed Packages" "apt list --installed"
capture_output "Active Services" "systemctl list-units --type=service --state=running"
capture_output "All Services Status" "service --status-all"

echo -e "\n# End of Baseline $spacer" >>"$filename"

echo "Baseline captured to $filename"
