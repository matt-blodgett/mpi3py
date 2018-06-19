import mpi3
from . import gui
from . import util
from . import pcui


def initiate():
    mpi3.initiate_resources('rsrcpc')
    mpi3.initiate_logging()
    mpi3.initiate_system('pc')
    mpi3.initiate_playback('pc')
    mpi3.initiate_library('pc')
    pcui.initiate_interface()
    mpi3.release()
