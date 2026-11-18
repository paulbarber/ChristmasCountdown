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

## Remote buttons (phones control the projector)

When someone presses **Flurry** or **Fireworks** on the web page, the same effect plays on
every projector linked to this repo, as well as on their own screen. Presses travel through
[ntfy.sh](https://ntfy.sh), a free public message relay that needs no account. Each press
sends only the button name and a random id.

Projectors that listen:

- **Raspberry Pi** (`ChristmasCountdown.py`): listens automatically. Nothing extra to install.
  Press `f` or `s` on a keyboard attached to the Pi to test fireworks or snow locally.
- **A browser used as a projector**: open the page with `?projector` on the end, e.g.
  `https://paulbarber.github.io/ChristmasCountdown/?projector`. This hides the buttons and listens.

### config.json

| Setting | Meaning |
|---|---|
| `remote_buttons` | `true` to link the web page and projectors, `false` to turn it off |
| `relay` | The ntfy server to use, `https://ntfy.sh` by default (or your own ntfy server) |
| `channel` | Any random text. Change it to start a fresh, separate channel |
| `repo` | Leave empty unless hosting somewhere other than GitHub Pages (see below) |

### Who is linked to whom

The channel used is worked out from `channel` **plus the GitHub owner/repo** that each copy
comes from: the web page from its GitHub Pages address, and each Pi from the repo it was
`git clone`d from. So:

- The website and **every Pi cloned from the same repo** share a channel. Add as many
  projectors as you like; they all respond.
- **A fork is automatically separate**, even though it copies `config.json`, because its
  owner name is different.
- To **start a fresh channel** (e.g. if someone finds a way to spam it), change `channel`,
  commit, then run `git pull` and reboot on each Pi.
- **Hosting somewhere else** (your own domain, or a Pi set up from a zip rather than
  `git clone`): set `repo` to the same value, e.g. `"paulbarber/christmascountdown"`, in the
  config used by the site and by every Pi. A fork that keeps a `repo` setting would share
  your channel, so forks should clear it or change `channel`.

Anyone who can press the public buttons can already make it snow, so the channel isn't a
secret. Projectors ignore anything except Flurry and Fireworks, act on each at most once
every 0.7 s, and the web buttons have a short cooldown.
