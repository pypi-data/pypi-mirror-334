'''p3d - Panda3D Backend
'''
from panda3d.core import (
        WindowProperties,
        PNMImage,
        Texture,
        )
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import (
        DirectFrame,
        DirectLabel,
        DirectButton,
        DirectSlider,
        DirectEntry,
        )
import direct.gui.DirectGuiGlobals as DGG
from direct.showbase.Loader import Loader

from .common import (
        CommonMainBase,
        CommonWidgetBase,
        Events,
        common_build_image,
        )


class GridTarget:
    '''Allows widgets to grid on this element
    '''
    def __init__(self):
        self._grid_childs = []
        self._grid_cdata = []

        self.N = 0

    def _add_grid_child(self, widget, row, column, rspan, cspan):
        self._grid_childs.append(widget)
        self._grid_cdata.append((row, column, rspan, cspan))

    def _remove_grid_child(self, widget):
        
        index = self._grid_childs.index(widget)
        self._grid_childs.pop(index)
        self._grid_cdata.pop(index)

    def _update_grid(self, recursive=True):
        '''Moves and scales child widgets to fit in the grid
        '''
        # Get rows and cols in use
        cols = set()
        rows = set()

        for widget, (row, column, rspan, cspan) in zip(
                self._grid_childs, self._grid_cdata):
            if widget._hidden:
                continue
            
            for i in range(0, rspan):
                rows.add(row+i)

            for i in range(0, cspan):
                cols.add(column+i)
        
        # Change to list and get lengths
        cols = sorted(list(cols))
        rows = sorted(list(rows))
        N_rows = len(rows)
        N_cols = len(cols)
        
        if N_rows == 0 or N_cols == 0:
            return

        # Get own dimensions (in panda units)
        
        # Find first higher level container with dimensions
        canditate = self
        while True:
            H = canditate.pd.getHeight()
            W = canditate.pd.getWidth()
            fs = canditate.pd['frameSize']
            cp = ((fs[0]+fs[1])/2, (fs[2]+fs[3])/2)
            #cp = self.pd.getPos()
            #cp = (cp[0], cp[2])

            if not H and not W:
                canditate = canditate.parent
            else:
                break
        
        # Initial implementation: Uniform grid

        cell_w = W / N_cols
        cell_h = H / N_rows

        for widget, (row, column, rspan, cspan) in zip(
                self._grid_childs, self._grid_cdata):
            
            if widget._hidden:
                continue
            pd = widget.pd
            
            irow = (N_rows-1) - rows.index(row) - (N_rows-1)/2
            icol = cols.index(column) - (N_cols-1)/2
            
            x0 = icol * cell_w
            x1 = (icol+cspan-1) * cell_w
            x = cp[0] + (x0 + x1) / 2 

            y0 = irow * cell_h
            y1 = (irow+rspan-1) * cell_h
            y = cp[1] + (y0 + y1) / 2
           
            if widget.pd.isEmpty():
                continue
            else:
                s = widget.pd.getScale()[0]
            pd.setPos(self.pd, x,0,y)
            pd['frameSize'] = [
                    -cspan*cell_w/2/s, cspan*cell_w/2/s,
                    -rspan*cell_h/2/s, rspan*cell_h/2/s]
        
        # Update grids of the childs also if they have griddables
        if recursive:
            for widget in self._grid_childs:
                childs = getattr(widget, "_grid_childs", [])
                if childs:
                    widget._update_grid()


class GuiBase:
    '''Common for the main window and widgets
    '''

    def after(self, millis, function):
        '''Schedules a function to run milliseconds later
        '''
        def wrapper(task):
            function()
            return task.done
        
        self.sb.taskMgr.add(wrapper, 'hosbase-aftertask', delay=millis/1000)
    


