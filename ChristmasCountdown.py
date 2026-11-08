#!/usr/bin/env python3
"""Christmas Countdown - full-screen countdown to Christmas Day (and New Year).

Intended for a Raspberry Pi without the desktop running, e.g. driving a projector
via xinit (see RUN_ChristmasCountdown.sh). Press Escape or Ctrl-C in the window to quit.

Schedule:
  until 25 Dec          counts down to Christmas Day
  25 Dec                "It's Christmas Day!"
  26-31 Dec             counts down to New Year
  1 Jan                 "Happy New Year!"
  from 2 Jan            counts down to next Christmas
"""

import random
from datetime import datetime

VERSION = "2.0.0"


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

    flakes = []
    for _ in range(nsf):
        s = speed + speed * random.random() * 3
        item = canvas.create_text(random.randrange(w), random.randrange(h),
                                  text="*", fill=random.choice(colours),
                                  font=("Times", int(fh3 * s / speed / 4)))
        flakes.append([item, wind + wind * random.random(), s])

    def update():
        heading, line1, line2 = countdown_state(datetime.now())
        canvas.itemconfigure(title, text=heading)
        canvas.itemconfigure(t1, text=line1)
        canvas.itemconfigure(t2, text=line2)
        root.after(200, update)

    def update_snow():
        for f in flakes:
            item, dx, dy = f
            canvas.move(item, dx, dy)
            x, y = canvas.coords(item)
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
        root.after(50, update_snow)

    root.focus_force()
    update()
    update_snow()
    root.mainloop()


if __name__ == "__main__":
    main()
