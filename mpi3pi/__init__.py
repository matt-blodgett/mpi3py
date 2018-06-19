import mpi3
from . import gui
from . import util
from . import rpiui


def initiate():
    mpi3.initiate_resources('rsrcpi')
    mpi3.initiate_logging()
    mpi3.initiate_system('pi')
    mpi3.initiate_playback('pi')
    mpi3.initiate_library('pi')

    # FOR TESTING
    mpi3.initiate_resources('rsrcpc')
    mpi3.initiate_library('pc')

    rpiui.initiate_interface()
    mpi3.release()
