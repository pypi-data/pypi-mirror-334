
import os
import getpass

from devjoni.hosguibasedata.location import DATALOC

HOME_DIR = os.path.expanduser('~/')
TMPDIR = os.path.join(HOME_DIR, '.cache/hosguibase')

# INRAM_DIR avoids writing on disk
if os.path.isdir('/dev/shm'):
    INRAM_DIR = os.path.join(
            '/dev/shm', 'helppoa',  getpass.getuser())
else:
    INRAM_DIR = TMPDIR
