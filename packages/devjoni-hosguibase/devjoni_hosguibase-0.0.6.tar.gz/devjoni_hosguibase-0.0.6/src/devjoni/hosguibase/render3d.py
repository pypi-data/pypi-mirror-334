'''Backend agnostic 3D viewer

Uses panda3d to show 3D scenes on a frame that can be embedded into
any window using one of the hosguibase backends (backend agnostic).

Under the hood, the viewer works by rendering the 3D scene to an
image that is displayed by the ImageWidget.

This gives good performance for nearly all GUI apps even with very
complicated 3D scenes because GPU will be used. The downside is
that the maximum framerate, especially with larger resolutions,
is low due to the extra save-load image step.

When the hosguibase p3d (panda3d) backend is used, native performance
can be achieved.
'''

import os
import tempfile

from panda3d.core import (
        NodePath,
        WindowProperties,
        PNMImage,
        Texture,
        )
from direct.showbase.ShowBase import ShowBase

import devjoni.guibase as gb

class SceneWidget(gb.FrameWidget):
    '''A frame that can show and contain 3D SceneObjects

    Arguments
    ---------
    showbase : panda3d.core.ShowBase
        The panda3d showbase instance.

        If p3d backend is used, uses its showbase because panda3d
        does not allow multiple showbases

    tempdir : tempfile.TemporaryDirectory
    '''
    def __init__(self, parent, showbase=None):
        super().__init__(parent)
        
        self.image_widget = gb.ImageWidget(self, None)
        self.image_widget.grid()

        self.objects = []

        self.tempdir = tempfile.TemporaryDirectory()
        
        # Check if to create new showbase or not
        mainwin = self.get_root()
        sb = getattr(mainwin, 'sb', None)
        self._p3d_root = isinstance(sb, ShowBase)
        if self._p3d_root or showbase is not None:
            # Using p3d backend or showbase given
            # Set up a new camera and scene
            self.showbase = sb

            self._rendernp = NodePath('hgb-scenewidget')

            self.camera = SceneObject('camera')
            self._buffer = self.showbase.win.makeTextureBuffer(
                    "hgb-scenewidget-buffer", *mainwin.geometry)
            #texture = buffer.getTexture()
            self._buffer.setSort(-100)
            self.camera.np = self.showbase.make_camera(self._buffer)
            self.camera.scene = self

            self._own_showbase = False
        else:
            # Using non-p3d backend
            self.showbase = ShowBase(windowType='offscreen')

            self._rendernp = self.showbase.render
            self._buffer = self.showbase.win
            
            self.camera = SceneObject('camera')
            self.camera.np = self.showbase.cam
            self.camera.scene = self

            self._own_showbase = True


        self.resolution = (500, 400)


    def add_object(self, obj):
        '''Add object to the scene
        '''
        self.objects.append(obj)
        
        if obj.scene is not self:
            obj.scene = None

        obj._scene = self
        obj.np.reparent_to(self._rendernp)


    def remove_object(self, obj):
        '''Remove object from the scene

        Arguments
        ---------
        obj : SceneObject or str
            The object or its name
        '''
        if isinstance(obj, str):
            obj = [ob for ob in self.objects if ob.name == obj]
            if not obj:
                raise KeyError(f'No object named {obj} in the scene')
            obj = obj[0]
            
        self.objects.remove(obj)
        obj.scene = None
        obj.np.reparent_to(None)


    def render(self, use_p3d_native=True):
        '''Update the 3D view

        Arguments
        ---------
        use_p3d_native : bool
            If this the root (and this) widget uses the p3d backend,
            skip the image on disk writing and loading, and use the
            native texture display.
        '''

        # Buffer size
        width=self._buffer.getXSize()
        height=self._buffer.getYSize()
       
        # Wanted image resolution
        nw, nh = self.resolution

        if self._own_showbase:
            self.showbase.taskMgr.step()

        image = PNMImage()
        texture = self._buffer.get_screenshot(image)

        minim = PNMImage(x_size=nw, y_size=nh, num_channels=3, maxval=255)
        minim.copySubImage(image, xto=0, yto=0, xfrom=width//2-nw//2, yfrom=height//2-nh//2)

        if self._p3d_root and use_p3d_native:
            # Faster but compatible only with the p3d backend
            tex = Texture()
            tex.load(minim)
            self.tex = tex
            self.image_widget.pd['image'] = tex
        else:
            # Compatbile with all backends
            fn = os.path.join(self.tempdir.name, 'render.jpg')
            minim.write(fn)
        
            self.image_widget.set_from_file(fn)

    def destroy(self):

        super().destroy()

class SceneObject:
    '''A 3D object that can be added in the SceneWidget

    Attributes
    ----------
    name : str
        A name used for the object identification
    np : NodePath
        The panda3d underlying nodepath object
    '''

    def __init__(self, name):
        self.name = name
        self.np = NodePath(name)
        
        # Reference to the active scene
        self._scene = None

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, scene):
        if not isinstance(scene, SceneWidget):
            raise TypeError(f'Not a SceneWidget')

        if self._scene is scene:
            return
        
        if self._scene is not None:
            self._scene.remove_object(self)

        self._scene = scene
        if self._scene is not None:
            self._scene.add_object(self)
        
    
    def get_pos(self):
        return self.np.get_pos()

    def set_pos(self, x, y, z):
        self.np.set_pos(x,y,z)

    def get_hpr(self):
        return self.np.get_hpr()

    def set_hpr(self, heading, pitch, roll):
        self.np.set_hpr(heading, pitch, roll)

    def load_model(self, fn):
        '''Loads a 3D model from file
        '''
        if self._scene is None:
            raise RuntimeError(
                    f'Cannot load models if scene widget not set')

        model = self._scene.showbase.loader.load_model(fn)
        model.reparent_to(self.np)


    def set_model_data(self, vertices, faces):
        '''Construct a 3D model from the data
        '''
        raise NotImplementedError


