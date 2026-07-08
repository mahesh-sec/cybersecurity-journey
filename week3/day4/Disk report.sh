#!/bin/bash
# disk_report.sh
# Generates a timestamped system report covering disk usage, top memory-consuming
# processes, and currently logged-in users.
# Usage: ./disk_report.sh

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTFILE="report_$TIMESTAMP.txt"

echo "=== Disk Usage ===" >> "$OUTFILE"
df -h >> "$OUTFILE"

echo "=== Top Processes by Memory ===" >> "$OUTFILE"
ps aux --sort=-%mem | head >> "$OUTFILE"

echo "=== Logged-in Users ===" >> "$OUTFILE"
w >> "$OUTFILE"

echo "Report saved to $OUTFILE"
