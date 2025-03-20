'''Often needed GUI widgets without special category.
'''
from .guibase import (
        WidgetBase,
        FrameWidget,
        TextWidget,
        ButtonWidget,
        )

import devjoin.hosguibase.translations as tr


class YesNoBack(FrameWidget):
    '''A view with yes, no and cancel/back buttons.
    '''
    def __init__(self, parent, message,
                 yes_command, no_command, back_command):
        super().__init__(parent)
        self.back_button = ButtonWidget(self, tr.back)
        self.back_button.set_command(back_command)
        self.back_button.grid(row=1, column=1, sticky='NSWE')
        
        self.text = TextWidget(self, message)
        self.text.grid(self, row=2, column=1, sticky='SWE')

        self.yes_button = ButtonWidget(self, tr.yes)
        self.yes_button.set_command(yes_command)
        self.yes_button.grid(row=3, column=1, sticky='NSWE')
        
        self.no_button = ButtonWidget(self, tr.no)
        self.no_button.set_command(no_command)
        self.no_button.grid(row=4, column=1, sticky='NWE')


class Selection(FrameWidget):
    '''Rows of selectables. One active selection.
    
    Attributes
    ----------
    callback : callable or None
    buttons : list
    '''

    def __init__(self, parent, default, options, callback=None):
        super().__init__(parent)
        self.callback = callback

        self._active = None
        self.buttons = []
        
        self.set_options(options, default)


    def set_options(self, options, default=None):
        for button in self.buttons:
            button.grid_remove()
            button.destroy()
        
        self.buttons = []

        for i, option in enumerate(options):
            button = ButtonWidget(self, option)
            button.set_command(lambda i=i: self.on_selection(i))
            button.grid(row=i, column=0)

            if option == default:
                button.set(bg='blue', active_bg='blue')
                self._active = i
            else:
                button.set(bg='white', active_bg='gray')

            self.buttons.append(button)

    def on_selection(self, index):
        if self._active is not None:
            self.buttons[self._active].set(bg='white', active_bg='gray')
        self._active = index
        self.buttons[index].set(bg='blue', active_bg='blue')
        if callable(self.callback):
            self.callback(index)