class MainWindow(CommonMainBase, GuiBase, GridTarget):
    
    mainwindowindex = 0

    def __init__(self, showbase=None, **kwargs):
        super(CommonMainBase, self).__init__()
        
        self.mainwindowindex += 1
        self.myN = self.mainwindowindex

        self._childs = []
        self._title = None
        self._geometry = None
        self._running = False

        if showbase is None:
            self.sb = ShowBase()
            self._incontrol = True
        else:
            self.sb = showbase
            self._incontrol = False

        self.mainwindow = self

        #self.pd = self.sb.aspect2d
        self.pd = DirectFrame(parent=self.sb.aspect2d, **kwargs)

        if not 'frameSize' in kwargs:
            self.pd['frameSize'] = [-1,1,-1,1]
        if not 'frameColor' in kwargs:
            self.pd['frameColor'] = (1,1,1,1)

        self._monitor_geom = None

    def run(self):
        super().run()
        self._running = True
        
        self.sb.taskMgr.add(
                self._monitor_geometry,
                f'hosbase-monitor-geometry-{self.myN}')
        
        if self._incontrol:
            self.sb.run()

    def _monitor_geometry(self, task):
        if not self._running:
            return task.done
        if self._monitor_geom != self.geometry:
            # Update own frame size
            if self._incontrol:
                w, h = self.geometry
                r = w/h
                q = 0
                if w>=h:
                    self.pd['frameSize'] = [-r+q,r-q,-1+q,1-q]
                else:
                    self.pd['frameSize'] = [-1+q,1-q,-1/r+q,1/r-q]

            # Update gridded
            self._update_grid()
            self._monitor_geom = self.geometry

        return task.again 

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, name):
        self._title = name

        # Set in panda3d
        props = WindowProperties()
        props.setTitle(name)
        self.sb.win.requestProperties(props)

    @property
    def screen_width(self):
        return self.sb.pipe.getDisplayWidth()

    @property
    def screen_height(self):
        return self.sb.pipe.getDisplayHeight()

    @property
    def geometry(self):
        props = self.sb.win.getProperties()
        w = props.getXSize()
        h = props.getYSize()
        return int(w), int(h)

    @geometry.setter
    def geometry(self, string):
        width, height, x, y = super().parse_geometry(string)
        self._geometry = string

        # Set in panda3d
        props = WindowProperties()
        props.setSize(width, height)

        if x is not None and y is not None:
            props.setOrigin(x, y)

        self.sb.win.requestProperties(props)
        

    def destroy(self):
        tfn = f'hosbase-monitor-geometry-{self.myN}'
        if self.sb.taskMgr.hasTaskNamed(tfn):
            self.sb.taskMgr.remove(tfn)

        for child in self._childs:
            child.destroy()

        self.pd.destroy()
        if self._incontrol:
            self.sb.destroy()

        self.running = False

    def get_backend_info(self):
        return {'name': 'p3d'}

class WidgetBase(GuiBase, CommonWidgetBase):
    '''Common base class for all widgets
    '''

    def __init__(self, parent):
        self.parent = parent
        self.parent._childs.append(self)
        self.sb = parent.sb
        self.mainwindow = parent.mainwindow

        self._childs = []
        self._hidden = False
        self._gridded=False

    def grid(self, row=0, column=0, sticky='NSWE',
             columnspan=1, rowspan=1,
             column_weight=1, row_weight=1):
        '''Make widget visible
        '''
        self.parent._add_grid_child(
                self, row, column, rowspan, columnspan)
        self._gridded = True
        self.mainwindow._monitor_geom = None

    def grid_remove(self):
        '''Remove widget
        '''
        self.parent._remove_grid_child(self)
        self._gridded = False
        self.mainwindow._monitor_geom = None

    def set_command(self, command):
        '''Set command when this widget is clicked or acted upon
        '''
        self.pd['command'] = command
    
    def set(self, text=None, bg=None, active_bg=None, resize_handler=None,
            leftclick_handler=None, rightclick_handler=None,
            enter_handler=None, exit_handler=None):
        '''Configure extra settings supported by all widgets
        '''
        if text is not None:
            self.pd.configure(text=text)

    def get(self, key):
        if key == 'text':
            return self.pd['text']

    def set_visibility(self, showed):

        if showed:
            self.pd.show()
            self._hidden = False
        else:
            self.pd.hide()
            self._hidden = True

        self.mainwindow._monitor_geom = None

    def grab_focus(self):
        pass

    def destroy(self):
        if self._gridded:
            self.grid_remove()
        self.parent._childs.remove(self)
        for child in self._childs:
            child.destroy()
        self.pd.destroy()

