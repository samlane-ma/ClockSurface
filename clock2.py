#!/usr/bin/env python3

from clocksurface import ClockSurface
import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

"""
Examples of ClockSurface class with customizations.
#1 is a ticking basic default clock
#2 is a manually set clock that does not move
#3 is a smaller clock with no time set
#4 is a larger ticking clock with customizations
"""

window = Gtk.Window()
window.connect("destroy", Gtk.main_quit)

grid = Gtk.Grid()
window.add(grid)

image1 = Gtk.Image()
clock1 = ClockSurface()
clock1.set_time(time.localtime())
image1.set_from_surface(clock1.get_surface())
grid.attach(image1,0,0,1,1)
clock1.start_clock(image1, 1)

image2 = Gtk.Image()
clock = ClockSurface()
clock.marktype = ClockSurface.NO_MARKS
clock.set_hour_min_sec(3,22)
clock.drawseconds = True
surface = clock.get_surface()
image2.set_from_surface(surface)
grid.attach(image2,1,0,1,1)

image3 = Gtk.Image()
clock = ClockSurface()
clock.set_size(50)
surface = clock.get_surface()
image3.set_from_surface(surface)
grid.attach(image3,0,1,1,1)

image4 = Gtk.Image()
clock4 = ClockSurface(200)
clock4.hourhand_color = "red"
clock4.minhand_color = "blue"
clock4.sechand_color = "green"
clock4.face_color = "rgba(33,245,45,.2)"
clock4.drawseconds = True
clock4.marktype = ClockSurface.MIXED_MARKS
grid.attach(image4,1,1,1,1)
clock4.start_clock(image4)

window.show_all()

Gtk.main()
