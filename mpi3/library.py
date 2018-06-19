import math
import pydub
import mutagen
import string
import random
import urllib
import inspect
import plistlib
import datetime
from six.moves import cPickle
from . import exceptions


PID_PREFIX = {
    'MediaLibrary': 'L:',
    'RaspiLibrary': 'R:',
    'Playlist': 'P:',
    'Folder': 'F:',
    'Song': 'S:'
}


def generate_pid():
    clist = [c for c in string.ascii_uppercase] + [str(n) for n in range(10)]
    return ''.join(random.choices(clist, k=16))


def sanitize_pid(library_function):
    def sanitize(*args, **kwargs):
        lib = args[0]
        args = [lib[a] if isinstance(a, str) else a for a in args]
        for k, v in kwargs.items():
            kwargs[k] = lib[v] if isinstance(v, str) else v
        if inspect.isgeneratorfunction(library_function):
            yield from library_function(*args, **kwargs)
        else: return library_function(*args, **kwargs)
    return sanitize


class _Mpi3Element:

    def __repr__(self):
        return '<Mpi3 Element: {}(pid \'{}\', name \'{}\')>'.format(
            self.__class__.__name__, self.pid, self.name)

    def __init__(self):
        self.pid = None
        self.name = None
        self.added = None

    @classmethod
    def new(cls):
        try:
            new_element = cls()
            new_element.pid = PID_PREFIX[cls.__name__] + generate_pid()
            new_element.added = str(datetime.datetime.now())
            return new_element
        except KeyError:
            return None


class Mpi3Library(_Mpi3Element):

    def __repr__(self):
        return '<Mpi3 Object: {}(pid \'{}\', name \'{}\', path \'{}\')>'.format(
            self.__class__.__name__, self.pid, self.name, self._path)

    def __init__(self):
        _Mpi3Element.__init__(self)
        self._path = None
        self.folders = {}
        self.playlists = {}
        self.songs = {}

    def __getitem__(self, pid):
        for d in [self.folders, self.playlists, self.songs]:
            if pid in d.keys(): return d[pid]
        raise KeyError('PID Not Found: {}'.format(pid))

    def __setitem__(self, pid, element):
        self[pid] = element

    def __delitem__(self, pid):
        del self[pid]

    def __iter__(self):
        for d in [self.folders, self.playlists, self.songs]:
            for e in d.values(): yield e

    def __contains__(self, item):
        if isinstance(item, _Mpi3Element):
            return item in self
        elif isinstance(item, str):
            return item in [obj.pid for obj in self]
        else: return False

    def __len__(self):
        return len(self.folders) + len(self.playlists) + len(self.songs)

    @classmethod
    def open(cls, path):
        with open(path, 'rb') as f:
            open_lib = cPickle.load(f)
            if isinstance(open_lib, cls):
                open_lib._path = path
                return open_lib
        return None

    def load(self, path):
        with open(path, 'rb') as f:
            load_lib = cPickle.load(f)
            for attr in ['pid', 'name', 'added', 'songs', 'playlists', 'folders']:
                self.__dict__[attr] = getattr(load_lib, attr)
        self._path = path

    def save(self, path=None):
        if path: self._path = path
        with open(self._path, 'wb') as f:
            cPickle.dump(self, f)

    @property
    def path(self):
        return self._path

    def get(self, pid):
        return self[pid]

    def add_folder(self):
        fldr = Folder.new()
        name, count = 'New Folder', ''
        while name + str(count) in (f.name for f in self.folders.values()):
            if count == '': count = 1
            else: count += 1
        fldr.name = name + str(count)
        self.folders[fldr.pid] = fldr
        return fldr

    def add_playlist(self):
        plist = Playlist.new()
        name, count = 'New Playlist', ''
        while name + str(count) in (f.name for f in self.playlists.values()):
            if count == '': count = 1
            else: count += 1
        plist.name = name + str(count)
        self.playlists[plist.pid] = plist
        return plist

    def add_song(self):
        song = Song.new()
        self.songs[song.pid] = song
        return song

    @sanitize_pid
    def remove_folder(self, folder):
        def remove_children(parent):
            del self[parent.pid]
            for c in self.children(parent):
                remove_children(c)
        remove_children(folder)

    @sanitize_pid
    def remove_playlist(self, playlist):
        del self[playlist.pid]
        for f in self.folders.values():
            if playlist in f:
                f.remove(playlist)

    @sanitize_pid
    def remove_song(self, song):
        del self[song.pid]
        for p in self.playlists.values():
            if song in p:
                p.remove(song)

    @sanitize_pid
    def children(self, parent=None):
        if parent is None:
            for f in self.folders.values():
                if f.folder is None:
                    yield f
            for p in self.playlists.values():
                if p.folder is None:
                    yield p
        elif isinstance(parent, Folder):
            for f in self.folders.values():
                if f.folder == parent.pid:
                    yield f
            for p in self.playlists.values():
                if p.folder == parent.pid:
                    yield p
        elif isinstance(parent, Playlist):
            for s in parent.songs:
                yield self[s]
        else:
            err = 'Non-container element {}'.format(parent)
            raise ValueError(err)

    def artists(self):
        for artist in set([
            s.artist for s in self.songs.values()
        ]): yield artist


