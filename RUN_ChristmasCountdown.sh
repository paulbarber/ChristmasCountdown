#!/bin/bash
# Start an X server with just the countdown (run from the console, not a desktop).
DIR="$(cd "$(dirname "$0")" && pwd)"
xinit "$DIR/ChristmasCountdown.sh" &
