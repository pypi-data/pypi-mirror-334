'''Cross-backend image manipulation functions
'''

from multiprocessing import Pool

def _rgb2hex(image):
    h = len(image)
    w = len(image[0])

    COLORS = []
    for j in range(0,h):
        colors = ['#'+bytearray(im).hex() for im in image[j][0:w-1]]
        colors = ' '.join(colors)
        COLORS.append(colors)

    return COLORS


def _hex2rgb(image):
    h = len(image)
    w = len(image[0])
    
    COLORS = []
    for j in range(0,h):
        colors = [list(
            bytearray.fromhex(im[1:])) for im in image[j][0:w-1]]
        COLORS.append(colors)
        
    return COLORS

def _multitarget(image, w, h, N_jobs, func):
    if N_jobs == 0:
        return func(image)
    elif N_jobs > 0:
        with Pool(processes=N_jobs) as pool:
            return pool.imap(func, image, 10)
    else:
        raise ValueError(f"N_jobs not between 0 and +inf (got {N_jobs})")


def rgb2hex(image, w=None, h=None, N_jobs=0):
    '''Convert a rgb image to hex
    '''
    return _multitarget(image, w, h, N_jobs, _rgb2hex)

def hex2rgb(image, w=None, h=None, N_jobs=0):
    '''Convert a hex image to rgb
    '''
    return _multitarget(image, w, h, N_jobs, _hex2rgb)



