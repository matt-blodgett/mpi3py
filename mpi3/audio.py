import pydub
import pyaudio
import threading


class Playback:

    def __repr__(self):
        return '<Mpi3 Playback>'

    def __init__(self):
        self.__dict__['_audio_out'] = pyaudio.PyAudio()
        self.__dict__['_audio_stream'] = None
        self.__dict__['_audio_segment'] = None
        self.__dict__['_db_floor'] = 40

        self.__dict__['song'] = None
        self.__dict__['playlist'] = []
        self.__dict__['volume'] = 0.0
        self.__dict__['active'] = False
        self.__dict__['loaded'] = False
        self.__dict__['_position'] = 0

        self.__dict__['update'] = {
            'song': lambda v: None,
            'position': lambda v: None,
            'volume': lambda v: None,
            'active': lambda v: None,
            'loaded': lambda v: None
        }

    def __setattr__(self, key, value):
        if key in self.update.keys():
            self.update[key](value)
        super().__setattr__(key, value)

    def play(self, playlist, song, position=0):
        self.active = False
        self.position = position
        self.playlist = playlist
        self.song = song

        if not self.loaded: self.loaded = True
        path = self.song.path

        codec = pydub.utils.mediainfo(path)['codec_name']
        self._audio_segment = pydub.AudioSegment.from_file(path, codec)

        d_default = self._audio_out.get_default_output_device_info()
        d_default_index = d_default['index']

        s_sample = self._audio_segment.frame_rate
        s_channels = self._audio_segment.channels
        s_width = self._audio_segment.sample_width
        s_format = self._audio_out.get_format_from_width(s_width)

        self._audio_stream = self._audio_out.open(
            s_sample, s_channels, s_format, output=True,
            output_device_index=d_default_index)

        self._spawn()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        try: self._position = max(0, min(position, len(self._audio_segment)))
        except TypeError: pass

    def pause(self):
        self.active = False

    def unpause(self, position=None):
        if position: self.position = position
        self._spawn()

    def play_next(self):
        self._play_shift(1)

    def play_prev(self):
        self._play_shift(-1)

    def _play_shift(self, shift):
        index = self.playlist.index(self.song) + shift
        if not (index < 0 or index > (len(self.playlist) - 1)):
            self.play(self.playlist, self.playlist[index])

    def seek(self, position):
        self.position = position

    def volume_ratio(self, vol_ratio):
        self.volume = max(0.0, min(vol_ratio, 1.0))

    def _spawn(self):
        self.active = True
        stream_thread = threading.Thread(target=self._output)
        stream_thread.name = self.__class__.__name__
        stream_thread.daemon = True
        stream_thread.start()

    def _output(self, position=None):
        if not position: position = self.position
        if position < len(self._audio_segment) and self.active:
            vol = self._db_floor-(self._db_floor * self.volume)
            vol = 120 if vol == self._db_floor else vol
            seg = self._audio_segment[position:position + 50] - vol
            self._audio_stream.write(seg.raw_data)
            self._output(position+50)

    def release(self):
        self._audio_out.terminate()

    # def test(self):
    #     s_info = pydub.utils.mediainfo(self.file_path)
    #     for i in s_info:
    #         print(i, ' ', s_info[i], '\n')
    #
    #     print(self._audio_out.get_device_count())
    #
    #     print(self._audio_stream.is_active())
    #     print(self._audio_stream.is_stopped())
    #     print(self._audio_stream.get_output_latency())
    #
    #     print('rms:', self._file_segment.rms)
    #     print('dBFS:', self._file_segment.dBFS)
    #     print('max:', self._file_segment.max)
    #     print('maxamp:', self._file_segment.max_possible_amplitude)
    #     print('max_dBFS:', self._file_segment.max_dBFS)
    #     print('sec:', self._file_segment.duration_seconds)
    #
    #     vol = pydub.utils.ratio_to_db(0.5, 1)
    #     print(vol)
    #     print(pydub.utils.ratio_to_db(5, 10))
    #     print(pydub.utils.ratio_to_db(1, 10))
    #     print(pydub.utils.ratio_to_db(10, 10))
    #     print(pydub.utils.ratio_to_db(20, 10))
