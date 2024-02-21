#!/usr/bin/env bash
filename=~/baseline.txt
spacer='\n-----------------------------------------------------------------\n'

# Write section header to file
write_section() {
    echo -e "\n# $1 \n$spacer" | tee -a "$filename" >/dev/null
}

# Run command and write output to file
capture_output() {
    echo -e "# $1 \n" | tee -a "$filename" >/dev/null
    $1 | tee -a "$filename" >/dev/null
}

# Get list of users assigned active shells
awk -F':' 'sh$/ {print $1,$7}' /etc/passwd >~/userlist_1.txt

# Get list of users with assigned passwords
awk -F':' '{print $1,$2}' /etc/shadow | sudo tee ~/passwordlist_1.txt >/dev/null

# store baseline file in home directory of user
echo -e "# $(date '+%F %T %Z') \n$spacer" >"$filename"

# System Information Sections
capture_output "lsb_release --all"
capture_output "uname -a"
capture_output "ifconfig -a"
capture_output "ip route show"
capture_output "df -hal"
capture_output "env"

# Cron Information
write_section "System Cron Information"
for x in /etc/crontab /etc/cron*/*; do
    [ -e "$x" ] && sudo cat "$x" | tee -a "$filename" >/dev/null
done

write_section "User Cron Information"
for x in /var/spool/cron/crontabs/*; do
    [ -e "$x" ] && sudo cat "$x" | tee -a "$filename" >/dev/null
done

# Firewall Information
capture_output "iptables --list-rules"

# System Users
capture_output "cat /etc/passwd"
sudo cat /etc/shadow | tee -a "$filename" >/dev/null

# Installed Applications
capture_output "apt list --installed"

# Running Services
capture_output "systemctl status"
capture_output "service --status-all"

echo -e "\n# Manual Alias Reminder\n\nMANUALLY RUN ALIAS" | tee -a "$filename" >/dev/null
echo "Please run this script with sudo if you haven't."
