# ClockSurface
## Python module to create a clock surface

ClockSurface is a python class written for a applet before deciding to rewrite the applet in Vala.  This module is by no means a perfect work of art, but rather than wasting the effort, possibly this will be of use to someone.

ClockSurface creates a cairo clock surface that can be used to set a Gtk.Image.  Without any parameters or customizations, it will return a 100px x 100px cairo.ImageSurface, with a white face, black hands, basic markings, and the time set to the current time.

The clock can be easily customized to change the color of the face, frame, and hands.  Furthermore, attributes such as length and width of the hands, the types of hour markings, and whether or not to show the second hand.

Using ClockSurface.start_clock, it will continually update the Gtk.Image passed to it, making the clock "tick".

The provided clock1.py and clock2.py are working examples of the class in action.

``` clock = ClockSurface(200) ```
  
  Creates a clock image 200px by 200px.  If no size is given, it defaults to 100px.

## Methods:


* ClockSurface.set_size(size: int, resize=True)

  Changes the clock to the specified pixel size.  If resize is False, preserve any customizations that may have been made to the hand and marking lengths / widths
  
* ClockSurface.set_linewidth(width: int)

  Sets the line width in pixels for all the hands, and markings.
  It is possible to change the attributes individually:
    * ClockSurface.hourhand_width = width (width of the hour hand)
    * ClockSurface.minhand_width  = width (width of the minute hand)
    * ClockSurface.sechand_width  = width (width of the second hand)
    * ClockSurface.mark_width     = width (size of the edge hour markings)
    * ClockSurface.dot_size       = width (size of the center dot)
     
* ClockSurface.set_framewidth(width: int)
  Sets the width of the clock frame (outline)
  
* ClockSurface.set_colors(face: str, frame: str, hand: str)
  
  Sets the colors of the clock.  Colors are passed as strings and can be in the formats:
    * name: "red", "blue", etc
    * rgb : "rgb(250, 128, 0)"
    * rgba: "rgba(128, 128, 128, .5)" (useful for making transparent)
    * hex " "#FF00EE"
  Hand colors can be set individually as well:
    * ClockSurface.hourhand_color = "black"
    * ClockSurface.minhand_color = "#FF0000"
    * ClockSurface.sechand_color = "red"

* ClockSurface.set_time(settime: time.time_struct)
  
  Sets the time to draw using a time.time_struct class.
    Ex: ClockSurface.set_time(time.localtime())

* ClockSurface.set_time(hours: int, minutes: int, seconds: int)
  
  Sets the time to draw using given hours, minutes, and seconds.  Seconds defaults to 0 if not given.

* ClockSurface.get_surface()
  
  Returns the cairo.ImageSurface that contains the clock drawing.  
  It can then be used with Gtk.Image.create_from_surface to make a clock image

* ClockSurface.start_clock(image: Gtk.Image, seconds: int)
  Updates the image passed with the current time at the interval passed by "seconds".  Defaults to 1 second.

* Other properties that can be modified:
  * ClockSurface.minhand_len  = <int>        (length of minute hand in px)
  * ClockSurface.hourhand_len = <int>        (length of hour hand in px)
  * ClockSurface.sechand_len  = <int>        (length of second hand in px)
  * ClockSurface.mark_len     = <int>        (length of hour marks)
  * ClockSurface.drawseconds  = True|False   (whether or not to draw the second hand)
  * ClockSurface.mark_type    = <mark type>  (which style to make the edge hour markings)
  * Valid options are:
      * ClockSurface.NO_MARKS      (no markings are drawn)
      * ClockSurface.ALL_MARKS     (all markings are drawn, all the same size)
      * ClockSurface.MIXED_MARKS   (full size markings at 3/6/9/12, rest are smaller)
      * ClockSurface.QUARTER_MARKS (only draw marks at 3/6/9/12)
