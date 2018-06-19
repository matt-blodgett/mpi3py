import os
import tkinter as tk
from mpi3pc.control import libinter
from mpi3pc.gui import tkit
from mpi3pc import gui
from mpi3 import settings
from mpi3 import medialib
from . import libtrees


class BaseManagerFrame(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(bd=0, highlightthickness=1)
        self.config(highlightbackground='#000000')
        self.config(bg='#EFF2FF', height=10)

        self.frm_west = tk.Frame(self)
        self.frm_east = tk.Frame(self)

        self.frm_west.config(bd=0, highlightthickness=0)
        self.frm_east.config(bd=0, highlightthickness=0)
        self.frm_west.config(bg='#EFF2FF')
        self.frm_east.config(bg='#EFF2FF')

        self.frm_west.grid(row=0, column=0, sticky=tk.NW)
        self.frm_east.grid(row=0, column=1, sticky=tk.NW)
        self.frm_west.grid(padx=20, pady=15)
        self.frm_east.grid(padx=0, pady=15)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, minsize=325)
        self.grid_columnconfigure(1, minsize=325)


class BaseManagerLabel(tk.Label):

    def __init__(self, master):
        tk.Label.__init__(self, master)
        self.config(bd=0, highlightthickness=0)
        self.config(bg='#EFF2FF', anchor=tk.W)
        self.config(font=gui.font(9))


