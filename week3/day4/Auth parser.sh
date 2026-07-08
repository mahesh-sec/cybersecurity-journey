#!/bin/bash
# auth_parser.sh
# Parses system logs for failed SSH login attempts and counts them by source IP.
# Uses journalctl instead of /var/log/auth.log since this system logs via systemd-journald.
# Usage: ./auth_parser.sh

echo "=== Failed SSH Login Attempts by Source IP ==="
journalctl | grep "Failed password" | awk '{print $(NF-3)}' | sort | uniq -c | sort -nr
