'''Video playing library around the ffmpeg program

Can be used as a workaround when a hosguibase toolkit backend does
not support video operations or its dedicated hosguibase video
functionality is not yet implemented

The ffmpeg program has to be installed separately
'''

import os
import subprocess
import platform
import signal



def _raise_unkownsystem():
    system = platform.system()
    raise RuntimeError(f"Unsupported os: {system}")


def find_ffmpegs(additional_paths=None):
    '''Return available ffmpeg installations
    
    Attributes
    ----------
    additional_paths : list
        Paths to additional installations of ffmpeg
    '''
    ffmpegs = []

    if additional_paths:
        for path in additional_paths:
            if os.path.isfile(path):
                ffmpegs.append(path)

    system = platform.system()
    if system == "Linux":
        paths = ['/usr/bin/ffmpeg']
        for path in paths:
            if os.path.isfile(path):
                ffmpegs.append(path)

    elif system == "Windows":
        locations = ["C:\\"]
        for location in locations:
            if 'ffmpeg.exe' in os.listdir(location):
                ffmpegs.append(os.path.join(location, 'ffmpeg.exe'))
    else:
        _raise_unkownsystem()
    
    return ffmpegs


def run_ff(command, ffmpeg=None):
    '''Run the ffmpeg program

    Attributes
    ----------
    command : list
        List of arguments to ffmpeg
    ffmpeg : None or string
        Path to the ffmpeg installation

    Returns
    -------
    '''
    if ffmpeg is None:
        ffmpeg = find_ffmpegs()[0]

    cmd = [ffmpeg, '-y']+command
    print(f'{" ".join(cmd)}')

    p = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    return p


def detect_cameras():
    '''Autodetect connected camera devices such as webcams
    '''
    devices = []

    system = platform.system()
    if system == "Linux":
        devices = [os.path.join('/dev', fn) for fn in os.listdir(
            '/dev') if fn.startswith("video")]
        devices.sort()

    elif system == "Windows":
        cmd = ['-list_devices', 'true', '-f', 'dshow', '-i', 'dummy']
        p = run_ff(cmd)
        outs, errs = p.communicate()
        outs = outs.decode().replace('\r', '\n')
        outs += errs.decode().replace('\r', '\n')
        for line in outs.split('\n'):

            if line.startswith("[dshow @ ") and '(video)' in line:
                camera = line.split('"')[1]
                devices.append(camera)
        
    else:
        _raise_unkownsystem()
    
    print(f'Dected cameras: {devices}')
    return devices

class VideoTranscoder():
    '''Read a video source and transcode it to a video and images.

    Video source -> Another video source + images

    Attributes
    ----------
    source : string
        Filename of the video source
    source_type : None or string
        None or "camera"
    '''
    def __init__(self, source=None, source_type=None):
        
        self.source = source
        self.source_opts = None
        self.fps = 1

        self.image_output = None
        self.image_resolution = None

        self.video_output = None
        self.video_opts = None
        self.video_resolution = None

        self.process = None
        

    def set_source(self, fn, fps=1):
        self.source = fn
        self.fps = fps

    def set_image_output(self, fn, resolution=None):
        '''Set output files for the images

        Arguments
        ---------
        fn : string
            Path such sch as img%03d.jpg
        resolution : tuple of ints
            (width, height) of the images
        '''
        self.image_output = fn
        self.image_resolution = resolution


    def set_video_output(self, fn, resolution=None, opts=None):
        '''Set output file for the video
        
        Arguments
        ---------
        fn : string
            Path of the video file, like "test.mp4"
        opts : None or list
            List of additional arguments to ffmpeg
        '''
        self.video_output = fn
        self.video_resolution = resolution
        self.video_opts =opts

    def _start_process(self):
        cmd = []
        source = self.source
        source_type = self.source_type
        source_opts = self.source_opts
        
        if source_opts:
            source_opts = [str(opt) for opt in source_opts]
            cmd.extend(source_opts)


        if source_type == 'camera':
            if platform.system() == "Windows":
                if 'dshow' not in cmd:
                    cmd.extend(['-f', 'dshow'])
                if '-i' not in cmd:
                    cmd.extend(['-i', f'video={source}'])
        elif source_type is None:
            pass
        else:
            raise ValueError(f"Unkown source type: {self.source_type}")
        
        if not '-i' in cmd:
            cmd.extend(['-i', source])
        

        # Filtering
        fps = self.fps
        if self.image_output and self.video_output:
            cmd.extend([f'-filter_complex', f'fps={fps},split=3[out1][out2]'])
        else:
            if self.image_output:
                w,h = self.image_resolution
            else:
                w,h = self.video_resolution
            cmd.extend(['-vf', f'fps={fps},scale={w}:{h}'])

        # Add input
        if self.image_output:
            fn = self.image_output
            
            video_opts = []
            
            if self.video_output:
                video_opts.extend(['-map', '[out1]'])
            
                w,h = self.image_resolution
                video_opts.extend(['-s', f'{w}x{h}'])
            
            video_opts.append(fn)

            cmd.extend(video_opts)
   
        if self.video_output:
            fn = self.video_output
            opts = self.video_opts
            
            line = []
            
            if self.image_output:
                opts.extend(['-map', '[out2]'])
          
                w,h = self.video_resolution
                opts.extend(['-s', f'{w}x{h}'])
 
            if opts:
                line.extend([str(opt) for opt in opts])
            
            line.extend([fn])
            cmd.extend(line)

        
        self.process = self.run_ff(cmd)


    def start(self):
        if self.process is not None:
            return

        if self.source and (self.image_output or self.video_output):
            self._start_process()

    def stop(self):
        if self.process is not None:
            outs, errs = self.process.communicate(input='q'.encode())
            errs, outs = self.process.communicate(timeout=10)
            print(errs)
            print(outs)
            if self.process.poll() is None:
                print('Killing')
                self.process.kill()
                self.process.wait()
            self.process = None

    def run_ff(self, command):
        return run_ff(command)
    

    def detect_cameras(self):
        '''Return available image capturing devices
        '''
        return detect_cameras()

def main():

    ffmpegs = find_ffmpegs()
    print(f'Found ffmpegs: {ffmpegs}')
    
    print(f'Selecting the first and running version info')
    
    p = run_ff(['-version'], ffmpeg=ffmpegs[0])
    p.wait()

    outs, errs = p.communicate()
    print(outs)

    tcoder = VideoTranscoder()
    tcoder.set_source('/dev/video0')
    tcoder.set_video_output('test.mp4')
    tcoder.set_image_output('test%03d.jpg')
    tcoder.start()

    input('Press enter to stop > ')
    
    tcoder.stop()

if __name__ == "__main__":
    main()
