#! /usr/bin/python

# If run from a window manager:
# tk.overrideredirect(1) causes full screen behaviour
# If run from the command line you can exit with Ctrl-c or Alt-F4 to close window
# If run via xinit these are not needed

import time
import random
from datetime import datetime
from Tkinter import *

tk = Tk()

# screen size
w, h = tk.winfo_screenwidth(), tk.winfo_screenheight()
#w, h = 480, 320
#w, h = 800, 600
print "w, h, ", w, h

# Centre text
w2 = w/2

# Title text pos
h1 = 0.22 * h
h2 = 0.42 * h

# Time to go text
h3 = 0.68 * h
h4 = 0.82 * h

# font size
fh1 = h / 6
fh2 = h / 8
fh3 = h / 16

# number of snowflakes
nsf = 30

# fall speed
speed = h / 300.0
wind = w / 10000.0
print "wind, speed, ", wind, speed

#tk.overrideredirect(1)
tk.geometry("%dx%d+0+0" % (w, h))

# If we run tk.mainloop(), these would enable keyboard input
#tk.focus_set() # <-- move focus to this widget
tk.bind("<Escape>", lambda e: e.widget.quit())
tk.bind("<Control-c>", lambda e: e.widget.quit())

canvas = Canvas(tk, width=w, height=h, bg='black')

canvas.create_text(w2, h1, text="Christmas",
                       fill='red', font=('Times', fh1))

canvas.create_text(w2, h2, text="Countdown!",
                       fill='red', font=('Times', fh1))
canvas.pack()

flake = [];
moves = []
for i in range(nsf):
    flake.append(canvas.create_text(random.randrange(w),random.randrange(h),text="*",
                                    fill='white',font=('Times', fh3)))
    moves.append([wind + wind*random.random(), speed + speed*random.random()])


def update():
    global canvas, tk, t1, t2

    try:
        canvas.delete(t1)
        canvas.delete(t2)
    except:
        pass
    
    d = 24 - int(datetime.now().strftime('%d'))
    days = str(d)
    hours = str(23 - int(datetime.now().strftime('%H')))
    mins = str(59 - int(datetime.now().strftime('%M')))
    secs = str(59 - int(datetime.now().strftime('%S')))

    if d >= 0:
        time_str1 = days+' days '+hours+' hours'
        time_str2 = mins+' mins '+secs+' seconds'
    elif d == -1:
        time_str1 = "It's Christmas Day!"
        time_str2 = ""
    else:
        time_str1 = "Till next year..."
        time_str2 = '11 months '+ str(d+7) +' days'

    t1=canvas.create_text(w2, h3, text=time_str1,
                       fill='green', font=('Times', fh2))
    t2=canvas.create_text(w2, h4, text=time_str2,
                       fill='green', font=('Times', fh2))

    tk.after(200, update)
        

def update_snow():
    global flake, canvas, tk, moves
    
    for i in range(len(flake)):
        p = canvas.coords(flake[i])
        p[0]+=moves[i][0]
        p[1]+=moves[i][1]
        canvas.coords(flake[i],p[0],p[1])
        if(p[1]>h+10):
            canvas.coords(flake[i],random.randrange(w),-10)

    tk.after(50, update_snow)

  
update()
update_snow()
tk.mainloop()

