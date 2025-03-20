'''Implementation of the hosguibase in GTK (using PyGObject).

Gtk versions 3 and 4 are supported (3 is recommended).

Use "--gtk4" switch to the program to use version 4, otherwise
it will use the version 3.
'''

import sys
import time

import gi

# GTK4 is newer but has annoingly blurry font rendering
# GTK3 is supported until GTK5 is released
if '--gtk4' in sys.argv:
    GTK_VERSION = 4
elif '--gtk3' in sys.argv:
    GTK_VERSION = 3
else:
    # Default
    GTK_VERSION = 3

if GTK_VERSION == 3:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
elif GTK_VERSION == 4:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Gdk', '4.0')
else:
    raise ValueError(f'Invalid GTK version: {GTK_VERSION}')
from gi.repository import Gtk, Gdk, GLib


from .common import CommonMainBase, CommonWidgetBase


class GuiBase:
    '''Common methods for the widgets and the main window.
    '''
    def after(self, millis, function):
        '''Schedules a function to be ran milliseconds later.
        '''
        def wrapper():
            function()
            return False
        return GLib.timeout_add(millis, wrapper)
    

class MainWindow(CommonMainBase, GuiBase):

    def __init__(self, frameless=False):
        super().__init__()

        self.gtk = Gtk.Window()
        self.gtk_grid = Gtk.Grid()
        self._title = ''

        if frameless:
            self.gtk.set_decorated(False)
        self.geometry = 'medium'

        self.gtk.add(self.gtk_grid)
        #self.gtk.present()
        
        # Workaround for showall in run that shows also hidden widgets 
        self._hidelist = []

    def exit(self, arg):
        self._exit = True
        print('exiting')

    def run(self):
        super().run()

        if GTK_VERSION == 3:
            #self.gtk.add(self.gtk_grid)
            self.gtk.connect('destroy', Gtk.main_quit)
            self.gtk.show_all()
            for widget in self._hidelist:
                widget.set_visibility(False)
            Gtk.main()
        else:
            # Using a manual looping for GTK4. The application-
            # signal API seem to unallow the current "tkinter-like"
            # GUI construction
            self.gtk.present()
            context = GLib.MainContext.default()
            self._exit = False
            self.gtk.connect('destroy', self.exit)
            while not self._exit:
                context.iteration(True)
        self.running = False


    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, name):
        self.gtk.set_title(name)
        self._title = name

    @staticmethod
    def _getmon():
        return Gdk.Display.get_default().get_monitor(0)

    @property
    def screen_width(self):
        return self._getmon().get_geometry().width
    
    @property
    def screen_height(self):
        return self._getmon().get_geometry().height
    
    @property
    def geometry(self):
        return self.gtk.get_size()

    @geometry.setter
    def geometry(self, string):
        width, height, x, y = super().parse_geometry(string)
        
        self.gtk.set_default_size(width, height)
        
        if x is not None and y is not None:
            self.gtk.move(x, y)

    
    def destroy(self):
        print('now closign')
        self.gtk.close()
        self.gtk.destroy()

    def withdraw(self):
        pass

    def get_backend_info(self):
        return {'name': 'gtk'}


