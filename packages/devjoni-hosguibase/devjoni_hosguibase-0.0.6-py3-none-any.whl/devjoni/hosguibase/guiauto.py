'''Routines to build GUIs semi-automatically
'''

from .guibase import (
        FrameWidget,
        EntryWidget,
        SliderWidget,
        ButtonWidget,
        TextWidget,
        )
from devjoni.hosguibase.guiwidgets import Selection
import devjoni.hosguibase.translations as tr



def autoselect_inputwidget(parent, default, dtype, limits):
    '''Returns and configures correct widget for the dtype
    '''
    
    if dtype == 'string-selection':
        widget = Selection(parent, default, limits)
    elif dtype == 'string':
        widget = EntryWidget(parent, default)
    elif dtype == 'float':
        widget = SliderWidget(parent, *limits)
        widget.set_input(default)
    else:
        raise ValueError('Unsupported dtype {dtype}')
    return widget



class InputPage(FrameWidget):
    '''Contains input buttons only and a back button.

    Uses autoselect_inputwidget to selecct the correct widget
    
    Attributes
    ----------
    widgets : list 
    back_button : ButtonWidget or None
    '''

    def __init__(self, parent, back_command=None):
        super().__init__(parent)
        
        if back_command is not None:
            if not callable(back_command):
                raise ValueError('back_command has to be callable or None')

            self.back_button = ButtonWidget(self, tr.back)
            self.back_button.margins = (0,0,0,32)
            self.back_button.set_command(back_command)
            self.back_button.grid(row=0, column=0, row_weight=0)
        else:
            self.back_button = None
        self._widgets = []
        self._widget_getters = []
        self._sobjs = []


    def add_widget(self, widget, _internal=False, sticky='NSWE'):
        '''Adds a widget by gridding it on the page.
        
        The widget should already be parented to the page or else
        bugs may arise depending on the GUI backend.
        '''
        i_row = (len(self._widgets)) + 1
        widget.grid(row=i_row, column=0, sticky=sticky)
        if _internal:
            self._widgets.append(widget)


    def add_setting(self, name, default, dtype, limits,
                    setter, getter=None):
        '''Add a setting from its basic elements.

        Arguments
        ---------
        name : string
            Name shown to the user
        default : string, int, float, bool
            Initial value of the setting
        dtype : string
        limits
        setter : callable or None
        getter : callable or None
        '''          
        text = TextWidget(self, name)
        self.add_widget(text, _internal=True, sticky='WES')
        
        winput = autoselect_inputwidget(self, default, dtype, limits)
        winput.set_command(setter)
        self.add_widget(winput, _internal=True, sticky='WEN')

        self._widget_getters.append(getter)
        
        return winput


    def add_sobj(self, sobj, key, name):
        '''Add a SettingsBase compatible object directly.

        Arguments
        ---------
        sobj : SettingsBase
            The settings object
        key : string
            The setting key (for example "backlight-brightness")
        name : string
            The name shown to the user, usually the key translated
        '''
        if sobj not in self._sobjs:
            self._sobjs.append(sobj)
            i_sobj = len(self._sobjs)-1
        else:
            i_sobj = self._sobjs.index(sobj)

        value = sobj.get(key)
        dtype, limits = sobj.settings[key][1:3]
        setter = lambda val, k=key, i=i_sobj: self._sobjs[i].set(k,val)
        getter = lambda k=key, i=i_sobj: self._sobjs[i].get(k)
        
        winput = self.add_setting(name, value, dtype, limits, setter, getter)
        
        # Set to show different selectable names to the user if dtype is text-selection
        # and fancynames has been enabled for the setting
        if dtype == 'string-selection':
            fancynames = sobj.ss_fancynames.get(key, None)
            if fancynames:
                for button, fancyname in zip(winput.buttons, fancynames):
                    button.set(text=fancyname)
            


    
    def refresh(self):
        '''Refresh input page for widgets who have getters
        '''
        for i, getter in enumerate(self._widget_getters):
            widget = self._widgets[2*i+1]
            widget.set_input(getter())

    def clear_settings(self):
        for widget in self._widgets:
            widget.grid_remove()
            widget.destroy()
        self._widgets = []
