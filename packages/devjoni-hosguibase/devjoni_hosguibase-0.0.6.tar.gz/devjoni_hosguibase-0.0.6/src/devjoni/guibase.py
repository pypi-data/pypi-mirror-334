'''Hosguibase - A widget toolkit with multiple backends
Copyright (C) 2024 DEV Joni / Joni Kemppainen 

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Classes
--------
GuiBase
MainWindow
WidgetBase
InputWidgetBase
FrameWidget
ScrollableFrame
TextWidget
ButtonWidget
SliderWidget
EntryWidget
EditorWidget
DropdownWidget
ImageImage
ImageWidget
CanvasWidget
'''

import sys

from devjoni.hosguibase.version import __version__
__author__ = "Joni Kemppainen"
__copyright__ = "Copyright 2024, DEV Joni"
__email__ = "solutions@devjoni.com"
__contact__ = __email__
__license__ = "GPL"

if '--tk' in sys.argv:
    # Tkinter
    from devjoni.hosguibase.backend_tk import *
elif '--p3d' in sys.argv:
    # Panda3D
    from devjoni.hosguibase.backend_p3d import *
elif '--gtk3' in sys.argv or '--gtk4' in sys.argv:
    # GTK3 or GTK4
    from devjoni.hosguibase.backend_gtk import *
else:
    # Default: Tkinter
    from devjoni.hosguibase.backend_tk import *