class WidgetBase(GuiBase, CommonWidgetBase):
    
    def __init__(self, parent):
        self.parent = parent
        self._root = self.get_root()
        self._visible = True

    def grid(self, row=0, column=0, sticky='NSWE',
             columnspan=1, rowspan=1,
             column_weight=1, row_weight=1):
        
        left, right, top, bottom = self.margins
        if not (left == right == top == bottom == 0):
            self.gtk.set_margin_start(left)
            self.gtk.set_margin_end(right)
            self.gtk.set_margin_top(top)
            self.gtk.set_margin_bottom(bottom)
        

        if not hasattr(self.parent, 'gtk_grid'):
            self.parent.gtk_grid = Gtk.Grid()

            if GTK_VERSION == 3:
                self.parent.gtk.add(
                        self.parent.gtk_grid)
            else:
                self.parent.gtk.set_child(
                        self.parent.gtk_grid)


        self.parent.gtk_grid.attach(
                self.gtk, column, row, columnspan, rowspan)
        
        we = 'W' in sticky and 'E' in sticky
        ns = 'N' in sticky and 'S' in sticky

        if column_weight != 0 and we:
            self.gtk.set_hexpand(True)
        else:
            self.gtk.set_hexpand(False)

        if row_weight != 0 and ns:
            self.gtk.set_vexpand(True)
        else:
            self.gtk.set_vexpand(False)
        
        if not we and 'W' in sticky:
            self.gtk.set_halign(Gtk.Align.START)
            print('w')
        elif not we and 'E' in sticky:
            self.gtk.set_halign(Gtk.Align.END)
            print('e')
        
        if not ns and 'N' in sticky:
            self.gtk.set_valign(Gtk.Align.START)
            print('w')
        elif not ns and 'S' in sticky:
            self.gtk.set_valign(Gtk.Align.END)
            print('e')
        
        if self._visible:
            self.gtk.show()

        #self.tk.grid(
        #        row=row, column=column, sticky=sticky,
        #        columnspan=columnspan, rowspan=rowspan)
        # 
        #self.parent.tk.columnconfigure(column, weight=column_weight)
        #self.parent.tk.rowconfigure(row, weight=row_weight)


    def set_command(self, command):
        #FIXME
        return None

        #if not callable(command):
        #    raise ValueError('Command has to be callable')
        #self.command = command
        #try:
        #    self.tk.configure(command=self._command_wrapper)
        #except:
        #    pass
    
    def set_visibility(self, showed):
        if showed:
            if not self._root.running and self in self._root._hidelist:
                self._root._hidelist.remove(self)
            self.gtk.show()
            self._visible = True
        else:
            if not self._root.running:
                self._root._hidelist.append(self)
            self.gtk.hide()
            self._visible = False

    def grid_remove(self):
        self.parent.gtk_grid.remove(self.gtk)
        self.gtk.hide()

    def _ensure_connect_button(self):
        
        # If handler already connected do not do again
        if getattr(self, 'leftclick_handler', None) is not None: return
        if getattr(self, 'rightclick_handler', None) is not None: return

        self.gtk.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.gtk.connect('button-release-event', self._click_wrapper)
        self.gtk.set_focus_on_click(True)
        self.gtk.set_sensitive(True)           



    def set(self, text=None, bg=None, active_bg=None, resize_handler=None,
            leftclick_handler=None, rightclick_handler=None,
            enter_handler=None, exit_handler=None):
        '''Configure extra settings supported by all widgets.

        Setting a parameter to None makes no changes to the setting
        and setting it False disables or sets the setting to its
        default value.

        text : string
            Sets the text label
        bg, active_bg : string or list/tuple?
            Sets the background colour
        resize_handler : callable or False
            Called when the widget is being resized
        leftclick_handler, rightclick_handler : callable or False
            When left and rightclick are pressed over the widget.
            It is better to use a command where applicable.
        enter_handler, exit_handler : callable or False
            When mouse comes to hover over and leaves
        '''

        if text is not None:
            self.gtk.set_text(text)
        
        #if bg is not None:
        #    self.tk.configure(bg=bg)
        #if active_bg is not None:
        #    self.tk.configure(activebackground=active_bg)
        if resize_handler is not None:
            if not callable(resize_handler):
                raise ValueError('Resize handler has to be callable')
            self.resize_handler = resize_handler
            self._last_resized = 0
            self.get_root().gtk.connect('configure-event', self._resize_handler_wrapper)

        if leftclick_handler is not None:
            self._ensure_connect_button()
            self.leftclick_handler = leftclick_handler
        if rightclick_handler is not None:
            self._ensure_connect_button()
            self.rightclick_handler = rightclick_handler
        
        #if enter_handler is not None:
        #    self.tk.bind('<Enter>', enter_handler)
        #if exit_handler is not None:
        #    self.tk.bind('<Enter>', exit_handler)

    def get(self, key):
        if key == 'text':
            return self.gtk.get_text()

    def _click_wrapper(self, box, button):
        if button.button == 1:
            cmd = getattr(self, 'leftclick_handler', None)
        elif button.button == 3:
            cmd = getattr(self, 'rightclick_handler', None)
        else:
            return
        if cmd is not None:
            cmd()

    def _resize_handler_wrapper(self, arg1, arg2):
        if time.time() > self._last_resized + 1/5:
            self.resize_handler(arg2.width, arg2.height)
            self._last_resized = time.time() 

    def grab_focus(self):
        self.gtk.grab_focus()
    
    def destroy(self):
        self.gtk.destroy()


class InputWidgetBase(WidgetBase):
    '''Common base class for all widgets taking in user input.
    '''

    def __init__(self, parent):
        super().__init__(parent)
    
    def get_input(self):
        '''Returns the state of the current value.
        '''
        return self.gtk.get_text()
    
    def set_input(self, text):
        '''Returns the state of the current value.
        '''
        return self.gtk.set_text(text)

    def _command_wrapper(self, arg):
        self.command(arg)


class FrameWidget(WidgetBase):
    def __init__(self, parent):
        super().__init__(parent)
        #self.gtk = Gtk.Frame()
        self.gtk = Gtk.Grid()
        self.gtk_grid = self.gtk

