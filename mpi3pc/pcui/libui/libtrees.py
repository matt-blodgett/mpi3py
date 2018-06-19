import tkinter as tk
from mpi3pc.control import libinter
from mpi3 import settings
from mpi3 import medialib
from mpi3 import library
from mpi3 import playback
from mpi3pc import gui


class BaseTreeview(gui.tkit.MediaTreeview):

    def __init__(self, master):
        gui.tkit.MediaTreeview.__init__(self, master)
        self.config(style=gui.MPI3_TREEVIEW_MEDIA)
        self._rclick_menu = MediaMenu(self)

    def pid_to_iids(self, pid):
        for row in self.get_children():
            if self.item(row)['tags'][0] == pid:
                yield row


class SongTreeview(BaseTreeview):

    def __init__(self, master):
        BaseTreeview.__init__(self, master)

        self.songlist = []

        self._curr_sort = (self.column('#0'), False)
        self.cmd_dbl_click = self.play_select
        self._box_popup.update_command = self.edit_song

    def play_select(self, event=None):
        if len(self.selection()) == 1:
            playback.play(self.songlist, medialib[self.selected_pid()])

    def set_songlist(self, songlist):
        self.songlist = songlist
        self.sort((None, None))

    def tree_items(self):
        self.delete(*self.get_children())
        for index, song in enumerate(self.songlist):
            v = (song.name, song.artist, song.album, song.f_time,
                 song.f_size, song.added, song.path)
            self.insert('', tk.END, text=str(index+1),
                        values=v, tags=(song.pid, str(index % 2)))
        self.tag_configure('1', background='#EDEDED')

    def select_action(self, event):
        if len(self.selection()) > 1:
            ct = str(len(self.selection()))
            ddrop_text = '   ' + ct + ' songs'
        else:
            ddrop_text = self.item(self.selection()[0])['values'][0]
        self._drag_drop.set_text(ddrop_text)

    def drag_action(self, event):
        self._drag_drop.move((event.x, event.y))

    def drop_action(self, event):
        pass

    def edit_song(self):
        row, col = self._box_popup.cell
        item = self.item(row)
        pid = item['tags'][0]
        if col in ['name', 'artist', 'album']:
            libinter.object_edit(pid, col, self.set(row, col))

    def edit_cell(self, cell):
        row, col = cell
        cid = self.column(col)['id']
        if cid in ['name', 'artist', 'album']:
            self._box_popup.popup(cell)

    def edit_cell_next(self, event):
        row, col = self._box_popup.cell
        cid = self.column(col)['id']

        ind_list = [
            self['displaycolumns'].index(c)
            for c in self['displaycolumns']
            if c in ['name', 'artist', 'album'] and c != cid
        ]

        c_ind = self['displaycolumns'].index(cid)
        e_cols = [*filter(lambda x: x > c_ind, ind_list)]

        if len(e_cols) > 0:
            c = self.column(self['displaycolumns'][e_cols[0]])
            self.edit_cell((row, c['id']))
        else:
            e_cols = [*filter(lambda x: x < c_ind, ind_list)]
            if len(e_cols) > 0:
                c = self.column(self['displaycolumns'][e_cols[0]])
                self.edit_cell((row, c['id']))

        return 'break'

    def sort(self, sort_column):
        curr_sort_column, reverse = self._curr_sort

        if not sort_column:
            sort_column = curr_sort_column
        elif sort_column == curr_sort_column:
            reverse = not reverse

        # sort_on = lambda tag: (sort_column == self.column(tag))
        # sort_list = lambda k: self.songlist.sort(key=k, reverse=reverse)
        #
        # if sort_on('#0'): sort_list(lambda s: self.songlist.index(s))
        # elif sort_on('name'): sort_list(lambda s: s.name)
        # elif sort_on('artist'): sort_list(lambda s: s.artist)
        # elif sort_on('album'): sort_list(lambda s: s.album)
        # elif sort_on('time'): sort_list(lambda s: int(s.time))
        # elif sort_on('size'): sort_list(lambda s: int(s.size))

        self._curr_sort = sort_column, reverse
        self.tree_items()


