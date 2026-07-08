#!/bin/bash
# localnet.sh
# Sweeps a /24 Host-Only VirtualBox subnet and reports which hosts respond to ping.
# Usage: ./localnet.sh

for x in 192.168.56.{1..254};
do
    if ping -q -c 2 -W 1 "$x" > /dev/null; then
        echo "$x is up"
    else
        echo "$x is down"
    fi
done
