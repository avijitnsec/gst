import gi 
from time import sleep

from threading import Thread
gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib

Gst.init()

main_loop = GLib.MainLoop()
main_loop_thread = Thread(target=main_loop.run)
main_loop_thread.start()

# pipeline = Gst.parse_launch("ksvideosrc ! decodebin  ! videoconvert ! autovideosink") # edgetv  rippletv
# pipeline = Gst.parse_launch(" videotestsrc ! autovideosink ")
# pipeline = Gst.parse_launch(" playbin uri=2.mp4 ")

# pipeline = Gst.parse_launch(" videotestsrc pattern=0 ! gdkpixbufoverlay location=logo1.png ! progressreport update-freq=1 ! autovideosink" )
# pipeline = Gst.parse_launch("playbin uri=https://www.freedesktop.org/software/gstreamer-sdk/data/media/sintel_trailer-480p.webm !\
#     timeoverlay halignment=right valignment=bottom text='Stream time:' shaded-background=true")

pipeline = Gst.parse_launch(" ksvideosrc \
        ! decodebin  \
        ! videoconvert \
        ! textoverlay name=txt halignment=right valignment=bottom shaded-background=true \
        ! videomixer  \
        ! timeoverlay halignment=left valignment=bottom text='Stream time:' shaded-background=true  \
        ! videomixer  \
        ! rippletv ! videoconvert \
        ! autovideosink window-width=640 window-height=480 \
        ")

pipeline.set_state(Gst.State.PLAYING)

t = 180*60
try:
    while True:
        sleep(1)
        txt = pipeline.get_by_name("txt")
        # txt.text = 20

        print (txt.get_property("text"))
        txt.set_property("text", str(t))
        t = t-1

except KeyboardInterrupt:
    pass

pipeline.set_state(Gst.State.NULL)
main_loop.quit()
main_loop_thread.join()