class AllSongTreeview(SongTreeview):

    def __init__(self, master):
        SongTreeview.__init__(self, master)
        column_schema = settings['TREEVIEWS']['ALLSONGS']['COLUMNS']
        self._columns_init(column_schema, 40)
        self['show'] = 'headings'

    def refresh(self):
        self.set_songlist(medialib.songs.values())
        self._box_popup.hide()
        return 'Song Library', len(medialib.songs), ' Song'


class PlaylistTreeview(SongTreeview):

    def __init__(self, master):
        SongTreeview.__init__(self, master)
        column_schema = settings['TREEVIEWS']['PLAYLISTS']['COLUMNS']
        self._columns_init(column_schema, 40)
        self.heading('#0', text='#')

        self._last_b1_row = None
        self.cmd_dbl_click = self.play_select
        self.playlist = None

    def select_action(self, event):
        if len(self.selection()) == 1:
            song_pos = self.item(self.selection()[0])['text']
            song_name = self.item(self.selection()[0])['values'][0]
            ddrop_text = song_pos + '. ' + song_name
        else:
            ddrop_text = '...'

        self._drag_drop.set_text(ddrop_text)

    def drag_action(self, event):
        self._drag_drop.move((event.x, event.y))

        row = self.identify_row(event.y)
        col = self.identify_column(event.x)

        if not self._last_b1_row == row:
            self._last_b1_row = row
            if self._curr_sort[0]['id'] == '':
                try:
                    self._drag_pos.drag_row(self.bbox(row, col)[1])
                except ValueError:
                    pass

    def drop_action(self, event):
        row = self.identify_row(event.y)
        # col = self.identify_column(event.x)

        if self._curr_sort[0] == self.column('#0'):
            move = list(self.selected_pids())
            move_to = self.item(row, 'tags')[0]
            libinter.playlist_order(self.playlist.pid, move, move_to)

    def set_playlist(self, pid):
        self.playlist = medialib[pid]

    def refresh(self):
        self._box_popup.hide()
        songs = list(medialib.children(self.playlist))
        self.set_songlist(songs)
        return self.playlist.name, len(self.playlist), ' Song'


class ArtistsTreeview(BaseTreeview):

    def __init__(self, master):
        BaseTreeview.__init__(self, master)
        column_schema = settings['TREEVIEWS']['ARTISTS']['COLUMNS']
        self._columns_init(column_schema, 200)
        self.heading('#0', text='Name')

    def refresh(self):
        self._box_popup.hide()
        self.delete(*self.get_children())

        artists = list(medialib.artists())
        artists.sort()

        for artist in artists:
            index = artists.index(artist)
            atag = 'a' + str(index % 2)
            iid = self._append_artist(artist, atag)
            for pos, song in enumerate(medialib.songs.values()):
                if song.artist == artist:
                    stag = 's' + str(pos % 2)
                    self._append_song(song, stag, iid)
                pos += 1

        self.tag_configure('a0', background='#ADADAD')
        self.tag_configure('a1', background='#CCCCCC')
        self.tag_configure('s0', background='#F4F4F4')
        self.tag_configure('s1', background='#FFFFFF')

        return 'Artists', len(artists), ' Artist'

    def _append_artist(self, artist, tag):
        t = (artist, tag)
        o = artist in self.opened
        return self.insert('', tk.END, open=o, text=artist, tags=t)

    def _append_song(self, song, tag, iid):
        t = (song.pid, tag)
        val = (song.f_time, song.f_size, song.added)
        return self.insert(iid, tk.END, text=song.name, tags=t, values=val)