class MediaLibrary(Mpi3Library):

    def __init__(self):
        Mpi3Library.__init__(self)

    def import_playlist(self, path):
        itunes_plist = ItunesPlaylist()
        itunes_plist.import_xml(path)
        plist = itunes_plist.get_playlist()

        if plist.pid in self.playlists.keys():
            raise exceptions.DuplicatePIDError(plist.pid)

        for song in itunes_plist.get_songs():
            if song.pid not in self.songs.keys():
                self.songs[song.pid] = song

        self.playlists[plist.pid] = plist
        return plist

    def add_song(self, path=None):
        song = super().add_song()

        if not path: return song

        afm = AudioFileMeta(path)
        song.path = path
        song.size, song.name, ext = afm.meta_path()
        song.sample, song.time = afm.meta_playback()
        song.artist, song.album, song.kind = '', '', ''

        self.songs[song.pid] = song
        return song

    @sanitize_pid
    def song_edit(self, song, attrib, value):
        song[attrib] = value
        # afm = AudioFileMeta(song.path)
        # b,s,l = afm.get_playback_info()
        # print(b,s,l)
        # afm.get_tag('title')
        # afm.get_tag('artist')
        # afm.get_all()
        # afm.set_tag('title', 'You_re somebody else')


class RaspiLibrary(Mpi3Library):

    def __init__(self):
        Mpi3Library.__init__(self)


class Folder(_Mpi3Element):

    def __init__(self):
        _Mpi3Element.__init__(self)
        self.folder = None
        self.playlists = []

    def __len__(self):
        return len(self.playlists)

    def __iter__(self):
        for p in self.playlists: yield p

    def add(self, playlist):
        if hasattr(playlist, 'pid'):
            self.playlists.append(playlist.pid)
        else: self.playlists.append(playlist)

    def remove(self, playlist):
        if hasattr(playlist, 'pid'):
            self.playlists.remove(playlist.pid)
        else: self.playlists.remove(playlist)


class Playlist(_Mpi3Element):

    def __init__(self):
        _Mpi3Element.__init__(self)
        self.folder = None
        self.created = None
        self.songs = []

    def __len__(self):
        return len(self.songs)

    def __iter__(self):
        for s in self.songs: yield s

    def add(self, song):
        if hasattr(song, 'pid'):
            self.songs.append(song.pid)
        else: self.songs.append(song)

    def remove(self, song):
        if hasattr(song, 'pid'):
            self.songs.remove(song.pid)
        else: self.songs.remove(song)


class Song(_Mpi3Element):

    def __init__(self):
        _Mpi3Element.__init__(self)
        self.sample = None
        self.artist = None
        self.album = None
        self.time = None
        self.path = None
        self.kind = None
        self.size = None
        self.bit = None

    @property
    def f_size(self):
        size_bytes = int(self.size)
        if size_bytes == 0: return '0B'
        size_name = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    @property
    def f_time(self):
        seconds = round(int(self.time) / 1000)
        m, s = divmod(seconds, 60)
        return '%2d:%02d' % (m, s)


class ItunesPlaylist:

    def __repr__(self):
        c, x = self.__class__.__name__, self.data
        return '<{} (\'{}\')>'.format(c, x)

    def __init__(self):
        self.data = None

    def import_xml(self, path):
        try:
            with open(path, 'rb') as xml_path:
                self.data = plistlib.load(xml_path, fmt=plistlib.FMT_XML)
        except plistlib.InvalidFileException:
            raise exceptions.XmlImportError(path)

    def get_songs(self):
        for trackid, attribs in self.data['Tracks'].items():
            s = Song()

            pid = attribs.get('Persistent ID')
            s.pid = PID_PREFIX[s.__class__.__name__] + pid
            s.name = attribs.get('Name')
            s.artist = attribs.get('Artist')
            s.album = attribs.get('Album')
            s.time = attribs.get('Total Time')
            s.added = attribs.get('Date Added')
            s.kind = attribs.get('Kind')
            s.size = attribs.get('Size')
            s.sample = attribs.get('Sample Rate')
            s.bit = attribs.get('Bit Rate')
            s.path = urllib.parse.unquote(
                urllib.parse.urlparse(attribs.get('Location')).path[1:])

            yield s

    def get_playlist(self):
        p = Playlist()

        for attribs in self.data['Playlists']:
            pid = attribs.get('Playlist Persistent ID')
            p.pid = PID_PREFIX[p.__class__.__name__] + pid
            p.name = attribs.get('Name')

            for ids in attribs.get('Playlist Items'):
                for trackid, attribs in self.data['Tracks'].items():
                    if trackid == str(ids['Track ID']):
                        pid = attribs.get('Persistent ID')
                        p.songs.append(PID_PREFIX['Song'] + pid)

        return p


class AudioFileMeta:

    def __repr__(self):
        c, p = self.__class__.__name__, self.path
        return '<{} (\'{}\')>'.format(c, p)

    def __init__(self, path):
        self.tag_dir = {
            'title': 'TIT2',
            'artist': 'TPE1',
            'album': 'TALB',
            'genre': 'TCON',
            'year': 'TDRC',
            'track': 'TRCK',
            'misc': 'TXXX'
        }

        self.path = path
        self.meta = mutagen.File(self.path)

    def tag_get(self, tag):
        return self.meta.get(self.tag_dir[tag])

    def tag_get_all(self):
        for key in self.meta:
            return key, self.meta[key]

    def tag_set(self, tag, text):
        try:
            tags = id3.ID3(self.path)
        except id3.ID3NoHeaderError:
            tags = id3.ID3()

        id3_tag = self.tag_dir[tag]
        id3_class = getattr(id3, id3_tag)
        tags[id3_tag] = id3_class(encoding=3, text=text)
        tags.save(self.path)

    def meta_playback(self):
        seg = pydub.AudioSegment.from_file(self.path, 'mp3')
        return seg.frame_rate, len(seg)

    def meta_path(self):
        fname = os.path.basename(path)
        name, ext = os.path.splitext(fname)
        size = os.stat(path).st_size
        return size, name, ext
