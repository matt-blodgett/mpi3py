from tkinter import filedialog as ask
from tkinter import messagebox as msg
from mpi3pc.util import fileutil
from mpi3 import exceptions
from mpi3 import medialib
from mpi3 import library


def display_refresh():
    pass


def system_refresh(control_function):
    def refresh(*args, **kwargs):
        control_function(*args, **kwargs)
        display_refresh()
    return refresh


@system_refresh
def object_edit(pid, attrib, value):
    setattr(medialib[pid], attrib, value)


@system_refresh
def object_delete(pids):
    del_folders = []
    del_plists = []
    del_songs = []

    for pid in pids:
        obj = medialib[pid]
        if isinstance(obj, library.Folder):
            del_folders.append(obj)

        elif isinstance(obj, library.Playlist):
            del_plists.append(obj)

        elif isinstance(obj, library.Song):
            del_songs.append(obj)

    title = 'Confirm Deletion'
    m = 'Confirm deletion of: \n\n'
    f_count = len(del_folders)
    p_count = len(del_plists)
    s_count = len(del_songs)

    if f_count > 0:
        plural = 's \n' if f_count > 1 else '\n'
        m = str(f_count) + ' folder' + plural

    if p_count > 0:
        plural = 's \n' if p_count > 1 else '\n'
        m = str(p_count) + ' playlist' + plural

    if s_count > 0:
        plural = 's \n' if s_count > 1 else '\n'
        m = str(s_count) + ' song' + plural

    if f_count > 0 and p_count + s_count == 0:
        for f in del_folders:
            if len(medialib[f]) == 0:
                medialib.remove_folder(f)
                del_folders.remove(f)

    del_ct = (p_count + s_count + len(del_folders))
    if del_ct > 0 and msg.askyesno(title=title, icon='warning', message=m):
        for f in del_folders:
            medialib.remove_folder(f)
        for p in del_plists:
            medialib.remove_playlist(p)
        for s in del_songs:
            medialib.remove_song(s)


@system_refresh
def import_playlists(join_folder=None):
    import_paths = ask.askopenfilenames(
        title='Import Itunes Playlist',
        initialdir=fileutil.path_desktop(),
        filetypes=(('XML Files', '*.xml'),))

    playlist = None
    imported_playlists = []

    for path in list(import_paths):
        title = 'Import Error'

        try:
            playlist = medialib.import_playlist(path)
            playlist.folder = join_folder

        except exceptions.DuplicatePIDError as e:

            playlist = medialib[str(e)]
            if playlist:
                m = ('Playlist: \n' + playlist.name + '\n\n' +
                     'From file: \n' + path + '\n\n' +
                     'Has already been imported to the library \n' +
                     'Overwrite the existing playlist?')

                if msg.askyesno(title=title, icon='warning', message=m):
                    folder = playlist.folder
                    medialib.remove_playlist(playlist)
                    medialib.import_playlist(path, folder)

        except exceptions.XmlImportError:
            m = ('The file: \n' + path + '\n' +
                 'Did not contain a valid iTunes playlist!')
            msg.showerror(title=title, message=m)

        finally:
            if playlist:
                imported_playlists.append(playlist)
                playlist = None

    # if imported_playlists:
    #     songs = []
    #     for plist in imported_playlists:
    #         for song_pid in plist:
    #             song_obj = medialib[song_pid]
    #             if song_obj not in songs:
    #                 songs.append(song_obj)
    #
    #     local_path = settings['PATHS']['MEDIA']
    #     move_songs = list(fileutil.path_check_local(songs, local_path))
    #     if move_songs: fileflow.ImportFiles(move_songs)


@system_refresh
def import_songs(playlist=None):
    pass
    # import_paths = ask.askopenfilenames(
    #     title='Import Audio Files',
    #     initialdir=fileutil.path_desktop(),
    #     filetypes=(('MP3 Files', '*.mp3'), ('All Files', '*.*')))
    #
    # songs = []
    # for path in list(import_paths):
    #     song = medialib.song_add(path)
    #     songs.append(song)
    #     if playlist is not None: playlist.append(song)
    #
    # local_path = settings['PATHS']['MEDIA']
    # move_songs = list(fileutil.path_check_local(songs, local_path))
    # if move_songs: fileflow.ImportFiles(move_songs)


@system_refresh
def download_songs():
    ytflow.PytubeInterface()


@system_refresh
def folder_add(join_folder=None):
    new_folder = medialib.add_folder()
    new_folder.folder = join_folder


@system_refresh
def folder_move_to(obj_pid, join_folder=None):
    medialib[obj_pid].folder = join_folder


@system_refresh
def playlist_add(join_folder=None):
    new_playlist = medialib.add_playlist()
    new_playlist.folder = join_folder


@system_refresh
def playlist_add_to(playlist_pid, songs):
    plist = medialib[playlist_pid]

    for song in songs:
        if song not in plist:
            plist.append(song)
        else:
            s = medialib[song]
            t = 'Duplicate Error'
            m = (s.name + '\n' + s.artist + '\n\n' +
                 'Already exists in playlist: \n' + plist.name)
            msg.showerror(title=t, message=m)


@system_refresh
def playlist_remove_from(playlist_pid, songs):
    plist = medialib[playlist_pid]

    for song in songs:
        plist.remove(song)


@system_refresh
def playlist_order(playlist_pid, move_pids, move_to_pid):
    playlist = medialib[playlist_pid]

    for pid in move_pids:
        playlist.songs.remove(pid)

    for pid in move_pids:
        move_to_index = playlist.songs.index(move_to_pid)
        playlist.songs.insert(move_to_index, pid)


@system_refresh
def playlist_duplicate(playlist_pid):
    plist = medialib[playlist_pid]

    copies = 1
    while plist.name + str(copies) in [p.name for p in medialib.playlists.values()]:
        copies += 1

    playlist = medialib.add_playlist()
    playlist.name = plist.name + str(copies)
    playlist.folder = plist.folder
    playlist.songs = [s for s in plist.songs]


@system_refresh
def library_new():
    pass
    # xml_path = ask.asksaveasfilename(
    #     title='New Library',
    #     initialdir='profile',
    #     filetypes=(('XML Files', '*.xml'),))
    #
    # if xml_path != '':
    #     if not xml_path.endswith('.xml'): xml_path += '.xml'
    #     medialib.folders = medialib.playlists = medialib.songs = []
    #     medialib.save(xml_path)
    #     info = 'Library successfully created: \n' + xml_path
    #     msg.showinfo('Success', info)


@system_refresh
def library_load():
    pass
    # xml_path = ask.askopenfilename(
    #     title='Load Library',
    #     initialdir='profile',
    #     filetypes=(('XML Files', '*.xml'),))
    #
    # if xml_path != '':
    #
    #     try:
    #         medialib.open(xml_path)
    #         info = 'Library successfully loaded from: \n' + xml_path
    #         msg.showinfo('Success', info)
    #
    #     except exceptions.XmlImportError:
    #         info = 'Bad library file: \n' + xml_path
    #         msg.showinfo('Bad file', info)


def library_save():
    m = 'Save and overwrite current library file?'
    if msg.askyesno(title='Confirm Save', message=m):
        medialib.save()


def library_saveas():
    pass


@system_refresh
def library_sync():
    pass
