import os
import math


def path_desktop():
    env = os.path.join(os.environ['USERPROFILE'])
    return os.path.abspath(os.path.join(env, 'Desktop'))


def path_walk(path, files_only=False):
    validate = os.path.isfile if files_only else os.path.isdir
    try:
        for sub_path in os.listdir(path):
            p = os.path.join(path, sub_path)
            if validate(p): yield p
    except PermissionError: pass
    except FileNotFoundError: pass


def path_search(path, search):
    for p in path_walk(path):
        path_test = '{}/{}'.format(p, search)
        if os.path.exists(path_test):
            yield os.path.abspath(path_test)
        yield from path_search(p, search)


def path_show_explorer(path):
    pipe = r'explorer /select,' + os.path.abspath(path)
    os.system(pipe)


def file_copy(srce, dest, update=None, length=(16*1024)):
    with open(srce, 'rb') as sfile, open(dest, 'wb') as dfile:
        copied = 0
        while True:
            buf = sfile.read(length)
            if not buf: break
            dfile.write(buf)
            copied += len(buf)
            if update: update((len(buf), copied))


def file_delete(path):
    print(path)
    #    try:
    #        os.remove(path)
    #    except FileNotFoundError as e:
    #        print(e)


def file_size(path):
    return os.stat(path).st_size


def file_size_format(size_bytes):
    if size_bytes == 0: return '0B'
    size_name = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def file_info(path):
    fname = os.path.basename(path)
    name, ext = os.path.splitext(fname)
    size = os.stat(path).st_size
    return size, name, ext


#
# create hidden file
# fn = 'E:\\test.txt'
#     open(fn, 'w')
#     os.popen('attrib +h ' + fn)


#
#
# PUT THIS SHIT SOMEWHERE ELSE
#
#
def path_check_local(songs, local_path):
    for song in songs:
        loc_path = path_song_local(song, local_path)
        if not os.path.exists(loc_path):
            yield song


def path_song_local(song, local_path):
    ext = os.path.splitext(song.path)[1]
    p = local_path
    a = song.artist.rstrip() if song.artist != '' else '.Unassigned'
    f = song.name + ext
    return '{}/{}/{}'.format(p, a, f)


def path_song_local_dir(song, local_path):
    p = local_path
    a = song.artist.rstrip() if song.artist != '' else '.Unassigned'
    dest_path = p + '/' + a
    return dest_path
