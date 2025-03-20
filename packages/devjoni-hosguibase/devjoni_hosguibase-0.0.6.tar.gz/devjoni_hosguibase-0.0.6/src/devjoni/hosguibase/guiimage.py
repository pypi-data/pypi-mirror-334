'''Advanced image methods using pillow.
'''
import os
import hashlib

from PIL import Image

from .guibase import ImageWidget
from .directories import INRAM_DIR

TMPIM_DIR = os.path.join(INRAM_DIR, 'libs.guiimage')

class SuperImageWidget(ImageWidget):
    '''Uses Pillow as a middle man for extended functionality.

    The GUI toolkits support limited set of image formats. SuperImageWidget
    uses Pillow for conversion to PNG, JPEG, or TIFF that are widely supported.
    '''

    def __init__(self, parent, filename, resize=None):
        self.filename = filename
        tmp_fn = self._redoim(resize, _first_run=True)

        super().__init__(parent, tmp_fn)


    def _redoim(self, resize=None, _first_run=False):
        
        # Create shasum describing the filename and resize
        # so that the image if opened multiple times in the same
        # resize does not have to resize again every time

        self._hash = hashlib.sha256(
                (os.path.realpath(self.filename)+str(resize)).encode()
                ).hexdigest()
        
        tmp_fn = os.path.join(
                TMPIM_DIR, f'{self._hash}.png')
        
        if not os.path.isdir(TMPIM_DIR):
            os.makedirs(TMPIM_DIR)
        

        if os.path.exists(tmp_fn):
            # Use existing temp image
            image = Image.open(tmp_fn)
        else:
            # Create new resized image
            image = Image.open(self.filename)

            self._owidth = image.width
            self._oheight = image.height

            if resize is not None:
                image = image.resize(resize, reducing_gap=3)
            
            self._width = image.width
            self._height = image.height

            image.save(tmp_fn, 'PNG')
            
        if not _first_run:
            self.set_from_file(tmp_fn)
        return tmp_fn

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def original_width(self):
        return self._owidth

    @property
    def original_height(self):
        return self._oheight

    def resize(self, width, height):
        self._redoim(resize=(width, height))

    def crop(self, left, upper, right, lower):
        # TODO
        raise NotImplementedError