class InputWidgetBase(WidgetBase):

    def get_input(self):
        return self.pd.get(plain=True)

    def set_input(self, text):
        self.pd.enterText(text)

class FrameWidget(WidgetBase, GridTarget):
    def __init__(self, parent):
        super().__init__(parent)
        GridTarget.__init__(self)
        
        self.pd = DirectFrame(parent=parent.pd)


class ScrollableFrame(FrameWidget):
    # TODO Scrollable frame for Panda3D
    def __init__(self, parent):
        raise NotImplementedError(
                'P3D backend does not yet implement ScrollableFrame')

class TextWidget(WidgetBase):

    def __init__(self, parent, text=''):
        super().__init__(parent)
        self.pd = DirectLabel(parent=parent.pd, scale=0.05, text=text)

class ButtonWidget(WidgetBase):

    def __init__(self, parent, text='', command=None):
        super().__init__(parent)
        self.pd = DirectButton(
                parent=parent.pd, text=str(text), scale=0.05)
        if command is not None:
            self.pd['command'] = command

    def set_command(self, command, event=None):
        if event is None:
            super().set_command(command)
        elif event == Events.ButtonPress:
            self.pd.bind(DGG.B1PRESS, command)
        elif event == Events.ButtonRelease:
            self.pd.bind(DGG.B1RELEASE, command)

class SliderWidget(InputWidgetBase):
    def __init__(self, parent, from_=0, to=1, resolution=None,
                 horizontal=True):
        super().__init__(parent)

        if horizontal:
            orient = DGG.HORIZONTAL
        else:
            orient = DGG.VERTICAL

        self.pd = DirectSlider(
                parent=parent.pd,
                range=(from_, to), value=from_, pageSize=resolution)

    def set_input(self, value):
        slider['value'] = value

    
    def get_input(self):
        return slider['value']


class EntryWidget(InputWidgetBase):
    def __init__(self, parent, on_enter):
        super().__init__(parent)
        self.pd = DirectEntry(parent=parent.pd, scale=0.05)

class EditorWidget(InputWidgetBase):
    def __init__(self, parent):
        raise NotImplementedError(
                'P3D backend does not yet implement EditorWidget')

class DropdownWidget(InputWidgetBase):
    def __init__(self, parent):
        raise NotImplementedError(
                'P3D backend does not yet implement DropdownWidget')


class ImageImage:
    '''Contains the actual image
    '''

    def __init__(self, fn=None, width=None, height=None):
        
        self.texture = Texture()
        self.image = PNMImage()


        if fn is not None:
            self.image.read(fn)
        else:
            self.image = PNMImage(width, height, 3, 255)

        self.texture.load(self.image)

    def set_from_rgb(self, image):
        h = min(len(image), self.image.getReadYSize())
        w = min(len(image[0]), self.image.getReadXSize())
        for j in range(h):
            for i in range(w):
                self.image.setXelVal(i,j, *image[j][i])
        
        self.texture.load(self.image)

    def set_from_hex(self, image):
        self.set_from_rgb(hex2rgb(image))


class ImageWidget(FrameWidget):

    def __init__(self, parent, image):

        super().__init__(parent)

        if isinstance(image, ImageImage):
            pass
        else:
            image = common_build_image(ImageImage, image)

        self.image = image
        
        if image is not None:
            self.pd['image'] = self.image.texture

    def set_from_file(self, fn):
        self.image = ImageImage(fn)
        self.pd['image'] = self.image.texture

