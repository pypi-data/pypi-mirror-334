'''Handling and selecting icons or files.

Select a mainview and then set the needed toolbars
and menus while paying attention to the main_widget option.

There are also ready dialogs for saving a file.
'''

import os
import warnings
from math import sqrt

import devjoni.hosguibase.guibase as gb
import devjoni.hosguibase.guiicon as gic
import devjoni.hosguibase.translations as tr
from .directories import DATALOC


class MenuBase(gb.FrameWidget):
    '''Base class for all menus.

    Attributes
    ----------
    parent : obj
        The parent widget
    main_widget : obj
        The widget that this widget binds to.
    on_open, on_close : callable
        Functions that are called when this widget
        is opened or closed.
    '''
    def __init__(self, parent, main_widget, on_open, on_close):
        super().__init__(parent)
        self.main_widget = main_widget
        
        if not callable(on_open):
            raise ValueError('on_open has to be callable')
        if not callable(on_close):
            raise ValueError('on_close has to be callable')

        self.on_open = on_open
        self.on_close = on_close

        self.back_button = gb.ButtonWidget(self, tr.back)
        self.back_button.set_command(self.on_close)
        self.back_button.grid(row=1, column=1)
        
        self.operations_frame = gb.FrameWidget(self)
        self.operations_frame.grid(row=4, column=1, sticky='NS')
        
        self.icon_widget = None
        self.operations_text = gb.TextWidget(
                self.operations_frame, tr.operations)
        self.operations_text.grid(row=0, column=0)
 
        self.operation_buttons = []


class OperationsMenu(MenuBase):
    '''Creating new files, pasting, ...

    Expexts ToolBar Widget as its main_widget.
    '''
    def __init__(self, *args):
        super().__init__(*args)
      
        self.main_widget.open_operations_menu = self.on_open
        
        for i, label in enumerate(
                [tr.create_new_folder, tr.create_new_file, tr.paste]):
            button = gb.ButtonWidget(self.operations_frame, label)
            button.grid(row=1+i, column=0, column_weight=0)

   

class RightMenu(MenuBase):
    '''The menu for a file selected with a right click.
    '''

    def __init__(self, *args):
        super().__init__(*args)
      
        self.main_widget.open_rightclick_menu = self.set_file
        
        for i, label in enumerate(
                [tr.copy, tr.cut, tr.rename, tr.remove]):
            button = gb.ButtonWidget(self.operations_frame, label)
            button.grid(row=1+i, column=0, column_weight=0)


    def set_file(self, fn):
        '''Sets the file operated on.
        '''
        self.on_open()
        
        if self.icon_widget:
            self.icon_widget.destroy()
            self.icon_widget = None

        self.icon_widget = gic.IconWidget(
                self, gic.get_icon_imagename(fn), os.path.basename(fn),
                max_text_length=32, max_text_rows=3)
        self.icon_widget.grid(row=2, column=1, sticky='SWE')

    

