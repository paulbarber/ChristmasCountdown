# Setting up the Christmas Countdown on a Raspberry Pi Zero 2 W

These steps build a small box that plugs into a projector or TV and shows the countdown
full screen whenever it is powered on. It gets the correct time over WiFi.

## What you need

- **Raspberry Pi Zero 2 W** (the header pins are not needed for this WiFi version)
- **Micro-SD card**, 16 or 32 GB, A1 rated (e.g. SanDisk or Samsung)
- **Mini-HDMI to HDMI cable or adapter** (the Zero's video socket is mini-HDMI)
- **Micro-USB power**: the official Pi supply (5 V 2.5 A), or the projector's USB port if it
  can supply enough current
- A computer to prepare the SD card, on the same WiFi network as the Pi

## 1. Prepare the SD card

1. Install **Raspberry Pi Imager** on your computer: https://www.raspberrypi.com/software/
2. Choose:
   - Device: **Raspberry Pi Zero 2 W**
   - OS: **Raspberry Pi OS (other) → Raspberry Pi OS Lite (64-bit)**
     (Lite has no desktop, which leaves the Zero's 512 MB of memory for the countdown)
   - Storage: your SD card
3. When asked, **edit the custom settings** so the Pi never needs a keyboard or screen:
   - **Hostname**: `countdown`
   - **Username and password**: your choice
   - **WiFi**: your network name and password, country **GB**.
     The Zero 2 W only works on **2.4 GHz** WiFi; a network that offers both bands under one
     name is fine, a 5 GHz-only network is not.
   - **Locale**: timezone **Europe/London**
   - **Services**: enable **SSH** with password authentication
4. Write the card, put it in the Pi, connect the projector, and power it on.
   The first boot takes a few minutes.

## 2. Install the countdown

From your computer, connect to the Pi (use the username you chose):

    ssh yourname@countdown.local

Then run:

    sudo apt update
    sudo apt install -y git python3-tk xserver-xorg xinit x11-xserver-utils
    git clone https://github.com/paulbarber/ChristmasCountdown.git ~/ChristmasCountdown

The install can take 10–15 minutes on a Zero.

## 3. Start it automatically at power-on

    sudo raspi-config nonint do_boot_behaviour B2
    echo '[ "$(tty)" = /dev/tty1 ] && [ -z "$DISPLAY" ] && exec startx ~/ChristmasCountdown/ChristmasCountdown.sh -- -nocursor' >> ~/.profile
    sudo reboot

- The first line makes the Pi log in automatically on its own screen.
- The second starts the countdown full screen on that screen only, so SSH logins are not
  affected.
- The countdown cannot be started from an SSH session, because it needs the Pi's own
  screen; that is why the last step is a reboot.

About 30 seconds after the reboot the countdown should appear on the projector.

## Looking after it

| To… | Run (over SSH) |
|---|---|
| Get the latest version | `cd ~/ChristmasCountdown && git pull && sudo reboot` |
| Restart the countdown | `pkill -f ChristmasCountdown.py` (it starts again by itself) |
| Turn off auto-start | `sudo raspi-config nonint do_boot_behaviour B1 && sudo reboot` |
| Turn auto-start back on | `sudo raspi-config nonint do_boot_behaviour B2 && sudo reboot` |
| Shut down safely | `sudo poweroff` (wait for the green light to stop, then unplug) |

If the countdown crashes, or someone presses Escape on an attached keyboard, it restarts by
itself.

## Remote buttons

Nothing to set up: the Pi listens for Flurry and Fireworks presses on the web page as soon
as it has WiFi. Every Pi cloned from the same repo responds. See *Remote buttons* in the
README for how channels work. To check, press Fireworks on the website on your phone and
watch the projector; it should respond within a second or two.

## Troubleshooting

- **`countdown.local` not found**: wait a few minutes after first boot, check the WiFi
  details and that it is a 2.4 GHz network, or find the Pi's IP address in your router's
  list of devices and use `ssh yourname@<ip address>`.
- **Blank screen after reboot**: make sure the HDMI cable was plugged in before power-on,
  and that the projector is on the right input.
- **Wrong time**: the Pi sets its clock from the internet at boot, so check it is connected
  to WiFi (`ping -c 3 raspberrypi.com`).
- **Picture cropped or with a black border**: check the projector's own zoom or
  "overscan" / "aspect" settings first.