class ContainersTreeview(BaseTreeview):

    def __init__(self, master):
        BaseTreeview.__init__(self, master)
        self._box_popup.update_command = self.edit_container
        self._icn_folder = tk.PhotoImage(file=gui.icon('folder'))
        self._icn_playlist = tk.PhotoImage(file=gui.icon('playlist'))

    def select_action(self, event):
        name = self.item(self.selection()[0], 'text')
        self._drag_drop.set_text(name)

    def drag_action(self, event):
        self._drag_drop.move((event.x, event.y))

    def drop_action(self, event):
        pass

    def edit_container(self):
        row, col = self._box_popup.cell
        item = self.item(row)
        pid = item['tags'][0]
        libinter.object_edit(pid, 'name', self.item(row)['text'])

    def edit_cell(self, cell):
        if cell[1] == '': self._box_popup.popup(cell)

    def edit_cell_next(self, event):
        row, col = self._box_popup.cell
        r_next = self.next(row)

        if r_next:
            self.edit_cell((r_next, ''))
            return 'break'
        elif len(self.get_children(self.parent(row))) > 1:
            r_first = self.get_children(self.parent(row))[0]
            self.edit_cell((r_first, ''))
            return 'break'
        else:
            self._box_popup.hide()

    def selected_pid_playlist(self):
        plist = medialib[self.selected_pid()]
        if isinstance(plist, library.Playlist):
            return plist.pid
        return None

    def refresh(self):
        self._box_popup.hide()
        self.delete(*self.get_children())

        for container in medialib.children():
            if isinstance(container, library.Folder):
                f = self._append_folder('', container)
                self._tree_folders(f, container)
            else: self._append_playlist('', container)

        return 'Playlists', len(medialib.playlists), ' Playlist'

    def _tree_folders(self, iid, parent):
        for child in medialib.children(parent):
            if isinstance(child, library.Playlist):
                self._append_playlist(iid, child)
        for child in medialib.children(parent):
            if isinstance(child, library.Folder):
                f = self._append_folder(iid, child)
                self._tree_folders(f, child)

    def _append_folder(self, iid, fldr):
        o = fldr.pid in self.opened
        item = self.insert(
            iid, tk.END, text=fldr.name,
            open=o, tags=fldr.pid,
            image=self._icn_folder)
        return item

    def _append_playlist(self, iid, plist):
        v = (len(plist), plist.created)
        self.insert(
            iid, tk.END, text=plist.name,
            values=v, tags=plist.pid,
            image=self._icn_playlist)


class CManagerTreeview(ContainersTreeview):

    def __init__(self, master):
        ContainersTreeview.__init__(self, master)
        column_schema = settings['TREEVIEWS']['CONTAINERS']['COLUMNS']
        self._columns_init(column_schema, 200)
        self.heading('#0', text='Name')

    def refresh(self):
        display = super().refresh()

        # strength = 1
        # for fldr in medialib.folders.values():
        #     parent_ct = len(list(medialib.folder_parents(fldr)))
        #     if parent_ct > strength: strength = parent_ct
        #
        # for fldr in medialib.folders:
        #     depth = len(list(medialib.folder_parents(fldr)))
        #     colour = gui.tkpil.mix_hex('#777777', '#919191', strength, depth)
        #     self.tag_configure(fldr.pid, font=gui.font(9, 'bold'),
        #                        background=colour, foreground='#FFFFFF')

        return display


class CSidebarTreeview(ContainersTreeview):

    def __init__(self, master):
        ContainersTreeview.__init__(self, master)
        self.config(style=gui.MPI3_TREEVIEW_SIDEBAR)
        self.heading('#0', text='Playlists', anchor=tk.W)


class CSyncTreeview(ContainersTreeview):

    def __init__(self, master):
        ContainersTreeview.__init__(self, master)
        self.config(style=gui.MPI3_TREEVIEW_TOGGLE)
        self.heading('#0', text='Library Media', anchor=tk.W)
        self.column('#0', width=280)
        self['selectmode'] = 'browse'
        self['height'] = 10

        self._checkboxes = []

        self.bind('<MouseWheel>', self._on_scroll)
        self.bind('<Configure>', self._checkboxes_reset, add=True)
        self.bind('<ButtonRelease-1>', self._checkboxes_reset, add=True)
        self.unbind('<ButtonPress-3>')

    def select_action(self, event):
        pass

    def drag_action(self, event):
        pass

    def drop_action(self, event):
        pass

    def _on_scroll(self, event):
        allow = super()._on_scroll(event)
        self._checkboxes_reset()
        return allow

    def yview(self, *args):
        super().yview(*args)
        self._checkboxes_reset()

    def refresh(self):
        super().refresh()
        self._checkboxes_reset()

    def _checkbox_get(self):
        cbx = tk.ttk.Checkbutton(self)
        cbx.config(style=gui.MPI3_CHECKBUTTON_TREE)
        cbx.var = tk.BooleanVar(cbx)
        cbx.config(variable=cbx.var)
        cbx.var.set(True)
        self._checkboxes.append(cbx)
        return cbx

    def _checkboxes_reset(self, event=None):

        for cbx in self._checkboxes:
            cbx.destroy()

        self._checkboxes = []

        def place_box(iid, offset):
            x, y, w, h = self.bbox(iid)
            x += offset * 6
            pid = self.item(iid, 'tags')[0]
            if offset > 0 and isinstance(medialib[pid], library.Playlist):
                x += 14
            cbx = self._checkbox_get()
            cbx.place(x=x, y=y)

        def recursive_place(parent, depth=1):
            for child in self.get_children(parent):
                if self.bbox(child):
                    place_box(child, depth)
                recursive_place(child, depth+1)

        for row in self.get_children():
            if self.bbox(row):
                place_box(row, 0)
            recursive_place(row)

        # print('')
        #
        # visible = [c for c in self.get_children() if self.bbox(c)]
        # print(len(visible))
        # print(len(self.checkboxes))

        # print(len(self.children))


