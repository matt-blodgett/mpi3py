import os
import sys
import logging


from . import audio
from . import library
from . import configset


playback = audio.Playback()
settings = configset.Settings()
medialib = library.MediaLibrary()
raspilib = library.RaspiLibrary()


RSRC_PATH = None


def initiate_resources(resourcepath):
    global RSRC_PATH
    RSRC_PATH = '{}/{}'.format(os.getcwd(), resourcepath)


def initiate_logging(resetlog=True, toconsole=True):
    log_path = os.path.abspath('{}/mpi3log.txt'.format(RSRC_PATH))

    log = logging.getLogger('MPI3')
    log.setLevel(logging.DEBUG)

    f_mode = 'w' if resetlog else 'a'
    log_fh = logging.FileHandler(
        filename=log_path, mode=f_mode)
    log_format_files = logging.Formatter(
        fmt='{}:{}:{}:[{}, {}]:{}'.format(
            '%(asctime)s', '%(name)s', '%(levelname)s',
            '%(module)s', '%(funcName)s', '%(message)s'))
    log_fh.setFormatter(log_format_files)
    log_fh.setLevel(logging.DEBUG)
    log.addHandler(log_fh)

    if toconsole:
        log_sh = logging.StreamHandler(stream=sys.stdout)
        log_format_stream = logging.Formatter(
            fmt='LOG: [{}, {}]: {}'.format(
                '%(module)s', '%(funcName)s', '%(message)s'))
        log_sh.setFormatter(log_format_stream)
        log_sh.setLevel(logging.DEBUG)
        log.addHandler(log_sh)

    log.info('Logging Initialized <{}>'.format(log_path))


def initiate_playback(platform):
    if platform == 'pi': return

    libav_path = os.path.abspath('{}/libav'.format(os.getcwd()))
    logging.getLogger('MPI3').info('Load libav <{}>'.format(libav_path))

    audio.pydub.utils.get_prober_name = lambda: libav_path + '\\avprobe.exe'
    audio.pydub.AudioSegment.converter = libav_path + '\\avconv.exe'


def initiate_library(platform):
    if platform == 'pi': return

    lib_path = os.path.abspath('{}/mpi3lib'.format(RSRC_PATH))
    logging.getLogger('MPI3').info('Load Library <{}>'.format(lib_path))

    if not os.path.exists(lib_path):
        medialib.save(lib_path)
    medialib.load(lib_path)


def initiate_system(platform, default_state=True):
    state_path = os.path.abspath('{}/mpi3cfg'.format(RSRC_PATH))
    p = 'DEFAULT' if default_state else state_path
    logging.getLogger('MPI3').info('Load State <{}>'.format(p))

    if platform == 'pc':
        settings.initiate(configset.DEFAULT_STATE_PC)
    elif platform == 'pi':
        settings.initiate(configset.DEFAULT_STATE_PI)

    if not os.path.exists(state_path) or default_state:
        settings.save(state_path)
    settings.load(state_path)


def release():
    log = logging.getLogger('MPI3')

    log.info('Save Volume: {}'.format(playback.volume))
    settings['PLAYBACK']['INITIALVOLUME'] = playback.volume

    log.info('Save Settings...')
    settings.save()

    log.info('Release Audio Stream...')
    playback.release()
    log.info('Audio Stream Successfully Released')

    log.info('Release Logging Handlers')
    log.info('Exit Protocol Complete')
    for handler in log.handlers:
        handler.flush()
        handler.close()
