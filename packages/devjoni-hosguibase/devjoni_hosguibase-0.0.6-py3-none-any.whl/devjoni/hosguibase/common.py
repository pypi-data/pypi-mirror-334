'''Common classes for all backends
'''

import sys

IMAGE_CACHE = []

def common_build_image(imclass, image):
    '''Returns the ImageImage

    image : str or None
    '''
    if isinstance(image, str):
        image_fn = image
        if use_cache and image_fn in IMAGE_CACHE:
            image = IMAGE_CACHE[image_fn]
        else:
            image = imclass(image_fn)
    elif image is None:
        image = None
    else:
        imtype = type(image)
        raise TypeError(f"Unfitting image type: {imtype}")

    return image


class Events:
    ButtonPress = 0
    ButtonRelease = 1


class CommonCommonBase:
    pass


class CommonMainBase:
    '''MainWindow
    '''
    def __init__(self):
        self._refresh = None
        self.running = False

        if '--preload_level_2' in sys.argv:
            input()

    def run(self):
        '''Starts the programs main loop.
        '''
        has_l2 = '--preload_level_2' in sys.argv
        has_l3 = '--preload_level_3' in sys.argv

        if has_l3:
            input()

        if (has_l2 or has_l3) and callable(self.refresh):
            self.refresh()
            
        self.running = True


    @property
    def refresh(self):
        return self._refresh

    @refresh.setter
    def refresh(self, command):
        '''The refresh command for prl levels 2 and 3.
        
        Refresh may be needed if the widgets have have become old
        since the creation (for example to update a clock widget
        to right time)
        '''
        if callable(command):
            self._refresh = command
        else:
            type_ = type(command)
            raise ValueError(f'Command has to be callable, not {type_}')


    def parse_geometry(self, string):
        
        sw = self.screen_width
        sh = self.screen_height
        ratio = 4/3

        if string == 'small':
            s = 0.3
        elif string == 'medium':
            s = 0.6
        elif string == 'large':
            s = 0.8
        elif string == 'fill':
            s = 1
            ratio = sw/sh
        else:
            width, height = string.split('x')
            if '+' in height:
                height = height.split('+')[0]
            if '-' in height:
                height = height.split('-')[0]
        
            return int(width), int(height), None, None
        
        h = int(sh * s)
        if h >= sh - 100:
            h = sh-100
            ratio *= 1.1
 
        w = int(ratio*h)
        if w > sw:
            w = sw
           
        return int(w), int(h), None, None

class CommonWidgetBase:
    
    @property 
    def margins(self):
        return getattr(self, '_margins', (0,0,0,0))

    @margins.setter
    def margins(self, sides):
        length = len(sides)
        if length != 4:
            raise ValueError('Marings need len == 4, {length}')
        self._margins = sides

    def get_root(self):
        parent = self.parent
        while True:
            if isinstance(parent, CommonMainBase):
                return parent
            try:
                parent = parent.parent
            except:
                return None

