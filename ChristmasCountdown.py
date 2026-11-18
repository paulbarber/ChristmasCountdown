#!/usr/bin/env python3
"""Christmas Countdown - full-screen countdown to Christmas Day (and New Year).

Intended for a Raspberry Pi without the desktop running, e.g. driving a projector
via xinit (see SETUP.md). Press Escape or Ctrl-C in the window to quit.

Schedule:
  until 25 Dec          counts down to Christmas Day
  25 Dec                "It's Christmas Day!"
  26-31 Dec             counts down to New Year
  1 Jan                 "Happy New Year!"
  from 2 Jan            counts down to next Christmas

Remote buttons: when "remote_buttons" is on in config.json, the Flurry and Fireworks
buttons on the web page also play here. See README.md for how channels work.
"""

import hashlib
import json
import math
import os
import queue
import random
import re
import subprocess
import threading
import time
import urllib.request
from datetime import datetime

VERSION = "2.1.0"
HERE = os.path.dirname(os.path.abspath(__file__))
ACTIONS = ("flurry", "fireworks")


def countdown_state(now):
    """Return (title, line1, line2) for the given datetime."""
    year = now.year
    if now.month == 12 and now.day == 25:
        return "Christmas", "It's Christmas Day!", ""
    if now.month == 1 and now.day == 1:
        return "New Year", "Happy New Year!", ""
    if now.month == 12 and now.day > 25:
        title, target = "New Year", datetime(year + 1, 1, 1)
    else:
        title, target = "Christmas", datetime(year, 12, 25)

    remaining = int((target - now).total_seconds())
    days, rem = divmod(remaining, 86400)
    hours, rem = divmod(rem, 3600)
    mins, secs = divmod(rem, 60)

    def unit(n, word):
        return "%d %s%s" % (n, word, "" if n == 1 else "s")

    return (title,
            unit(days, "day") + " " + unit(hours, "hour"),
            unit(mins, "min") + " " + unit(secs, "second"))


# --- Remote buttons: channel naming (must match index.html) ---

def norm_repo(r):
    r = str(r or "").strip().lower()
    r = re.sub(r"\.git$", "", r)
    return r.strip("/")


def repo_from_git(folder=HERE):
    """owner/repo of the GitHub repo this copy was cloned from, or None."""
    try:
        url = subprocess.run(["git", "-C", folder, "remote", "get-url", "origin"],
                             capture_output=True, text=True, timeout=10).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    if not url:
        return None
    m = re.search(r"github\.com[:/]+([^/]+)/([^/]+?)(?:\.git)?/?$", url, re.I)
    return norm_repo(m.group(1) + "/" + m.group(2)) if m else norm_repo(url)


def topic_for(channel, repo):
    digest = hashlib.sha256(("%s|%s" % (channel, repo)).encode("utf-8")).hexdigest()
    return "xmascd-" + digest[:24]


def load_remote(folder=HERE):
    """Return (relay_topic_url, repo) or (None, reason)."""
    try:
        with open(os.path.join(folder, "config.json")) as f:
            cfg = json.load(f)
    except (OSError, ValueError) as e:
        return None, "no config.json (%s)" % e
    if not cfg.get("remote_buttons") or not cfg.get("relay") or not cfg.get("channel"):
        return None, "remote buttons turned off in config.json"
    repo = norm_repo(cfg.get("repo")) or repo_from_git(folder)
    if not repo:
        return None, "can't tell which repo this is; set \"repo\" in config.json"
    return cfg["relay"].rstrip("/") + "/" + topic_for(cfg["channel"], repo), repo


