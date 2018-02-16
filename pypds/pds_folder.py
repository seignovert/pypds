# -*- coding: utf-8 -*-

import datetime as dt

from ._communs import INSTRUMENT, VERBOSE, PDS_OBJ

class FOLDER(PDS_OBJ):
    def __init__(self, name, release, inst=INSTRUMENT, fmt='%Y%jT%H%M%S'):
        PDS_OBJ.__init__(self, inst)
        self.name = name
        self.start, self.end = self.split(fmt)
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

    def split(self, fmt='%Y%jT%H%M%S'):
        '''Split Date1_Date2 folder into datetime'''
        start, end = self.name.split('_')

        # BugFix wrong date in PDS (covims_0003)
        if start[:4] == '1866':
            # Use the end year for substitution
            print('[Warning] Wrong year %s -> %s (%s)' % (
                start[:4], end[:4], self.name
            ))
            start = end[:4]+start[4:]

        if end[:4] == '1866':
            # Use the start year for substitution
            print('[Warning] Wrong year %s -> %s (%s)' % (
                end[:4], start[:4], self.name
            ))
            end = start[:4]+end[4:]

        return dt.datetime.strptime(start, fmt),\
               dt.datetime.strptime(end, fmt)

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
