# ChristmasCountdown

A Python 3 program and scripts to show days, hours, mins and seconds until Christmas Day,
with falling snow. After Christmas it counts down to New Year, then on to the next Christmas.

Intended for use on a Raspberry Pi without the desktop running. Runs full screen for use with a projector.

## Setup (Raspberry Pi OS Lite)

    sudo apt install python3-tk xserver-xorg xinit x11-xserver-utils

## Use

From the console (not inside a desktop session):

    ./RUN_ChristmasCountdown.sh     # start
    ./STOP_ChristmasCountdown.sh    # stop

Escape or Ctrl-C in the window also quits. The scripts find each other relative to their
own folder, so the repo can live anywhere.

## Browser version

`index.html` is a self-contained version that runs in any browser (no install, no Pi).
Hosted with GitHub Pages at https://paulbarber.github.io/ChristmasCountdown/ -
click or tap for full screen. It uses the device's own clock.

On a phone, use "Add to Home Screen" (Safari share menu, or the Chrome menu) to get a
Christmas tree icon that opens the countdown full screen.

Buttons along the bottom: **Flurry** (a burst of snow), **Fireworks** (5 seconds of fireworks)
and **Donate** (opens the Alzheimer's Society donation page in a new tab).