def listen(url, actions, stop=None):
    """Background thread: stream messages from the relay and queue known actions."""
    backoff = 5
    last = {}
    while not (stop and stop.is_set()):
        try:
            req = urllib.request.Request(url + "/json",
                                         headers={"User-Agent": "ChristmasCountdown/" + VERSION})
            with urllib.request.urlopen(req, timeout=120) as resp:
                print("Remote buttons: listening", flush=True)
                backoff = 5
                for line in resp:
                    if stop and stop.is_set():
                        return
                    try:
                        ev = json.loads(line)
                        if ev.get("event") != "message":
                            continue
                        action = json.loads(ev.get("message", "")).get("action")
                    except (ValueError, AttributeError):
                        continue
                    now = time.monotonic()        # at most one of each per 0.7 s
                    if action in ACTIONS and now - last.get(action, 0) >= 0.7:
                        last[action] = now
                        actions.put(action)
        except Exception as e:                    # network down, relay restarting, ...
            print("Remote buttons: %s; retrying in %ds" % (e, backoff), flush=True)
        if stop and stop.wait(backoff):
            return
        if not stop:
            time.sleep(backoff)
        backoff = min(backoff * 2, 60)


def shade(hex_colour, f):
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))


def main():
    import tkinter as tk

    root = tk.Tk()
    print("Christmas Countdown: version", VERSION)

    # Screen size (uncomment a fixed size to test in a window)
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    # w, h = 800, 600
    print("w, h:", w, h)

    w2 = w // 2
    h1, h2 = 0.22 * h, 0.42 * h     # title lines
    h3, h4 = 0.68 * h, 0.82 * h     # time-to-go lines
    fh1, fh2, fh3 = h // 6, h // 8, h // 16  # font sizes

    nsf = 30                 # number of snowflakes
    speed = h / 300.0        # fall speed
    wind = w / 10000.0
    colours = ["white", "orange", "white", "yellow", "white",
               "cyan", "white", "blue", "white", "violet"]

    root.geometry("%dx%d+0+0" % (w, h))
    root.configure(cursor="none")
    root.bind("<Escape>", lambda e: root.destroy())
    root.bind("<Control-c>", lambda e: root.destroy())

    canvas = tk.Canvas(root, width=w, height=h, bg="black",
                       highlightthickness=0)
    canvas.pack()

    # Create text items once; update their text in place
    title = canvas.create_text(w2, h1, text="Christmas",
                               fill="red", font=("Times", fh1))
    canvas.create_text(w2, h2, text="Countdown!",
                       fill="red", font=("Times", fh1))
    t1 = canvas.create_text(w2, h3, fill="green", font=("Times", fh2))
    t2 = canvas.create_text(w2, h4, fill="green", font=("Times", fh2))

    # each flake: [item, dx, dy, temporary]
    flakes = []
    for _ in range(nsf):
        s = speed + speed * random.random() * 3
        item = canvas.create_text(random.randrange(w), random.randrange(h),
                                  text="*", fill=random.choice(colours),
                                  font=("Times", int(fh3 * s / speed / 4)))
        flakes.append([item, wind + wind * random.random(), s, False])

    def update():
        heading, line1, line2 = countdown_state(datetime.now())
        canvas.itemconfigure(title, text=heading)
        canvas.itemconfigure(t1, text=line1)
        canvas.itemconfigure(t2, text=line2)
        root.after(200, update)

    # --- Flurry: a burst of extra, faster snow that falls away ---
    def flurry():
        if len(flakes) > 400:                    # don't let repeated presses pile up
            return
        for _ in range(120):
            s = speed * (3 + random.random() * 4)
            item = canvas.create_text(random.uniform(-0.1 * w, w), -10 - random.random() * h * 0.5,
                                      text="*", fill=random.choice(colours),
                                      font=("Times", max(6, int(fh3 * (0.3 + random.random() * 0.9)))))
            flakes.append([item, wind * (4 + random.random() * 8), s, True])

    def update_snow():
        for f in list(flakes):
            item, dx, dy, temp = f
            canvas.move(item, dx, dy)
            x, y = canvas.coords(item)
            if temp:
                if y > h + 10 or x > w + 10:
                    canvas.delete(item)
                    flakes.remove(f)
                continue
            if y > h + 10:
                # back to the top with a new colour
                canvas.coords(item, random.randrange(w), -10)
                canvas.itemconfigure(item, fill=random.choice(colours))
                if random.random() > 0.99:   # send a few back up
                    f[2] = -abs(dy)
                    canvas.coords(item, random.randrange(w), h)
            elif y < -10:                    # stop those going up forever
                f[2] = abs(dy)
            if x > w + 10:                   # wrap if blown off the side
                canvas.coords(item, -10, y)

    # --- Fireworks: rockets and bursts for 5 seconds (lighter than the web version for the Pi) ---
    fw_colours = ["#ff3b3b", "#ffd700", "#3bff6b", "#3bd5ff", "#ff5bf0", "#ffffff", "#ff9a2e"]
    fw_fades = {c: [shade(c, f) for f in (1.0, 0.75, 0.5, 0.3, 0.15)] for c in fw_colours}
    fw = {"until": 0.0, "next": 0.0}
    rockets, sparks = [], []      # rocket: [item, x, y, vy, top, colour]; spark: dict
    r = max(2, h // 260)

    def fireworks():
        fw["until"] = time.monotonic() + 5

    def burst(x, y, colour):
        v = h / 110.0
        for _ in range(45):
            a = random.random() * 6.283
            sp = v * (0.4 + random.random() * 0.8)
            c = "#ffffff" if random.random() < 0.15 else colour
            item = canvas.create_oval(x - r, y - r, x + r, y + r, fill=c, outline="")
            life = random.randint(25, 45)
            sparks.append({"item": item, "vx": sp * math.cos(a),
                           "vy": sp * math.sin(a), "life": life,
                           "full": life, "colour": c, "level": 0})

    def update_fireworks():
        now = time.monotonic()
        if now < fw["until"] and now >= fw["next"]:   # a rocket every 0.2-0.45 s
            x = w * (0.1 + random.random() * 0.8)
            item = canvas.create_line(x, h, x, h + r * 6, fill="#ffe9b0", width=r)
            rockets.append([item, x, float(h), -h / 38.0 * (0.85 + random.random() * 0.3),
                            h * (0.12 + random.random() * 0.35), random.choice(fw_colours)])
            fw["next"] = now + 0.2 + random.random() * 0.25
        for rk in list(rockets):
            item, x, y, vy, top, colour = rk
            canvas.move(item, 0, vy)
            rk[2] = y + vy
            if rk[2] <= top:
                canvas.delete(item)
                rockets.remove(rk)
                burst(x, rk[2], colour)
        g = h / 4000.0
        for p in list(sparks):
            p["vx"] *= 0.97
            p["vy"] = p["vy"] * 0.97 + g
            canvas.move(p["item"], p["vx"], p["vy"])
            p["life"] -= 1
            if p["life"] <= 0:
                canvas.delete(p["item"])
                sparks.remove(p)
                continue
            level = min(4, int((1 - p["life"] / p["full"]) * 5))
            if level != p["level"]:               # only recolour when the shade changes
                p["level"] = level
                canvas.itemconfigure(p["item"], fill=fw_fades.get(p["colour"], [p["colour"]] * 5)[level])

    # --- Remote buttons from the web page ---
    actions = queue.Queue()
    url, info = load_remote()
    if url:
        print("Remote buttons: channel for", info, flush=True)
        threading.Thread(target=listen, args=(url, actions), daemon=True).start()
    else:
        print("Remote buttons off:", info, flush=True)

    def tick():
        try:
            while True:
                a = actions.get_nowait()
                if a == "flurry":
                    flurry()
                elif a == "fireworks":
                    fireworks()
        except queue.Empty:
            pass
        update_snow()
        update_fireworks()
        root.after(50, tick)

    # Keys for testing on the Pi itself
    root.bind("f", lambda e: fireworks())
    root.bind("s", lambda e: flurry())

    root.focus_force()
    update()
    tick()
    root.mainloop()


if __name__ == "__main__":
    main()