class IconBrowser(gb.FrameWidget):
    '''Main view for browsing "imaginary" files.
    
    Attributes
    ----------
    listdir : callable
        Function that takes in a path and returns
        names of items.
    isdir : callable
        Function that takes in a path and returns True if is a directory
        or false if not.
    folder_widgets : list
        Folder-like entries that contain more entries
    file_widgets : list
        File-like entries that for example can open
        a program or a special view.
    gridded_widgets : list
        A subset of folder and file widgets that are
        visible on the current page.
    '''
    
    def __init__(self, parent, listdir, isdir, initial_dir=None):
        super().__init__(parent)
        self.listdir = listdir
        self.isdir = isdir

        self.folder_widgets = []
        self.file_widgets = []       
        
        self.gridded_widgets = []
        
        self._i_page = 0
        self.N_cols = 4
        self.N_rows = 4

        self.update_callbacks = []
        self.set(resize_handler=self.on_resize)

        if initial_dir:
            self.set_path(initial_dir)
   
    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self.set_path(path)

    @property
    def i_page(self):
        '''Index of the page.
        '''
        return self._i_page

    @i_page.setter
    def i_page(self, index):
        upper_lim = self.N_pages
        if index < 0:
            index = 0
        elif index > upper_lim:
            index = upper_lim
        self._i_page = int(index)
    
    @property
    def N_pages(self):
        pgs = (len(self.folder_widgets)+len(self.file_widgets)) / (self.N_cols*self.N_rows)
        return int(round(pgs))

    def on_resize(self, w, h):
        self.N_cols = int(w/(64*2))
        self.N_rows = int(h/(64*2))
        self.refresh_view()
    
    def open_rightclick_menu(self, filename):
        pass

    def on_leftclick(self, filename):
        pass

    def set_path(self, path):
        
        # Remove old
        for icon in self.folder_widgets+self.file_widgets:
            icon.destroy()
        self.folder_widgets = []
        self.file_widgets = []
        self.gridded_widgets = []
        
        # Add icons
        for item in sorted(self.listdir(path)):
            if item.startswith('.'):
                continue
            fullfn = os.path.join(path, item)
            funcR = lambda *args, f=fullfn: self.open_rightclick_menu(f)

            if self.isdir(fullfn):
                icon_imagename = os.path.join(DATALOC, 'folder.png')
                icon = gic.IconWidget(self, icon_imagename, item)
                func = lambda *args, f=fullfn: self.set_path(f)
                icon.image_widget.set(leftclick_handler=func)
                

                self.folder_widgets.append(icon)
            else:
                icon_imagename = os.path.join(DATALOC, 'file.png')
                icon = gic.IconWidget(self, icon_imagename, item)
                self.file_widgets.append(icon)
                funcL = lambda *args, f=fullfn: self.on_leftclick(f)
                icon.image_widget.set(leftclick_handler=funcL)
            icon.image_widget.set(rightclick_handler=funcR)
 
        
        self._path = path
        self.i_page = self._i_page  # Change to the page
        self.refresh_view()

   
    def refresh_view(self):
        
        for icon in self.gridded_widgets:
            icon.grid_remove()
      
        self.gridded_widgets = []

        N_cols = self.N_cols
        N_rows = self.N_rows
        i_widget_start = int(self.i_page*N_cols*N_rows)
        i_row = 0
        i_col = 0
        for icon in (self.folder_widgets+self.file_widgets)[i_widget_start:]:
            icon.grid(row=i_row, column=i_col)
            self.gridded_widgets.append(icon)
            i_col+=1
            if i_col >= N_cols:
                i_col = 0
                i_row += 1

            if i_row >= N_rows:
                break
        
        for func in self.update_callbacks:
            func()


    def go_uplevel(self):
        '''Goes one step "backwards" in the directory structure.
        '''
        self.path = os.path.dirname(self.path)

   

class FileBrowser(IconBrowser):
    '''Main view for browsing files on disk.
    '''

    def __init__(self, parent, initial_dir='~/'):
        super().__init__(parent, self._listdir, os.path.isdir)
        
        self.set_path(os.path.expanduser(initial_dir))

    def _listdir(self, path):
        return sorted(os.listdir(path))

    def set_path(self, path):
        '''Sets the view to the current directory.
        '''
        if not os.path.isdir(path):
            warnings.warn(f'Tried to open a nonexisting directory {path}')
            return

        super().set_path(path)

                     
       


class PageControl(gb.FrameWidget):
    '''Controls the main widget's page change ("scrolling")

    requires attributes/properties
        i_page, N_pages
    '''

    def __init__(self, parent, main_widget):
        super().__init__(parent)
        self.main_widget = main_widget
        self.main_widget.update_callbacks.append(self.on_update)

        self.previous_button = gb.ButtonWidget(self, tr.previous_page)
        self.previous_button.set_command(self.previous_page)
        self.previous_button.grid(row=0, column=0)

        self.status_text = gb.TextWidget(self, '')
        self.status_text.grid(row=0, column=1)

        self.next_button = gb.ButtonWidget(self, tr.next_page)
        self.next_button.set_command(self.next_page)
        self.next_button.grid(row=0, column=2)
    

    def on_update(self):
        text = f'{tr.page} {self.main_widget.i_page+1}/{self.main_widget.N_pages+1}'
        self.status_text.set(text=text)

    def next_page(self):
        self.main_widget.i_page += 1
        self.main_widget.refresh_view()

    def previous_page(self):
        self.main_widget.i_page -= 1
        self.main_widget.refresh_view()



