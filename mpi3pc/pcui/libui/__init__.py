import logging
import tkinter as tk
from mpi3pc.control import libinter
from mpi3pc.gui import tkit
from mpi3pc import gui
from mpi3 import settings
from . import libframes
from . import libtrees


class LibraryManager(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master, bd=0)

    def initiate(self):
        self._layout()
        self.btn_vlibrary.bind('<ButtonRelease-1>', lambda e: self.view_library())
        self.btn_vraspi.bind('<ButtonRelease-1>', lambda e: self.view_raspi())
        self.btn_vsongs.bind('<ButtonRelease-1>', lambda e: self.view_allsongs())
        self.btn_vartists.bind('<ButtonRelease-1>', lambda e: self.view_allartists())
        self.btn_vcontain.bind('<ButtonRelease-1>', lambda e: self.view_containers())
        self.btn_options.bind('<ButtonRelease-1>', lambda e: self._manage())
        self.tree_containers.cmd_dbl_click = self._view_playlist_tree
        self.tree_sidebar.cmd_dbl_click = self._view_playlist_tree

    def load(self):
        self.frm_library.initiate(libframes.LibraryManagerPanel)
        self.frm_raspi.initiate(libframes.RaspiManagerPanel)

        self.tree_artists.refresh()
        self.tree_containers.refresh()
        self.tree_sidebar.refresh()
        self.tree_artists.set_open(True)
        self.tree_containers.set_open(True)
        self.tree_sidebar.set_open(True)

        view_init = settings['PLAYBACK']['INITIALVIEW']
        if view_init.startswith('P:'):
            self.view_playlist(view_init)
        else: getattr(self, view_init)()

    def view_library(self):
        libinter.display_refresh = self.view_library
        self.tree_sidebar.refresh()
        self.frm_library.refresh()
        self._view_pane(self.pane_library)

    def view_raspi(self):
        libinter.display_refresh = self.view_raspi
        self.frm_raspi.refresh()
        self._view_pane(self.pane_raspi)

    def view_allsongs(self):
        libinter.display_refresh = self.view_allsongs
        self._view_pane(self.pane_tree)
        self._view_tree(self.tree_songs)

    def view_allartists(self):
        libinter.display_refresh = self.view_allartists
        self._view_pane(self.pane_tree)
        self._view_tree(self.tree_artists)

    def view_containers(self):
        libinter.display_refresh = self.view_containers
        self._view_pane(self.pane_tree)
        self._view_tree(self.tree_containers)

    def _view_playlist_tree(self, tree):
        pid = tree.selected_pid_playlist()
        if pid: self.view_playlist(pid)

    def view_playlist(self, pid):
        libinter.display_refresh = lambda: self.view_playlist(pid)
        self.tree_playlist.set_playlist(pid)
        self._view_pane(self.pane_tree)
        self._view_tree(self.tree_playlist)

    def _view_tree(self, tree):
        self.tree_songs.grid_remove()
        self.tree_artists.grid_remove()
        self.tree_containers.grid_remove()
        self.tree_playlist.grid_remove()

        tree.grid()
        self._display(tree.refresh())
        self.tree_sidebar.refresh()
        self.bar_scroll_tree.config(command=tree.yview)
        tree.config(yscrollcommand=self.bar_scroll_tree.set)

    def _view_pane(self, pane):
        pane_current = self.pane_window.panes()[1]
        if pane_current is not pane:
            self.pane_window.forget(pane_current)
            self.pane_window.add(pane)

    def _display(self, display):
        name, count, append = display
        disp = str(count) + append
        if not count == 1: disp += 's'
        self.lbl_name.config(text=name)
        self.lbl_count.config(text=disp)

    def _manage(self):
        pass

    def _layout(self):
        self.pane_window = tk.PanedWindow(self, orient='horizontal')

        self.pane_view = tk.Frame(self.pane_window)
        self.btn_vlibrary = tkit.Mpi3TButton(self.pane_view)
        self.btn_vraspi = tkit.Mpi3TButton(self.pane_view)
        self.sep_buttons = tk.Frame(self.pane_view, bg='#000000', height=1)
        self.btn_vsongs = tkit.Mpi3TButton(self.pane_view)
        self.btn_vartists = tkit.Mpi3TButton(self.pane_view)
        self.btn_vcontain = tkit.Mpi3TButton(self.pane_view)
        self.sep_sidebar = tk.Frame(self.pane_view, bg='#000000', height=1)
        self.tree_sidebar = libtrees.CSidebarTreeview(self.pane_view)

        self.btn_vlibrary.config(text='Library')
        self.btn_vraspi.config(text='Raspi')
        self.btn_vsongs.config(text='Songs')
        self.btn_vartists.config(text='Artists')
        self.btn_vcontain.config(text='Playlists')

        self.btn_vlibrary.grid(row=0, column=0, sticky=tk.NSEW)
        self.btn_vraspi.grid(row=1, column=0, sticky=tk.NSEW)
        self.sep_buttons.grid(row=2, column=0, sticky=tk.NSEW)
        self.btn_vsongs.grid(row=3, column=0, sticky=tk.NSEW)
        self.btn_vartists.grid(row=4, column=0, sticky=tk.NSEW)
        self.btn_vcontain.grid(row=5, column=0, sticky=tk.NSEW)
        self.sep_sidebar.grid(row=6, column=0, sticky=tk.NSEW)
        self.tree_sidebar.grid(row=7, column=0, sticky=tk.NSEW)
        self.sep_buttons.grid(padx=3, pady=4)
        self.sep_sidebar.grid(padx=3, pady=3)

        self.pane_view.config(width=180)
        self.pane_view.grid_propagate(False)
        self.pane_view.grid_rowconfigure(7, weight=1)
        self.pane_view.grid_columnconfigure(0, weight=1)

        self.pane_library = tk.Frame(self.pane_window)
        self.frm_library = libframes.ControlFrame(self.pane_library)
        self.frm_library.grid(row=0, column=0, sticky=tk.NSEW)
        self.pane_library.grid_rowconfigure(0, weight=1)
        self.pane_library.grid_columnconfigure(0, weight=1)

        self.pane_raspi = tk.Frame(self.pane_window)
        self.frm_raspi = libframes.ControlFrame(self.pane_raspi)
        self.frm_raspi.grid(row=0, column=0, sticky=tk.NSEW)
        self.pane_raspi.grid_rowconfigure(0, weight=1)
        self.pane_raspi.grid_columnconfigure(0, weight=1)

        self.pane_tree = tk.Frame(self.pane_window)
        self.tree_songs = libtrees.AllSongTreeview(self.pane_tree)
        self.tree_artists = libtrees.ArtistsTreeview(self.pane_tree)
        self.tree_containers = libtrees.CManagerTreeview(self.pane_tree)
        self.tree_playlist = libtrees.PlaylistTreeview(self.pane_tree)
        self.bar_scroll_tree = tk.Scrollbar(self.pane_tree)

        self.bar_display = tk.Frame(self.pane_tree)
        self.lbl_name = tk.Label(self.bar_display)
        self.lbl_count = tk.Label(self.bar_display)
        self.btn_options = tkit.Mpi3TButton(self.bar_display)

        self.lbl_name.config(font=gui.font(20))
        self.lbl_count.config(font=gui.font(11))
        self.lbl_name.config(background='#FFFFFF')
        self.lbl_count.config(background='#FFFFFF')
        self.btn_options.config(text='...')
        self.btn_options.config(width=8)

        self.lbl_name.grid(row=0, column=0, sticky=tk.NS + tk.W)
        self.lbl_count.grid(row=1, column=0, sticky=tk.NS + tk.W)
        self.btn_options.grid(row=0, column=1, sticky=tk.NS + tk.E)

        self.lbl_name.grid(padx=10, pady=2)
        self.lbl_count.grid(padx=10, pady=0)
        self.btn_options.grid(padx=10, pady=5)
        self.btn_options.grid(rowspan=2)

        self.bar_display.config(height=80, bg='#FFFFFF')
        self.bar_display.grid_propagate(False)
        self.bar_display.grid_columnconfigure(1, weight=1)

        self.sep_tree = tk.Frame(self.pane_tree, bg='#000000', height=1)

        self.bar_display.grid(row=0, column=0, sticky=tk.NSEW)
        self.sep_tree.grid(row=1, column=0, sticky=tk.NSEW)
        self.tree_songs.grid(row=2, column=0, sticky=tk.NSEW)
        self.tree_artists.grid(row=2, column=0, sticky=tk.NSEW)
        self.tree_containers.grid(row=2, column=0, sticky=tk.NSEW)
        self.tree_playlist.grid(row=2, column=0, sticky=tk.NSEW)
        self.bar_scroll_tree.grid(row=2, column=1, sticky=tk.NS + tk.E)
        self.bar_display.grid(columnspan=2)
        self.sep_tree.grid(columnspan=2)

        self.tree_songs.grid_remove()
        self.tree_artists.grid_remove()
        self.tree_containers.grid_remove()
        self.tree_playlist.grid_remove()

        self.pane_tree.grid_rowconfigure(2, weight=1)
        self.pane_tree.grid_columnconfigure(0, weight=1)

        self.pane_window.add(self.pane_view)
        self.pane_window.config(sashwidth=3, bg='#666666')
        self.pane_window.paneconfig(self.pane_view, minsize=100)
        self.pane_window.paneconfig(self.pane_tree, minsize=200)
        self.pane_window.grid(sticky=tk.NSEW)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def save(self):
        schema = settings['TREEVIEWS']
        log = logging.getLogger('MPI3')

        log.info('Save Treeview: ALLSONGS')
        tree_rwidth, tree_columns = self.tree_songs.get_schema()
        schema['ALLSONGS']['ROOTWIDTH'] = tree_rwidth
        schema['ALLSONGS']['COLUMNS'] = tree_columns

        log.info('Save Treeview: ARTISTS')
        tree_rwidth, tree_columns = self.tree_artists.get_schema()
        schema['ARTISTS']['ROOTWIDTH'] = tree_rwidth
        schema['ARTISTS']['COLUMNS'] = tree_columns

        log.info('Save Treeview: CONTAINERS')
        tree_rwidth, tree_columns = self.tree_containers.get_schema()
        schema['CONTAINERS']['ROOTWIDTH'] = tree_rwidth
        schema['CONTAINERS']['COLUMNS'] = tree_columns

        log.info('Save Treeview: PLAYLISTS')
        tree_rwidth, tree_columns = self.tree_playlist.get_schema()
        schema['PLAYLISTS']['ROOTWIDTH'] = tree_rwidth
        schema['PLAYLISTS']['COLUMNS'] = tree_columns

        view_init = libinter.display_refresh.__name__
        if view_init == '<lambda>': view_init = self.tree_playlist.playlist
        log.info('{}: {}'.format('Save Last View', view_init))
        settings['PLAYBACK']['INITIALVIEW'] = view_init


