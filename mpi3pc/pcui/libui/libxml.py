# from xml.etree import ElementTree as et
# from xml.dom import minidom


# @system_refresh
# def library_xml_import(xml_path):
#     try:
#         with open(xml_path, 'r') as xml_file:
#             xml_str = xml_file.read()
#             lib_meta = et.fromstring(xml_str)
#     except FileNotFoundError:
#         raise exceptions.XmlImportError(xml_path)
#     except et.ParseError:
#         raise exceptions.XmlImportError(xml_path)
#
#     if not lib_meta: return
#
#     medialib.name = str(lib_meta.find('name').text)
#     medialib.added = str(lib_meta.find('created').text)
#
#     medialib.folders = []
#     medialib.playlists = []
#     medialib.songs = []
#
#     # LOAD SONGS
#     for song in lib_meta.find('songs'):
#         s = Song()
#
#         s.pid = str(song.find('pid').text)
#         s.name = str(song.find('name').text)
#         s.artist = str(song.find('artist').text)
#         s.album = str(song.find('album').text)
#         s.time = int(song.find('time').text)
#         s.added = str(song.find('added').text)
#         s.path = str(song.find('path').text)
#         s.kind = str(song.find('data').attrib['kind'])
#         s.size = int(song.find('data').attrib['size'])
#         s.sample = int(song.find('data').attrib['sample'])
#         s.bit = int(song.find('data').attrib['bit'])
#
#         medialib.songs.append(s)
#
#     # LOAD PLAYLISTS
#     for playlist in lib_meta.find('playlists'):
#         p = Playlist()
#
#         p.pid = str(playlist.find('pid').text)
#         p.name = str(playlist.find('name').text)
#         p.folder = str(playlist.find('folder').text)
#         p.added = str(playlist.find('added').text)
#         p.created = str(playlist.find('created').text)
#
#         for s in playlist.find('songs'):
#             p.songs.append(str(s.attrib['pid']))
#
#         if p.folder == 'None': p.folder = None
#
#         medialib.playlists.append(p)
#
#     # LOAD FOLDERS
#     for folder in lib_meta.find('folders'):
#         f = Folder()
#
#         f.pid = str(folder.find('pid').text)
#         f.name = str(folder.find('name').text)
#         f.folder = str(folder.find('folder').text)
#
#         for p in folder.find('playlists'):
#             f.playlists.append(str(p.attrib['pid']))
#
#         if f.folder == 'None': f.folder = None
#
#         medialib.folders.append(f)
#
#
# @system_refresh
# def library_xml_export():
#     xml_path = ask.asksaveasfilename(
#         title='Export Library',
#         initialdir=fileutil.path_desktop(),
#         filetypes=(('XML Files', '*.xml'),))
#
#     if xml_path == '': return
#
#     if not xml_path.endswith('.xml'):
#         xml_path += '.xml'
#
#     lib_meta = et.Element('mpi3Library')
#     lib_meta.set('version', '1.0')
#
#     name = et.SubElement(lib_meta, 'name')
#     added = et.SubElement(lib_meta, 'created')
#
#     name.text = str(medialib.name)
#     added.text = str(medialib.added)
#
#     # SAVE SONGLIST
#     songlist = et.SubElement(lib_meta, 'songs')
#     for s in medialib.songs:
#         song = et.SubElement(songlist, 'song')
#
#         pid = et.SubElement(song, 'pid')
#         name = et.SubElement(song, 'name')
#         artist = et.SubElement(song, 'artist')
#         album = et.SubElement(song, 'album')
#         time = et.SubElement(song, 'time')
#         added = et.SubElement(song, 'added')
#         path = et.SubElement(song, 'path')
#         data = et.SubElement(song, 'data')
#
#         pid.text = str(s.pid)
#         name.text = str(s.name)
#         artist.text = str(s.artist)
#         album.text = str(s.album)
#         time.text = str(s.time)
#         added.text = str(s.added)
#         path.text = str(s.path)
#
#         data.attrib = {
#             'kind': str(s.kind),
#             'size': str(s.size),
#             'sample': str(s.sample),
#             'bit': str(s.bit)
#         }
#
#     # SAVE PLAYLISTS
#     playlists = et.SubElement(lib_meta, 'playlists')
#     for p in medialib.playlists:
#         plist = et.SubElement(playlists, 'playlist')
#
#         pid = et.SubElement(plist, 'pid')
#         name = et.SubElement(plist, 'name')
#         folder = et.SubElement(plist, 'folder')
#         added = et.SubElement(plist, 'added')
#         created = et.SubElement(plist, 'created')
#         songs = et.SubElement(plist, 'songs')
#
#         pid.text = str(p.pid)
#         name.text = str(p.name)
#         folder.text = str(p.folder)
#         added.text = str(p.added)
#         created.text = str(p.created)
#
#         for s in p.songs:
#             song = et.SubElement(songs, 'song')
#             song.attrib = {'pid': str(s)}
#
#     # SAVE FOLDERS
#     folders = et.SubElement(lib_meta, 'folders')
#     for f in medialib.folders:
#         fldr = et.SubElement(folders, 'folder')
#
#         pid = et.SubElement(fldr, 'pid')
#         name = et.SubElement(fldr, 'name')
#         folder = et.SubElement(fldr, 'folder')
#         playlists = et.SubElement(fldr, 'playlists')
#
#         pid.text = str(f.pid)
#         name.text = str(f.name)
#         folder.text = str(f.folder)
#
#         for p in f.playlists:
#             playlist = et.SubElement(playlists, 'playlist')
#             playlist.attrib = {'pid': str(p)}
#
#     # OUTPUT XML
#     tree = et.ElementTree(lib_meta)
#     tree.write(xml_path)
#     xml_formatted = minidom.parse(xml_path).toprettyxml()
#     with open(xml_path, 'w') as overwrite:
#         overwrite.write(xml_formatted)
#
#     msg.showinfo('Success', 'Library exported to: \n' + xml_path)
