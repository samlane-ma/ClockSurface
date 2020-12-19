#!/usr/bin/env python3

from clocksurface import ClockSurface
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

"""
Most basic example of the ClockSurface class in action.
Creates a simple ticking clock with the defaults.
"""

window = Gtk.Window()
window.connect("destroy", Gtk.main_quit)

image = Gtk.Image()
window.add(image)

clock = ClockSurface()
clock.start_clock(image)

window.show_all()

Gtk.main()