class BaseManagerSeparator(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(bg='#000000', height=1)
        self.grid(padx=2, pady=5)


class LibraryManagerFrame(BaseManagerFrame):

    def __init__(self, master):
        BaseManagerFrame.__init__(self, master)

        self.lbl_info_title = BaseManagerLabel(self.frm_west)
        self.lbl_info_name = BaseManagerLabel(self.frm_west)
        self.lbl_info_ppid = BaseManagerLabel(self.frm_west)
        self.lbl_info_date = BaseManagerLabel(self.frm_west)

        self.lbl_name = BaseManagerLabel(self.frm_west)
        self.lbl_ppid = BaseManagerLabel(self.frm_west)
        self.lbl_date = BaseManagerLabel(self.frm_west)

        self.lbl_info_title.grid(row=0, column=0, sticky=tk.NSEW)
        self.lbl_info_ppid.grid(row=1, column=0, sticky=tk.NSEW)
        self.lbl_info_date.grid(row=2, column=0, sticky=tk.NSEW)
        self.lbl_info_title.grid(rowspan=1, columnspan=2)
        self.lbl_info_title.grid(padx=0, pady=4)
        self.lbl_info_ppid.grid(padx=0, pady=2)
        self.lbl_info_date.grid(padx=0, pady=2)

        self.lbl_ppid.grid(row=1, column=1, sticky=tk.NSEW)
        self.lbl_date.grid(row=2, column=1, sticky=tk.NSEW)
        self.lbl_ppid.grid(padx=6, pady=1)
        self.lbl_date.grid(padx=6, pady=1)

        self.lbl_file = BaseManagerLabel(self.frm_east)
        self.btn_export = tkit.Mpi3TButton(self.frm_east)
        self.btn_import = tkit.Mpi3TButton(self.frm_east)
        self.btn_cnew = tkit.Mpi3TButton(self.frm_east)
        self.btn_save = tkit.Mpi3TButton(self.frm_east)
        self.btn_export.config(width=16)

        self.lbl_file.grid(row=0, column=0, sticky=tk.NSEW)
        self.btn_export.grid(row=1, column=0, sticky=tk.NSEW)
        self.btn_import.grid(row=2, column=0, sticky=tk.NSEW)
        self.btn_cnew.grid(row=3, column=0, sticky=tk.NSEW)
        self.btn_save.grid(row=4, column=0, sticky=tk.NSEW)
        self.lbl_file.grid(padx=0, pady=5)

        self.lbl_info_ppid.config(text='Unique ID:')
        self.lbl_info_date.config(text='Created:')
        self.lbl_info_title.config(font=gui.font(11, 'bold'))
        self.lbl_info_date.config(font=gui.font(9, 'bold'))
        self.lbl_info_ppid.config(font=gui.font(9, 'bold'))

        self.lbl_file.config(text='Library Files')
        self.lbl_file.config(font=gui.font(11, 'bold'))
        self.btn_export.config(text='Export')
        self.btn_import.config(text='Import')
        self.btn_cnew.config(text='Create New')
        self.btn_save.config(text='Save Current')

    def refresh(self):
        self.lbl_info_title.config(text=medialib.name)
        self.lbl_ppid.config(text=medialib.pid)
        self.lbl_date.config(text=medialib.added[:10])


class MediaManagerFrame(BaseManagerFrame):

    def __init__(self, master):
        BaseManagerFrame.__init__(self, master)

        self.lbl_info_title = BaseManagerLabel(self.frm_west)
        self.lbl_info_path = BaseManagerLabel(self.frm_west)
        self.lbl_info_size = BaseManagerLabel(self.frm_west)
        self.lbl_info_songs = BaseManagerLabel(self.frm_west)

        self.lbl_path = BaseManagerLabel(self.frm_west)
        self.lbl_size = BaseManagerLabel(self.frm_west)
        self.lbl_songs = BaseManagerLabel(self.frm_west)

        self.lbl_info_title.grid(row=0, column=0, sticky=tk.NSEW)
        self.lbl_info_path.grid(row=1, column=0, sticky=tk.NSEW)
        self.lbl_info_size.grid(row=2, column=0, sticky=tk.NSEW)
        self.lbl_info_songs.grid(row=3, column=0, sticky=tk.NSEW)
        self.lbl_info_title.grid(rowspan=1, columnspan=2)
        self.lbl_info_title.grid(padx=0, pady=5)
        self.lbl_info_path.grid(padx=0, pady=2)
        self.lbl_info_songs.grid(padx=0, pady=2)
        self.lbl_info_size.grid(padx=0, pady=2)

        self.lbl_path.grid(row=1, column=1, sticky=tk.NSEW)
        self.lbl_size.grid(row=2, column=1, sticky=tk.NSEW)
        self.lbl_songs.grid(row=3, column=1, sticky=tk.NSEW)
        self.lbl_path.grid(padx=6, pady=0)
        self.lbl_size.grid(padx=6, pady=0)
        self.lbl_songs.grid(padx=6, pady=0)

        self.lbl_files = BaseManagerLabel(self.frm_east)
        self.btn_download = tkit.Mpi3TButton(self.frm_east)
        self.btn_import_songs = tkit.Mpi3TButton(self.frm_east)
        self.btn_import_playlists = tkit.Mpi3TButton(self.frm_east)
        self.btn_download.config(width=16)

        self.lbl_files.grid(row=0, column=0, sticky=tk.NSEW)
        self.btn_download.grid(row=1, column=0, sticky=tk.NSEW)
        self.btn_import_songs.grid(row=2, column=0, sticky=tk.NSEW)
        self.btn_import_playlists.grid(row=3, column=0, sticky=tk.NSEW)
        self.lbl_files.grid(padx=0, pady=5)

        self.lbl_info_title.config(text='Library Media')
        self.lbl_info_path.config(text='Location:')
        self.lbl_info_size.config(text='Total Size:')
        self.lbl_info_songs.config(text='Total Songs:')
        self.lbl_info_title.config(font=gui.font(11, 'bold'))
        self.lbl_info_path.config(font=gui.font(9, 'bold'))
        self.lbl_info_size.config(font=gui.font(9, 'bold'))
        self.lbl_info_songs.config(font=gui.font(9, 'bold'))

        self.lbl_files.config(text='Media Files')
        self.lbl_files.config(font=gui.font(11, 'bold'))
        self.btn_download.config(text='Download Songs')
        self.btn_import_songs.config(text='Import Songs')
        self.btn_import_playlists.config(text='Import Playlists')

    def refresh(self):
        self.lbl_path.config(text=os.path.abspath(settings['PATHS']['MEDIA']))
        self.lbl_size.config(text='406.21 MB')
        self.lbl_songs.config(text=str(len(medialib.songs)))


class DrivesManagerFrame(BaseManagerFrame):

    def __init__(self, master):
        BaseManagerFrame.__init__(self, master)

        self.lbl_info_option = BaseManagerLabel(self.frm_east)
        self.btn_make_volume = tkit.Mpi3TButton(self.frm_east)
        self.btn_load_volume = tkit.Mpi3TButton(self.frm_east)
        self.lbl_make_volume = BaseManagerLabel(self.frm_east)
        self.lbl_load_volume = BaseManagerLabel(self.frm_east)

        self.lbl_info_option.grid(row=0, column=0, sticky=tk.NSEW)
        self.btn_make_volume.grid(row=1, column=0, sticky=tk.NSEW)
        self.btn_load_volume.grid(row=2, column=0, sticky=tk.NSEW)
        self.lbl_make_volume.grid(row=1, column=1, sticky=tk.NSEW)
        self.lbl_load_volume.grid(row=2, column=1, sticky=tk.NSEW)
        self.lbl_info_option.grid(rowspan=1, columnspan=2)
        self.lbl_make_volume.grid(padx=2, pady=0)
        self.lbl_load_volume.grid(padx=2, pady=0)

        self.lbl_tree = BaseManagerLabel(self.frm_west)
        self.frm_drives = tk.Frame(self.frm_west)
        self.tree_drives = RRDTreeview(self.frm_drives)
        self.bar_scroll = tk.Scrollbar(self.frm_drives)

        self.frm_drives.config(bd=1, highlightthickness=1)
        self.frm_drives.config(highlightbackground='#000000')
        self.bar_scroll.config(command=self.tree_drives.yview)
        self.tree_drives.config(yscrollcommand=self.bar_scroll.set)
        self.tree_drives.grid(row=0, column=0, sticky=tk.NSEW)
        self.bar_scroll.grid(row=0, column=1, sticky=tk.NSEW)

        self.lbl_tree.grid(row=0, column=0, sticky=tk.NSEW)
        self.frm_drives.grid(row=1, column=0, sticky=tk.NSEW)
        self.frm_drives.grid_columnconfigure(0, weight=1)
        self.lbl_tree.grid(padx=0, pady=5)

        self.lbl_info_option.config(text='Libraries')
        self.lbl_info_option.config(font=gui.font(9, 'bold'))
        self.lbl_make_volume.config(text='Create a new library')
        self.lbl_load_volume.config(text='Load selected library')
        self.btn_make_volume.config(text='Create')
        self.btn_load_volume.config(text='Load')

        self.lbl_tree.config(text='Removable Drives')
        self.lbl_tree.config(font=gui.font(9, 'bold'))

        self.btn_load_volume.state(['disabled'])
        self.tree_drives.bind('<ButtonRelease-1>', self._on_lclick, add=True)

    def _on_lclick(self, event):
        if len(self.tree_drives.selection()) > 0:
            if self.tree_drives.item(self.tree_drives.selection()[0])['tags'][0] not in ['drive', 'empty']:
                self.btn_load_volume.state(['!disabled'])
            else: self.btn_load_volume.state(['disabled'])
        else: self.btn_load_volume.state(['disabled'])


class RaspiMediaManagerFrame(BaseManagerFrame):

    def __init__(self, master):
        BaseManagerFrame.__init__(self, master)

        self.frm_north = tk.Frame(self)
        self.frm_north.config(bg='#EFF2FF')
        self.frm_north.config(bd=0, highlightthickness=0)
        self.frm_north.grid(row=0, column=0, sticky=tk.NSEW)
        self.frm_north.grid(padx=20, pady=10)

        self.lbl_info = BaseManagerLabel(self.frm_north)

        self.lbl_info.grid(row=0, column=0, sticky=tk.NSEW)

        self.lbl_info.grid(padx=0, pady=5)

        self.sep_frames = BaseManagerSeparator(self)
        self.sep_frames.grid(row=1, column=0, sticky=tk.NSEW)
        self.sep_frames.grid(rowspan=1, columnspan=2)
        self.sep_frames.grid(padx=20, pady=10)

        self.lbl_info_name = BaseManagerLabel(self.frm_west)
        self.lbl_info_path = BaseManagerLabel(self.frm_west)
        self.lbl_info_date = BaseManagerLabel(self.frm_west)
        self.lbl_info_size = BaseManagerLabel(self.frm_west)

        self.lbl_path = BaseManagerLabel(self.frm_west)
        self.lbl_date = BaseManagerLabel(self.frm_west)
        self.lbl_size = BaseManagerLabel(self.frm_west)

        self.lbl_info_name.grid(row=0, column=0, sticky=tk.NSEW)
        self.lbl_info_path.grid(row=1, column=0, sticky=tk.NSEW)
        self.lbl_info_date.grid(row=2, column=0, sticky=tk.NSEW)
        self.lbl_info_size.grid(row=3, column=0, sticky=tk.NSEW)
        self.lbl_info_name.grid(rowspan=1, columnspan=2)
        self.lbl_info_name.grid(padx=0, pady=5)
        self.lbl_info_path.grid(padx=0, pady=2)
        self.lbl_info_date.grid(padx=0, pady=2)
        self.lbl_info_size.grid(padx=0, pady=2)

        self.lbl_path.grid(row=1, column=1, sticky=tk.NSEW)
        self.lbl_date.grid(row=2, column=1, sticky=tk.NSEW)
        self.lbl_size.grid(row=3, column=1, sticky=tk.NSEW)
        self.lbl_path.grid(padx=5, pady=0)
        self.lbl_date.grid(padx=5, pady=0)
        self.lbl_size.grid(padx=5, pady=0)

        self.lbl_sync = BaseManagerLabel(self.frm_east)
        self.frm_sync = tk.Frame(self.frm_east)
        self.tree_sync = libtrees.CSyncTreeview(self.frm_sync)
        self.bar_scroll = tk.Scrollbar(self.frm_sync)

        self.frm_sync.config(bd=1, highlightthickness=1)
        self.frm_sync.config(highlightbackground='#000000')
        self.bar_scroll.config(command=self.tree_sync.yview)
        self.tree_sync.config(yscrollcommand=self.bar_scroll.set)
        self.tree_sync.grid(row=0, column=0, sticky=tk.NSEW)
        self.bar_scroll.grid(row=0, column=1, sticky=tk.NSEW)

        self.lbl_sync.grid(row=0, column=0, sticky=tk.NSEW)
        self.frm_sync.grid(row=1, column=0, sticky=tk.NSEW)
        self.frm_sync.grid_columnconfigure(0, weight=1)
        self.lbl_sync.grid(padx=0, pady=5)

        self.frm_west.grid(row=2, column=0, sticky=tk.NW)
        self.frm_east.grid(row=2, column=1, sticky=tk.NW)

        self.frm_south = tk.Frame(self)
        self.frm_south.config(bg='#EFF2FF')
        self.frm_south.config(bd=0, highlightthickness=0)
        self.frm_south.grid(row=3, column=0, sticky=tk.NSEW)
        self.frm_south.grid(padx=20, pady=10)
        self.frm_south.grid(rowspan=1, columnspan=2)
        self.frm_south.grid_columnconfigure(0, weight=1)

        self.lbl_drive = BaseManagerLabel(self.frm_south)
        self.btn_sync = tkit.Mpi3TButton(self.frm_south)
        self.disp_storage = tkit.StorageSpaceDisplay(self.frm_south)

        self.lbl_drive.grid(row=0, column=0, sticky=tk.NSEW)
        self.btn_sync.grid(row=1, column=1, sticky=tk.NSEW)
        self.disp_storage.grid(row=1, column=0, sticky=tk.NSEW)
        self.lbl_drive.grid(padx=2, pady=2)

        self.lbl_info.config(text='Raspi Test Library')
        self.lbl_info.config(font=gui.font(16, 'bold'))

        self.lbl_sync.config(text='Sync Media')
        self.lbl_sync.config(font=gui.font(11, 'bold'))

        self.lbl_info_name.config(text='Raspi Test Library')
        self.lbl_info_path.config(text='Location:')
        self.lbl_info_date.config(text='Created:')
        self.lbl_info_size.config(text='Total Size:')
        self.lbl_info_name.config(font=gui.font(11, 'bold'))
        self.lbl_info_path.config(font=gui.font(9, 'bold'))
        self.lbl_info_date.config(font=gui.font(9, 'bold'))
        self.lbl_info_size.config(font=gui.font(9, 'bold'))
        self.btn_sync.config(text='Sync')

        self.lbl_drive.config(text='RASPI (E:)')
        self.lbl_path.config(text='E:\\mpi3pc')
        self.lbl_date.config(text='2017-10-23')
        self.lbl_size.config(text='00.46 GB')

        self.display()

    def refresh(self):
        self.tree_sync.refresh()

    def display(self, connected=False):
        if not connected:
            self.sep_frames.grid_remove()
            self.frm_west.grid_remove()
            self.frm_east.grid_remove()
            self.frm_south.grid_remove()
            self.frm_sync.grid_remove()

            self.lbl_info.config(text='No library loaded')

    def redisplay(self, connected=True):
        if connected:
            self.sep_frames.grid()
            self.frm_west.grid()
            self.frm_east.grid()
            self.frm_south.grid()
            self.frm_sync.grid()

            self.disp_storage.refresh(5_804_000_000, 18_175_000_000, 30_000_000_000)
            self.lbl_info.config(text='Raspi Test Library')


class RRDTreeview(tkit.Mpi3Treeview):
    # Raspi Removable Drives

    def __init__(self, master):
        tkit.Mpi3Treeview.__init__(self, master)

        self._rclick_menu = RRDMenu(self)

        self.config(selectmode='browse')
        self.config(style=gui.MPI3_TREEVIEW_DRIVES)
        self.config(height=5)

        self['columns'] = ['size', 'free']

        self.column('#0', width=160, anchor=tk.W)
        self.column('size', width=50, anchor=tk.W)
        self.column('free', width=50, anchor=tk.W)

        self.heading('#0', text='Drive', anchor=tk.W)
        self.heading('size', text='Size', anchor=tk.W)
        self.heading('free', text='Free', anchor=tk.W)

        self.bind('<MouseWheel>', self._on_scroll)
        self.bind('<ButtonPress-1>', self._on_lclick)
        self.bind('<ButtonRelease-3>', self._on_rclick)

        d1 = self.insert('', tk.END, text='E: (RASPI)', values=('31GB', '24GB'), open=True, tags='drive')
        d2 = self.insert('', tk.END, text='F: (FLASH)', values=('128GB', '90GB'), open=True, tags='drive')

        self.insert(d1, tk.END, text='Raspi Test Library', values=('', ''), tags='R:S4A8QMZ12WVHG76S')
        self.insert(d1, tk.END, text='Raspi Test Library 2', values=('', ''), tags='R:QSD8ASD2WSAD12L')
        self.insert(d1, tk.END, text='Raspi Test Library 3', values=('', ''), tags='R:58PGG84ZZAFS5854')
        self.insert(d2, tk.END, text='(no library detected)', values=('', ''), tags='empty')

        self.delete(d1)

    def _on_scroll(self, event):
        direction = int(-1*(event.delta/120))
        self.yview_scroll(direction, 'units')

        tree_items = self.get_children()

        try:
            if not self.bbox(tree_items[0]) and direction < 0:
                return 'break'
            elif not self.bbox(tree_items[-1]) and direction > 0:
                return 'break'
        except IndexError:
            pass

    def _on_lclick(self, event):
        region_id = self.identify_region(event.x, event.y)

        if region_id in ['heading', 'separator']:
            return 'break'
        elif region_id == 'nothing':
            self.selection_remove(*self.get_children())

    def _on_rclick(self, event):
        row = self.identify_row(event.y)

        if row and row not in self.selection():
            self.selection_set(row)
        elif not row:
            self.selection_remove(*self.get_children())

        if len(self.selection()) > 0:
            self._rclick_menu.setup(event)

    def refresh_drives(self, drive):
        pass

    def refresh_library(self, pid):
        pass


class RRDMenu(tk.Menu):

    def __init__(self, master):
        tk.Menu.__init__(self, master)
        self.config(tearoff=False)
        self.config(font=gui.font(9))

    def setup(self, event):
        self.delete(0, tk.END)

        selected_row = self.master.selection()[0]

        self.add_command(label='Expand All', command=lambda: self._expcoll_all(True))
        self.add_command(label='Collapse All', command=lambda: self._expcoll_all(False))
        self.add_separator()

        if 'drive' in self.master.item(selected_row)['tags']:
            self.add_command(label='Create')
        else:
            self.add_command(label='Load')
            self.add_command(label='Delete')

        self.tk_popup(event.x_root, event.y_root)

    def _expcoll_all(self, open):
        for item in self.master.get_children():
            self.master.item(item, open=open)


class LibraryManagerPanel(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(bd=0, highlightthickness=0)
        self.config(bg='#FFFFFF')

    def initiate(self):
        self._layout()

        self.frm_media.btn_download.bind('<ButtonRelease-1>', lambda e: libinter.download_songs())
        self.frm_media.btn_import_songs.bind('<ButtonRelease-1>', lambda e: libinter.import_songs())
        self.frm_media.btn_import_playlists.bind('<ButtonRelease-1>', lambda e: libinter.import_playlists())

        self.frm_library.btn_export.bind('<ButtonRelease-1>', lambda e: libinter.library_saveas())
        self.frm_library.btn_import.bind('<ButtonRelease-1>', lambda e: libinter.library_load())
        self.frm_library.btn_cnew.bind('<ButtonRelease-1>', lambda e: libinter.library_new())
        self.frm_library.btn_save.bind('<ButtonRelease-1>', lambda e: libinter.library_save())

    def refresh(self):
        self.frm_library.refresh()
        self.frm_media.refresh()

    def _layout(self):
        self.container_lib = tk.Frame(self)
        self.lbl_lib = tk.Label(self.container_lib)
        self.frm_library = LibraryManagerFrame(self.container_lib)
        self.lbl_lib.grid(row=0, column=0, sticky=tk.NSEW)
        self.frm_library.grid(row=1, column=0, sticky=tk.NSEW)
        self.container_lib.grid_rowconfigure(1, weight=1)
        self.container_lib.grid_columnconfigure(0, weight=1)

        self.container_media = tk.Frame(self)
        self.lbl_media = tk.Label(self.container_media)
        self.frm_media = MediaManagerFrame(self.container_media)
        self.lbl_media.grid(row=0, column=0, sticky=tk.NSEW)
        self.frm_media.grid(row=1, column=0, sticky=tk.NSEW)
        self.container_media.grid_rowconfigure(1, weight=1)
        self.container_media.grid_columnconfigure(0, weight=1)

        self.lbl_lib.config(text='Library')
        self.lbl_media.config(text='Media')
        self.lbl_lib.config(bg='#FFFFFF', fg='#000000')
        self.lbl_media.config(bg='#FFFFFF', fg='#000000')
        self.lbl_lib.config(font=gui.font(16), anchor=tk.W)
        self.lbl_media.config(font=gui.font(16), anchor=tk.W)

        self.container_lib.grid(row=0, column=1, sticky=tk.NSEW)
        self.container_media.grid(row=1, column=1, sticky=tk.NSEW)
        self.container_lib.grid(padx=15, pady=15)
        self.container_media.grid(padx=15, pady=15)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)


class RaspiManagerPanel(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(bd=0, highlightthickness=0)
        self.config(bg='#FFFFFF')

    def initiate(self):
        self._layout()
        self.frm_raspi.tree_sync.refresh()
        self.frm_raspi.tree_sync.set_open(True)

        self.frm_devices.btn_load_volume.bind('<ButtonRelease-1>', lambda e: self.frm_raspi.redisplay())
        self.frm_devices.btn_make_volume.bind('<ButtonRelease-1>', lambda e: self.frm_raspi.display())
        # self.frm_devices.btn_create_volume.bind('<ButtonRelease-1>', lambda e: raspinter.new_volume())

        self.frm_raspi.btn_sync.bind('<ButtonRelease-1>', lambda e: libinter.library_sync())

        self.frm_raspi.disp_storage.refresh(5_804_000_000, 18_175_000_000, 30_000_000_000)
        # self.disp_storage.refresh(5_804_000_000, 22_100_000_000, 30_000_000_000)
        # self.disp_storage.refresh(2_000_000_000, 27_100_000_000, 30_000_000_000)
        # self.disp_storage.refresh(20_000_000_000, 4_000_000_000, 30_000_000_000)

    def refresh(self):
        self.frm_raspi.refresh()

    def _layout(self):
        self.container_devices = tk.Frame(self)
        self.lbl_devices = tk.Label(self.container_devices)
        self.frm_devices = DrivesManagerFrame(self.container_devices)
        self.lbl_devices.grid(row=0, column=0, sticky=tk.NSEW)
        self.frm_devices.grid(row=1, column=0, sticky=tk.NSEW)
        self.container_devices.grid_rowconfigure(1, weight=1)
        self.container_devices.grid_columnconfigure(0, weight=1)

        self.container_raspi = tk.Frame(self)
        self.lbl_raspi = tk.Label(self.container_raspi)
        self.frm_raspi = RaspiMediaManagerFrame(self.container_raspi)
        self.lbl_raspi.grid(row=0, column=0, sticky=tk.NSEW)
        self.frm_raspi.grid(row=1, column=0, sticky=tk.NSEW)
        self.container_raspi.grid_rowconfigure(1, weight=1)
        self.container_raspi.grid_columnconfigure(0, weight=1)

        self.lbl_devices.config(text='Drives')
        self.lbl_raspi.config(text='Raspberry Pi')
        self.lbl_devices.config(bg='#FFFFFF', fg='#000000')
        self.lbl_raspi.config(bg='#FFFFFF', fg='#000000')
        self.lbl_devices.config(font=gui.font(16), anchor=tk.W)
        self.lbl_raspi.config(font=gui.font(16), anchor=tk.W)

        self.container_devices.grid(row=0, column=1, sticky=tk.NSEW)
        self.container_raspi.grid(row=1, column=1, sticky=tk.NSEW)

        self.container_devices.grid(padx=15, pady=15)
        self.container_raspi.grid(padx=15, pady=15)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)


class ControlFrame(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(bd=0, highlightthickness=0)
        self.config(bg='#FFFFFF')

        self.frm_canvas = tk.Canvas(self)
        self.bar_scroll = tk.Scrollbar(self)
        self.bar_scroll.config(command=self.frm_canvas.yview)
        self.frm_canvas.config(yscrollcommand=self.bar_scroll.set)
        self.frm_canvas.config(bd=0, highlightthickness=0)
        self.frm_canvas.config(bg='#FFFFFF')

        self.frm_canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.bar_scroll.grid(row=0, column=1, sticky=tk.NSEW)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _on_configure(self, event):
        self.frm_canvas.itemconfig(self.frm_window, width=event.width)
        self.frm_canvas.config(scrollregion=self.frm_canvas.bbox(self.frm_window))

    def initiate(self, manageframe):
        self.frm_manage = manageframe(self.frm_canvas)
        self.frm_window = self.frm_canvas.create_window(
            (0, 0), window=self.frm_manage, anchor=tk.NW)

        self.bind('<Configure>', self._on_configure)
        self.frm_manage.bind('<Configure>', self._on_configure)
        self.frm_manage.initiate()

        def scroll(event):
            if self.frm_canvas.winfo_height() < self.frm_manage.winfo_height():
                self.frm_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

        def scroll_bind(parent):
            if not isinstance(parent, tk.Scrollbar):
                parent.bind('<MouseWheel>', scroll, add=True)
            for child in parent.children.values():
                scroll_bind(child)
        scroll_bind(self)

    def refresh(self):
        self.frm_manage.refresh()
