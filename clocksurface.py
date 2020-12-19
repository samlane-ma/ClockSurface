import cairo
import gi
import time
from math import cos, sin, pi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

"""
ClockSurface class
Author: Sam Lane
Copyright © 2020 Sam Lane
Website: https://github.com/samlane-ma/

Simple class that creates a Cairo ImageSurface that contains a clock drawing.
Useful for adding to a Gtk.Image to display a clock.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or any later version. This
program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details. You
should have received a copy of the GNU General Public License along with this
program.  If not, see <http://www.gnu.org/licenses/>.
"""

class ClockSurface():
    # Used to indicate if / how the hour markings are drawn
    NO_MARKS=0        # Don't draw any markings
    ALL_MARKS=1       # Draw all markings, all same size
    MIXED_MARKS=2     # Full size markings at 3,6,9,12 - rest drawn shorter
    QUARTER_MARKS=3   # Only draw markings at 3,6,9,12

    def __init__(self, size: int = 100):
        # Default clock with no options set will be 100px with white face,
        # black hands and frame
        self.FULL_CIRCLE = pi * 2
        self.set_size(size)
        self.marktype = ClockSurface.ALL_MARKS
        self.drawseconds = False
        self.set_hour_min_sec(12,0,0)
        self.set_color("white","black","black")

    def set_size(self, size: int = 100, resize = True):
        # Sets the clock size.  If resize = False, it will not change
        # existing line widths / hand lengths
        self.size = size
        self.center = self.size / 2
        self.radius = self.size / 2
        if resize:
            self.frame_width = self.size / 50
            self.set_linewidth(size / 50)
            self.minhand_len = (self.size / 2) * .75
            self.hourhand_len = (self.size / 2) * .5
            self.sechand_len = (self.size / 2) * .75
            self.mark_len = self.radius - (self.radius * .92) + (self.frame_width / 3)
        self.radius = self.size / 2 - self.frame_width

    def set_linewidth(self, width: int = 2):
        # sets all drawing sizes except the frame to the given width
        self.hourhand_width = width
        self.minhand_width = width
        self.sechand_width = width * .5
        self.dot_size = width
        self.mark_width = width

    def set_framewidth(self, width: int = 2):
        # sets the frame to the given width, and updates the radius
        # to make sure the frame doesn't extend outside the image
        self.frame_width = width
        self.radius = self.size / 2 - self.frame_width

    def set_color(self, face="", frame="" , hand=""):
        # Colors can be set in:
        #    hex        : "#FF00EEE"
        #    rgb/rgba   : "rgba(232,143,222,0.3)"
        #    color name : "red"
        if not face == "":
            self.face_color = face
        if not frame == "":
            self.frame_color = frame
        if not hand == "":
            self.hourhand_color = hand
            self.minhand_color = hand
            self.sechand_color = hand

    def set_time(self, settime: time.struct_time):
        # set the time to draw using a time.struct_time
        # such as that returned by time.localtime()
        self.set_hour_min_sec(settime.tm_hour, settime.tm_min, settime.tm_sec)

    def set_hour_min_sec(self, hours: int, minutes: int , seconds: int = 0):
        # set the time to draw using manually given values
        self.hours = hours
        if self.hours > 12:
            self.hours = self.hours - 12
        self.hours = self.hours * 5 + (minutes / 12)
        self.minutes = minutes
        self.seconds = seconds

    def _get_coord(self, c_type, hand_position, length, center):
        # used internally to get the x / y coordinates to draw the hands
        # based on position on the clock (1..60)
        hand_position -= 15;
        if hand_position < 0:
            hand_position += 60
        radians = (hand_position * self.FULL_CIRCLE / 60);
        if c_type == "x":
            return center + length * cos(radians)
        elif c_type == "y":
            return center + length * sin(radians)
        else:
            return 0

    def get_surface(self):
        # returns a Cairo ImageSurface containing the clock drawing, with which
        # a Gtk.Image can be set to, using set_from_surface

        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.size, self.size)
        cr = cairo.Context(self.surface)
        color = Gdk.RGBA()
        color.parse(self.face_color)
        cr.set_source_rgba(color.red, color.green, color.blue, color.alpha)
        cr.arc(self.center, self.center, self.radius, 0, self.FULL_CIRCLE)
        cr.fill()

        color.parse(self.frame_color);
        cr.set_source_rgba(color.red, color.green, color.blue, color.alpha)
        cr.set_line_width(self.frame_width)
        cr.arc(self.center, self.center, self.radius, 0, self.FULL_CIRCLE)
        cr.stroke()

        if not self.marktype == ClockSurface.NO_MARKS:
            cr.set_line_cap(cairo.LineCap.BUTT)
            cr.set_line_width(self.mark_width)
            for i in range(12):
                if i % 3 == 0 or not self.marktype == ClockSurface.QUARTER_MARKS:
                    if self.marktype == ClockSurface.MIXED_MARKS and not i % 3 == 0:
                        drawsize = self.mark_len * .6
                    else:
                        drawsize = self.mark_len
                    cr.move_to(self._get_coord("x", i * 5, self.radius, self.center),
                               self._get_coord("y", i * 5, self.radius, self.center))
                    cr.line_to(self._get_coord("x", i * 5, self.radius - drawsize, self.center),
                               self._get_coord("y", i * 5, self.radius - drawsize, self.center))
                    cr.stroke()

        color.parse(self.minhand_color)
        cr.set_source_rgba(color.red, color.green, color.blue, color.alpha)
        cr.set_line_width(self.minhand_width)
        cr.set_line_cap(cairo.LineCap.ROUND)
        cr.move_to(self.center,self.center);
        cr.line_to(self._get_coord("x", self.minutes, self.minhand_len, self.center),
                   self._get_coord("y", self.minutes, self.minhand_len, self.center))
        cr.stroke()

        color.parse(self.hourhand_color)
        cr.set_source_rgba(color.red, color.green, color.blue, color.alpha)
        cr.set_line_width(self.hourhand_width)
        cr.set_line_cap(cairo.LineCap.ROUND)
        cr.move_to(self.center, self.center)
        cr.line_to(self._get_coord("x", self.hours, self.hourhand_len, self.center),
                   self._get_coord("y", self.hours, self.hourhand_len, self.center))
        cr.stroke()

        if self.drawseconds:
            color.parse(self.sechand_color)
            cr.set_source_rgba(color.red, color.green, color.blue, color.alpha)
            cr.set_line_width(self.sechand_width)
            cr.set_line_cap(cairo.LineCap.ROUND)
            cr.move_to(self.center, self.center)
            cr.line_to(self._get_coord("x", self.seconds, self.sechand_len, self.center),
                       self._get_coord("y", self.seconds, self.sechand_len, self.center))
            cr.stroke()

        cr.arc(self.center, self.center, self.dot_size * 0.75, 0, self.FULL_CIRCLE);
        cr.fill();

        return self.surface

    def _tick(self, image):
        # internal - called by start_clock to update the image passed to it
        self.set_time(time.localtime())
        image.set_from_surface(self.get_surface())
        time.tzset()  #catch possible change to timezone / daylight savings
        return True

    def start_clock(self, image, seconds = 1):
        # adds the clock drawing to the image passed, and starts updating it
        self.set_time(time.localtime())
        image.set_from_surface(self.get_surface())
        GLib.timeout_add_seconds(seconds,self._tick,image)