class ScrollableFrame(WidgetBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.gtk = Gtk.ScrolledWindow()

class TextWidget(WidgetBase):

    def __init__(self, parent, text=''):
        super().__init__(parent)
        self.gtk = Gtk.Label()
        self.gtk.set_text(text)

class ButtonWidget(WidgetBase):
    def __init__(self, parent, text='', command=None):
        super().__init__(parent)
        self.gtk = Gtk.Button.new_with_label(str(text))
        
        if command is not None:
            self.set_command(command)
   
    
    def set(self, text=None, **kwargs):
        if text is not None:
            self.gtk.set_label(text)

    def set_command(self, command):
        self._command = command
        self.gtk.connect('clicked', self._run_command)

    def _run_command(self, *args):
        self._command()

class SliderWidget(InputWidgetBase):
    def __init__(self, parent, from_=0, to=1, resolution=None, horizontal=True):
        super().__init__(parent)
        if horizontal:
            orientation = Gtk.Orientation.HORIZONTAL
        else:
            orientation = Gtk.Orientation.VERTICAL

        if resolution is None:
            resolution = (to-from_)/100

        #adjustment = Gtk.Adjustment(0.5, from_, to, (to-from_)/100, 1,1)
        self.gtk = Gtk.Scale.new_with_range(
                orientation, from_, to, resolution)
        #self.gtk = Gtk.Scale(orientation, adjustment)
   
    def set_command(self, command):
        self._on_change = command
        self.gtk.connect('value-changed', self._on_change_wrapper)
    
    def _on_change_wrapper(self, arg1):
        value = self.get_input()
        self._on_change(value)

    def get_input(self):
        '''Returns the state of the current value.
        '''
        return self.gtk.get_value()

    def set_input(self, value):
        self.gtk.set_value(value)

 
class EntryWidget(InputWidgetBase):
    def __init__(self, parent, on_enter=None):
        super().__init__(parent)
        self.gtk = Gtk.Entry()
        if on_enter is not None:
            self._on_enter = on_enter
            self.gtk.connect('activate', self._on_enter_wrapper)
    
    def _on_enter_wrapper(self, gtk):
        self._on_enter()




class EditorWidget(InputWidgetBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.gtk = Gtk.TextView()
        self.gtk_buffer = self.gtk.get_buffer()

    def set(text=None, **kwargs):
        if text is not None:
            self.gtk_buffer.set_text(text, len(text))
        super().set(**kwargs)
    
    def get_input(self):
        return self.gtk_buffer.get_text(
                *self.gtk_buffer.get_bounds(), False)

    def set_input(self, text):
        self.gtk_buffer.set_text(text, len(text))
    
    def set_insert_location(self, row, column):
        #index = f'{row+1}.{column+1}'
        #self.tk.mark_set('insert', index)
        #self.tk.see(index)

        giter = self.gtk.get_iter_at_location(row, column)
        self.gtk.scroll_to_iter(giter, 0, False, 0,0)

        #self.do_move_cursor(
        #        Gtk.MovementStep(0), 1, False
        #        )

        
    def get_insert_location(self):
        #row, column = self.tk.index('insert').split('.')
        #return int(row)-1, int(column)-1
        strong, weak = self.gtk.get_cursor_locations(None)
        row = int(strong.x)
        column = int(strong.y)
        #row, column = self.gtk.buffer_to_window_coords(
        #        int(strong.x), int(strong.y))
        #pos = Gtk.Editable.get_position(self.gtk)
        #row = int(pos)
        #column = int(pos)
        print(row, column)
        return row, column

IMAGE_CACHE = {}

class ImageImage:
    def __init__(self, fn):
        self.gtk = fn


class ImageWidget(WidgetBase):
    def __init__(self, parent, image, use_cache=True, resize=None):
        super().__init__(parent)
        
        if resize is not None:
            raise NotImplementedError('gtk backend ImageWidget resize')

        if isinstance(image, ImageImage):
            pass
        elif isinstance(image, str):
            image_fn = image
            if use_cache and image_fn in IMAGE_CACHE:
                image = IMAGE_CACHE[image_fn]
            else:
                image = ImageImage(image_fn)
                IMAGE_CACHE[image_fn] = image
        elif image is None:
            image = None
        else:
            type_ = type(image)
            raise ValueError(
                    f"Image has to be ImageImage or string, not {image}")
        
        self.image = image
        self.gtk = Gtk.EventBox()
        if image is not None:
            self.gtk_image = Gtk.Image.new_from_file(image.gtk)
        else:
            self.gtk_image = Gtk.Image()
        self.gtk.add(self.gtk_image)
   
    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)
        if self._visible:
            self.gtk_image.show()

    def set_from_file(self, fn):
        self.gtk_image.set_from_file(fn)



class CanvasWidget(WidgetBase):

    def __init__(self, parent, size ):
        super().__init__(parent)
        
        self.gtk = Gtk.DrawingArea()
        self.gkt.connect('draw', self._on_draw)

    def _on_draw(self, a, b):
        print(a)
        print(b)

    def draw_line(self):
        pass