class MediaMenu(tk.Menu):

    def __init__(self, master):
        tk.Menu.__init__(self, master)
        self.config(tearoff=False)
        self.config(font=gui.font(9))

        self.event = None

    def add_cmd(self, label, command):
        self.add_command(label=label, command=command)

    def add_casc(self, label, menu):
        self.add_cascade(label=label, menu=menu)

    def setup(self, event):
        self.event = event
        self.delete(0, tk.END)

        region_id = self.master.identify_region(event.x, event.y)
        column_id = self.master.identify_column(event.x)
        column = self.master.column(column_id)['id']

        is_empty_space = ((column == 'fill') and (region_id == 'nothing'))

        add_del = True
        if region_id == 'heading':
            self._header_menu()
            add_del = False

        elif not is_empty_space and region_id in ['cell', 'tree']:

            if isinstance(self.master, SongTreeview):
                self._song_menu()

            if isinstance(self.master, ArtistsTreeview):
                self._artist_menu()

            if isinstance(self.master, PlaylistTreeview):
                self._playlist_menu()

            if isinstance(self.master, ContainersTreeview):
                self._containers_menu()

        else:

            add_del = False
            if isinstance(self.master, SongTreeview):
                self._song_menu_persistent()

            if isinstance(self.master, ContainersTreeview):
                self._containers_menu_persistent()

        if add_del:
            obj_del = self._obj_del
            if isinstance(self.master, ArtistsTreeview):
                obj_del = self._obj_del_artist
            self.add_cmd('Remove from Library', obj_del)

        self.tk_popup(event.x_root, event.y_root)

    def _song_menu(self):
        add_to_menu = tk.Menu(self, tearoff=False)

        curr_playlist = None
        if hasattr(self.master, 'playlist'):
            curr_playlist = self.master.playlist.pid

        for playlist in medialib.playlists.values():
            if playlist.pid != curr_playlist:
                cmd = lambda p=playlist.pid: self._song_add_to(p)
                add_to_menu.add_command(label=playlist.name, command=cmd)

        self.add_cmd('Play', self._song_play)
        self.add_cmd('Rename', self._object_rename)
        self.add_cmd('Details', self._object_details)
        self.add_casc('Add to...', add_to_menu)
        self.add_separator()
        self._song_menu_persistent()
        self.add_separator()

    def _song_menu_persistent(self):
        self.add_cmd('Import Songs', self._song_add)

    def _artist_menu(self):

        try:
            s = medialib[self._get_sel_pid()]
        except KeyError:
            self._expand_collapse()
            self.add_separator()

        self._song_menu_persistent()
        self.add_separator()

    def _playlist_menu(self):
        self.add_cmd('Remove from Playlist', self._playlist_remove_song)
        self.add_separator()

    def _containers_menu(self):
        self._containers_menu_persistent()
        self.add_separator()

        move_to_menu = tk.Menu(self, tearoff=False)
        sel_obj = medialib[self._get_sel_pid()]

        if sel_obj.folder:
            cmd = lambda o=sel_obj.pid, f=None: self._obj_move_to(o, f)
            move_to_menu.add_command(label='Library', command=cmd)

        if isinstance(sel_obj, library.Playlist):
            for fldr in medialib.folders.values():

                if not fldr.pid == sel_obj.folder:
                    cmd = lambda o=sel_obj.pid, f=fldr.pid: (
                        self._obj_move_to(o, f))

                    move_to_menu.add_command(
                        label=fldr.name, command=cmd)

        elif isinstance(sel_obj, library.Folder):
            for fldr in medialib.folders.values():

                in_tree = False
                for child_fldr in medialib.children(sel_obj):
                    if fldr.pid == child_fldr.pid: in_tree = True
                is_sel = (fldr.pid == sel_obj.pid)
                is_parent = (fldr.pid == sel_obj.folder)

                if not in_tree and not is_sel and not is_parent:
                    cmd = lambda o=sel_obj.pid, f=fldr.pid: (
                        self._obj_move_to(o, f))

                    move_to_menu.add_command(
                        label=fldr.name, command=cmd)

        self.add_casc('Move to...', move_to_menu)
        if isinstance(sel_obj, library.Playlist):
            self.add_cmd('Duplicate', self._obj_duplicate)
        self.add_cmd('Rename', self._object_rename)
        self.add_cmd('Details', self._object_details)
        self.add_separator()

    def _containers_menu_persistent(self):
        self._expand_collapse()
        self.add_separator()
        self.add_cmd('Add Folder', self._add_folder)
        self.add_cmd('Add Playlist', self._add_playlist)
        self.add_cmd('Import Playlists', self._import_playlists)

    def _expand_collapse(self):
        self.add_cmd('Expand All', self._expand_all)
        self.add_cmd('Collapse All', self._collapse_all)

    def _expand_all(self):
        self.master.set_open(True)

    def _collapse_all(self):
        self.master.set_open(False)
        self.master.opened = []

    @staticmethod
    def _object_details():
        print('sdet')

    def _object_rename(self):
        row = self.master.selection()[0]
        col = self.master.identify_column(self.event.x)
        self.master.edit_cell((row, col))

    def _song_play(self):
        self.master.play_select()

    def _song_add(self):
        playlist = None
        if hasattr(self.master, 'playlist'):
            playlist = self.master.playlist

        libinter.import_songs(playlist)

    @staticmethod
    def _song_edit():
        print('edit song')

    def _song_add_to(self, playlist_pid):
        libinter.playlist_add_to(
            playlist_pid, self.master.selected_pids())

    def _playlist_remove_song(self):
        libinter.playlist_remove_from(
            self.master.playlist.pid, self.master.selected_pids())

    @staticmethod
    def _obj_edit():
        print('edit container')

    @staticmethod
    def _obj_move_to(move_obj_pid, move_to_pid):
        libinter.folder_move_to(move_obj_pid, move_to_pid)

    def _obj_duplicate(self):
        libinter.playlist_duplicate(self._get_sel_pid())

    def _add_folder(self):
        libinter.folder_add(self._get_join_folder())

    def _add_playlist(self):
        libinter.playlist_add(self._get_join_folder())

    def _import_playlists(self):
        libinter.import_playlists(self._get_join_folder())

    def _get_join_folder(self):
        pid = self._get_sel_pid()

        if not pid: return None

        obj = medialib[pid]
        if isinstance(obj, library.Playlist):
            pid = obj.folder
        if pid not in self.master.opened:
            self.master.opened.append(pid)
        return pid

    def _get_sel_pid(self):
        rid = self.master.identify_region(self.event.x, self.event.y)
        if rid == 'nothing': return None
        return list(self.master.selected_pids())[0]

    def _obj_del_artist(self):
        for artist in self.master.get_children():
            if artist in self.master.selection():
                self.master.selection_remove(artist)
                for song in self.master.get_children(artist):
                    self.master.selection_add(song)
        libinter.object_delete(self.master.selected_pids())

    def _obj_del(self):
        libinter.object_delete(self.master.selected_pids())

    def _header_menu(self):
        self.var_list = []
        for c in self.master.column_schema:
            if c['id'] != 'fill':
                name = c['heading']
                tk_var = tk.BooleanVar()
                tk_var.set(c['visible'])
                self.var_list.append(tk_var)
                cmd = lambda col=c: self._toggle_col(col)
                self.add_checkbutton(label=name, variable=tk_var, command=cmd)

    def _toggle_col(self, col):
        vis = not col['visible']
        self.master.columns_setvis([col['id']], vis)
        self.tk_popup(self.event.x_root, self.event.y_root)
