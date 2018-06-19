

class Mpi3Error(Exception):
    pass


class DuplicatePIDError(Mpi3Error):
    def __init__(self, pid=None):
        self._pid = pid

    def __str__(self):
        if not self._pid:
            return self.__class__.__name__
        else:
            return self._pid


class XmlImportError(Mpi3Error):
    def __init__(self, path=None):
        self._path = path

    def __str__(self):
        if not self._path:
            return self.__class__.__name__
        else:
            return self._path
