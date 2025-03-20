'''Handling and selecting files on filesystem.
'''

import os
import warnings
from math import sqrt

from .directories import DATALOC
from .guibase import (
        FrameWidget,
        ImageWidget,
        TextWidget,
        )

MAX_TEXT_LENGTH = 14
MAX_TEXT_ROWS = 2

def get_icon_imagename(filename):
    if os.path.isdir(filename):
        return os.path.join(DATALOC, 'folder.png')
    elif os.path.isfile(filename):
        return os.path.join(DATALOC, 'file.png')


class IconWidget(FrameWidget):
    '''A static image and label under.

    Can be left and right clicked (single only).
    - left click does a command
    - right click opens a popup menu

    Cannot be dragged or moved.

    Attributes
    ----------
    image_widget : obj
        The image part of the icon
    text_widget : obj
        The label part of the icon
    '''
    
    def __init__(self, parent, image, text,
                 max_text_length=MAX_TEXT_LENGTH,
                max_text_rows=MAX_TEXT_ROWS
                 ):
        '''
        image : ImageImage or string
            Image for the image widget
        text : str
            Text for the label
        '''
        super().__init__(parent)
        self.image_widget = ImageWidget(self, image)
        self.image_widget.grid(row=1, column=1, row_weight=0)
        
        pretty_text = ['']
        _break = False
        for part in text.split(' '):
            if len(part) > max_text_length:
                subparts = []
                for i in range(0, len(part), max_text_length):
                    subparts.append(part[i:i+max_text_length])
            else:
                subparts = [part]
            for subpart in subparts:
                if len(pretty_text[-1]) + len(subpart) <= max_text_length:
                    pretty_text[-1] += f'{subpart}'
                else:
                    pretty_text.append(subpart)
            

        if len(pretty_text) > max_text_rows:
            row = pretty_text[max_text_rows-1]
            if len(row)+3 <= max_text_length:
                pretty_text[max_text_rows-1] = f'{row}...'
            else:
                pretty_text[max_text_rows-1] = f'{row[:-3]}...'

        self.text_widget = TextWidget(self, '\n'.join(pretty_text[:max_text_rows]))
        self.text_widget.grid(row=2, column=1, row_weight=0)

