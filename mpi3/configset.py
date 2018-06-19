from six.moves import cPickle


DEFAULT_STATE_PC = {
    'PATHS': {
        'DOWNLOADS': 'E:/yt_downloads',
        'MEDIA': 'E:/mpi3pc'
    },
    'PLAYBACK': {
        'INITIALVOLUME': 0.5,
        'INITIALVIEW': 'view_allsongs'
    },
    'ROOT': {
        'DIMENSIONS': (1000, 600)
    },
    'TREEVIEWS': {
        'ALLSONGS': {
            'ROOTWIDTH': 40,
            'COLUMNS': [
                {'id': 'name', 'width': 200,
                 'visible': True, 'heading': 'Name'},
                {'id': 'artist', 'width': 125,
                 'visible': True, 'heading': 'Artist'},
                {'id': 'album', 'width': 125,
                 'visible': True, 'heading': 'Album'},
                {'id': 'time', 'width': 50,
                 'visible': True, 'heading': 'Length'},
                {'id': 'size', 'width': 60,
                 'visible': True, 'heading': 'Size'},
                {'id': 'added', 'width': 100,
                 'visible': True, 'heading': 'Added'},
                {'id': 'path', 'width': 200,
                 'visible': True, 'heading': 'Path'}
            ]
        },
        'ARTISTS': {
            'ROOTWIDTH': 200,
            'COLUMNS': [
                {'id': 'time', 'width': 50,
                 'visible': True, 'heading': 'Length'},
                {'id': 'size', 'width': 60,
                 'visible': True, 'heading': 'Size'},
                {'id': 'added', 'width': 100,
                 'visible': True, 'heading': 'Added'}
            ]
        },
        'CONTAINERS': {
            'ROOTWIDTH': 200,
            'COLUMNS': [
                {'id': 'total_songs', 'width': 125,
                 'visible': True, 'heading': 'Songs'},
                {'id': 'added', 'width': 100,
                 'visible': True, 'heading': 'Added'}
            ]
        },
        'PLAYLISTS': {
            'ROOTWIDTH': 40,
            'COLUMNS': [
                {'id': 'name', 'width': 200,
                 'visible': True, 'heading': 'Name'},
                {'id': 'artist', 'width': 125,
                 'visible': True, 'heading': 'Artist'},
                {'id': 'album', 'width': 125,
                 'visible': True, 'heading': 'Album'},
                {'id': 'time', 'width': 50,
                 'visible': True, 'heading': 'Length'},
                {'id': 'size', 'width': 60,
                 'visible': True, 'heading': 'Size'},
                {'id': 'added', 'width': 100,
                 'visible': True, 'heading': 'Added'},
                {'id': 'path', 'width': 200,
                 'visible': True, 'heading': 'Path'}
            ]
        }
    }
}
DEFAULT_STATE_PI = {
    'PLAYBACK': {
        'INITIALVOLUME': 0.5,
    }
}


class Settings:

    def __init__(self):
        self._properties = None
        self._save_path = None

    def initiate(self, defaultstate):
        self._properties = defaultstate

    def __getitem__(self, item):
        return self._properties[item]

    def __setitem__(self, key, value):
        self._properties[key] = value

    def __len__(self):
        return len(self._properties)

    def load(self, path):
        self._save_path = path
        with open(path, 'rb') as rf:
            self._properties = cPickle.load(rf)

    def save(self, path=None):
        if path: self._save_path = path
        with open(self._save_path, 'wb') as wf:
            cPickle.dump(self._properties, wf)
