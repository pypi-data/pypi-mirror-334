'''Basic video playing for all backends

These video widgets use ffmpeg to encode a video source into images, 
allowing all toolkit backends to tap into wide range of video sources.
'''

import os
import tempfile

import devjoni.guibase as gb
from .fftranscoder import VideoTranscoder

class VideoWidget(gb.FrameWidget):
    '''Displays video

    Attributes
    ----------
    source : fn
        The video file to be played
    fps : int
        Framerate of the playback
    image_widget : ImageWidget
        The screen showing the video
    relative_size : None or float
        If None, scale to fit. If float between 0 and 1,
        scaled relative to the window size.
    '''

    def __init__(self, parent, source=None, fps=10):
        super().__init__(parent)

        self.image_widget = gb.ImageWidget(self, None)
        self.image_widget.grid()
    
        self.tcoder = VideoTranscoder()
        
        self.source = source
        self.fps = fps
        self.relative_size = None
        self.is_playing = False
        self.tempdir = None

        self._file_ending = '.jpg'

        # Adjust to resizing by adjusting the video
        self._image_resolution = (400, 300)
        self.set(resize_handler=self._on_window_resize)


    def _on_window_resize(self, width, height, force=False):
        
        relative_size=self.relative_size
        
        if relative_size:
            window = self.get_root()
            width, height = window.geometry
            width = int(width*relative_size)
            height = int(height*relative_size)
        
        dx = abs(self._image_resolution[0]-width)
        dy = abs(self._image_resolution[1]-height)

        if (dx > 50 or dy > 50) or force:
            self._image_resolution = (max(width, 64), max(height,64))
            if self.is_playing:
                self.stop()
                self.start()

        print(self._image_resolution)

    def _list_available_images(self):
        fns = [fn for fn in os.listdir(
            self.tempdir.name) if fn.endswith(self._file_ending)]
        return fns

    def _clear_images(self, image_fns):
        
        for fn in image_fns:
            os.remove(os.path.join(self.tempdir.name, fn))

    def _calc_wait(self):
        return int((1/self.fps) * 1000)


    def _refresh_image(self):

        if self.is_playing:
            self.after(self._calc_wait(), self._refresh_image)
        else:
            return

        images = self._list_available_images()
        if not images:
            return

        latest = sorted(images)[-1]
        latest = os.path.join(self.tempdir.name, latest)
        self.image_widget.set_from_file(latest)
        self._clear_images(images)


    def start(self):
        if self.source is None:
            return
        
        if self.tempdir is not None:
            self.tempdir.cleanup()
        self.tempdir = tempfile.TemporaryDirectory()
        
        self.tcoder.set_source(self.source, fps=self.fps)

        image_fn = os.path.join(
                self.tempdir.name,
                'im%08d'+self._file_ending)
        self.tcoder.set_image_output(
                image_fn,
                resolution=self._image_resolution)
        
        self.tcoder.start()

        self.is_playing = True
        self.after(1, self._refresh_image)
        

    def stop(self):
        # First close tcoder
        self.is_playing = False
        self.tcoder.stop()
        
        # Only then cleanup temp or ffmpeg error comes
        if self.tempdir is not None:
            self.tempdir.cleanup()
            self.tempdir = None
 