def main_menu(frame):
    btn_file = tk.Menubutton(frame, text='File')
    btn_media = tk.Menubutton(frame, text='Media')
    btn_raspi = tk.Menubutton(frame, text='Raspi')

    btn_file.menu = tk.Menu(btn_file, tearoff=False)
    btn_file['menu'] = btn_file.menu
    lib = tk.Menu(btn_file, tearoff=False)
    lib.add_command(label='Export')
    lib.add_command(label='Import')
    lib.add_separator()
    lib.add_command(label='Create New')
    lib.add_command(label='Save Current')
    lib.add_separator()
    lib.add_command(label='Delete')

    lib.entryconfig(0, command=libinter.library_saveas)
    lib.entryconfig(1, command=libinter.library_load)
    lib.entryconfig(3, command=libinter.library_new)
    lib.entryconfig(4, command=libinter.library_save)
    lib.entryconfig(6, command=lambda: print('delete library'))

    proj = tk.Menu(btn_file.menu, tearoff=False)
    proj.add_command(label='Raspi')
    proj.add_command(label='Manager')

    proj.entryconfig(0, command=lambda: print('Raspi'))
    proj.entryconfig(1, command=lambda: print('Manager'))

    btn_file.menu.add_cascade(label='Library')
    btn_file.menu.add_separator()
    btn_file.menu.add_command(label='Audio Settings')
    btn_file.menu.add_separator()
    btn_file.menu.add_cascade(label='Interface')

    btn_file.menu.entryconfig(0, menu=lib)
    btn_file.menu.entryconfig(2, command=lambda: print('audio'))
    btn_file.menu.entryconfig(4, menu=proj)

    btn_media.menu = tk.Menu(btn_media, tearoff=False)
    btn_media['menu'] = btn_media.menu
    btn_media.menu.add_command(label='Download Songs')
    btn_media.menu.add_command(label='Import Songs')
    btn_media.menu.add_command(label='Import Playlists')

    btn_media.menu.entryconfig(0, command=libinter.download_songs)
    btn_media.menu.entryconfig(1, command=libinter.import_songs)
    btn_media.menu.entryconfig(2, command=libinter.import_playlists)

    btn_raspi.menu = tk.Menu(btn_raspi, tearoff=False)
    btn_raspi['menu'] = btn_raspi.menu

    mfont = gui.font(8)
    lib.config(font=mfont)
    proj.config(font=mfont)
    btn_file.config(font=mfont)
    btn_media.config(font=mfont)
    btn_file.menu.config(font=mfont)
    btn_raspi.menu.config(font=mfont)
    btn_media.menu.config(font=mfont)

    btn_file.config(bg='#000000', fg='#FFFFFF')
    btn_media.config(bg='#000000', fg='#FFFFFF')
    btn_raspi.config(bg='#000000', fg='#FFFFFF')

    btn_file.grid(row=0, column=0)
    btn_media.grid(row=0, column=1)
    btn_raspi.grid(row=0, column=2)
