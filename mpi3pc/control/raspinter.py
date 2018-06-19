import os
import threading
from tkinter import filedialog as ask
from mpi3pc.util import fileutil
from mpi3pc.util import winutil
from mpi3 import library

# http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html


loaded_volumes = {}


def initiate():
    for drive in winutil.removable_drives():
        print(drive)

        sd_thread = threading.Thread(target=lambda d=drive: scan_drive(d))
        sd_thread.name = 'SCAN DRIVE'
        sd_thread.daemon = True
        sd_thread.start()

    while 'SCAN DRIVE' in [t.name for t in threading.enumerate()]:
        pass

    for k in loaded_volumes.keys():
        print(k, ' - ', loaded_volumes[k])


def new_volume():
    raspi_dir = ask.askdirectory(
        title='New Raspberry Pi Library Volume',
        initialdir=fileutil.path_desktop())

    if raspi_dir == '': return

    raspilib = library.RaspiLibrary.new()

    volume_dir = '{}/mpi3raspi'.format(raspi_dir)
    library_dir = '{}/.mpi3pc'.format(volume_dir)
    library_file = '{}/mpi3lib'.format(library_dir)
    library_cfg = '{}/mpi3cfg'.format(library_dir)

    os.mkdir(volume_dir)
    os.mkdir(library_dir)
    raspilib.save(library_file)

    with open(library_cfg, 'wb') as cfg:
        cfg.write(b'raspberry pi configuration file')


def scan_drive(drive):
    dir_root = '{}/'.format(drive)
    lib_file = '.mpi3pc/mpi3lib'
    for p in fileutil.path_search(dir_root, lib_file):
        raspilib = library.RaspiLibrary.open(p)
        if raspilib is not None:
            loaded_volumes[raspilib.pid] = raspilib
