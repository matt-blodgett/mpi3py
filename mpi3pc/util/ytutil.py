import pytube

dl_path = 'utube/'
yt_path = 'https://www.youtube.com/watch?v=tSkCqj6T_NQ'

yt = pytube.YouTube(yt_path)


# ripped_file = 'C:/Users/mablodgett/Desktop/ytdl/'


def on_prog(stream, chunk, file_handler, bytes_remaining):
    remaining = (1 - (bytes_remaining / stream.filesize)) * 100
    print('{0:.0f}%'.format(remaining))
    # print(bytes_remaining)


def on_comp(file_handler, bytes_remaining):
    print(file_handler, bytes_remaining)


yt.register_on_progress_callback(on_prog)
yt.register_on_complete_callback(on_comp)

yt_stream = yt.streams.filter(only_audio=True).asc().first()

print(yt_stream.default_filename)
print(yt_stream.bitrate)
print(yt_stream.filesize)
print(yt_stream.fmt_profile)
print(yt_stream.s)
print(yt_stream.type)
print(yt_stream.subtype)
print(yt_stream.url)

# yt_stream.download(dl_path)


##print('all')
##for s in yt.streams.all():
##    print(s)
##
##
##print()
##
##
##print('audio')
##for s in yt.streams.filter(only_audio=True).all():
##    print(s)








from pydub import AudioSegment

import os

song_path = 'utube/Tom Walker - Leave a Light On  Lyrics.mp4'

import pydub


# print(pydub.utils.get_encoder_name())
# print(pydub.utils.get_player_name())
# print(pydub.utils.mediainfo(song_path))


# song = AudioSegment.from_file(song_path, 'mp4')
# song.export('utube/Leave A Light On.mp3',format='mp3')


