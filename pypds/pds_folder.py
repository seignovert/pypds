# -*- coding: utf-8 -*-

from ._communs import INSTRUMENT, VERBOSE, PDS_OBJ, date_split

class FOLDER(PDS_OBJ):
    def __init__(self, name, release, inst=INSTRUMENT, fmt='%Y%jT%H%M%S'):
        PDS_OBJ.__init__(self, inst)
        self.name = name
        self.start, self.end = date_split(name, fmt)
        self.release = release
        self.imgs = []
        return

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'PDS release folder: %s' % str(self)

    def __len__(self):
        return self.nb_imgs

    @property
    def nb_imgs(self):
        '''Number of images in the folder'''
        return len(self.imgs)

    @property
    def url(self):
        return '/'.join([
            self.root_url,
            'data',
            self.mission,
            self.spacecraft,
            self.release,
            'data',
            self.name
        ]) + '/'

    @property
    def first(self):
        '''Folder first image'''
        if len(self.imgs) == 0:
            return None
        return self.imgs[0]

    @property
    def last(self):
        '''Folder last image'''
        if len(self.imgs) == 0:
            return None
        return self.imgs[-1]
