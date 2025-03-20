

from .backend_gtk import WidgetBase, Gtk, Gdk, gi, FrameWidget
gi.require_version('Gst', '1.0')
from gi.repository import Gst


class VideoWidget(WidgetBase):
    
    def __init__(self, parent, toplevel):
        super().__init__(parent)
        self.toplevel = toplevel.gtk 
        #self.gtk = Gtk.Frame()
 
        #self.gtk = Gtk.DrawingArea()
        #Gtk.init()
        Gst.init()
        factory = Gst.ElementFactory()
        
        self.playbin = factory.make('playbin')
        self.playbin.set_property(
                'uri',
                'https://gstreamer.freedesktop.org/data/media/sintel_trailer-480p.webm',)

        self.gtksink = factory.make('gtksink')
        if not self.gtksink:
            raise RuntimeError('Could not create gtksink')
        self.audiosink = factory.make('alsasink')
        if not self.audiosink:
            raise RuntimeError('Could not create alsasink')

        self.sink_widget = self.gtksink.get_property('widget')
        self.gtk = self.sink_widget     
        self.playbin.set_property('video-sink', self.gtksink)
        #self.playbin.set_property('audio-sink', self.audiosink)
        

        #self.videosink.set_property('sink', self.gtksink)
        #print(dir(self.sink))
        #self.pipeline.add(self.sink)
       
        print(dir(self.playbin))

        #self.playbin.set_property('video-sink', self.videosink)

        #self.playbin.add(self.sink)
        #self.src.link(self.sink)
        
        #self.src.link(self.convert)
        #self.convert.link(self.gtksink)
        #self.videosink.link(self.gtksink)
        
        #self.gtk = self.sink_widget
        #self.gtk.show()
        #self.sink_widget.show()
        #self.gtk.add(self.sink_widget)
        #self.gtk.add(self.sink_widget)
        #self.gtk_grid.add(self.sink_widget)
        self.playbin.set_state(Gst.State.PLAYING)
    
    def grid(self):
        #print(self.gtk.)
        self.gtk.unparent() 
        parent = self.gtk.get_parent()
        print(parent)
        #parent.remove(self.gtk)
        
        self.gtk.reparent(self.toplevel)

        #self.toplevel.add(self.gtk)
        super().grid()
        #print(dir(self.gtk))
        #self.gtk.set_window(self.active_window)
        #self.gtk.show_all()
        #self.parent.gtk.add(self.gtk)