class DefaultToolbar(gb.FrameWidget):
    '''Controls the main widget

    Required methods for the main widget:
        - go_uplevel
    '''
    def __init__(self, parent, main_widget):
        super().__init__(parent)

        self.main_widget = main_widget
        self.main_widget.update_callbacks.append(self.on_update)
        
        self.back_button = gb.ButtonWidget(self, tr.back)
        self.back_button.set_command(main_widget.go_uplevel)
        self.back_button.grid(row=0, column=0, column_weight=0)

        self.location_text = gb.TextWidget(self)
        self.location_text.grid(row=0, column=1, column_weight=1)
        self.location_text.set(bg='white')

        self.operations_button = gb.ButtonWidget(
                self, tr.operations, command=lambda: self.open_operations_menu())
        self.operations_button.grid(row=0, column=2, column_weight=0)
        

    def on_update(self):
        text=self.main_widget.path
        self.location_text.set(text=text)


    def open_operations_menu(self):
        print('lol')


class SelectToolbar(DefaultToolbar):
    '''Operations menu replaced with folder selection

    Attributes
    ----------
    on_select : callable
        Function that is called when selecting the folder.
    '''
    def __init__(self, parent, main_widget, on_select):
        super().__init__(parent, main_widget)
        self.on_select = on_select

        self.operations_button.set(text=tr.select_folder)

    def open_operations_menu(self):
        self.on_select(self.main_widget.path)


# DIALOG PARTS

class FolderSelect(gb.FrameWidget):
    '''Puts together a complete widget-set for selecting a folder.
    '''
    def __init__(self, parent, on_select):
        '''
        on_select : callable
        '''
        super().__init__(parent)
        self.main_view = FileBrowser(self)
        self.main_view.grid(row=3, column=1)

        self.page_change = PageControl(
                self, self.main_view)
        self.page_change.grid(row=2, column=1, row_weight=0)

        self.toolbar = SelectToolbar(
                self, self.main_view, on_select)
        self.toolbar.grid(row=1, column=1, row_weight=0)


class SaveDialog(gb.FrameWidget):
    '''Filename and save folder selected separately.
    '''

    def __init__(self, parent, initial_name, initial_folder,
                 on_save, on_cancel):
        super().__init__(parent)

        if initial_folder is None:
            initial_folder = os.path.expanduser('~/')
        
        self.initial_view = gb.FrameWidget(self)
        self.initial_view.grid()

        self.back_button = gb.ButtonWidget(self.initial_view, tr.back)
        self.back_button.set_command(on_cancel)
        self.back_button.grid(row=1, column=1, columnspan=2)
        
        self.name_label = gb.TextWidget(self.initial_view, tr.filename)
        self.name_label.grid(row=2, column=1, sticky='WES')

        self.name_entry = gb.EntryWidget(self.initial_view)
        self.name_entry.grid(row=2, column=2, sticky='WES')
        
        self.folder_label = gb.TextWidget(self.initial_view, tr.folder)
        self.folder_label.grid(row=3, column=1, sticky='WEN')
        
        self.folder_entry = gb.ButtonWidget(
                self.initial_view, initial_folder)
        self.folder_entry.set_command(self.select_folder)
        self.folder_entry.grid(row=3, column=2, sticky='WEN')
        
        self.save_button = gb.ButtonWidget(self.initial_view, tr.save)
        self.save_button.set_command(self._on_save)
        self.save_button.grid(row=4, column=1, columnspan=2)

        self.folder = initial_folder
        self.on_save = on_save
    
    def _on_save(self):
        if not os.path.isdir(self.folder):
            warnings.warn('Selected folder isdir==False, skipping save')
            return
        name = self.name_entry.get_input()
        path = os.path.join(self.folder, name)
        self.on_save(path)

    def select_folder(self):
        self.folder_select = FolderSelect(self, self._post_folder_select)
        self.folder_select.grid()
        self.initial_view.grid_remove()

    def _post_folder_select(self, path):
        self.folder_select.grid_remove()
        self.folder_select.destroy()
        del self.folder_select
        self.initial_view.grid()

        if os.path.isdir(path):
            self.folder_entry.set(text=path)
            self.folder = path

