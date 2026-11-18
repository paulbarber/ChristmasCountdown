# ChristmasCountdown

A Python 3 program and scripts to show days, hours, mins and seconds until Christmas Day,
with falling snow. After Christmas it counts down to New Year, then on to the next Christmas.

Intended for use on a Raspberry Pi without the desktop running. Runs full screen for use with a projector.

## Setup

**See [SETUP.md](SETUP.md)** for step-by-step instructions to build a Raspberry Pi Zero 2 W
box that starts the countdown automatically at power-on.

In short, on Raspberry Pi OS Lite:

    sudo apt install python3-tk xserver-xorg xinit x11-xserver-utils

## Use

To run it by hand from the Pi's own console (not inside a desktop session or over SSH):

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
and **Donate** (opens the Christmas Countdown JustGiving page in a new tab).
