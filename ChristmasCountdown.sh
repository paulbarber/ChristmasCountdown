#!/bin/bash
# X client script run by xinit: disable screen blanking, then start the countdown.
DIR="$(cd "$(dirname "$0")" && pwd)"
xset s off
xset -dpms
exec python3 "$DIR/ChristmasCountdown.py"
